"""
obsidian_bridge.py — Puente completo KALMIYA ↔ Obsidian
=========================================================
Permite a KALMIYA:
  - Crear, leer, actualizar y buscar notas en el vault
  - Actualizar el dashboard automáticamente
  - Registrar conversaciones como notas
  - Organizar notas por categoría
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from _logging import get_logger
from os_ops import load_obsidian_vault_path

logger = get_logger(__name__)

# ── Rutas del vault ────────────────────────────────────────────────────────────

def get_vault() -> Path:
    """Devuelve la ruta del vault de Obsidian."""
    path = load_obsidian_vault_path()
    if path:
        return Path(path)
    raise ValueError("OBSIDIAN_VAULT_PATH no está configurado en el .env")


def _ensure_folder(folder: str) -> Path:
    """Crea una carpeta dentro del vault si no existe."""
    p = get_vault() / folder
    p.mkdir(parents=True, exist_ok=True)
    return p


# ══════════════════════════════════════════════════════════════════════════════
#  OPERACIONES DE NOTAS
# ══════════════════════════════════════════════════════════════════════════════

def create_note(title: str, content: str, folder: str = "KALMIYA_Notes",
                tags: list[str] | None = None) -> Path:
    """
    Crea una nueva nota en el vault de Obsidian.

    Args:
        title:   Título de la nota (también nombre del archivo).
        content: Contenido en Markdown.
        folder:  Carpeta dentro del vault (se crea si no existe).
        tags:    Lista de tags para el frontmatter.

    Returns:
        Path al archivo creado.
    """
    folder_path = _ensure_folder(folder)
    safe_title  = re.sub(r'[\\/:*?"<>|]', '_', title)
    file_path   = folder_path / f"{safe_title}.md"

    tags_str = "\n".join(f"  - {t}" for t in (tags or ["kalmiya"]))
    ts       = datetime.now().strftime("%Y-%m-%d %H:%M")

    note_content = f"""---
title: "{title}"
created: "{ts}"
tags:
{tags_str}
source: KALMIYA
---

# {title}

{content}
"""
    file_path.write_text(note_content, encoding="utf-8")
    logger.info(f"[OBSIDIAN] Nota creada: {file_path}")
    return file_path


def read_note(note_name: str, folder: str | None = None) -> str:
    """
    Lee el contenido de una nota del vault.

    Args:
        note_name: Nombre del archivo (con o sin .md) o path relativo al vault.
        folder:    Carpeta donde buscar (opcional — busca en todo el vault si es None).

    Returns:
        Contenido de la nota como string, o mensaje de error.
    """
    vault = get_vault()

    # Buscar en carpeta específica
    if folder:
        candidates = [
            vault / folder / note_name,
            vault / folder / f"{note_name}.md",
        ]
        for c in candidates:
            if c.exists():
                return c.read_text(encoding="utf-8")

    # Buscar recursivamente en todo el vault
    for ext in ("", ".md", ".txt"):
        for p in vault.rglob(f"{note_name}{ext}"):
            return p.read_text(encoding="utf-8")

    return f"Nota '{note_name}' no encontrada en el vault."


def update_note(note_name: str, new_content: str,
                folder: str | None = None, append: bool = False) -> bool:
    """
    Actualiza o añade contenido a una nota existente.

    Args:
        note_name:   Nombre del archivo (con o sin .md).
        new_content: Nuevo contenido o texto a añadir.
        folder:      Carpeta donde buscar.
        append:      Si True, añade al final en lugar de reemplazar.

    Returns:
        True si se actualizó, False si no se encontró.
    """
    vault = get_vault()

    def _do_update(path: Path) -> bool:
        existing = path.read_text(encoding="utf-8")
        if append:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M")
            path.write_text(
                existing + f"\n\n---\n*Actualizado: {ts}*\n\n{new_content}",
                encoding="utf-8"
            )
        else:
            path.write_text(new_content, encoding="utf-8")
        logger.info(f"[OBSIDIAN] Nota actualizada: {path}")
        return True

    if folder:
        for ext in ("", ".md"):
            p = vault / folder / f"{note_name}{ext}"
            if p.exists():
                return _do_update(p)

    for ext in ("", ".md", ".txt"):
        for p in vault.rglob(f"{note_name}{ext}"):
            return _do_update(p)

    return False


def search_notes(query: str, max_results: int = 5,
                 folder: str | None = None) -> list[dict]:
    """
    Busca notas en el vault que contengan el texto dado.

    Returns:
        Lista de dicts con 'file', 'line', 'text', 'score'.
    """
    vault  = get_vault()
    q_lower = query.lower()
    matches: list[dict] = []

    search_root = vault / folder if folder else vault

    for path in search_root.rglob("*.md"):
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            score = 0
            snippets = []
            for i, line in enumerate(lines):
                if q_lower in line.lower():
                    score += 1
                    snippets.append({"line": i + 1, "text": line.strip()[:120]})
            if score > 0:
                matches.append({
                    "file":     str(path.relative_to(vault)),
                    "score":    score,
                    "snippets": snippets[:3],
                })
        except Exception:
            continue

    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[:max_results]


def list_notes(folder: str = "KALMIYA_Notes") -> list[str]:
    """Lista todas las notas en una carpeta del vault."""
    try:
        folder_path = get_vault() / folder
        if not folder_path.exists():
            return []
        return [p.stem for p in sorted(folder_path.glob("*.md"))]
    except Exception:
        return []


def delete_note(note_name: str, folder: str = "KALMIYA_Notes") -> bool:
    """Elimina una nota del vault (mueve a _TEMP como seguridad)."""
    vault = get_vault()
    for ext in ("", ".md"):
        p = vault / folder / f"{note_name}{ext}"
        if p.exists():
            trash = vault / "_TEMP"
            trash.mkdir(exist_ok=True)
            p.rename(trash / p.name)
            logger.info(f"[OBSIDIAN] Nota movida a _TEMP: {p.name}")
            return True
    return False


# ══════════════════════════════════════════════════════════════════════════════
#  REGISTRO DE CONVERSACIONES
# ══════════════════════════════════════════════════════════════════════════════

def save_conversation_to_obsidian(messages: list[dict],
                                   summary: str = "") -> Path:
    """
    Guarda una conversación con KALMIYA como nota en Obsidian.

    Args:
        messages: Lista de dicts con 'role' y 'content'.
        summary:  Resumen opcional generado por IA.

    Returns:
        Path a la nota creada.
    """
    ts      = datetime.now()
    title   = f"Chat {ts.strftime('%Y-%m-%d %H-%M')}"
    folder  = f"KALMIYA_Chats/{ts.strftime('%Y-%m')}"

    lines = []
    if summary:
        lines.append(f"**Resumen:** {summary}\n")
        lines.append("---\n")

    for msg in messages:
        role = "👤 Sara" if msg["role"] == "user" else "🤖 KALMIYA"
        lines.append(f"**{role}:** {msg['content']}\n")

    content = "\n".join(lines)
    return create_note(title, content, folder=folder,
                       tags=["chat", "kalmiya", ts.strftime("%Y-%m")])


# ══════════════════════════════════════════════════════════════════════════════
#  PROCESAMIENTO DE COMANDOS DE CHAT
# ══════════════════════════════════════════════════════════════════════════════

def process_obsidian_command(user_input: str) -> str | None:
    """
    Detecta si el usuario quiere realizar una operación de Obsidian desde el chat.
    Devuelve la respuesta si es un comando de Obsidian, None si no lo es.

    Comandos reconocidos:
      - "crea una nota sobre X"
      - "busca en mis notas X"
      - "lee la nota X"
      - "añade a la nota X: contenido"
      - "lista mis notas"
      - "guarda esta conversación"
    """
    text = user_input.strip()
    tl   = text.lower()

    # ── Crear nota ─────────────────────────────────────────────────────────────
    m = re.search(r'crea(?:r)?\s+(?:una\s+)?nota\s+(?:sobre|de|titulada?)?\s+"?(.+?)"?\s*(?:con|:|$)',
                  tl, re.IGNORECASE)
    if m or "nueva nota" in tl:
        title   = m.group(1).strip() if m else datetime.now().strftime("Nota %Y-%m-%d %H-%M")
        content_match = re.search(r'(?:con|:)\s*(.+)$', text, re.IGNORECASE | re.DOTALL)
        content = content_match.group(1).strip() if content_match else "*(nota creada desde KALMIYA)*"
        path    = create_note(title, content)
        return f"✅ Nota creada en Obsidian: **{title}**\n📁 `{path.relative_to(get_vault())}`"

    # ── Buscar notas ───────────────────────────────────────────────────────────
    m = re.search(r'busca(?:r)?\s+(?:en\s+)?(?:mis\s+)?notas?\s+"?(.+?)"?\s*$',
                  tl, re.IGNORECASE)
    if m:
        query   = m.group(1).strip()
        results = search_notes(query)
        if not results:
            return f"🔍 No encontré notas sobre **{query}** en tu vault."
        lines = [f"🔍 Encontré **{len(results)}** nota(s) sobre **{query}**:\n"]
        for r in results:
            lines.append(f"📄 `{r['file']}` ({r['score']} coincidencia(s))")
            for s in r['snippets'][:2]:
                lines.append(f"   › {s['text']}")
        return "\n".join(lines)

    # ── Leer nota ──────────────────────────────────────────────────────────────
    m = re.search(r'lee(?:r)?\s+(?:la\s+)?nota\s+"?(.+?)"?\s*$', tl, re.IGNORECASE)
    if m:
        name    = m.group(1).strip()
        content = read_note(name)
        if "no encontrada" in content:
            return f"❌ {content}"
        preview = content[:800] + ("..." if len(content) > 800 else "")
        return f"📄 **{name}**:\n\n{preview}"

    # ── Listar notas ───────────────────────────────────────────────────────────
    if re.search(r'lista(?:r)?\s+(?:mis\s+)?notas?', tl):
        notes = list_notes()
        if not notes:
            return "📂 No tienes notas en KALMIYA_Notes todavía."
        return f"📂 **Tus notas** ({len(notes)}):\n" + "\n".join(f"  • {n}" for n in notes)

    # ── Guardar conversación ───────────────────────────────────────────────────
    if re.search(r'guarda(?:r)?\s+(?:esta\s+)?conversaci[oó]n', tl):
        try:
            from brain import _conversation_history
            if not _conversation_history:
                return "💬 No hay conversación activa para guardar."
            path = save_conversation_to_obsidian(_conversation_history)
            return f"✅ Conversación guardada en Obsidian:\n📁 `{path.relative_to(get_vault())}`"
        except Exception as e:
            return f"❌ Error guardando conversación: {e}"

    return None  # No es un comando de Obsidian
