"""Pruebas de la capa de seguridad e inteligencia avanzada de KALMIYA."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "01_systems" / "KALMIYA_System"))


def test_intelligence_module_import():
    """Verifica que el módulo ASI se importa de forma estable."""
    try:
        from intelligence.kalmiya_asi import (
            INTELLIGENCE_LEVELS,
            activate_asi,
            deactivate_asi,
            get_asi_status,
            asi_multidimensional_analysis,
            asi_cognitive_synthesis,
            asi_metacognition,
            asi_predictive_thought,
            asi_creative_solution,
            generate_asi_thought,
            get_intelligence_level,
            is_asi_active,
        )
        assert "ASI" in INTELLIGENCE_LEVELS
        assert INTELLIGENCE_LEVELS["ASI"]["thought_interval"] == 60
        assert callable(activate_asi)
        assert callable(generate_asi_thought)
        assert callable(get_asi_status)
    except Exception as exc:  # pragma: no cover
        raise AssertionError(f"No se pudo importar el módulo ASI: {exc}")


def test_asi_mode_state_basics():
    """Verifica que el estado de ASI mantiene formato básico correcto."""
    from intelligence.kalmiya_asi import get_asi_status, get_intelligence_level, is_asi_active

    status = get_asi_status()
    assert "nivel_activo" in status
    assert "capacidades" in status
    assert "thought_interval" in status
    assert get_intelligence_level() in {"ANI", "AGI", "ASI"}
    assert isinstance(is_asi_active(), bool)


def test_asi_generators_return_meaningful_content():
    """Verifica que las funciones de generación ASI devuelven contenido útil."""
    from intelligence.kalmiya_asi import generate_asi_thought

    thought = generate_asi_thought()
    assert isinstance(thought, str)
    assert len(thought) > 80
    assert "KALMIYA" in thought or "ASI" in thought


def test_security_capacity_keywords_exist():
    """Verifica que el modelo ASI incluye capacidades de seguridad e inteligencia."""
    from intelligence.kalmiya_asi import INTELLIGENCE_LEVELS

    asi_caps = INTELLIGENCE_LEVELS["ASI"]["capacidades"]
    text = " ".join(asi_caps).lower()

    for keyword in [
        "razonamiento",
        "síntesis",
        "metacognición",
        "predictivo",
        "creatividad",
    ]:
        assert keyword in text or keyword.lower().replace("í", "i") in text


def test_domain_security_scan_returns_summary():
    """Verifica que el escaneo básico de seguridad de dominio devuelve un resumen útil."""
    from services.security_ops import analyze_domain_security

    result = analyze_domain_security("example.com")
    assert isinstance(result, dict)
    assert "domain" in result
    assert "resolved_ips" in result
    assert "summary" in result
    assert "risk_score" in result
    assert "security_headers" in result


def test_chat_domain_security_handler_short_circuits():
    """Verifica que el chat detecta peticiones de análisis de seguridad de dominio."""
    from intelligence import brain

    reply = brain.ask_kalmiya("analiza la seguridad de example.com")
    assert isinstance(reply, str)
    assert "example.com" in reply.lower()
    assert "riesgo" in reply.lower() or "estado" in reply.lower()
