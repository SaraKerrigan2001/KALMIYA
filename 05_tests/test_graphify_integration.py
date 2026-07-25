import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "01_systems" / "KALMIYA_System"))

from kalmiya_nuevas_funciones import obtener_informacion_graphify


class FakeResponse:
    def __init__(self, text: str, status_code: int = 200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(self.status_code)


def test_obtener_informacion_graphify(monkeypatch):
    def fake_get(url: str, timeout: int = 10, headers=None):
        if "api.github.com/repos/Graphify-Labs/graphify" in url:
            return FakeResponse('{"full_name": "Graphify-Labs/graphify", "description": "Graph database tools", "html_url": "https://github.com/Graphify-Labs/graphify"}')
        if "graphify.com" in url:
            return FakeResponse("<html><title>Graphify</title><meta name='description' content='Graphify helps teams reason over connected data.'></html>")
        raise AssertionError(f"URL inesperada: {url}")

    monkeypatch.setattr(requests, "get", fake_get)

    resultado = obtener_informacion_graphify()

    assert resultado["titulo"] == "Graphify"
    assert resultado["repositorio"] == "Graphify-Labs/graphify"
    assert "connected data" in resultado["descripcion"].lower()
    assert resultado["url"] == "https://graphify.com"


def test_ejecutar_graphify_proyecto(monkeypatch, tmp_path):
    import kalmiya_nuevas_funciones as funciones

    class FakeCompletedProcess:
        def __init__(self, returncode, stdout, stderr):
            self.returncode = returncode
            self.stdout = stdout
            self.stderr = stderr

    captured = {}

    def fake_run(cmd, capture_output=True, text=True, cwd=None, check=False):
        captured["cmd"] = cmd
        captured["cwd"] = cwd
        return FakeCompletedProcess(0, "grafo creado", "")

    monkeypatch.setattr(funciones.shutil, "which", lambda name: "graphify")
    monkeypatch.setattr(funciones.subprocess, "run", fake_run)

    resultado = funciones.ejecutar_graphify_proyecto(str(tmp_path), modo="sin_viz")

    assert resultado["exito"] is True
    assert str(tmp_path) in captured["cmd"]
    assert "--no-viz" in captured["cmd"]
