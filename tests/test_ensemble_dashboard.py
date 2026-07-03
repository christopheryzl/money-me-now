import pandas as pd

from bot.dashboard_export import candles_from_bars, serialize_ensemble
from bot.ensemble import evaluate_ensemble, normalize_weights
from bot.models import Signal
from bot.strategies.moving_average import MovingAverageTrendStrategy


def test_normalize_weights_scales_positive_weights():
    weights = normalize_weights({"a": 2.0, "b": 1.0})
    assert weights["a"] == 2 / 3
    assert weights["b"] == 1 / 3


def test_ensemble_combines_weighted_strategy_votes():
    df = pd.DataFrame({"Close": [float(value) for value in range(1, 20)]})
    result = evaluate_ensemble(
        "AAPL",
        df,
        [MovingAverageTrendStrategy(fast_window=2, slow_window=5)],
        {"moving-average-trend": 1.0},
    )
    assert result.signal == Signal.BUY
    assert result.score > 0
    assert result.votes[0].confidence > 0


def test_dashboard_serializes_candles_and_ensemble():
    df = pd.DataFrame(
        {"Open": [1.0], "High": [2.0], "Low": [0.5], "Close": [1.5]},
        index=pd.to_datetime(["2026-01-01"]),
    )
    candles = candles_from_bars(df)
    assert candles == [{"time": "2026-01-01", "open": 1.0, "high": 2.0, "low": 0.5, "close": 1.5}]

    result = evaluate_ensemble(
        "AAPL",
        pd.DataFrame({"Close": [float(value) for value in range(1, 20)]}),
        [MovingAverageTrendStrategy(fast_window=2, slow_window=5)],
        {"moving-average-trend": 1.0},
    )
    payload = serialize_ensemble(result)
    assert payload["signal"] == "BUY"
    assert payload["votes"][0]["strategy"] == "moving-average-trend"
