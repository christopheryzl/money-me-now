"""Shared domain models for scanner output."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Signal(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

    @property
    def direction(self) -> int:
        if self == Signal.BUY:
            return 1
        if self == Signal.SELL:
            return -1
        return 0


@dataclass(frozen=True)
class SignalResult:
    symbol: str
    strategy: str
    signal: Signal
    score: float
    price: float
    reason: str
    metadata: dict[str, float | int | str] = field(default_factory=dict)
