from __future__ import annotations

import json
import sys
from typing import Any

from .common import evaluate_snapshot, position_multiplier


def evaluate_payload(payload: dict[str, Any]) -> dict[str, Any]:
    decision = evaluate_snapshot(
        symbol=str(payload["symbol"]),
        fundamentals=tuple(float(x) for x in payload["fundamentals"]),
        market_return=float(payload["market_return"]),
        observed_seconds=float(payload["observed_seconds"]),
        target_distance=float(payload["target_distance"]),
        config=payload.get("config"),
    )
    return {
        "action": decision.action,
        "anomaly_score": decision.score,
        "position_multiplier": position_multiplier(decision),
        "metadata": decision.metadata,
    }


def main() -> None:
    payload = json.loads(sys.stdin.read())
    print(json.dumps(evaluate_payload(payload), ensure_ascii=False))


if __name__ == "__main__":
    main()


# LEAN integration approach:
# 1. Serialize the current symbol snapshot to JSON in C#.
# 2. Call this bridge as a local process or wrap it in an HTTP service.
# 3. Parse action, anomaly_score and position_multiplier.
# 4. Run in shadow mode before allowing automated order rejection.
