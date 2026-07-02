"""Bollinger-style z-score mean reversion strategy."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from bot.indicators import require_close, zscore
from bot.models import Signal, SignalResult


@dataclass(frozen=True)
class MeanReversionStrategy:
    window: int = 20
    entry_z: float = 2.0

    name: str = "mean-reversion"

    def evaluate(self, symbol: str, df: pd.DataFrame) -> SignalResult:
        close = require_close(df)
        scores = zscore(close, self.window).dropna()
        if scores.empty:
            raise ValueError(f"Not enough data to compute {self.name} for {symbol}")

        latest = float(scores.iloc[-1])
        price = float(close.iloc[-1])
        signal = Signal.HOLD
        if latest <= -self.entry_z:
            signal = Signal.BUY
        elif latest >= self.entry_z:
            signal = Signal.SELL

        return SignalResult(
            symbol=symbol,
            strategy=self.name,
            signal=signal,
            score=latest,
            price=price,
            reason=f"z-score {latest:.2f} vs entry threshold +/-{self.entry_z:.2f}",
            metadata={"window": self.window, "entry_z": self.entry_z},
        )


MeanReversionParams = MeanReversionStrategy


def compute_zscore(close: pd.Series, window: int) -> pd.Series:
    return zscore(close, window)


def generate_signal(
    df: pd.DataFrame,
    params: MeanReversionParams = MeanReversionParams(),
) -> Signal:
    return params.evaluate("", df).signal
