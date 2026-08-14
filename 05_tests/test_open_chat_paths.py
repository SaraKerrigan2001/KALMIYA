from pathlib import Path
import importlib


def test_open_kalmiya_chat_prefers_ui_entrypoint(monkeypatch):
    import core.open_chat as open_chat_module

    calls = {}

    class DummyProcess:
        pass

    def fake_popen(args, cwd=None, creationflags=None):
        calls['args'] = args
        calls['cwd'] = cwd
        calls['creationflags'] = creationflags
        return DummyProcess()

    monkeypatch.setattr(open_chat_module.sys, 'platform', 'win32')
    monkeypatch.setattr(open_chat_module.subprocess, 'Popen', fake_popen)
    monkeypatch.setattr(open_chat_module.subprocess, 'CREATE_NEW_CONSOLE', 0, raising=False)

    result = open_chat_module.open_kalmiya_chat()

    assert result is True
    assert len(calls['args']) == 2
    assert Path(calls['args'][1]).name == 'kalmiya_chat.py'
    assert 'ui' in str(Path(calls['args'][1]).resolve().parent)


def test_system_prompt_avoids_sensitive_profile_defaults():
    import intelligence.brain as brain

    prompt = brain._build_system_prompt()

    assert 'Cúcuta' not in prompt
    assert 'SENA' not in prompt
    assert 'Nació' not in prompt


def test_check_ai_status_does_not_start_blocking_update_loop(monkeypatch):
    import types

    import kalmiya_chat as chat_module

    class DummyRoot:
        def after(self, *args, **kwargs):
            return None

    root = DummyRoot()
    chat = object.__new__(chat_module.KalmiyaChat)
    chat.root = root
    chat.engine_label = types.SimpleNamespace(configure=lambda *args, **kwargs: None)
    chat.time_label = types.SimpleNamespace(configure=lambda *args, **kwargs: None)
    chat.status_dot = types.SimpleNamespace(delete=lambda *args, **kwargs: None, create_oval=lambda *args, **kwargs: None)
    chat._running = True
    chat._pulse_state = True
    chat._draw_status_dot = lambda *_args, **_kwargs: None

    def fail_update_loop():
        raise AssertionError('blocking update loop should not be started here')

    chat._update_loop = fail_update_loop
    monkeypatch.setattr(chat_module, 'is_gemini_configured', lambda: True)
    monkeypatch.setattr(chat_module, 'is_ollama_running', lambda: False)

    chat._check_ai_status()
