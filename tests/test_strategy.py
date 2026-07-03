import pandas as pd
import pytest

from bot.models import Signal
from bot.strategy import MeanReversionParams, generate_signal
from bot.strategies.mean_reversion import MeanReversionStrategy
from bot.strategies.moving_average import MovingAverageTrendStrategy
from bot.strategies.rsi_reversal import RsiReversalStrategy
from bot.strategies.macd_momentum import MacdMomentumStrategy
from bot.strategies.donchian_breakout import DonchianBreakoutStrategy


def _make_df(closes: list[float]) -> pd.DataFrame:
    return pd.DataFrame({"Close": closes})


def test_generate_signal_buy_when_oversold():
    closes = [100.0] * 19 + [80.0]
    signal = generate_signal(_make_df(closes), MeanReversionParams(window=20, entry_z=2.0))
    assert signal == Signal.BUY


def test_generate_signal_sell_when_overbought():
    closes = [100.0] * 19 + [130.0]
    signal = generate_signal(_make_df(closes), MeanReversionParams(window=20, entry_z=2.0))
    assert signal == Signal.SELL


def test_generate_signal_hold_when_within_bands():
    closes = [
        100,
        101,
        99,
        102,
        98,
        101,
        99,
        100,
        102,
        98,
        101,
        100,
        99,
        102,
        98,
        101,
        99,
        100,
        101,
        100,
    ]
    signal = generate_signal(_make_df([float(c) for c in closes]), MeanReversionParams())
    assert signal == Signal.HOLD


def test_mean_reversion_rejects_insufficient_data():
    with pytest.raises(ValueError, match="Not enough data"):
        MeanReversionStrategy(window=20).evaluate("AAPL", _make_df([100.0, 101.0]))


def test_rsi_reversal_buy_when_oversold():
    closes = [100.0, 99.0, 98.0, 97.0, 96.0]
    result = RsiReversalStrategy(window=3, oversold=30, overbought=70).evaluate(
        "AAPL",
        _make_df(closes),
    )
    assert result.signal == Signal.BUY


def test_rsi_reversal_sell_when_overbought():
    closes = [96.0, 97.0, 98.0, 99.0, 100.0]
    result = RsiReversalStrategy(window=3, oversold=30, overbought=70).evaluate(
        "AAPL",
        _make_df(closes),
    )
    assert result.signal == Signal.SELL


def test_moving_average_trend_buy_when_fast_average_above_slow_average():
    closes = [float(value) for value in range(1, 11)]
    result = MovingAverageTrendStrategy(fast_window=2, slow_window=5).evaluate(
        "AAPL",
        _make_df(closes),
    )
    assert result.signal == Signal.BUY


def test_moving_average_trend_rejects_invalid_windows():
    with pytest.raises(ValueError, match="fast_window"):
        MovingAverageTrendStrategy(fast_window=5, slow_window=5)


def test_macd_momentum_signals_on_uptrend():
    df = _make_df([float(value) for value in range(1, 50)])
    result = MacdMomentumStrategy(fast_window=3, slow_window=6, signal_window=3).evaluate(
        "AAPL",
        df,
    )
    assert result.signal == Signal.BUY


def test_donchian_breakout_buy_when_price_breaks_prior_high():
    df = pd.DataFrame(
        {
            "High": [10.0, 11.0, 12.0, 13.0, 14.0],
            "Low": [8.0, 9.0, 10.0, 11.0, 12.0],
            "Close": [9.0, 10.0, 11.0, 12.0, 15.0],
        },
    )
    result = DonchianBreakoutStrategy(window=3).evaluate("AAPL", df)
    assert result.signal == Signal.BUY
