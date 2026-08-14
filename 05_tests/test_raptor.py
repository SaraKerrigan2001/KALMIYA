#!/usr/bin/env python3
"""
Test script para RAPTOR Security Agent

Documentación: [[06_docs/RAPTOR_INTEGRATION|🔒 RAPTOR Integration]]
Índice: [[INDEX|← Índice Principal]]
Ubicación: 05_tests/test_raptor.py
"""

import sys
import os
from pathlib import Path

# Agregar ruta de módulos
sys.path.insert(0, str(Path(__file__).parent / "01_systems" / "KALMIYA_System"))

from modules.raptor_security_agent import RaptorSecurityAgent, initialize_raptor_agent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🔴 RAPTOR Security Agent - Test")
    print("="*50 + "\n")
    
    # Inicializar agente
    agent = initialize_raptor_agent()
    
    if agent:
        print("✓ RAPTOR Agent inicializado correctamente\n")
        
        # Ejemplo 1: Analizar amenaza
        print("📋 Analizando amenaza de seguridad...")
        threat = agent.analyze_threat("Posible inyección SQL en módulo de base de datos")
        
        print(f"\nAmenza: {threat['threat']}")
        print("\nEstrategias Ofensivas:")
        for strategy in threat["offensive_strategies"]:
            print(f"  • {strategy}")
        
        print("\nEstrategias Defensivas:")
        for defense in threat["defensive_strategies"]:
            print(f"  • {defense}")
        
        print("\nRecomendaciones:")
        for rec in threat["recommendations"]:
            print(f"  → {rec}")
        
        # Ejemplo 2: Generar reporte (simulado)
        print("\n" + "-"*50)
        print("\n📊 Generando reporte de seguridad...")
        
        try:
            result = agent.analyze_codebase("01_systems/KALMIYA_System")
            report = agent.generate_security_report([result])
            print(report)
        except Exception as e:
            print(f"⚠ Error en análisis: {e}")
            print("(Esto es normal si RAPTOR aún no está completamente configurado)")
    else:
        print("✗ Error: No se pudo inicializar RAPTOR")
        print("Asegúrate de que:")
        print("  1. El submódulo RAPTOR está clonado: 01_systems/RAPTOR/")
        print("  2. Tu variable de entorno CLAUDE_API_KEY está configurada")
