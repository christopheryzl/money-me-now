"""Donchian channel breakout strategy."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from bot.indicators import donchian_channels, require_close
from bot.models import Signal, SignalResult


@dataclass(frozen=True)
class DonchianBreakoutStrategy:
    window: int = 20

    name: str = "donchian-breakout"

    def evaluate(self, symbol: str, df: pd.DataFrame) -> SignalResult:
        close = require_close(df)
        channels = donchian_channels(df, self.window).dropna()
        if len(channels) < 2:
            raise ValueError(f"Not enough data to compute {self.name} for {symbol}")

        previous_channels = channels.iloc[-2]
        latest_price = float(close.iloc[-1])
        upper = float(previous_channels["upper"])
        lower = float(previous_channels["lower"])
        channel_range = max(upper - lower, 1e-9)

        signal = Signal.HOLD
        if latest_price > upper:
            signal = Signal.BUY
        elif latest_price < lower:
            signal = Signal.SELL

        score = (latest_price - float(previous_channels["middle"])) / channel_range
        return SignalResult(
            symbol=symbol,
            strategy=self.name,
            signal=signal,
            score=float(score),
            price=latest_price,
            reason=f"price {latest_price:.2f} vs prior Donchian {lower:.2f}-{upper:.2f}",
            metadata={"window": self.window, "upper": upper, "lower": lower},
        )
