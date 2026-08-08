from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01_systems" / "KALMIYA_System"))

from modules.advanced_capabilities import PersonalityStyleEngine


def test_personality_style_humano():
    engine = PersonalityStyleEngine(style="humano")
    result = engine.apply("Hola, necesito ayuda")
    assert "Hola" in result or "calidez" in result


def test_personality_style_divertido():
    engine = PersonalityStyleEngine(style="divertido")
    result = engine.apply("Estoy muy frustrado")
    assert "estilo" in result or "golpe" in result


def test_personality_style_estrategico():
    engine = PersonalityStyleEngine(style="estrategico")
    result = engine.apply("Necesito un plan")
    assert "objetivo" in result or "prioridades" in result


def test_personality_style_emocional():
    engine = PersonalityStyleEngine(style="emocional")
    result = engine.apply("Estoy muy frustrado")
    assert "empatía" in result or "calidez" in result or "creativa" in result
