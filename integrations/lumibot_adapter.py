from __future__ import annotations

from typing import Any, Mapping

from .common import evaluate_snapshot, position_multiplier


def lumibot_risk_gate(
    *,
    symbol: str,
    fundamentals: tuple[float, ...],
    current_price: float,
    previous_price: float,
    observed_seconds: float,
    target_price: float,
    config: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
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
    return {
        "allow_new_order": decision.action != "BLOCK",
        "requires_review": decision.action == "REVIEW",
        "position_multiplier": position_multiplier(decision),
        "dvm": decision.metadata,
    }


# LumiBot usage sketch inside on_trading_iteration():
# gate = lumibot_risk_gate(...)
# if not gate["allow_new_order"]:
#     self.log_message("DVM blocked new order")
#     return
# quantity = int(base_quantity * gate["position_multiplier"])
