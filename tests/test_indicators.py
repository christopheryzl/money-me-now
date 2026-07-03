import pandas as pd
import pytest

from bot.indicators import donchian_channels, macd, require_close, rsi, simple_moving_average, zscore


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


def test_macd_returns_histogram_column():
    values = pd.Series([float(value) for value in range(1, 40)])
    result = macd(values, fast_window=3, slow_window=6, signal_window=3)
    assert "histogram" in result
    assert result["histogram"].notna().all()


def test_donchian_channels_uses_high_low_when_available():
    df = pd.DataFrame(
        {
            "High": [10.0, 11.0, 12.0],
            "Low": [8.0, 7.0, 9.0],
            "Close": [9.0, 10.0, 11.0],
        },
    )
    result = donchian_channels(df, 2).dropna()
    assert result.iloc[-1]["upper"] == 12.0
    assert result.iloc[-1]["lower"] == 7.0
