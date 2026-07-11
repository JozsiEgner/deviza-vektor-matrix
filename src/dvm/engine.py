from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable
import math

import numpy as np


@dataclass(frozen=True)
class CurrencyObservation:
    symbol: str
    fundamentals: tuple[float, ...]
    market_return: float
    observed_seconds: float
    target_distance: float


@dataclass(frozen=True)
class EngineConfig:
    factor_weights: tuple[float, ...]
    angle_warning_deg: float = 30.0
    angle_block_deg: float = 90.0
    speed_ratio_block: float = 2.0
    minimum_projected_speed: float = 1e-9


@dataclass(frozen=True)
class EngineResult:
    symbol: str
    fundamental_score: float
    market_return: float
    angle_deg: float
    projected_speed: float
    calculated_seconds_to_target: float | None
    real_to_calculated_ratio: float | None
    anomaly_score: float
    action: str
    reasons: tuple[str, ...]

    def to_dict(self) -> dict:
        return asdict(self)


class VectorMatrixEngine:
    """Reference anomaly and divergence engine.

    The engine does not prove manipulation, identify an actor, or guarantee
    future prices. It provides an auditable model-consistency signal.
    """

    def __init__(self, config: EngineConfig):
        weights = np.asarray(config.factor_weights, dtype=float)
        if weights.ndim != 1 or weights.size == 0:
            raise ValueError("factor_weights must be a non-empty vector")
        if not np.isfinite(weights).all():
            raise ValueError("factor_weights must be finite")
        total = float(np.abs(weights).sum())
        if total == 0:
            raise ValueError("factor_weights cannot all be zero")
        self.config = config
        self.weights = weights / total

    def evaluate(self, observation: CurrencyObservation) -> EngineResult:
        fundamentals = np.asarray(observation.fundamentals, dtype=float)
        if fundamentals.shape != self.weights.shape:
            raise ValueError(
                f"{observation.symbol}: expected {self.weights.size} fundamentals, "
                f"received {fundamentals.size}"
            )
        if observation.observed_seconds <= 0:
            raise ValueError("observed_seconds must be positive")
        if observation.target_distance < 0:
            raise ValueError("target_distance cannot be negative")

        normalized = self._normalize(fundamentals)
        fundamental_score = float(np.dot(normalized, self.weights))

        fundamental_vector = normalized * self.weights
        market_vector = np.sign(observation.market_return or 1.0) * np.abs(self.weights)
        angle = self._angle_deg(fundamental_vector, market_vector)

        market_speed = abs(observation.market_return) / observation.observed_seconds
        alignment = max(0.0, math.cos(math.radians(min(angle, 90.0))))
        projected_speed = market_speed * alignment

        calculated = None
        ratio = None
        reasons: list[str] = []

        if observation.target_distance == 0:
            calculated = 0.0
            ratio = 1.0
        elif projected_speed > self.config.minimum_projected_speed:
            calculated = observation.target_distance / projected_speed
            ratio = observation.observed_seconds / calculated if calculated > 0 else None
        else:
            reasons.append("Projected speed is too small to estimate a finite stopping time.")

        angle_component = min(angle / max(self.config.angle_block_deg, 1e-9), 1.0)
        speed_component = 0.0
        if ratio is not None:
            speed_component = min(max((0.5 - ratio) / 0.5, 0.0), 1.0)

        anomaly_score = round(100.0 * (0.65 * angle_component + 0.35 * speed_component), 2)

        action = "ALLOW"
        if angle >= self.config.angle_block_deg:
            action = "BLOCK"
            reasons.append("Market direction is orthogonal or opposed to the fundamental vector.")
        elif ratio is not None and ratio < (1.0 / self.config.speed_ratio_block):
            action = "BLOCK"
            reasons.append("Observed movement arrived materially faster than the modelled transit time.")
        elif angle >= self.config.angle_warning_deg:
            action = "REVIEW"
            reasons.append("Fundamental-market divergence exceeds the warning threshold.")

        if not reasons:
            reasons.append("Movement remains inside configured divergence and speed thresholds.")

        return EngineResult(
            symbol=observation.symbol,
            fundamental_score=round(fundamental_score, 8),
            market_return=observation.market_return,
            angle_deg=round(angle, 4),
            projected_speed=round(projected_speed, 12),
            calculated_seconds_to_target=None if calculated is None else round(calculated, 4),
            real_to_calculated_ratio=None if ratio is None else round(ratio, 6),
            anomaly_score=anomaly_score,
            action=action,
            reasons=tuple(reasons),
        )

    def evaluate_many(self, observations: Iterable[CurrencyObservation]) -> list[EngineResult]:
        return [self.evaluate(item) for item in observations]

    @staticmethod
    def _normalize(values: np.ndarray) -> np.ndarray:
        scale = float(np.linalg.norm(values))
        return values if scale == 0 else values / scale

    @staticmethod
    def _angle_deg(a: np.ndarray, b: np.ndarray) -> float:
        norm = float(np.linalg.norm(a) * np.linalg.norm(b))
        if norm == 0:
            return 90.0
        cosine = float(np.clip(np.dot(a, b) / norm, -1.0, 1.0))
        return math.degrees(math.acos(cosine))
