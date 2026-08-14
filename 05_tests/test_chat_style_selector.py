from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01_systems" / "KALMIYA_System"))

from modules.advanced_capabilities import PersonalityStyleEngine


def test_selector_supports_available_styles():
    engine = PersonalityStyleEngine(style="humano")
    for style in ["humano", "divertido", "estrategico", "emocional"]:
        engine.set_style(style)
        assert engine.style == style
