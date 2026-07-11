from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .common import evaluate_snapshot, position_multiplier


@dataclass(frozen=True)
class NautilusRiskDecision:
    block_order: bool
    reduce_only: bool
    size_multiplier: float
    reason: str
    metadata: dict[str, Any]


def nautilus_risk_decision(
    *,
    symbol: str,
    fundamentals: tuple[float, ...],
    current_price: float,
    previous_price: float,
    observed_seconds: float,
    target_price: float,
    config: Mapping[str, Any] | None = None,
) -> NautilusRiskDecision:
    if min(current_price, previous_price) <= 0:
        raise ValueError("Prices must be positive")

    decision = evaluate_snapshot(
        symbol=symbol,
        fundamentals=fundamentals,
        market_return=(current_price - previous_price) / previous_price,
        observed_seconds=observed_seconds,
        target_distance=abs(target_price - current_price) / current_price,
        config=config,
    )

    return NautilusRiskDecision(
        block_order=decision.action == "BLOCK",
        reduce_only=decision.action in {"BLOCK", "REVIEW"},
        size_multiplier=position_multiplier(decision),
        reason="; ".join(decision.metadata["reasons"]),
        metadata=decision.metadata,
    )


# NautilusTrader usage sketch:
# decision = nautilus_risk_decision(...)
# if decision.block_order:
#     self.log.warning(f"DVM blocked order: {decision.reason}")
#     return
# qty = base_qty * decision.size_multiplier
# submit_order(qty=qty, reduce_only=decision.reduce_only)
