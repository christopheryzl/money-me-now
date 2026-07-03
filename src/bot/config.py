"""Static configuration for the scanner."""

WATCHLIST = ["AAPL", "MSFT", "NVDA"]

DEFAULT_PERIOD = "6mo"
DEFAULT_STRATEGIES = [
    "mean-reversion",
    "rsi-reversal",
    "moving-average-trend",
    "macd-momentum",
    "donchian-breakout",
]

STRATEGY_WEIGHTS = {
    "mean-reversion": 0.25,
    "rsi-reversal": 0.15,
    "moving-average-trend": 0.25,
    "macd-momentum": 0.20,
    "donchian-breakout": 0.15,
}

GLOBAL_BUY_THRESHOLD = 0.25
GLOBAL_SELL_THRESHOLD = -0.25

MEAN_REVERSION_WINDOW = 20
MEAN_REVERSION_ENTRY_Z = 2.0

RSI_WINDOW = 14
RSI_OVERSOLD = 30.0
RSI_OVERBOUGHT = 70.0

TREND_FAST_WINDOW = 20
TREND_SLOW_WINDOW = 50

MACD_FAST_WINDOW = 12
MACD_SLOW_WINDOW = 26
MACD_SIGNAL_WINDOW = 9

DONCHIAN_WINDOW = 20

ACCOUNT_EQUITY = 10_000.0
RISK_PER_TRADE = 0.01
