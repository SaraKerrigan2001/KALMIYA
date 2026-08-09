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
import platform
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
        self.platform_name = platform.system().lower()
        self.runtime_mode = self._detect_runtime_mode()
        self.platform_supported = self._is_platform_supported()
        
        if not self.enabled:
            logger.warning(f"RAPTOR no encontrado en {self.raptor_path}")
        else:
            logger.info(f"RAPTOR inicializado desde {self.raptor_path}")
            logger.info(
                "RAPTOR runtime profile: %s / host=%s / supported=%s",
                self.runtime_mode,
                self.platform_name,
                self.platform_supported,
            )
            if not self.platform_supported:
                logger.warning(
                    "RAPTOR instalado, pero el entorno actual no cumple los requisitos "
                    "de sandbox Unix. `resource` / namespaces Linux no están disponibles."
                )
    
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

    def select_runtime_mode(self, mode: str) -> str:
        """Ajusta el modo operativo del runtime según el perfil solicitado."""
        allowed = {"auto", "windows", "macos", "linux"}
        normalized = (mode or "auto").lower()
        if normalized not in allowed:
            normalized = "auto"

        if normalized == "auto":
            self.runtime_mode = self._detect_runtime_mode()
        elif normalized == "windows":
            self.runtime_mode = "windows-safe"
        elif normalized == "macos":
            self.runtime_mode = "macos-fallback"
        elif normalized == "linux":
            self.runtime_mode = "linux-sandbox"

        # Revalúa compatibilidad con el perfil solicitado.
        if self.runtime_mode == "linux-sandbox":
            self.platform_supported = self._is_platform_supported()
        elif self.runtime_mode in {"windows-safe", "macos-fallback"}:
            self.platform_supported = False
        else:
            self.platform_supported = self._is_platform_supported()

        return self.runtime_mode

    def get_runtime_profile(self) -> Dict[str, Any]:
        """Expone el perfil de runtime con adaptación activa por SO."""
        return {
            "host_platform": self.platform_name,
            "runtime_mode": self.runtime_mode,
            "supported": bool(self.platform_supported),
            "raptor_path": str(self.raptor_path),
            "enabled": bool(self.enabled),
            "policy": "sandbox-enabled" if self.platform_supported else "secure-local-fallback",
            "message": (
                "RAPTOR puede arrancar con sandbox Unix" if self.platform_supported
                else "RAPTOR requiere runtime Unix; KALMIYA usa análisis seguro local"
            ),
        }

    @staticmethod
    def _detect_runtime_mode() -> str:
        os_name = platform.system().lower()
        if os_name == "windows":
            return "windows-safe"
        if os_name == "darwin":
            return "macos-fallback"
        if os_name == "linux":
            return "linux-sandbox"
        return "unknown"

    @staticmethod
    def _is_platform_supported() -> bool:
        """
        RAPTOR necesita una plataforma que pueda importar su runtime de sandbox.
        En Windows y macOS se debe adaptar la ejecución a un perfil compatible
        o a un análisis local. En Linux, solo se habilita el modo real si la
        dependencia `resource` está presente y hay API Unix estándar.
        """
        os_name = platform.system().lower()
        if os_name == "windows":
            return False
        if os_name == "darwin":
            return False
        try:
            import resource  # noqa: F401
            return hasattr(os, "getuid")
        except Exception:
            return False
    
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
        if not self.platform_supported:
            logger.warning(
                "RAPTOR requiere soporte Unix para el sandbox; el intérprete actual "
                "está en Windows y no puede montar el flujo de seguridad real. "
                "Se aplica análisis local de compatibilidad, no ejecución de Sandbox."
            )
            return self._offline_fallback_analysis(target_path, analysis_type)
        
        logger.info(f"Iniciando análisis {analysis_type} de {target_path}")
        
        try:
            # Construye comando RAPTOR
            cmd = self._build_raptor_command(target_path, analysis_type)
            logger.info(f"Ejecutando RAPTOR: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600,
                check=False,
            )
            
            # Si el proceso devolvió error, lo registramos y devolvemos resumen seguro
            if result.returncode != 0:
                logger.warning(
                    f"RAPTOR devolvió código {result.returncode} para {target_path}: "
                    f"{result.stderr.strip() or result.stdout.strip()[:160]}"
                )
                
            # Procesa resultados
            analysis = self._parse_raptor_output(result.stdout, result.stderr)
            analysis.target = target_path
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
        """
        Construye comando RAPTOR válido para Windows/Python.

        RAPTOR se invoca con el intérprete de Python y el launcher principal
        `raptor.py`, no como un binario directo. Ese detalle evita `WinError 193`
        (`%1 no es una aplicación Win32 válida`) que ocurre al ejecutar un
        `.py` como si fuera un PE nativo.
        """
        raptor_launcher = self.raptor_path / "raptor.py"
        if not raptor_launcher.exists():
            raise FileNotFoundError(f"No se encontró el launcher RAPTOR: {raptor_launcher}")

        # Modo por defecto para codebase: `scan` y `--repo`
        analysis_type = (analysis_type or "comprehensive").lower()
        
        if analysis_type == "binary":
            # El modo binary de RAPTOR necesita un binario/lista; aquí usamos
            # el mismo objetivo como binario/ejecutable si el usuario lo indicó.
            cmd = [sys.executable, str(raptor_launcher), "binary", "investigate", target]
        elif analysis_type == "static":
            cmd = [sys.executable, str(raptor_launcher), "scan", "--repo", target]
        elif analysis_type == "comprehensive":
            # El agente completo exige un flujo con LLM y puede comportarse como
            # un workflow pesado. Para no romper la integración, usamos `agentic`
            # con el target que se desea auditar, siguiendo el CLI del framework.
            cmd = [sys.executable, str(raptor_launcher), "agentic", "--repo", target]
        else:
            cmd = [sys.executable, str(raptor_launcher), "scan", "--repo", target]
        
        return cmd
    
    def _parse_raptor_output(self, stdout: str, stderr: str) -> RaptorAnalysisResult:
        """Parsea la salida de RAPTOR."""
        target = "unknown"
        try:
            # RAPTOR's CLI usually emits text and SBOM/report logs, not JSON
            # on the stdout channel. The integration should therefore degrade
            # gracefully to a safe empty payload, not crash on JSON decoding.
            if stdout.strip().startswith("{"):
                data = json.loads(stdout) if stdout else {}
                target = data.get("target", "unknown")
                return RaptorAnalysisResult(
                    target=target,
                    timestamp=datetime.now(),
                    vulnerabilities=data.get("vulnerabilities", []),
                    exploits=data.get("exploits", []),
                    patches=data.get("patches", []),
                    risk_level=data.get("risk_level", "unknown"),
                    summary=data.get("summary", stdout[:300] or stderr[:300])
                )

            # Fall back to a conservative summary for non-JSON text output
            summary = stdout.strip()[:500] or stderr.strip()[:500] or "RAPTOR analysis completed"
            return RaptorAnalysisResult(
                target=target,
                timestamp=datetime.now(),
                vulnerabilities=[],
                exploits=[],
                patches=[],
                risk_level="unknown",
                summary=summary
            )
        except json.JSONDecodeError:
            logger.warning("No se pudo parsear salida JSON de RAPTOR")
            return self._empty_result(target)
    
    def _offline_fallback_analysis(
        self,
        target_path: str,
        analysis_type: str = "comprehensive",
    ) -> RaptorAnalysisResult:
        """
        Análisis local seguro para hosts donde RAPTOR no puede arrancar su
        runtime Unix dependency chain. Esto NO reemplaza a RAPTOR; solo ofrece
        un resultado conservador para mantener KALMIYA estable.
        """
        root = Path(target_path)
        findings = []
        summary_lines = []
        if root.exists():
            scanned = 0
            for py_file in root.rglob("*.py"):
                if scanned >= 50:
                    break
                try:
                    text = py_file.read_text(encoding="utf-8", errors="ignore")
                    scanned += 1
                    suspicious_terms = [
                        "os.system",
                        "subprocess",
                        "shell=True",
                        "eval(",
                        "exec(",
                        "password",
                        "secret",
                        "token",
                        "api_key",
                    ]
                    matched = [term for term in suspicious_terms if term in text]
                    if matched:
                        findings.append({
                            "name": "heuristic-scan-marker",
                            "description": f"Archivo {py_file} contiene patrones de riesgo: {', '.join(matched)}",
                            "file": str(py_file),
                            "severity": "low",
                        })
                        summary_lines.append(
                            f"Heurística en {py_file}: {', '.join(matched)}"
                        )
                except Exception:
                    pass
        else:
            summary_lines.append(f"Ruta de análisis no encontrada: {target_path}")

        return RaptorAnalysisResult(
            target=target_path,
            timestamp=datetime.now(),
            vulnerabilities=findings,
            exploits=[],
            patches=[],
            risk_level="low" if findings else "unknown",
            summary=(
                "RAPTOR runtime no compatible con este host. "
                "Se realizó un análisis local ligero y seguro. "
                + ("; ".join(summary_lines) if summary_lines else "Sin patrones evidentes detectados.")
            ),
        )

    def _empty_result(
        self,
        target: str,
        summary: str = "Análisis no disponible",
        risk_level: str = "unknown",
    ) -> RaptorAnalysisResult:
        """Retorna resultado vacío o de degradación segura."""
        return RaptorAnalysisResult(
            target=target,
            timestamp=datetime.now(),
            vulnerabilities=[],
            exploits=[],
            patches=[],
            risk_level=risk_level,
            summary=summary
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
