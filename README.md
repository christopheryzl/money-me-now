# money-me-now

A practice project for building a quantitative trading bot in Python 3.12.

## Setup

```
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell
# source .venv/bin/activate  # macOS/Linux

pip install -e ".[dev]"
```

## Project Structure

```
src/bot/
  config.py    - watchlist and strategy parameters
  data.py      - market data fetching (yfinance)
  strategy.py  - signal generation logic
  scanner.py   - CLI entry point
tests/         - unit tests
```

## Usage

Scan the default watchlist symbol for a signal:

```
python -m bot.scanner --symbol AAPL
```

Prints the current signal, z-score, and closing price, e.g. `AAPL: signal=HOLD zscore=1.49 close=307.66`.

## Running Tests

```
pytest
```

## Strategy: Bollinger Band Z-Score Mean Reversion

The initial model (`bot.strategy`) is a **mean reversion** strategy: it tracks
a rolling 20-day mean and standard deviation of closing price, converts the
latest close into a z-score, and signals **BUY** when price is 2+ standard
deviations below the mean (oversold) or **SELL** when 2+ standard deviations
above (overbought).

**Why this model first:**
- It only needs OHLCV price data — no fundamentals, no alternative data, no
  broker integration — so it's the smallest possible end-to-end pipeline
  (fetch → compute → signal) to get right before adding complexity.
- Z-score thresholds are simple, interpretable, and easy to unit test, which
  matters more than edge when the goal is learning the plumbing.
- It introduces the building blocks (rolling statistics, a `Signal` enum,
  configurable parameters) that later, more sophisticated models can reuse.

The default instrument is **AAPL**: a highly liquid NASDAQ mega-cap with
tight spreads and deep volume, which keeps price action closer to "signal"
and reduces the microstructure noise (wide spreads, thin books) that would
confound this model on a smaller/illiquid name. The watchlist is
configurable in `src/bot/config.py`.

**Disclaimer:** this is an educational exercise, not investment advice. Any
signal produced here has not been backtested or risk-managed — do not trade
on it.

## Roadmap / Known Gaps

This is a signal scanner only. Notably missing before this could touch real
(or even paper) money:

- **Execution/broker integration** — no order placement or paper-trading
  connection (e.g. Alpaca, Interactive Brokers).
- **Backtesting** — the strategy only evaluates the latest bar; there's no
  historical simulation to validate edge before trusting a signal.
- **Risk management** — no position sizing, stop-loss/take-profit, or
  portfolio-level exposure limits.
- **Secrets management** — no `.env` / `python-dotenv` pattern yet for the
  API keys a broker integration will need (`.env` is gitignored, but there's
  no `.env.example` template).
- **Scheduling & market calendar awareness** — nothing runs the scanner
  periodically, and it doesn't check NASDAQ trading hours/holidays or
  timezones.
- **Logging & alerting** — signals only print to stdout; no structured logs
  or notification channel (email/Slack/webhook).
- **CI pipeline** — no GitHub Actions workflow running tests/linting on
  push/PR.
- **Linting/formatting** — no ruff/black/mypy configured.
- **Data persistence** — signals aren't stored, so there's no way to review
  history or measure live accuracy over time.
- **Broader test coverage** — only the strategy math is unit tested; no
  tests for data-fetch failures, retries, or malformed responses.

---

# Git Best Practices

A quick reference for working effectively with Git on this repository.

## Branching

- **Never commit directly to `main`.** Treat it as always deployable.
- Create a new branch for every feature, fix, or experiment:
  ```
  git checkout -b feature/short-description
  ```
- Use a consistent naming scheme, e.g. `feature/...`, `fix/...`, `chore/...`, `experiment/...`.
- Keep branches short-lived. Long-running branches drift from `main` and accumulate painful merge conflicts.
- Branch off the latest `main` (`git pull` first) so you're not building on stale code.
- Delete branches after they're merged (`git branch -d feature/short-description`) to keep the branch list clean.

## Pulling

- **Pull before you start work** each session to make sure you're building on the latest code.
- **Pull before you push** if others may have pushed in the meantime — this avoids unnecessary conflicts.
- Prefer `git pull --rebase` over a plain `git pull` on feature branches you own alone. It keeps history linear instead of creating merge commits for every sync.
  ```
  git pull --rebase origin main
  ```
- Never `pull --rebase` on a branch other people are also pushing to — it rewrites history they may depend on.

## Committing

- Commit early and often on your own branch; squash/clean up before merging if needed.
- Write commit messages that explain **why**, not just what — the diff already shows what changed.
- Keep commits focused on a single logical change. Avoid mixing unrelated changes in one commit.
- Don't commit secrets, credentials, or generated/build artifacts. Use a `.gitignore`.

## Merging / Pull Requests

- Open a pull request instead of pushing straight to `main`, even solo — it gives you a diff to review and a record of why the change happened.
- Prefer **squash merging** for feature branches to keep `main`'s history clean, one commit per change.
- Resolve conflicts locally (via rebase or merge) before requesting/using a PR merge — don't resolve them in the GitHub UI for anything non-trivial.

## Other Key Practices

- **`.gitignore` early.** Set it up before your first commit so build output, `node_modules`, `.env` files, etc. never enter history.
- **Tag releases** (`git tag v1.0.0`) for meaningful milestones so you can always check out a known-good state.
- **Use `git status` and `git diff` before every commit** to confirm exactly what you're staging.
- **Avoid force-pushing (`git push --force`) to shared branches.** If you must rewrite your own feature branch's history after pushing, use `git push --force-with-lease` instead — it fails safely if someone else pushed in the meantime.
- **Stash, don't discard.** If you need to switch branches with uncommitted work, use `git stash` rather than losing changes.
- **Review history with `git log --oneline --graph --all`** to understand branch structure at a glance.
- **Never rewrite published history on `main`** (no `rebase`, `commit --amend`, or `reset --hard` on commits others may have pulled).
