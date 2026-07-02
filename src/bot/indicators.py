"""Reusable technical indicator calculations."""

from __future__ import annotations

import pandas as pd


def require_close(df: pd.DataFrame) -> pd.Series:
    if "Close" not in df:
        raise ValueError("DataFrame must include a 'Close' column")
    close = df["Close"].dropna()
    if close.empty:
        raise ValueError("Close series is empty")
    return close.astype(float)


def zscore(close: pd.Series, window: int) -> pd.Series:
    if window < 2:
        raise ValueError("window must be at least 2")
    rolling_mean = close.rolling(window).mean()
    rolling_std = close.rolling(window).std()
    return (close - rolling_mean) / rolling_std


def rsi(close: pd.Series, window: int = 14) -> pd.Series:
    if window < 2:
        raise ValueError("window must be at least 2")
    delta = close.diff()
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)
    avg_gain = gains.rolling(window).mean()
    avg_loss = losses.rolling(window).mean()
    relative_strength = avg_gain / avg_loss
    return 100 - (100 / (1 + relative_strength))


def simple_moving_average(close: pd.Series, window: int) -> pd.Series:
    if window < 1:
        raise ValueError("window must be at least 1")
    return close.rolling(window).mean()
