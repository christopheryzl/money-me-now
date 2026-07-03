"""Export chart and ensemble data for the static dashboard."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

from bot import config
from bot.data import get_daily_bars
from bot.ensemble import EnsembleResult, evaluate_ensemble
from bot.models import Signal
from bot.strategies import default_strategies


def _timestamp(value: Any) -> str:
    return pd.Timestamp(value).date().isoformat()


def _clean_number(value: Any) -> float | None:
    if pd.isna(value):
        return None
    return float(value)


def candles_from_bars(df: pd.DataFrame) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for index, row in df.iterrows():
        rows.append(
            {
                "time": _timestamp(index),
                "open": float(row["Open"]) if "Open" in df else float(row["Close"]),
                "high": float(row["High"]) if "High" in df else float(row["Close"]),
                "low": float(row["Low"]) if "Low" in df else float(row["Close"]),
                "close": float(row["Close"]),
            },
        )
    return rows


def ensemble_markers(symbol: str, df: pd.DataFrame) -> list[dict[str, str]]:
    strategies = default_strategies()
    markers: list[dict[str, str]] = []
    for end in range(2, len(df) + 1):
        sample = df.iloc[:end]
        try:
            result = evaluate_ensemble(symbol, sample, strategies)
        except ValueError:
            continue
        if result.signal == Signal.HOLD:
            continue
        markers.append(
            {
                "time": _timestamp(sample.index[-1]),
                "position": "belowBar" if result.signal == Signal.BUY else "aboveBar",
                "color": "#108a5d" if result.signal == Signal.BUY else "#c24141",
                "shape": "arrowUp" if result.signal == Signal.BUY else "arrowDown",
                "text": f"{result.signal.value} {result.score:.2f}",
            },
        )
    return markers


def serialize_ensemble(result: EnsembleResult) -> dict[str, Any]:
    return {
        "symbol": result.symbol,
        "signal": result.signal.value,
        "score": result.score,
        "price": result.price,
        "votes": [
            {
                "strategy": vote.result.strategy,
                "signal": vote.result.signal.value,
                "score": vote.result.score,
                "weight": vote.weight,
                "confidence": vote.confidence,
                "contribution": vote.contribution,
                "reason": vote.result.reason,
            }
            for vote in result.votes
        ],
    }


def moving_average_series(df: pd.DataFrame, window: int) -> list[dict[str, float | str]]:
    values = df["Close"].astype(float).rolling(window).mean()
    rows: list[dict[str, float | str]] = []
    for index, raw_value in values.items():
        value = _clean_number(raw_value)
        if value is not None:
            rows.append({"time": _timestamp(index), "value": value})
    return rows


def export_dashboard_data(
    symbol: str,
    output: Path,
    period: str = config.DEFAULT_PERIOD,
) -> Path:
    df = get_daily_bars(symbol, period=period)
    strategies = default_strategies()
    ensemble = evaluate_ensemble(symbol, df, strategies)
    payload = {
        "symbol": symbol,
        "period": period,
        "candles": candles_from_bars(df),
        "markers": ensemble_markers(symbol, df),
        "overlays": {
            "sma_fast": moving_average_series(df, config.TREND_FAST_WINDOW),
            "sma_slow": moving_average_series(df, config.TREND_SLOW_WINDOW),
        },
        "ensemble": serialize_ensemble(ensemble),
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Export static dashboard data.")
    parser.add_argument("--symbol", default=config.WATCHLIST[0])
    parser.add_argument("--period", default=config.DEFAULT_PERIOD)
    parser.add_argument(
        "--output",
        default="dashboard/data/latest.json",
        help="JSON output path consumed by dashboard/app.js",
    )
    args = parser.parse_args()

    path = export_dashboard_data(args.symbol, Path(args.output), args.period)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
