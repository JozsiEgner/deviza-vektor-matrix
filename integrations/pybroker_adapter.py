from __future__ import annotations

from typing import Any, Mapping

from .common import evaluate_snapshot, position_multiplier


def pybroker_signal(
    *,
    symbol: str,
    fundamentals: tuple[float, ...],
    current_price: float,
    previous_price: float,
    observed_seconds: float,
    target_price: float,
    config: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if previous_price <= 0 or current_price <= 0:
        raise ValueError("Prices must be positive")

    market_return = (current_price - previous_price) / previous_price
    target_distance = abs(target_price - current_price) / current_price
    decision = evaluate_snapshot(
        symbol=symbol,
        fundamentals=fundamentals,
        market_return=market_return,
        observed_seconds=observed_seconds,
        target_distance=target_distance,
        config=config,
    )

    return {
        "symbol": symbol,
        "dvm_action": decision.action,
        "anomaly_score": decision.score,
        "position_multiplier": position_multiplier(decision),
        "metadata": decision.metadata,
    }


# PyBroker usage sketch:
# def execution(ctx):
#     signal = pybroker_signal(...)
#     if signal["dvm_action"] == "BLOCK":
#         ctx.sell_all_shares()
#         return
#     ctx.buy_shares = int(base_size * signal["position_multiplier"])
