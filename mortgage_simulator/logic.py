from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Payment:
    period: int
    payment: float
    interest: float
    principal: float
    balance: float
    annual_rate: float

class Mortgage:
    """
    French amortisation mortgage (used by most Spanish banks).
    Parameters
    ----------
    principal : float
        Initial loan amount.
    annual_rate : float
        Annual nominal interest rate (e.g. 0.03 for 3%).
    years : int
        Mortgage term in years.
    """
    def __init__(self, principal: float, annual_rate: float, years: int):
        self.original_principal = principal
        self.principal = principal
        self.annual_rate = annual_rate
        self.monthly_rate = annual_rate / 12
        self.total_months = years * 12

    @staticmethod
    def monthly_payment(principal: float,
                        annual_rate: float,
                        months: int) -> float:
        """
        French amortisation payment formula.
        """
        if months <= 0:
            return 0.0

        r = annual_rate / 12

        if abs(r) < 1e-12:
            return principal / months

        return principal * r / (1 - (1 + r) ** (-months))

    def payment(self) -> float:
        return self.monthly_payment(
            self.principal,
            self.annual_rate,
            self.total_months
        )

    def amortisation_schedule(
        self,
        extra_payment: float = 0.0,
        recalculate_after_extra: bool = False
    ) -> List[Payment]:
        """
        Generate the amortisation schedule.

        Parameters
        ----------
        extra_payment : float
            Extra principal paid each month.

        recalculate_after_extra : bool
            If True, payment is recalculated after each extra payment,
            keeping the original maturity.
            If False, payment stays fixed and mortgage ends earlier.
        """

        balance = self.principal
        months_remaining = self.total_months
        payment = self.payment()
        schedule = []
        for month in range(1, self.total_months + 1):
            interest = balance * self.monthly_rate
            principal_paid = payment - interest
            principal_paid += extra_payment
            if principal_paid > balance:
                principal_paid = balance
                payment_actual = interest + balance
            else:
                payment_actual = payment + extra_payment
            balance -= principal_paid
            schedule.append(
                Payment(
                    period=month,
                    payment=round(payment_actual, 2),
                    interest=round(interest, 2),
                    principal=round(principal_paid, 2),
                    balance=round(balance, 2),
                    annual_rate=self.annual_rate,
                )
            )
            if balance <= 0:
                break
            months_remaining -= 1
            if recalculate_after_extra and extra_payment > 0:
                payment = self.monthly_payment(
                    balance,
                    self.annual_rate,
                    months_remaining
                )
        return schedule

    @staticmethod
    def outstanding_balance(principal: float,
                            annual_rate: float,
                            months: int,
                            payments_made: int) -> float:
        """
        Closed-form outstanding balance.
        """

        r = annual_rate / 12
        payment = Mortgage.monthly_payment(
            principal,
            annual_rate,
            months
        )
        if abs(r) < 1e-12:
            return principal - payment * payments_made
        balance = (
            principal * (1 + r) ** payments_made
            - payment * (((1 + r) ** payments_made - 1) / r)
        )
        return max(balance, 0.0)

    def revise_interest_rate(self,
                             new_annual_rate: float,
                             balance: float,
                             months_remaining: int):
        """
        Simulate a Spanish variable-rate mortgage review.

        After a Euribor review, Spanish banks typically:
        - keep the remaining term fixed
        - recalculate the monthly payment
        """

        self.principal = balance
        self.annual_rate = new_annual_rate
        self.monthly_rate = new_annual_rate / 12
        self.total_months = months_remaining

