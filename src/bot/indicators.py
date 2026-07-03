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


def exponential_moving_average(close: pd.Series, window: int) -> pd.Series:
    if window < 1:
        raise ValueError("window must be at least 1")
    return close.ewm(span=window, adjust=False).mean()


def macd(
    close: pd.Series,
    fast_window: int = 12,
    slow_window: int = 26,
    signal_window: int = 9,
) -> pd.DataFrame:
    if fast_window >= slow_window:
        raise ValueError("fast_window must be lower than slow_window")
    macd_line = exponential_moving_average(close, fast_window) - exponential_moving_average(
        close,
        slow_window,
    )
    signal_line = exponential_moving_average(macd_line, signal_window)
    histogram = macd_line - signal_line
    return pd.DataFrame({"macd": macd_line, "signal": signal_line, "histogram": histogram})


def donchian_channels(df: pd.DataFrame, window: int) -> pd.DataFrame:
    if window < 2:
        raise ValueError("window must be at least 2")
    close = require_close(df)
    high = df["High"].astype(float) if "High" in df else close
    low = df["Low"].astype(float) if "Low" in df else close
    return pd.DataFrame(
        {
            "upper": high.rolling(window).max(),
            "lower": low.rolling(window).min(),
            "middle": (high.rolling(window).max() + low.rolling(window).min()) / 2,
        },
    )
