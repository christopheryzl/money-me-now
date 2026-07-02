"""Small backtesting harness for signal sanity checks."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from bot.models import Signal
from bot.strategies.base import Strategy


@dataclass(frozen=True)
class BacktestResult:
    strategy: str
    symbol: str
    bars: int
    trades: int
    cumulative_return: float


def backtest_long_short(symbol: str, df: pd.DataFrame, strategy: Strategy) -> BacktestResult:
    if "Close" not in df:
        raise ValueError("DataFrame must include a 'Close' column")

    close = df["Close"].astype(float)
    returns = close.pct_change().fillna(0.0)
    positions: list[int] = []
    current_position = 0

    for end in range(1, len(df) + 1):
        try:
            signal = strategy.evaluate(symbol, df.iloc[:end]).signal
        except ValueError:
            positions.append(current_position)
            continue

        if signal == Signal.BUY:
            current_position = 1
        elif signal == Signal.SELL:
            current_position = -1
        positions.append(current_position)

    shifted_positions = pd.Series(positions, index=df.index).shift(1).fillna(0)
    strategy_returns = shifted_positions * returns
    trades = int((shifted_positions.diff().fillna(0) != 0).sum())

    return BacktestResult(
        strategy=strategy.name,
        symbol=symbol,
        bars=len(df),
        trades=trades,
        cumulative_return=float((1 + strategy_returns).prod() - 1),
    )
