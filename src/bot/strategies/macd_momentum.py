"""MACD momentum strategy."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from bot.indicators import macd, require_close
from bot.models import Signal, SignalResult


@dataclass(frozen=True)
class MacdMomentumStrategy:
    fast_window: int = 12
    slow_window: int = 26
    signal_window: int = 9

    name: str = "macd-momentum"

    def evaluate(self, symbol: str, df: pd.DataFrame) -> SignalResult:
        close = require_close(df)
        values = macd(close, self.fast_window, self.slow_window, self.signal_window).dropna()
        if len(values) < 2:
            raise ValueError(f"Not enough data to compute {self.name} for {symbol}")

        latest = values.iloc[-1]
        previous = values.iloc[-2]
        histogram = float(latest["histogram"])
        crossed_up = previous["histogram"] <= 0 < latest["histogram"]
        crossed_down = previous["histogram"] >= 0 > latest["histogram"]

        signal = Signal.HOLD
        if crossed_up or (latest["macd"] > latest["signal"] and histogram > 0):
            signal = Signal.BUY
        elif crossed_down or (latest["macd"] < latest["signal"] and histogram < 0):
            signal = Signal.SELL

        return SignalResult(
            symbol=symbol,
            strategy=self.name,
            signal=signal,
            score=histogram,
            price=float(close.iloc[-1]),
            reason=f"MACD histogram is {histogram:.4f}",
            metadata={
                "fast_window": self.fast_window,
                "slow_window": self.slow_window,
                "signal_window": self.signal_window,
                "macd": float(latest["macd"]),
                "signal_line": float(latest["signal"]),
            },
        )
