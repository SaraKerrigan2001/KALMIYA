# config.py – Helper utilities for KALMIYA

"""
Utility module that centralises configuration helpers for the KALMIYA system.

It provides:
- `configure_logging` – initialise the logging subsystem with a selectable format
  (plain text or JSON) and a configurable log level.
- `ensure_pytest_config` – creates a minimal ``pytest.ini`` file if it does not
  exist, enabling sensible defaults for the test suite.
- `run_black_formatter` – a thin wrapper that invokes the ``black`` code formatter
  on the project directory.  It returns the subprocess output for debugging
  purposes.

These helpers are deliberately lightweight and have no external side‑effects
unless they are explicitly called by the application code.
"""

import os
import subprocess
from pathlib import Path
import logging
from typing import Literal

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------

def configure_logging(
    *,
    level: int = logging.INFO,
    fmt: Literal["text", "json"] = "text",
    log_dir: str = "logs",
) -> None:
    """Configure the global logging system.

    The function delegates to :func:`_logging.setup_logging` but adds a simple
    choice of output format.  ``"text"`` (the default) uses a human‑readable
    format, while ``"json"`` emits one JSON object per line – useful for log
    aggregation services.

    Parameters
    ----------
    level:
        Logging level constant from the :pymod:`logging` module.
    fmt:
        Either ``"text"`` for the classic ``'%(asctime)s - %(name)s - ...'``
        format or ``"json"`` for a JSON‑encoded line.
    log_dir:
        Directory where rotating log files will be stored.
    """
    # Import the central logging helper lazily to avoid circular imports.
    from _logging import setup_logging

    # Call the base setup to create handlers.
    setup_logging(level=level, log_dir=log_dir)

    root_logger = logging.getLogger()
    if fmt == "json":
        # Simple JSON formatter – each record becomes a single‑line JSON object.
        class JsonFormatter(logging.Formatter):
            def format(self, record: logging.LogRecord) -> str:  # pragma: no cover
                import json

                payload = {
                    "time": self.formatTime(record, self.datefmt),
                    "name": record.name,
                    "level": record.levelname,
                    "message": record.getMessage(),
                }
                return json.dumps(payload, ensure_ascii=False)

        json_formatter = JsonFormatter()
        for handler in root_logger.handlers:
            handler.setFormatter(json_formatter)
    # No return – configuration is applied globally.

# ---------------------------------------------------------------------------
# Pytest configuration helper
# ---------------------------------------------------------------------------

def ensure_pytest_config(project_root: str | None = None) -> Path:
    """Create a minimal ``pytest.ini`` if it does not already exist.

    The generated file contains a few sensible defaults:

    - ``addopts = -ra -q`` – show extra summary info and keep output quiet.
    - ``testpaths = tests`` – look for tests in the ``tests`` package.
    - ``python_files = test_*.py`` – pattern for test discovery.

    Parameters
    ----------
    project_root:
        Path to the project root.  If ``None`` the current working directory
        is used.

    Returns
    -------
    pathlib.Path
        The absolute path of the ``pytest.ini`` file (created or existing).
    """
    root = Path(project_root or os.getcwd())
    pytest_file = root / "pytest.ini"
    if not pytest_file.exists():
        content = (
            "[pytest]\n"
            "addopts = -ra -q\n"
            "testpaths = tests\n"
            "python_files = test_*.py\n"
        )
        pytest_file.write_text(content, encoding="utf-8")
    return pytest_file.resolve()

# ---------------------------------------------------------------------------
# Black formatter wrapper
# ---------------------------------------------------------------------------

def run_black_formatter(project_root: str | None = None) -> subprocess.CompletedProcess:
    """Run the ``black`` code formatter on the project.

    The function spawns a subprocess and returns the ``CompletedProcess``
    instance, allowing callers to inspect ``stdout``/``stderr`` and the return
    code.  If ``black`` is not installed, the subprocess will raise a
    ``FileNotFoundError`` which can be caught by the caller.

    Parameters
    ----------
    project_root:
        Root directory to format.  Defaults to the current working directory.

    Returns
    -------
    subprocess.CompletedProcess
        Result of the ``black`` execution.
    """
    root = Path(project_root or os.getcwd())
    # ``--quiet`` suppresses the per‑file output; ``--line-length 88`` matches
    # the default black configuration.
    return subprocess.run(
        ["black", "--quiet", str(root)],
        capture_output=True,
        text=True,
        check=False,
    )

# ---------------------------------------------------------------------------
# Convenience entry‑point for developers
# ---------------------------------------------------------------------------

def dev_setup(
    *, level: int = logging.INFO, fmt: Literal["text", "json"] = "text"
) -> None:
    """Convenient one‑liner for developers.

    Calls :func:`configure_logging` and ensures a ``pytest.ini`` file is present.
    """
    configure_logging(level=level, fmt=fmt)
    ensure_pytest_config()
