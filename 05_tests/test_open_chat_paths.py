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
    assert Path(calls['args'][1]).name == 'kalmiya_chat_v4.py'
    assert 'ui' in str(Path(calls['args'][1]).resolve().parent)


def test_system_prompt_avoids_sensitive_profile_defaults(monkeypatch):
    import intelligence.brain as brain
    monkeypatch.setattr(brain, 'get_memory', lambda x: None)

    prompt = brain._build_system_prompt()

    assert 'Cúcuta' not in prompt
    assert 'SENA' not in prompt
    assert 'Nació' not in prompt


# The test test_check_ai_status_does_not_start_blocking_update_loop has been removed
# because kalmiya_chat_v4.py no longer implements _check_ai_status nor blocking loops.
