"""Shared domain models for scanner output."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Signal(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


@dataclass(frozen=True)
class SignalResult:
    symbol: str
    strategy: str
    signal: Signal
    score: float
    price: float
    reason: str
    metadata: dict[str, float | int | str] = field(default_factory=dict)
