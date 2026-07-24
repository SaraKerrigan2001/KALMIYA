# run_all.py
"""Unified command-line interface for the KALMIYA project.
Provides sub-commands to interact with the Obsidian bridge (list, read, write, create)
and to run the pylint analysis script.
"""

import argparse
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Path configuration
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent.parent  # raíz del proyecto (env/)
llm_wiki_scripts = ROOT / "01_systems" / "LLM_Wiki" / "scripts"
if llm_wiki_scripts.is_dir():
    sys.path.append(str(llm_wiki_scripts))
kalmiya_system = ROOT / "01_systems" / "KALMIYA_System"
if kalmiya_system.is_dir():
    sys.path.append(str(kalmiya_system))

# ---------------------------------------------------------------------------
# Import project modules with clear error messages
# ---------------------------------------------------------------------------
try:
    from antigravity_bridge import (
        list_notes,
        read_note,
        write_note,
        create_note,
    )
except ImportError as e:
    sys.exit(f"Failed to import Antigravity bridge module: {e}")

try:
    from analyze_lint import analyze_pylint
except ImportError as e:
    sys.exit(f"Failed to import lint analysis module: {e}")

# ---------------------------------------------------------------------------
# Helper functions for each sub-command
# ---------------------------------------------------------------------------

def _handle_list(_: argparse.Namespace) -> None:
    for note in list_notes():
        print(note)


def _handle_read(args: argparse.Namespace) -> None:
    print(read_note(args.note))


def _handle_write(args: argparse.Namespace) -> None:
    path = write_note(args.note, args.content, overwrite=args.overwrite)
    print(f"Wrote to {path}")


def _handle_create(args: argparse.Namespace) -> None:
    path = create_note(args.note, args.title, tags=args.tags, body=args.body)
    print(f"Created note at {path}")


def _handle_lint(_: argparse.Namespace) -> None:
    result = analyze_pylint()
    if result is not None:
        print(result)

# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="KALMIYA unified CLI")
    subparsers = parser.add_subparsers(dest="command")
    if hasattr(subparsers, "required"):
        subparsers.required = True

    subparsers.add_parser("list", help="List all markdown notes in the vault")

    parser_read = subparsers.add_parser("read", help="Read a markdown note")
    parser_read.add_argument("note", help="Path to note relative to vault root")

    parser_write = subparsers.add_parser("write", help="Write or append content to a note")
    parser_write.add_argument("note")
    parser_write.add_argument("content")
    parser_write.add_argument("--overwrite", action="store_true")

    parser_create = subparsers.add_parser("create", help="Create a new note")
    parser_create.add_argument("note")
    parser_create.add_argument("title")
    parser_create.add_argument("--tags", nargs="*", default=[])
    parser_create.add_argument("--body", default="")

    subparsers.add_parser("lint", help="Run pylint analysis on the project")

    parser.set_defaults(func=lambda _: parser.print_help())
    return parser

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    command_handlers = {
        "list":   _handle_list,
        "read":   _handle_read,
        "write":  _handle_write,
        "create": _handle_create,
        "lint":   _handle_lint,
    }
    handler = command_handlers.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
