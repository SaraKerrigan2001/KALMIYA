"""
backup_engine.py — Motor de respaldo de KALMIYA
================================================
Copia segura de kalmiya.db con rotación automática.
"""

import json
import sqlite3
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).parent
VAULT_DIR = BASE_DIR.parent.parent
DB_PATH = BASE_DIR / "kalmiya.db"
BACKUP_DIR = VAULT_DIR / "_BACKUPS"
LOG_FILE = BASE_DIR / "data" / "backup_log.json"

DEFAULT_RETENTION_DAYS = 7
BACKUP_PREFIX = "kalmiya_backup_"


def _load_retention_days() -> int:
    try:
        from decouple import config
        return int(config("KALMIYA_BACKUP_RETENTION_DAYS", default=str(DEFAULT_RETENTION_DAYS)))
    except Exception:
        return DEFAULT_RETENTION_DAYS


def _ensure_dirs() -> None:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def _append_log(entry: dict) -> None:
    _ensure_dirs()
    history: list = []
    if LOG_FILE.exists():
        try:
            history = json.loads(LOG_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            history = []
    history.append(entry)
    history = history[-50:]
    LOG_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")


def list_backups() -> list[dict]:
    """Lista backups disponibles, más reciente primero."""
    if not BACKUP_DIR.exists():
        return []
    backups = []
    for path in BACKUP_DIR.glob(f"{BACKUP_PREFIX}*.db"):
        stat = path.stat()
        backups.append({
            "file": path.name,
            "path": str(path),
            "size_kb": round(stat.st_size / 1024, 1),
            "created": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        })
    return sorted(backups, key=lambda x: x["created"], reverse=True)


def get_last_backup_time() -> datetime | None:
    backups = list_backups()
    if not backups:
        return None
    return datetime.fromisoformat(backups[0]["created"])


def should_run_backup(hours: int = 24) -> bool:
    """True si no hay backup reciente en las últimas N horas."""
    last = get_last_backup_time()
    if last is None:
        return True
    return datetime.now() - last > timedelta(hours=hours)


def _safe_sqlite_copy(src: Path, dst: Path) -> None:
    """Copia SQLite con API de backup (seguro con BD en uso)."""
    src_conn = sqlite3.connect(f"file:{src}?mode=ro", uri=True)
    dst_conn = sqlite3.connect(str(dst))
    try:
        src_conn.backup(dst_conn)
    finally:
        dst_conn.close()
        src_conn.close()


def cleanup_old_backups(retention_days: int | None = None) -> dict:
    """Elimina backups más antiguos que retention_days."""
    days = retention_days if retention_days is not None else _load_retention_days()
    cutoff = datetime.now() - timedelta(days=days)
    deleted = []

    for path in BACKUP_DIR.glob(f"{BACKUP_PREFIX}*.db"):
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        if mtime < cutoff:
            path.unlink(missing_ok=True)
            deleted.append(path.name)

    return {"retention_days": days, "deleted": deleted, "count": len(deleted)}


def run_backup(reason: str = "manual") -> dict[str, Any]:
    """
    Ejecuta backup de kalmiya.db.

    Returns:
        dict con status, file, size_kb, deleted_old, etc.
    """
    _ensure_dirs()

    if not DB_PATH.exists():
        result = {"status": "error", "message": f"Base de datos no encontrada: {DB_PATH}"}
        _append_log({**result, "reason": reason, "timestamp": datetime.now().isoformat()})
        _notify_failure(result["message"])
        return result

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"{BACKUP_PREFIX}{timestamp}.db"

    try:
        try:
            _safe_sqlite_copy(DB_PATH, backup_path)
        except sqlite3.Error:
            shutil.copy2(DB_PATH, backup_path)

        size_kb = round(backup_path.stat().st_size / 1024, 1)
        cleanup = cleanup_old_backups()

        result = {
            "status": "ok",
            "file": backup_path.name,
            "path": str(backup_path),
            "size_kb": size_kb,
            "reason": reason,
            "deleted_old": cleanup["deleted"],
            "retention_days": cleanup["retention_days"],
            "timestamp": datetime.now().isoformat(),
        }
        _append_log(result)
        return result

    except Exception as e:
        result = {
            "status": "error",
            "message": str(e),
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
        }
        _append_log(result)
        _notify_failure(str(e))
        return result


def restore_backup(backup_file: str) -> dict[str, Any]:
    """Restaura kalmiya.db desde un backup (crea copia de seguridad previa)."""
    src = BACKUP_DIR / backup_file if not Path(backup_file).is_absolute() else Path(backup_file)
    if not src.exists():
        return {"status": "error", "message": f"Backup no encontrado: {backup_file}"}

    pre_restore = run_backup(reason="pre_restore")
    try:
        shutil.copy2(src, DB_PATH)
        return {
            "status": "ok",
            "restored_from": src.name,
            "pre_restore": pre_restore.get("file"),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_backup_status() -> dict[str, Any]:
    """Estado del sistema de backups."""
    backups = list_backups()
    last = get_last_backup_time()
    return {
        "db_path": str(DB_PATH),
        "db_size_kb": round(DB_PATH.stat().st_size / 1024, 1) if DB_PATH.exists() else 0,
        "backup_dir": str(BACKUP_DIR),
        "total_backups": len(backups),
        "last_backup": last.isoformat() if last else None,
        "needs_backup": should_run_backup(),
        "retention_days": _load_retention_days(),
        "recent": backups[:5],
    }


def _notify_failure(message: str) -> None:
    """Intenta avisar por Telegram si está configurado."""
    try:
        from decouple import config
        token = config("TELEGRAM_BOT_TOKEN", default="")
        chat_id = config("TELEGRAM_CHAT_ID", default="")
        if not token or token.startswith("TU_") or not chat_id or chat_id.startswith("TU_"):
            return
        import requests
        text = f"⚠️ KALMIYA — Backup falló\n{message}"
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=10,
        )
    except Exception:
        pass
