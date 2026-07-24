# antigravity_bridge.py
"""Bridge between the Antigravity agent and an Obsidian vault.

The vault path is defined in `VAULT_PATH`. The functions below allow the
agent (or any external script) to:
- list markdown files in the vault,
- read a file's content,
- write/append content to a file,
- create a new note with front‑matter.

This file can be imported by the Antigravity runtime or executed from the
command line.
"""
import os
import json
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration – modify if your vault lives elsewhere
# ---------------------------------------------------------------------------
VAULT_PATH = Path(r"C:\\Users\\maria\\env\\LLM_Wiki\\wiki")

if not VAULT_PATH.is_dir():
    raise FileNotFoundError(f"Obsidian vault not found at {VAULT_PATH}")

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def _markdown_files():
    """Return a list of all *.md files inside the vault (recursive)."""
    return [p for p in VAULT_PATH.rglob("*.md")]

def list_notes():
    """List note filenames relative to the vault root."""
    return [str(p.relative_to(VAULT_PATH)) for p in _markdown_files()]

def read_note(note_path: str) -> str:
    """Read a markdown note.

    `note_path` is relative to the vault root, e.g. "index.md" or
    "00-System/CONFIG.md".
    """
    full_path = VAULT_PATH / note_path
    if not full_path.is_file():
        raise FileNotFoundError(f"Note not found: {note_path}")
    return full_path.read_text(encoding="utf-8")

def write_note(note_path: str, content: str, overwrite: bool = False):
    """Write content to a note.

    If ``overwrite`` is False and the file exists, the content will be appended
    with a newline separator.
    """
    full_path = VAULT_PATH / note_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    mode = "w" if overwrite else "a"
    with open(full_path, mode, encoding="utf-8") as f:
        if not overwrite and full_path.exists():
            f.write("\n")  # ensure separation when appending
        f.write(content)
    return str(full_path)

def create_note(note_path: str, title: str, tags: list[str] = None, extra_frontmatter: dict = None, body: str = ""):
    """Create a new markdown note with YAML front‑matter.

    Example::
        create_note("entities/person.md", "Juan Pérez",
                    tags=["person"], extra_frontmatter={"source":"import"},
                    body="Detalles de la persona…")
    """
    front = {
        "title": title,
        "tags": tags or [],
        "created": datetime.utcnow().isoformat() + "Z",
    }
    if extra_frontmatter:
        front.update(extra_frontmatter)
    yaml = "---\n" + "\n".join(f"{k}: {json.dumps(v)}" for k, v in front.items()) + "\n---\n"
    content = yaml + "\n" + body
    return write_note(note_path, content, overwrite=True)

# ---------------------------------------------------------------------------
# Simple CLI for quick testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse, sys
    parser = argparse.ArgumentParser(description="Antigravity ↔ Obsidian bridge")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("list", help="list all notes")
    read = sub.add_parser("read", help="read a note")
    read.add_argument("note")
    write = sub.add_parser("write", help="write/append a note")
    write.add_argument("note")
    write.add_argument("content")
    write.add_argument("--overwrite", action="store_true")
    create = sub.add_parser("create", help="create a new note with front‑matter")
    create.add_argument("note")
    create.add_argument("title")
    create.add_argument("--tags", nargs="*", default=[]) 
    create.add_argument("--body", default="")
    args = parser.parse_args()
    if args.cmd == "list":
        for n in list_notes():
            print(n)
    elif args.cmd == "read":
        print(read_note(args.note))
    elif args.cmd == "write":
        write_note(args.note, args.content, overwrite=args.overwrite)
    elif args.cmd == "create":
        create_note(args.note, args.title, tags=args.tags, body=args.body)
    else:
        parser.print_help()
        sys.exit(1)
