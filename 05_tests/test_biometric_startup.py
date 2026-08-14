import os
import sys
import tempfile
import types

sys.path.insert(0, os.path.abspath('c:/Users/maria/env/01_systems/KALMIYA_System'))

import pytest

import core.main as main_module
import core.kalmiya_launcher as launcher_module


class DummyBiometrics(types.SimpleNamespace):
    def __init__(self, session=None, auth_result=None):
        super().__init__()
        self._session = session
        self._auth_result = auth_result

    def obtener_sesion_activa(self):
        return self._session

    def verificacion_biometrica_completa(self, *args, **kwargs):
        return self._auth_result

    def estado_biometrico(self):
        return {'activo': bool(self._session), 'sesion': self._session and self._session.get('nombre')}


@pytest.fixture(autouse=True)
def patch_speak(monkeypatch):
    def fake_speak(message):
        return message

    monkeypatch.setattr(main_module, 'speak', fake_speak)
    monkeypatch.setattr(launcher_module, '_log', lambda tag, msg, level='info': None)
    return None


def test_ensure_biometric_session_disabled_by_config(monkeypatch):
    monkeypatch.setattr(main_module, 'config', lambda key, default=None: 'false')
    assert main_module._ensure_biometric_session() is True


def test_ensure_biometric_session_with_active_session(monkeypatch):
    dummy = DummyBiometrics(session={'nombre': 'Sara Kerrigan', 'nivel_acceso': 5})
    monkeypatch.setitem(sys.modules, 'kalmiya_biometrics', dummy)
    monkeypatch.setattr(main_module, 'config', lambda key, default=None: 'true')

    assert main_module._ensure_biometric_session() is True


def test_ensure_biometric_session_authentication_fails(monkeypatch):
    dummy = DummyBiometrics(session=None, auth_result=None)
    monkeypatch.setitem(sys.modules, 'kalmiya_biometrics', dummy)
    monkeypatch.setattr(main_module, 'config', lambda key, default=None: 'true')

    assert main_module._ensure_biometric_session() is False


def test_ensure_biometric_session_authentication_succeeds(monkeypatch):
    dummy = DummyBiometrics(session=None, auth_result={'nombre': 'Sara Kerrigan', 'nivel_acceso': 5})
    monkeypatch.setitem(sys.modules, 'kalmiya_biometrics', dummy)
    monkeypatch.setattr(main_module, 'config', lambda key, default=None: 'true')

    assert main_module._ensure_biometric_session() is True


def test_launcher_biometric_authentication_requires_module(monkeypatch):
    monkeypatch.setattr(launcher_module, 'config', lambda key, default='true', cast=str: 'false')
    assert launcher_module._run_biometric_authentication() is True


def test_launcher_biometric_authentication_fails_when_required(monkeypatch):
    dummy = DummyBiometrics(session=None, auth_result=None)
    monkeypatch.setitem(sys.modules, 'kalmiya_biometrics', dummy)
    monkeypatch.setattr(launcher_module, 'config', lambda key, default='true', cast=str: 'true')

    assert launcher_module._run_biometric_authentication() is False
