from pathlib import Path

from modules.raptor_security_agent import RaptorSecurityAgent


def test_raptor_analyze_codebase_falls_back_on_unsupported_platform(tmp_path, monkeypatch):
    """Regression test: Windows/Unix-incompatible host should return a safe fallback result."""
    monkeypatch.setattr(RaptorSecurityAgent, "_is_platform_supported", staticmethod(lambda: False))

    agent = RaptorSecurityAgent(kalmiya_root=str(Path(__file__).resolve().parents[1]))
    result = agent.analyze_codebase(str(tmp_path), "static")

    assert result.target == str(tmp_path)
    assert isinstance(result.vulnerabilities, list)
    assert result.risk_level in {"low", "unknown"}
    assert "RAPTOR runtime no compatible" in result.summary or "RAPTOR runtime no compatible con este host" in result.summary
