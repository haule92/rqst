from logic import Mortgage

mortgage = Mortgage(
    principal=110000,
    annual_rate=0.03,
    years=12,
)

print(f"Monthly payment: ${mortgage.payment():,.2f}")

schedule = mortgage.amortisation_schedule()

for s in schedule:
    print(s)
