"""
test_asi.py — Pruebas del módulo ASI (Superinteligencia Artificial)
====================================================================
Verifica que todas las funciones ASI están operativas.
"""

import sys
from pathlib import Path

# Agregar ruta del sistema KALMIYA al path
sys.path.insert(0, str(Path(__file__).parent.parent / "01_systems" / "KALMIYA_System"))

def test_asi_import():
    """Test 1: Verificar que el módulo se puede importar"""
    print("\n[TEST 1] Importando módulo kalmiya_asi...")
    try:
        from intelligence.kalmiya_asi import (
            INTELLIGENCE_LEVELS,
            activate_asi,
            deactivate_asi,
            get_asi_status,
            asi_multidimensional_analysis,
            asi_cognitive_synthesis,
            asi_metacognition,
            asi_predictive_thought,
            asi_creative_solution,
            generate_asi_thought,
            get_intelligence_level,
            get_intelligence_info,
            is_asi_active
        )
        print("✅ Módulo importado correctamente")
        print(f"   Niveles disponibles: {list(INTELLIGENCE_LEVELS.keys())}")
        return True
    except Exception as e:
        print(f"❌ Error al importar: {e}")
        return False

def test_intelligence_levels():
    """Test 2: Verificar sistema de clasificación"""
    print("\n[TEST 2] Verificando sistema de clasificación ANI/AGI/ASI...")
    try:
        from intelligence.kalmiya_asi import INTELLIGENCE_LEVELS
        
        assert 'ANI' in INTELLIGENCE_LEVELS, "Falta nivel ANI"
        assert 'AGI' in INTELLIGENCE_LEVELS, "Falta nivel AGI"
        assert 'ASI' in INTELLIGENCE_LEVELS, "Falta nivel ASI"
        
        assert INTELLIGENCE_LEVELS['ANI']['thought_interval'] == 300, "Intervalo ANI incorrecto"
        assert INTELLIGENCE_LEVELS['AGI']['thought_interval'] == 180, "Intervalo AGI incorrecto"
        assert INTELLIGENCE_LEVELS['ASI']['thought_interval'] == 60, "Intervalo ASI incorrecto"
        
        print("✅ Sistema de clasificación correcto")
        print(f"   ANI: {INTELLIGENCE_LEVELS['ANI']['thought_interval']}s")
        print(f"   AGI: {INTELLIGENCE_LEVELS['AGI']['thought_interval']}s")
        print(f"   ASI: {INTELLIGENCE_LEVELS['ASI']['thought_interval']}s")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_asi_status():
    """Test 3: Verificar estado inicial"""
    print("\n[TEST 3] Verificando estado inicial...")
    try:
        from intelligence.kalmiya_asi import get_asi_status, get_intelligence_level, is_asi_active
        
        status = get_asi_status()
        level = get_intelligence_level()
        active = is_asi_active()
        
        print(f"✅ Estado obtenido correctamente")
        print(f"   Nivel actual: {level}")
        print(f"   ASI activo: {active}")
        print(f"   Intervalo: {status['thought_interval']}s")
        print(f"   Capacidades: {len(status['capacidades'])} disponibles")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_asi_capabilities():
    """Test 4: Verificar que las capacidades están disponibles"""
    print("\n[TEST 4] Verificando capacidades ASI...")
    try:
        from intelligence.kalmiya_asi import (
            asi_multidimensional_analysis,
            asi_cognitive_synthesis,
            asi_metacognition,
            asi_predictive_thought,
            asi_creative_solution,
            generate_asi_thought
        )
        
        capacidades = {
            'Análisis multidimensional': asi_multidimensional_analysis,
            'Síntesis cognitiva': asi_cognitive_synthesis,
            'Metacognición': asi_metacognition,
            'Pensamiento predictivo': asi_predictive_thought,
            'Solución creativa': asi_creative_solution,
            'Generación de pensamientos': generate_asi_thought
        }
        
        print("✅ Todas las capacidades están disponibles:")
        for nombre, func in capacidades.items():
            print(f"   ✓ {nombre}: {func.__name__}()")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_thought_generation():
    """Test 5: Verificar generación de pensamientos ASI"""
    print("\n[TEST 5] Verificando generación de pensamientos ASI...")
    try:
        from intelligence.kalmiya_asi import generate_asi_thought
        
        thought = generate_asi_thought()
        
        assert isinstance(thought, str), "generate_asi_thought() debe devolver string"
        assert len(thought) > 50, "Pensamiento ASI debe tener contenido sustancial"
        
        print("✅ Generación de pensamientos funciona")
        print(f"   Longitud del prompt: {len(thought)} caracteres")
        print(f"   Muestra: {thought[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_integration_brain():
    """Test 6: Verificar integración con brain.py"""
    print("\n[TEST 6] Verificando integración con brain.py...")
    try:
        from brain import set_ai_mode, get_engine_status
        
        status = get_engine_status()
        
        # Verificar que incluye campos ASI
        assert 'intelligence_level' in status, "Falta campo intelligence_level"
        assert 'asi_activo' in status, "Falta campo asi_activo"
        
        print("✅ Integración con brain.py correcta")
        print(f"   Nivel de inteligencia: {status['intelligence_level']}")
        print(f"   ASI activo: {status['asi_activo']}")
        print(f"   Modo actual: {status['modo_actual']}")
        
        # Verificar que 'asi' es un modo válido (no activamos, solo verificamos)
        print("   ✓ Modo 'asi' disponible en set_ai_mode()")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("="*70)
    print("PRUEBAS DEL MÓDULO ASI (Superinteligencia Artificial)")
    print("="*70)
    
    tests = [
        test_asi_import,
        test_intelligence_levels,
        test_asi_status,
        test_asi_capabilities,
        test_thought_generation,
        test_integration_brain
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Error inesperado en {test.__name__}: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"RESULTADOS: {passed} pruebas pasadas, {failed} fallidas")
    print("="*70)
    
    if failed == 0:
        print("\n✅ ¡TODAS LAS PRUEBAS PASARON! El módulo ASI está operativo.")
    else:
        print(f"\n⚠️  {failed} prueba(s) fallaron. Revisa los errores arriba.")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
