"""Simple risk helpers for research and paper-trading preparation."""

from __future__ import annotations


def position_size(
    account_equity: float,
    risk_per_trade: float,
    entry_price: float,
    stop_price: float,
) -> int:
    if account_equity <= 0:
        raise ValueError("account_equity must be positive")
    if not 0 < risk_per_trade <= 1:
        raise ValueError("risk_per_trade must be between 0 and 1")
    risk_per_share = abs(entry_price - stop_price)
    if risk_per_share <= 0:
        raise ValueError("entry_price and stop_price must differ")
    return int((account_equity * risk_per_trade) // risk_per_share)
