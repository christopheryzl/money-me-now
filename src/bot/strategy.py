"""Bollinger Band z-score mean reversion strategy.

Assumes price oscillates around a rolling mean over the lookback window.
A signal triggers when price has stretched far enough from that mean (in
standard deviations) that reversion back toward it is statistically likely.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import pandas as pd


class Signal(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


@dataclass
class MeanReversionParams:
    window: int = 20
    entry_z: float = 2.0


def compute_zscore(close: pd.Series, window: int) -> pd.Series:
    rolling_mean = close.rolling(window).mean()
    rolling_std = close.rolling(window).std()
    return (close - rolling_mean) / rolling_std


def generate_signal(df: pd.DataFrame, params: MeanReversionParams = MeanReversionParams()) -> Signal:
    zscore = compute_zscore(df["Close"], params.window).dropna()
    latest = zscore.iloc[-1]

    if latest <= -params.entry_z:
        return Signal.BUY
    if latest >= params.entry_z:
        return Signal.SELL
    return Signal.HOLD
