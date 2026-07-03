"""CLI entry point for scanning configured instruments."""

from __future__ import annotations

import argparse

from bot import config
from bot.alerts import format_ensemble, format_signal
from bot.data import get_daily_bars
from bot.ensemble import evaluate_ensemble
from bot.strategies import get_strategies


def scan_symbol(
    symbol: str,
    strategy_name: str = "all",
    period: str = config.DEFAULT_PERIOD,
    include_ensemble: bool = True,
) -> list[str]:
    df = get_daily_bars(symbol, period=period)
    strategies = get_strategies(strategy_name)
    lines: list[str] = []
    for strategy in strategies:
        result = strategy.evaluate(symbol, df)
        lines.append(format_signal(result))
    if include_ensemble and len(strategies) > 1:
        lines.append(format_ensemble(evaluate_ensemble(symbol, df, strategies)))
    return lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan instruments for trading signals.")
    parser.add_argument("--symbol", action="append", help="Ticker symbol to scan; repeatable")
    parser.add_argument(
        "--strategy",
        default="all",
        help="Strategy to run: all, mean-reversion, rsi-reversal, moving-average-trend",
    )
    parser.add_argument("--period", default=config.DEFAULT_PERIOD, help="yfinance lookback period")
    parser.add_argument(
        "--no-ensemble",
        action="store_true",
        help="Only print per-strategy signals",
    )
    args = parser.parse_args()

    symbols = args.symbol or config.WATCHLIST
    for symbol in symbols:
        for line in scan_symbol(symbol, args.strategy, args.period, not args.no_ensemble):
            print(line)


if __name__ == "__main__":
    main()
