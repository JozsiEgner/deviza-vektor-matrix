from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import CurrencyObservation, EngineConfig, VectorMatrixEngine


def main() -> None:
    parser = argparse.ArgumentParser(description="Deviza-Vektor Matrix evaluator")
    parser.add_argument("input_json", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.input_json.read_text(encoding="utf-8"))
    config = EngineConfig(**payload["config"])
    observations = [CurrencyObservation(**item) for item in payload["observations"]]
    results = VectorMatrixEngine(config).evaluate_many(observations)
    print(json.dumps([result.to_dict() for result in results], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
