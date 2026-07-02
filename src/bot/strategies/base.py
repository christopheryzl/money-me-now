"""Strategy protocol and registry helpers."""

from __future__ import annotations

from typing import Protocol

import pandas as pd

from bot.models import SignalResult


class Strategy(Protocol):
    name: str

    def evaluate(self, symbol: str, df: pd.DataFrame) -> SignalResult:
        """Evaluate the latest bar and return a signal result."""
