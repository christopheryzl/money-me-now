"""Strategy factory functions."""

from __future__ import annotations

from bot import config
from bot.strategies.base import Strategy
from bot.strategies.mean_reversion import MeanReversionStrategy
from bot.strategies.moving_average import MovingAverageTrendStrategy
from bot.strategies.rsi_reversal import RsiReversalStrategy


def default_strategies() -> list[Strategy]:
    return [
        MeanReversionStrategy(config.MEAN_REVERSION_WINDOW, config.MEAN_REVERSION_ENTRY_Z),
        RsiReversalStrategy(config.RSI_WINDOW, config.RSI_OVERSOLD, config.RSI_OVERBOUGHT),
        MovingAverageTrendStrategy(config.TREND_FAST_WINDOW, config.TREND_SLOW_WINDOW),
    ]


def get_strategy(name: str) -> Strategy:
    strategies = {strategy.name: strategy for strategy in default_strategies()}
    try:
        return strategies[name]
    except KeyError as exc:
        options = ", ".join(sorted(strategies))
        raise ValueError(f"Unknown strategy '{name}'. Choose one of: {options}") from exc


def get_strategies(name: str) -> list[Strategy]:
    if name == "all":
        return default_strategies()
    return [get_strategy(name)]
