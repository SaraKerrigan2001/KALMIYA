"""
RAPTOR Security Agent Integration for KALMIYA

Integrates RAPTOR (Recursive Autonomous Penetration Testing and Observation Robot)
into KALMIYA for autonomous offensive/defensive security research and threat analysis.

Authors: KALMIYA Security Team (based on gadievron/raptor)
License: MIT
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class RaptorAnalysisResult:
    """Resultado del análisis de seguridad con RAPTOR"""
    target: str
    timestamp: datetime
    vulnerabilities: List[Dict[str, Any]]
    exploits: List[Dict[str, Any]]
    patches: List[Dict[str, Any]]
    risk_level: str  # critical, high, medium, low
    summary: str


class RaptorSecurityAgent:
    """
    Agente de seguridad autónomo basado en RAPTOR para KALMIYA.
    
    Proporciona capacidades de:
    - Análisis estático de código
    - Análisis binario
    - Validación de vulnerabilidades con IA
    - Generación de exploits
    - Generación de patches
    """
    
    def __init__(self, kalmiya_root: Optional[str] = None):
        """
        Inicializa el agente de seguridad RAPTOR.
        
        Args:
            kalmiya_root: Ruta raíz de KALMIYA (por defecto detecta automáticamente)
        """
        self.kalmiya_root = Path(kalmiya_root or self._detect_kalmiya_root())
        self.raptor_path = self.kalmiya_root / "01_systems" / "RAPTOR"
        self.enabled = self.raptor_path.exists()
        
        if not self.enabled:
            logger.warning(f"RAPTOR no encontrado en {self.raptor_path}")
        else:
            logger.info(f"RAPTOR inicializado desde {self.raptor_path}")
    
    @staticmethod
    def _detect_kalmiya_root() -> str:
        """Detecta automáticamente la raíz de KALMIYA"""
        # Intenta encontrar desde la variable de entorno o busca hacia arriba
        current = Path(__file__).resolve()
        while current != current.parent:
            if (current / "01_systems" / "KALMIYA_System").exists():
                return str(current)
            current = current.parent
        
        # Fallback a directorio actual
        return os.getcwd()
    
    def analyze_codebase(
        self,
        target_path: str,
        analysis_type: str = "comprehensive"
    ) -> RaptorAnalysisResult:
        """
        Analiza una base de código buscando vulnerabilidades.
        
        Args:
            target_path: Ruta a la base de código a analizar
            analysis_type: "static", "binary", o "comprehensive"
        
        Returns:
            RaptorAnalysisResult con los hallazgos
        """
        if not self.enabled:
            logger.error("RAPTOR no está disponible")
            return self._empty_result(target_path)
        
        logger.info(f"Iniciando análisis {analysis_type} de {target_path}")
        
        try:
            # Construye comando RAPTOR
            cmd = self._build_raptor_command(target_path, analysis_type)
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            # Procesa resultados
            analysis = self._parse_raptor_output(result.stdout, result.stderr)
            return analysis
            
        except subprocess.TimeoutExpired:
            logger.error(f"Análisis de {target_path} agotó tiempo")
            return self._empty_result(target_path)
        except Exception as e:
            logger.error(f"Error analizando {target_path}: {e}")
            return self._empty_result(target_path)
    
    def analyze_threat(self, threat_description: str) -> Dict[str, Any]:
        """
        Analiza una amenaza de seguridad describiendo estrategias
        ofensivas y defensivas.
        
        Args:
            threat_description: Descripción de la amenaza
        
        Returns:
            Análisis de amenaza con recomendaciones
        """
        logger.info(f"Analizando amenaza: {threat_description}")
        
        analysis = {
            "threat": threat_description,
            "timestamp": datetime.now().isoformat(),
            "offensive_strategies": [
                "Análisis de vectores de ataque",
                "Evaluación de perimetro",
                "Pruebas de penetración",
            ],
            "defensive_strategies": [
                "Hardening del sistema",
                "Segmentación de red",
                "Monitoreo y detección",
            ],
            "recommendations": [
                "Implementar WAF (Web Application Firewall)",
                "Actualizar sistemas operativos",
                "Establecer políticas de acceso",
            ]
        }
        
        return analysis
    
    def generate_security_report(
        self,
        analysis_results: List[RaptorAnalysisResult]
    ) -> str:
        """
        Genera un reporte de seguridad a partir de análisis.
        
        Args:
            analysis_results: Lista de resultados de análisis
        
        Returns:
            Reporte en formato Markdown
        """
        report = f"# Reporte de Seguridad RAPTOR\n\n"
        report += f"**Generado:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        total_vulns = sum(len(r.vulnerabilities) for r in analysis_results)
        critical_count = sum(
            1 for r in analysis_results if r.risk_level == "critical"
        )
        
        report += f"## Resumen\n"
        report += f"- Total de Vulnerabilidades: {total_vulns}\n"
        report += f"- Críticas: {critical_count}\n\n"
        
        for result in analysis_results:
            report += f"### Análisis: {result.target}\n"
            report += f"Riesgo: **{result.risk_level.upper()}**\n\n"
            
            if result.vulnerabilities:
                report += "#### Vulnerabilidades Encontradas\n"
                for vuln in result.vulnerabilities:
                    report += f"- {vuln.get('name', 'Desconocida')}: "
                    report += f"{vuln.get('description', '')}\n"
                report += "\n"
        
        return report
    
    def _build_raptor_command(self, target: str, analysis_type: str) -> List[str]:
        """Construye comando RAPTOR"""
        cmd = [
            str(self.raptor_path / "raptor.py"),
            "--target", target,
            f"--{analysis_type}",
            "--output-json"
        ]
        return cmd
    
    def _parse_raptor_output(self, stdout: str, stderr: str) -> RaptorAnalysisResult:
        """Parsea la salida de RAPTOR"""
        try:
            data = json.loads(stdout) if stdout else {}
            return RaptorAnalysisResult(
                target=data.get("target", "unknown"),
                timestamp=datetime.now(),
                vulnerabilities=data.get("vulnerabilities", []),
                exploits=data.get("exploits", []),
                patches=data.get("patches", []),
                risk_level=data.get("risk_level", "unknown"),
                summary=data.get("summary", "")
            )
        except json.JSONDecodeError:
            logger.warning("No se pudo parsear salida JSON de RAPTOR")
            return self._empty_result(data.get("target", "unknown"))
    
    def _empty_result(self, target: str) -> RaptorAnalysisResult:
        """Retorna resultado vacío"""
        return RaptorAnalysisResult(
            target=target,
            timestamp=datetime.now(),
            vulnerabilities=[],
            exploits=[],
            patches=[],
            risk_level="unknown",
            summary="Análisis no disponible"
        )


def initialize_raptor_agent() -> Optional[RaptorSecurityAgent]:
    """Inicializa el agente RAPTOR para KALMIYA"""
    try:
        agent = RaptorSecurityAgent()
        if agent.enabled:
            logger.info("✓ RAPTOR Security Agent inicializado correctamente")
            return agent
        else:
            logger.warning("⚠ RAPTOR Security Agent no está disponible")
            return None
    except Exception as e:
        logger.error(f"✗ Error inicializando RAPTOR: {e}")
        return None


# Exporta el agente como módulo
__all__ = [
    "RaptorSecurityAgent",
    "RaptorAnalysisResult",
    "initialize_raptor_agent",
]
