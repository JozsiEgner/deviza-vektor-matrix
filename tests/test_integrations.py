from integrations.common import TradingDecision, position_multiplier
from integrations.pybroker_adapter import pybroker_signal


def test_position_multiplier_mapping():
    assert position_multiplier(TradingDecision("EUR", "ALLOW", 10.0, {})) == 1.0
    assert position_multiplier(TradingDecision("EUR", "REVIEW", 50.0, {})) == 0.25
    assert position_multiplier(TradingDecision("EUR", "BLOCK", 90.0, {})) == 0.0


def test_pybroker_adapter_returns_risk_fields():
    result = pybroker_signal(
        symbol="EURUSD",
        fundamentals=(0.3, 0.2, -0.1, -0.2),
        current_price=1.10,
        previous_price=1.099,
        observed_seconds=60,
        target_price=1.105,
    )
    assert result["dvm_action"] in {"ALLOW", "REVIEW", "BLOCK"}
    assert 0.0 <= result["position_multiplier"] <= 1.0
    assert "metadata" in result
