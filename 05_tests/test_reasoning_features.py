import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01_systems" / "KALMIYA_System"))

from brain import ask_kalmiya, clear_conversation


def test_ask_kalmiya_uses_local_reasoning_when_no_engine_is_available():
    clear_conversation()
    response = ask_kalmiya("Estoy muy frustrado y no sé cómo resolver este problema", force_engine="gemini")
    lowered = response.lower()
    assert "entiendo" in lowered or "estoy aquí" in lowered or "paso" in lowered
    assert "problema" in lowered or "resolver" in lowered


def test_ask_kalmiya_supports_structured_problem_solving():
    clear_conversation()
    response = ask_kalmiya("Necesito planear una rutina de estudio para aprobar el examen", force_engine="gemini")
    lowered = response.lower()
    assert "paso 1" in lowered or "1." in lowered or "objetivo" in lowered
    assert "estudio" in lowered or "rutina" in lowered
