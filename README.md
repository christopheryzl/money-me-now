# money-me-now

A practice project for building a quantitative trading bot in Python 3.12.

This is an educational signal scanner and research harness. It does not place
orders and should not be used as investment advice.

## Setup

```
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate  # macOS/Linux

pip install -e ".[dev]"
```

## Usage

Scan all configured symbols with all strategies:

```
python -m bot.scanner
```

Scan one symbol with one strategy:

```
python -m bot.scanner --symbol AAPL --strategy rsi-reversal
```

The scanner prints structured signal lines such as:

```
AAPL mean-reversion: signal=HOLD score=1.49 price=307.66 reason=z-score 1.49 within +/-2.00
```

## Strategies

The project intentionally starts with a small strategy set instead of one
monolithic method:

- **Mean reversion**: buys statistically oversold closes and sells
  statistically overbought closes using a rolling z-score.
- **RSI reversal**: buys when RSI is below an oversold threshold and sells
  when RSI is above an overbought threshold.
- **Moving-average trend**: follows simple trend direction using fast/slow
  moving-average crossovers.

These three strategies cover different market assumptions: stretched-price
reversion, momentum exhaustion, and trend following. They are simple enough to
test and backtest before broker integration enters the picture.

## Project Structure

```
src/bot/
  alerts.py              - human-readable signal formatting
  backtest.py            - simple historical signal evaluation
  config.py              - watchlist and strategy parameters
  data.py                - market data fetching with yfinance
  indicators.py          - reusable indicator calculations
  models.py              - shared Signal and SignalResult types
  risk.py                - position sizing helpers
  scanner.py             - CLI entry point
  strategies/            - pluggable strategy implementations
tests/                   - unit tests
```

## Running Tests

```
pytest
ruff check .
```

## Roadmap

Before this can touch paper or real money, keep building in this order:

1. Backtest strategies against clean historical data.
2. Add risk limits and position sizing.
3. Persist signals and backtest results.
4. Add market calendar awareness and scheduling.
5. Add alerts for reviewed signals.
6. Add paper trading behind explicit disabled-by-default settings.
7. Add broker integration only after tests, backtests, and risk controls are in place.

## Git Best Practices

- Never commit directly to `main`; open a pull request.
- Keep branches short-lived and focused.
- Pull before starting work and before pushing if others may have changed the repo.
- Do not commit secrets, credentials, local data, or generated artifacts.
