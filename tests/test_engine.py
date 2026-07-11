from dvm import CurrencyObservation, EngineConfig, VectorMatrixEngine


def test_engine_returns_valid_action():
    engine = VectorMatrixEngine(EngineConfig(factor_weights=(0.4, 0.3, 0.2, 0.1)))
    result = engine.evaluate(
        CurrencyObservation(
            symbol="EUR",
            fundamentals=(0.5, 0.3, -0.1, 0.2),
            market_return=0.001,
            observed_seconds=60,
            target_distance=0.003,
        )
    )
    assert result.action in {"ALLOW", "REVIEW", "BLOCK"}
    assert 0 <= result.anomaly_score <= 100


def test_dimension_validation():
    engine = VectorMatrixEngine(EngineConfig(factor_weights=(0.5, 0.5)))
    try:
        engine.evaluate(
            CurrencyObservation(
                symbol="EUR",
                fundamentals=(1.0,),
                market_return=0.01,
                observed_seconds=10,
                target_distance=0.02,
            )
        )
    except ValueError:
        return
    raise AssertionError("Expected ValueError")
