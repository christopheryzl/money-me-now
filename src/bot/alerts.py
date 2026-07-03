"""Human-readable signal formatting."""

from __future__ import annotations

from bot.models import SignalResult
from bot.ensemble import EnsembleResult


def format_signal(result: SignalResult) -> str:
    return (
        f"{result.symbol} {result.strategy}: "
        f"signal={result.signal.value} "
        f"score={result.score:.2f} "
        f"price={result.price:.2f} "
        f"reason={result.reason}"
    )


def format_ensemble(result: EnsembleResult) -> str:
    return (
        f"{result.symbol} ensemble: "
        f"signal={result.signal.value} "
        f"score={result.score:.2f} "
        f"price={result.price:.2f} "
        f"votes={len(result.votes)}"
    )
