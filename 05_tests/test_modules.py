#!/usr/bin/env python3
"""
test_modules.py — Script de Prueba de Módulos KALMIYA
======================================================
Verifica que todos los módulos funcionan correctamente.
"""

import sys
import os
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Setup paths — este archivo está en 05_tests/
KALMIYA_DIR = Path(__file__).parent.parent / "01_systems" / "KALMIYA_System"
sys.path.insert(0, str(KALMIYA_DIR))

def test_modules_manager():
    """Prueba el gestor de módulos."""
    print("=" * 60)
    print("🧪 PRUEBA 1: Gestor de Módulos")
    print("=" * 60)

    try:
        from modules_manager import get_manager
        manager = get_manager()

        print(f"✅ Manager inicializado")
        print(f"📦 Total de módulos: {len(manager.list_modules())}")
        print(f"📋 Módulos cargados:")

        for mod in sorted(manager.list_modules()):
            print(f"   • {mod}")

        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_kalmiya_functions():
    """Prueba las funciones KALMIYA."""
    print("\n" + "=" * 60)
    print("🧪 PRUEBA 2: Funciones KALMIYA")
    print("=" * 60)

    try:
        from kalmiya_functions import (
            init_kalmiya_functions,
            list_all_functions,
            get_available_functions
        )

        init_kalmiya_functions()
        print(f"✅ Sistema de funciones inicializado")

        functions = list_all_functions()
        print(f"📚 Total de funciones: {len(functions)}")

        avail = get_available_functions()
        print(f"📂 Categorías: {len(avail)}")
        for category, funcs in avail.items():
            print(f"   • {category}: {len(funcs)} funciones")

        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_execute_function():
    """Prueba ejecutar una función."""
    print("\n" + "=" * 60)
    print("🧪 PRUEBA 3: Ejecutar Funciones")
    print("=" * 60)

    try:
        from kalmiya_functions import execute_kalmiya_function

        print("Probando: add_todo")
        result = execute_kalmiya_function('add_todo', 'test1', 'Tarea de prueba', priority='high')
        print(f"   Resultado: OK")

        print("Probando: add_expense")
        result = execute_kalmiya_function('add_expense', 'test', 10.50, 'prueba')
        print(f"   Resultado: OK")

        print("✅ Funciones ejecutadas correctamente")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_module_individual():
    """Prueba un módulo individual."""
    print("\n" + "=" * 60)
    print("🧪 PRUEBA 4: Módulos Individuales")
    print("=" * 60)

    try:
        from modules.todo_manager import TODOManager
        from modules.expense_tracker import ExpenseTracker
        from modules.health_tracker import HealthTracker

        # Test TODOManager
        todo = TODOManager()
        todo.add_todo('t1', 'Test', priority='high')
        summary = todo.get_daily_summary()
        print(f"✅ TODOManager: {len(summary)} tareas")

        # Test ExpenseTracker
        expense = ExpenseTracker()
        expense.add_expense('test', 50)
        print(f"✅ ExpenseTracker: Gasto registrado")

        # Test HealthTracker
        health = HealthTracker()
        health.log_activity('test', 30)
        health.log_vital_signs(70, '120/80', 37)
        summary = health.get_health_summary()
        print(f"✅ HealthTracker: {summary['activities']} actividades, {summary['vital_readings']} lecturas")

        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_adso_study_mode():
    """Prueba el modo estudio ADSO."""
    print("\n" + "=" * 60)
    print("🧪 PRUEBA 5: Modo Estudio ADSO")
    print("=" * 60)

    try:
        from modules.adso_study_mode import ADSOStudyMode

        study = ADSOStudyMode()
        study.add_assignment("ev1", "Proyecto Java POO", "Java", "2026-07-30", "high")
        pending = study.get_pending_assignments()
        session = study.start_study_session("Java", "Repasar herencia")
        brief = study.get_morning_brief()
        question = study.get_java_question("POO")
        status = study.get_study_status()

        print(f"✅ Entregas pendientes: {len(pending)}")
        print(f"✅ Sesión iniciada: {session['task']}")
        print(f"✅ Brief matutino: {brief['pending_count']} pendientes")
        print(f"✅ Pregunta Java ({question['topic']}): {question['question'][:50]}…")
        print(f"✅ Estado: {status['program']}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ejecuta todas las pruebas."""
    print("\n")
    print("🤖 PRUEBAS DE MÓDULOS KALMIYA")
    print("=" * 60)

    results = {
        'Manager': test_modules_manager(),
        'Funciones': test_kalmiya_functions(),
        'Ejecutar': test_execute_function(),
        'Módulos': test_module_individual(),
        'Estudio ADSO': test_adso_study_mode(),
    }

    print("\n" + "=" * 60)
    print("📊 RESULTADOS")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "✅ PASÓ" if passed else "❌ FALLÓ"
        print(f"{test_name:20} {status}")

    total_passed = sum(1 for v in results.values() if v)
    total_tests = len(results)

    print(f"\nTotal: {total_passed}/{total_tests} pruebas pasadas")

    if total_passed == total_tests:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        return 0
    else:
        print(f"\n⚠️  {total_tests - total_passed} pruebas fallaron")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
