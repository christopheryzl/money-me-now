import pandas as pd
import pytest

from bot.indicators import require_close, rsi, simple_moving_average, zscore


def test_require_close_rejects_missing_column():
    with pytest.raises(ValueError, match="Close"):
        require_close(pd.DataFrame({"Open": [1.0]}))


def test_zscore_returns_latest_value_for_rolling_window():
    values = pd.Series([100.0] * 19 + [80.0])
    assert zscore(values, 20).dropna().iloc[-1] < -2.0


def test_rsi_detects_losses():
    values = pd.Series([100.0, 99.0, 98.0, 97.0, 96.0])
    assert rsi(values, 3).dropna().iloc[-1] == 0.0


def test_simple_moving_average():
    values = pd.Series([1.0, 2.0, 3.0])
    assert simple_moving_average(values, 2).iloc[-1] == 2.5
