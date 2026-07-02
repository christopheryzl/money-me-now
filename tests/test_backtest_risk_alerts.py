import pandas as pd

from bot.alerts import format_signal
from bot.backtest import backtest_long_short
from bot.models import Signal
from bot.risk import position_size
from bot.strategies.moving_average import MovingAverageTrendStrategy


def test_position_size_uses_cash_risk_budget():
    assert position_size(10_000.0, 0.01, 100.0, 95.0) == 20


def test_format_signal_includes_key_fields():
    df = pd.DataFrame({"Close": [float(value) for value in range(1, 11)]})
    result = MovingAverageTrendStrategy(fast_window=2, slow_window=5).evaluate("AAPL", df)
    text = format_signal(result)
    assert "AAPL" in text
    assert "moving-average-trend" in text
    assert Signal.BUY.value in text


def test_backtest_returns_summary():
    df = pd.DataFrame({"Close": [10.0] * 5 + [20.0] * 5})
    result = backtest_long_short(
        "AAPL",
        df,
        MovingAverageTrendStrategy(fast_window=2, slow_window=5),
    )
    assert result.symbol == "AAPL"
    assert result.strategy == "moving-average-trend"
    assert result.bars == 10
