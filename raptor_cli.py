#!/usr/bin/env python3
"""
RAPTOR Security Agent - Interfaz completa para KALMIYA
Proporciona análisis autónomo de seguridad ofensiva/defensiva

Uso:
    python raptor_cli.py              # Menú interactivo
    python raptor_cli.py analyze      # Analizar código
    python raptor_cli.py threat       # Analizar amenaza
    python raptor_cli.py report       # Generar reporte
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
import argparse

# Configurar rutas
sys.path.insert(0, str(Path(__file__).parent / "01_systems" / "KALMIYA_System"))

from modules.raptor_security_agent import (
    RaptorSecurityAgent,
    initialize_raptor_agent,
    RaptorAnalysisResult
)
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)


class RaptorCLI:
    """Interfaz CLI para RAPTOR Security Agent en KALMIYA"""
    
    def __init__(self):
        self.agent = initialize_raptor_agent()
        self.reports_dir = Path(__file__).parent / "08_reports" / "security_reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        
    def run_interactive(self):
        """Menú interactivo"""
        if not self.agent:
            print("✗ RAPTOR no está disponible")
            return 1
        
        while True:
            print("\n" + "="*60)
            print("🔴 RAPTOR Security Agent - KALMIYA")
            print("="*60)
            print("\n1. 🔍 Analizar Codebase")
            print("2. ⚠️  Analizar Amenaza de Seguridad")
            print("3. 📊 Generar Reporte de Seguridad")
            print("4. 🛡️  Auditoria Rápida de KALMIYA")
            print("5. 📁 Ver Reportes Anteriores")
            print("6. 🚀 Análisis Completo")
            print("0. ❌ Salir")
            
            choice = input("\n→ Selecciona opción: ").strip()
            
            if choice == "0":
                print("\n👋 Cerrando RAPTOR...\n")
                break
            elif choice == "1":
                self.analyze_codebase_interactive()
            elif choice == "2":
                self.analyze_threat_interactive()
            elif choice == "3":
                self.generate_report_interactive()
            elif choice == "4":
                self.quick_audit()
            elif choice == "5":
                self.view_reports()
            elif choice == "6":
                self.full_analysis()
            else:
                print("⚠️  Opción no válida")
    
    def analyze_codebase_interactive(self):
        """Analizar codebase interactivamente"""
        print("\n📂 Rutas disponibles:")
        paths = [
            "01_systems/KALMIYA_System",
            "01_systems/KALMIYA_System/modules",
            "01_systems/KALMIYA_System/services",
            "01_systems/KALMIYA_System/core",
        ]
        
        for i, path in enumerate(paths, 1):
            print(f"  {i}. {path}")
        print("  0. Ruta personalizada")
        
        idx = input("\n→ Selecciona (0-5): ").strip()
        
        if idx == "0":
            target = input("→ Ingresa ruta a analizar: ").strip()
        elif 1 <= int(idx) <= len(paths):
            target = paths[int(idx)-1]
        else:
            print("⚠️  Opción no válida")
            return
        
        print("\n🔧 Tipo de análisis:")
        print("  1. Static (análisis estático)")
        print("  2. Binary (análisis binario)")
        print("  3. Comprehensive (completo)")
        
        analysis_type = input("\n→ Selecciona (1-3): ").strip()
        type_map = {"1": "static", "2": "binary", "3": "comprehensive"}
        
        if analysis_type not in type_map:
            analysis_type = "comprehensive"
        else:
            analysis_type = type_map[analysis_type]
        
        print(f"\n🔍 Analizando {target} ({analysis_type})...")
        result = self.agent.analyze_codebase(target, analysis_type)
        
        print(f"\n✓ Análisis completado")
        print(f"  • Vulnerabilidades: {len(result.vulnerabilities)}")
        print(f"  • Exploits: {len(result.exploits)}")
        print(f"  • Patches: {len(result.patches)}")
        print(f"  • Riesgo: {result.risk_level}")
        
        # Guardar resultado
        self._save_result(result)
    
    def analyze_threat_interactive(self):
        """Analizar amenaza interactivamente"""
        print("\nDescribe la amenaza de seguridad que quieres analizar:")
        threat = input("→ ").strip()
        
        if not threat:
            print("⚠️  Amenaza vacía")
            return
        
        print(f"\n⚠️  Analizando: {threat}...")
        analysis = self.agent.analyze_threat(threat)
        
        print("\n" + "="*60)
        print("📋 ANÁLISIS DE AMENAZA")
        print("="*60)
        
        print(f"\n🎯 Amenaza:\n  {analysis['threat']}")
        
        print("\n🔴 Estrategias Ofensivas:")
        for strategy in analysis["offensive_strategies"]:
            print(f"  • {strategy}")
        
        print("\n🟢 Estrategias Defensivas:")
        for defense in analysis["defensive_strategies"]:
            print(f"  • {defense}")
        
        print("\n💡 Recomendaciones:")
        for rec in analysis["recommendations"]:
            print(f"  → {rec}")
        
        # Guardar análisis
        self._save_threat_analysis(threat, analysis)
    
    def generate_report_interactive(self):
        """Generar reporte interactivo"""
        targets = [
            "01_systems/KALMIYA_System",
            "01_systems/KALMIYA_System/modules",
            "01_systems/KALMIYA_System/services",
        ]
        
        print("\n📊 Generando análisis para:")
        analyses = []
        
        for target in targets:
            print(f"  • {target}...", end=" ", flush=True)
            result = self.agent.analyze_codebase(target)
            analyses.append(result)
            print("✓")
        
        print("\n📝 Generando reporte...")
        report = self.agent.generate_security_report(analyses)
        
        print(report)
        
        # Guardar reporte
        self._save_report(report)
    
    def quick_audit(self):
        """Auditoría rápida de KALMIYA"""
        print("\n🛡️  Ejecutando auditoría rápida de KALMIYA...")
        
        print("  • Verificando seguridad del código...", end=" ", flush=True)
        result = self.agent.analyze_codebase("01_systems/KALMIYA_System", "static")
        print("✓")
        
        print("  • Analizando amenazas comunes...", end=" ", flush=True)
        threats = [
            "Inyección SQL en módulo de base de datos",
            "Acceso no autorizado a credenciales",
            "Ejecución remota de código",
        ]
        threat_analyses = [self.agent.analyze_threat(t) for t in threats]
        print("✓")
        
        print("\n📋 REPORTE DE AUDITORÍA RÁPIDA")
        print("="*60)
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Vulnerabilidades encontradas: {len(result.vulnerabilities)}")
        print(f"Nivel de riesgo: {result.risk_level}")
        print("\nAmenazas analizadas:")
        for threat in threats:
            print(f"  ✓ {threat}")
        
        self._save_audit_report(result, threat_analyses)
    
    def view_reports(self):
        """Ver reportes anteriores"""
        reports = list(self.reports_dir.glob("*.md")) + list(self.reports_dir.glob("*.json"))
        
        if not reports:
            print("\n📁 No hay reportes guardados")
            return
        
        print("\n📁 Reportes disponibles:")
        for i, report in enumerate(sorted(reports), 1):
            size = report.stat().st_size / 1024  # KB
            print(f"  {i}. {report.name} ({size:.1f} KB)")
        
        choice = input("\n→ Selecciona reporte (0 para volver): ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(reports):
                report_path = sorted(reports)[idx]
                print(f"\n📄 Contenido de {report_path.name}:\n")
                print(report_path.read_text())
        except (ValueError, IndexError):
            pass
    
    def full_analysis(self):
        """Análisis completo exhaustivo"""
        print("\n🚀 Iniciando análisis completo de KALMIYA...")
        print("Esto puede tomar unos minutos...\n")
        
        all_analyses = []
        targets = [
            "01_systems/KALMIYA_System",
            "01_systems/KALMIYA_System/modules",
            "01_systems/KALMIYA_System/services",
            "01_systems/KALMIYA_System/core",
        ]
        
        for target in targets:
            print(f"  • Analizando {target}...", end=" ", flush=True)
            result = self.agent.analyze_codebase(target, "comprehensive")
            all_analyses.append(result)
            print(f"✓ ({len(result.vulnerabilities)} issues)")
        
        print("\n📊 Generando reporte completo...")
        report = self.agent.generate_security_report(all_analyses)
        
        print(report)
        
        # Estadísticas
        total_vulns = sum(len(a.vulnerabilities) for a in all_analyses)
        total_critical = sum(1 for a in all_analyses if a.risk_level == "critical")
        
        print("\n" + "="*60)
        print("📊 RESUMEN")
        print("="*60)
        print(f"Total de vulnerabilidades: {total_vulns}")
        print(f"Críticas: {total_critical}")
        print(f"Reportes analizados: {len(all_analyses)}")
        print("="*60)
        
        self._save_report(report, "full_analysis")
    
    def _save_result(self, result: RaptorAnalysisResult, name: str = None):
        """Guardar resultado en JSON"""
        if not name:
            name = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = self.reports_dir / f"{name}.json"
        data = {
            "target": result.target,
            "timestamp": result.timestamp.isoformat(),
            "vulnerabilities": result.vulnerabilities,
            "exploits": result.exploits,
            "patches": result.patches,
            "risk_level": result.risk_level,
            "summary": result.summary,
        }
        
        filepath.write_text(json.dumps(data, indent=2))
        print(f"✓ Guardado en: {filepath.relative_to(Path.cwd())}")
    
    def _save_threat_analysis(self, threat: str, analysis: dict):
        """Guardar análisis de amenaza"""
        filepath = self.reports_dir / f"threat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath.write_text(json.dumps(analysis, indent=2))
        print(f"✓ Guardado en: {filepath.relative_to(Path.cwd())}")
    
    def _save_report(self, report: str, name: str = None):
        """Guardar reporte en Markdown"""
        if not name:
            name = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        filepath = self.reports_dir / f"{name}.md"
        filepath.write_text(report)
        print(f"\n✓ Reporte guardado en: {filepath.relative_to(Path.cwd())}")
    
    def _save_audit_report(self, result: RaptorAnalysisResult, threat_analyses: list):
        """Guardar reporte de auditoría"""
        filepath = self.reports_dir / f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        data = {
            "timestamp": datetime.now().isoformat(),
            "code_analysis": {
                "vulnerabilities": len(result.vulnerabilities),
                "risk_level": result.risk_level,
            },
            "threats_analyzed": len(threat_analyses),
        }
        filepath.write_text(json.dumps(data, indent=2))
        print(f"\n✓ Auditoría guardada en: {filepath.relative_to(Path.cwd())}")


def main():
    """Punto de entrada principal"""
    parser = argparse.ArgumentParser(
        description="RAPTOR Security Agent - CLI para KALMIYA"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="interactive",
        choices=["interactive", "analyze", "threat", "report", "audit", "full"],
        help="Comando a ejecutar"
    )
    parser.add_argument(
        "--platform",
        choices=["auto", "windows", "macos", "linux"],
        default="auto",
        help="Perfil adaptativo para la instalación del host: auto/windows/macos/linux"
    )
    parser.add_argument(
        "--target",
        help="Ruta a analizar (para comando analyze)"
    )
    parser.add_argument(
        "--threat",
        help="Descripción de amenaza (para comando threat)"
    )
    
    args = parser.parse_args()
    cli = RaptorCLI()

    # Adaptación declarativa por perfil solicitado. Esto convierte un mismo CLI
    # en una capa de fachada que puede desacoplarse del servidor actual y ajustar
    # el resultado a la plataforma donde se instala.
    if args.platform != "auto":
        cli.agent.select_runtime_mode(args.platform)

    profile = cli.agent.get_runtime_profile() if cli.agent else {}
    if profile:
        logger.info(
            "RAPTOR runtime profile exposed: host=%s mode=%s supported=%s",
            profile.get("host_platform"),
            profile.get("runtime_mode"),
            profile.get("supported"),
        )
    
    if args.command == "interactive":
        return cli.run_interactive()
    elif args.command == "analyze":
        target = args.target or "01_systems/KALMIYA_System"
        result = cli.agent.analyze_codebase(target)
        print(f"Vulnerabilidades encontradas: {len(result.vulnerabilities)}")
        print(f"Riesgo: {result.risk_level}")
        cli._save_result(result)
    elif args.command == "threat":
        if args.threat:
            print(f"⚠️  Analizando: {args.threat}")
            analysis = cli.agent.analyze_threat(args.threat)
            print(json.dumps(analysis, indent=2))
    elif args.command == "report":
        cli.generate_report_interactive()
    elif args.command == "audit":
        cli.quick_audit()
    elif args.command == "full":
        cli.full_analysis()
    
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación cancelada")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error fatal: {e}", exc_info=True)
        sys.exit(1)
