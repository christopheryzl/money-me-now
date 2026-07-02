"""Static configuration for the initial scanner feature."""

# Symbols the scanner will look at. Start with one liquid, high-volume
# NASDAQ name to keep the pipeline simple; extend this list once the
# scanner, backtest, and risk layers are proven out.
WATCHLIST = ["AAPL"]

# Mean reversion parameters (see bot.strategy for the model itself).
LOOKBACK_WINDOW = 20
ENTRY_ZSCORE = 2.0
