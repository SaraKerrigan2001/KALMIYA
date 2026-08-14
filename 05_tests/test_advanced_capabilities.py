from pathlib import Path

from modules.advanced_capabilities import (
    BehaviorAnalytics,
    IoTCommandParser,
    LocalBlockchainLedger,
    ResponsePredictionEngine,
)


def test_response_prediction_engine_detects_emotional_support():
    engine = ResponsePredictionEngine()
    prediction = engine.analyze("Estoy muy frustrado y no sé cómo resolver este problema")

    assert prediction["intent"] == "emotional_support"
    assert prediction["confidence"] >= 0.5


def test_behavior_analytics_tracks_user_style(tmp_path):
    analytics = BehaviorAnalytics(data_dir=str(tmp_path))
    profile = analytics.observe("Necesito un plan para estudiar", "Plan claro")

    assert profile["interaction_count"] >= 1
    assert profile["preferred_style"] in {"empathetic", "direct", "structured"}


def test_blockchain_ledger_is_verifiable(tmp_path):
    ledger = LocalBlockchainLedger(data_dir=str(tmp_path))
    entry = ledger.record({"message": "hola", "response": "hola"})

    assert entry["hash"]
    assert ledger.verify()


def test_iot_parser_detects_device_commands():
    parser = IoTCommandParser()
    result = parser.parse("enciende la luz del cuarto")

    assert result["action"] == "on"
    assert result["device"] == "light"
