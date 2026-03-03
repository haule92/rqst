import pandas as pd
import numpy as np
import math

def compute_sharpe_ratio(r: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the Sharpe ratio for a given DataFrame r which are returns.
    :param r:
    :return: The Sharpe ratio
    """
    avg_r = r.mean()
    vol_r = r.std()
    return avg_r / vol_r

def compute_annualised_sharpe_ratio(r: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the Sharpe ratio for a given DataFrame r which are returns.
    :param r:
    :return: The Sharpe ratio
    """
    avg_r = r.mean() * 252
    vol_r = r.std() * np.sqrt(252)
    return avg_r / vol_r

def compute_annualised_sharpe_ratio_using_math(r: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the Sharpe ratio for a given DataFrame r which are returns.
    :param r:
    :return: The Sharpe ratio
    """
    avg_r = r.mean() * 252
    vol_r = r.std() * math.sqrt(252)
    return avg_r / vol_r

def compute_annualised_sharpe_ratio_with_rolling_window(r: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the Sharpe ratio for a given DataFrame r which are returns.
    :param r:
    :return: The Sharpe ratio
    """
    avg_r = r.rolling(252).mean() * 252
    vol_r = r.rolling(252).std() * np.sqrt(252)
    return avg_r / vol_r


def compute_annualised_sharpe_ratio_with_rolling_window_using_math(r: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the Sharpe ratio for a given DataFrame r which are returns.
    :param r:
    :return: The Sharpe ratio
    """
    avg_r = r.rolling(252).mean() * 252
    vol_r = r.rolling(252).std() * math.sqrt(252)
    return avg_r / vol_r

def compute_annualised_sharpe_ratio_with_rolling_window_using_math_at_once(r: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the Sharpe ratio for a given DataFrame r which are returns.
    :param r:
    :return: The Sharpe ratio
    """
    return r.rolling(252).mean() / r.rolling(252).std() * math.sqrt(252)
