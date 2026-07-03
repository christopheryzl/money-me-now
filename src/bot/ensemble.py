"""Concurrent weighted strategy ensemble."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from bot import config
from bot.models import Signal, SignalResult
from bot.strategies.base import Strategy


@dataclass(frozen=True)
class WeightedVote:
    result: SignalResult
    weight: float
    confidence: float
    contribution: float


@dataclass(frozen=True)
class EnsembleResult:
    symbol: str
    signal: Signal
    score: float
    votes: list[WeightedVote]

    @property
    def price(self) -> float:
        if not self.votes:
            raise ValueError("EnsembleResult has no votes")
        return self.votes[0].result.price


def confidence_for_result(result: SignalResult) -> float:
    if result.signal == Signal.HOLD:
        return 0.0

    score = abs(result.score)
    metadata = result.metadata
    if result.strategy == "mean-reversion":
        return min(score / float(metadata["entry_z"]), 1.0)
    if result.strategy == "rsi-reversal":
        neutral = 50.0
        threshold = (
            abs(neutral - float(metadata["oversold"]))
            if result.signal == Signal.BUY
            else abs(float(metadata["overbought"]) - neutral)
        )
        return min(abs(score - neutral) / threshold, 1.0)
    if result.strategy == "moving-average-trend":
        return min(score / max(result.price * 0.03, 1e-9), 1.0)
    if result.strategy == "macd-momentum":
        return min(score / max(result.price * 0.01, 1e-9), 1.0)
    if result.strategy == "donchian-breakout":
        return min(score, 1.0)
    return min(score, 1.0)


def normalize_weights(weights: dict[str, float]) -> dict[str, float]:
    total = sum(weight for weight in weights.values() if weight > 0)
    if total <= 0:
        raise ValueError("At least one strategy weight must be positive")
    return {name: max(weight, 0.0) / total for name, weight in weights.items()}


def global_signal(score: float) -> Signal:
    if score >= config.GLOBAL_BUY_THRESHOLD:
        return Signal.BUY
    if score <= config.GLOBAL_SELL_THRESHOLD:
        return Signal.SELL
    return Signal.HOLD


def evaluate_ensemble(
    symbol: str,
    df: pd.DataFrame,
    strategies: list[Strategy],
    weights: dict[str, float] | None = None,
) -> EnsembleResult:
    active_weights = normalize_weights(weights or config.STRATEGY_WEIGHTS)
    votes: list[WeightedVote] = []

    for strategy in strategies:
        result = strategy.evaluate(symbol, df)
        weight = active_weights.get(result.strategy, 0.0)
        confidence = confidence_for_result(result)
        contribution = result.signal.direction * confidence * weight
        votes.append(
            WeightedVote(
                result=result,
                weight=weight,
                confidence=confidence,
                contribution=contribution,
            ),
        )

    score = sum(vote.contribution for vote in votes)
    return EnsembleResult(symbol=symbol, signal=global_signal(score), score=score, votes=votes)
