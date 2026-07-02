"""Market data fetching utilities."""

from __future__ import annotations

import pandas as pd
import yfinance as yf


def get_daily_bars(symbol: str, period: str = "6mo") -> pd.DataFrame:
    """Fetch daily OHLCV bars for a single symbol."""
    df = yf.download(symbol, period=period, interval="1d", progress=False, auto_adjust=True)
    if df.empty:
        raise ValueError(f"No data returned for symbol '{symbol}'")
    if isinstance(df.columns, pd.MultiIndex):
        # yfinance returns a (Price, Ticker) MultiIndex even for a single
        # symbol; drop the ticker level since we only ever fetch one.
        df.columns = df.columns.droplevel("Ticker")
    df.index.name = "date"
    return df
