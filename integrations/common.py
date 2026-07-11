from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from dvm import CurrencyObservation, EngineConfig, EngineResult, VectorMatrixEngine


@dataclass(frozen=True)
class TradingDecision:
    symbol: str
    action: str
    score: float
    metadata: dict[str, Any]


def build_engine(config: Mapping[str, Any] | None = None) -> VectorMatrixEngine:
    cfg = dict(config or {})
    return VectorMatrixEngine(
        EngineConfig(
            factor_weights=tuple(cfg.get("factor_weights", (0.35, 0.30, 0.20, 0.15))),
            angle_warning_deg=float(cfg.get("angle_warning_deg", 30.0)),
            angle_block_deg=float(cfg.get("angle_block_deg", 90.0)),
            speed_ratio_block=float(cfg.get("speed_ratio_block", 2.0)),
        )
    )


def evaluate_snapshot(
    *,
    symbol: str,
    fundamentals: tuple[float, ...],
    market_return: float,
    observed_seconds: float,
    target_distance: float,
    config: Mapping[str, Any] | None = None,
) -> TradingDecision:
    engine = build_engine(config)
    result: EngineResult = engine.evaluate(
        CurrencyObservation(
            symbol=symbol,
            fundamentals=fundamentals,
            market_return=market_return,
            observed_seconds=observed_seconds,
            target_distance=target_distance,
        )
    )
    return TradingDecision(
        symbol=symbol,
        action=result.action,
        score=result.anomaly_score,
        metadata=result.to_dict(),
    )


def position_multiplier(decision: TradingDecision) -> float:
    """Risk scaling only. This is not a guaranteed trading signal."""
    if decision.action == "BLOCK":
        return 0.0
    if decision.action == "REVIEW":
        return 0.25
    return 1.0
