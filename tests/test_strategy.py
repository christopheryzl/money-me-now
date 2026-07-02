from signal import signal
import pandas as pd

from bot.strategy import MeanReversionParams, Signal, generate_signal


def _make_df(closes: list[float]) -> pd.DataFrame:
    return pd.DataFrame({"Close": closes})


def test_generate_signal_buy_when_oversold():
    closes = [100.0] * 19 + [80.0]  # sharp drop below rolling mean
    signal = generate_signal(_make_df(closes), MeanReversionParams(window=20, entry_z=2.0))
    assert signal == Signal.BUY
    print(signal)


def test_generate_signal_sell_when_overbought():
    closes = [100.0] * 19 + [130.0]  # sharp jump above rolling mean
    signal = generate_signal(_make_df(closes), MeanReversionParams(window=20, entry_z=2.0))
    assert signal == Signal.SELL
    print(signal)


def test_generate_signal_hold_when_within_bands():
    closes = [
        100, 101, 99, 102, 98, 101, 99, 100, 102, 98,
        101, 100, 99, 102, 98, 101, 99, 100, 101, 100,
    ]
    signal = generate_signal(_make_df([float(c) for c in closes]), MeanReversionParams(window=20, entry_z=2.0))
    assert signal == Signal.HOLD

    print(signal)