"""RSI threshold reversal strategy."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from bot.indicators import require_close, rsi
from bot.models import Signal, SignalResult


@dataclass(frozen=True)
class RsiReversalStrategy:
    window: int = 14
    oversold: float = 30.0
    overbought: float = 70.0

    name: str = "rsi-reversal"

    def evaluate(self, symbol: str, df: pd.DataFrame) -> SignalResult:
        close = require_close(df)
        scores = rsi(close, self.window).dropna()
        if scores.empty:
            raise ValueError(f"Not enough data to compute {self.name} for {symbol}")

        latest = float(scores.iloc[-1])
        price = float(close.iloc[-1])
        signal = Signal.HOLD
        if latest <= self.oversold:
            signal = Signal.BUY
        elif latest >= self.overbought:
            signal = Signal.SELL

        return SignalResult(
            symbol=symbol,
            strategy=self.name,
            signal=signal,
            score=latest,
            price=price,
            reason=f"RSI {latest:.2f} vs {self.oversold:.2f}/{self.overbought:.2f}",
            metadata={
                "window": self.window,
                "oversold": self.oversold,
                "overbought": self.overbought,
            },
        )
