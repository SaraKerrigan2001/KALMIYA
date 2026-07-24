#!/usr/bin/env python3
"""Lanzador rápido del modo estudio ADSO."""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

KALMIYA_DIR = Path(__file__).parent.parent / "01_systems" / "KALMIYA_System"
sys.path.insert(0, str(KALMIYA_DIR))

from kalmiya_functions import init_kalmiya_functions, execute_kalmiya_function


def main():
    init_kalmiya_functions()
    brief = execute_kalmiya_function("get_morning_brief")
    status = execute_kalmiya_function("get_study_status")

    print("=" * 50)
    print("  KALMIYA — Modo Estudio ADSO")
    print("=" * 50)

    if brief.get("date"):
        print(f"\n📅 Fecha: {brief['date']}")
        print(f"📋 Entregas pendientes: {brief['pending_count']}")
        if brief.get("due_today"):
            print("\n⏰ Vencen hoy:")
            for a in brief["due_today"]:
                print(f"   • [{a['subject']}] {a['title']}")
        if brief.get("urgent"):
            print("\n🔴 Urgentes:")
            for a in brief["urgent"]:
                print(f"   • [{a['subject']}] {a['title']}")
        print(f"\n💡 Tip: {brief.get('study_tip', '')}")

    if status.get("program"):
        print(f"\n🎓 {status['program']}")
        print(f"👥 Grupo: {status.get('group', '')}")
        print(f"⏱️  Sesiones Pomodoro: {status.get('pomodoro_sessions', 0)}")

    print("\nComandos disponibles:")
    print("  python 03_launchers/estudio_adso.py brief")
    print("  python 03_launchers/estudio_adso.py java")
    print("  python 03_launchers/estudio_adso.py status")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        init_kalmiya_functions()
        cmd = sys.argv[1].lower()
        if cmd == "brief":
            import json
            print(json.dumps(execute_kalmiya_function("get_morning_brief"), indent=2, ensure_ascii=False))
        elif cmd == "java":
            q = execute_kalmiya_function("get_java_question")
            print(f"\n[{q.get('topic')}] {q.get('question')}\n")
            print(f"Respuesta: {q.get('answer')}")
        elif cmd == "status":
            import json
            print(json.dumps(execute_kalmiya_function("get_study_status"), indent=2, ensure_ascii=False))
        else:
            main()
    else:
        main()
