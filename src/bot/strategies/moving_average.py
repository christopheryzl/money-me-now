"""Moving-average crossover trend-following strategy."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from bot.indicators import require_close, simple_moving_average
from bot.models import Signal, SignalResult


@dataclass(frozen=True)
class MovingAverageTrendStrategy:
    fast_window: int = 20
    slow_window: int = 50

    name: str = "moving-average-trend"

    def __post_init__(self) -> None:
        if self.fast_window >= self.slow_window:
            raise ValueError("fast_window must be lower than slow_window")

    def evaluate(self, symbol: str, df: pd.DataFrame) -> SignalResult:
        close = require_close(df)
        fast = simple_moving_average(close, self.fast_window)
        slow = simple_moving_average(close, self.slow_window)
        spread = (fast - slow).dropna()
        if spread.empty:
            raise ValueError(f"Not enough data to compute {self.name} for {symbol}")

        latest = float(spread.iloc[-1])
        price = float(close.iloc[-1])
        signal = Signal.BUY if latest > 0 else Signal.SELL if latest < 0 else Signal.HOLD

        return SignalResult(
            symbol=symbol,
            strategy=self.name,
            signal=signal,
            score=latest,
            price=price,
            reason=(
                f"SMA{self.fast_window} minus SMA{self.slow_window} "
                f"spread is {latest:.2f}"
            ),
            metadata={"fast_window": self.fast_window, "slow_window": self.slow_window},
        )
