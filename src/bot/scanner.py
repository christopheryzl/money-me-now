"""CLI entry point: scan a single NASDAQ instrument for a mean-reversion signal."""

from __future__ import annotations

import argparse

from . import config
from .data import get_daily_bars
from .strategy import MeanReversionParams, compute_zscore, generate_signal


def scan(symbol: str) -> None:
    df = get_daily_bars(symbol)
    params = MeanReversionParams(window=config.LOOKBACK_WINDOW, entry_z=config.ENTRY_ZSCORE)
    signal = generate_signal(df, params)
    zscore = compute_zscore(df["Close"], params.window).dropna().iloc[-1]
    close = df["Close"].iloc[-1]

    print(f"{symbol}: signal={signal.value} zscore={zscore:.2f} close={close:.2f}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scan a NASDAQ instrument for a mean-reversion signal.")
    parser.add_argument("--symbol", default=config.WATCHLIST[0], help="Ticker symbol to scan")
    args = parser.parse_args()
    scan(args.symbol)


if __name__ == "__main__":
    main()
