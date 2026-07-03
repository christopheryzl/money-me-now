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

Export dashboard data and serve the visual dashboard:

```
python -m bot.dashboard_export --symbol AAPL --output dashboard/data/latest.json
cd dashboard
python -m http.server 8787
```

Then open `http://127.0.0.1:8787`.

The scanner prints structured signal lines such as:

```
AAPL mean-reversion: signal=HOLD score=1.49 price=307.66 reason=z-score 1.49 within +/-2.00
AAPL ensemble: signal=HOLD score=0.05 price=308.63 votes=5
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
- **MACD momentum**: uses MACD histogram direction to detect momentum shifts.
- **Donchian breakout**: watches for price breaking out beyond the prior
  channel high or low.

These strategies cover different market assumptions: stretched-price reversion,
momentum exhaustion, trend following, momentum confirmation, and breakout
continuation. They are simple enough to test and backtest before broker
integration enters the picture.

## Weighted Ensemble

Strategies are evaluated concurrently on the same latest bar. Each strategy
produces a direction, confidence, and configured weight. The ensemble converts
those votes into a global score:

```
global_score = sum(strategy_direction * confidence * normalized_weight)
```

The default weights are configured in `src/bot/config.py`:

- mean reversion: `0.25`
- RSI reversal: `0.15`
- moving-average trend: `0.25`
- MACD momentum: `0.20`
- Donchian breakout: `0.15`

The global signal is `BUY` above `0.25`, `SELL` below `-0.25`, and `HOLD`
between those thresholds. These are research defaults, not trading advice.

## Dashboard

The dashboard in `dashboard/` uses TradingView Lightweight Charts to visualize:

- daily candlesticks
- fast and slow moving averages
- ensemble BUY/SELL markers
- per-strategy weight, confidence, and contribution
- the current global signal and score

## Project Structure

```
dashboard/              - static chart dashboard
src/bot/
  alerts.py              - human-readable signal formatting
  backtest.py            - simple historical signal evaluation
  config.py              - watchlist and strategy parameters
  dashboard_export.py    - dashboard JSON exporter
  data.py                - market data fetching with yfinance
  ensemble.py            - weighted concurrent strategy voting
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
