"""
habitos.py - Seguimiento de hábitos diarios para KALMIYA
=========================================================
Registra hábitos diarios, calcula rachas, detecta patrones
y motiva a Sara con análisis de IA integrado.
"""

import json
import os
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Optional


# Hábitos predefinidos sugeridos por KALMIYA
HABITOS_SUGERIDOS = [
    {"nombre": "Tomar agua (8 vasos)", "categoria": "salud", "emoji": "💧"},
    {"nombre": "Ejercicio (30 min)", "categoria": "salud", "emoji": "🏃"},
    {"nombre": "Leer (20 min)", "categoria": "aprendizaje", "emoji": "📚"},
    {"nombre": "Meditar (10 min)", "categoria": "bienestar", "emoji": "🧘"},
    {"nombre": "Estudiar inglés", "categoria": "aprendizaje", "emoji": "🌎"},
    {"nombre": "Sin redes sociales (1h)", "categoria": "bienestar", "emoji": "📵"},
    {"nombre": "Dormir antes de las 11pm", "categoria": "salud", "emoji": "😴"},
    {"nombre": "Comer frutas o verduras", "categoria": "salud", "emoji": "🥗"},
    {"nombre": "Programar / estudiar ADSO", "categoria": "trabajo", "emoji": "💻"},
    {"nombre": "Escribir en diario", "categoria": "bienestar", "emoji": "✍️"},
]


class Habitos:
    """
    Sistema de seguimiento de hábitos diarios con rachas,
    estadísticas y motivación inteligente.
    """

    def __init__(self, data_dir: str = None):
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            self.data_dir = Path(__file__).parent.parent / "data" / "habitos"

        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.habitos_path = self.data_dir / "habitos.json"
        self.registros_path = self.data_dir / "registros.json"

        self.habitos: dict[str, dict] = self._cargar(self.habitos_path)
        self.registros: dict[str, list] = self._cargar(self.registros_path)

        # Días de racha para celebración (desde .env o default 7)
        self.racha_premio = int(os.environ.get("HABITOS_RACHA_PREMIO", "7"))

    # ── Persistencia ──────────────────────────────────────────────────────────

    def _cargar(self, path: Path) -> dict:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _guardar(self):
        try:
            with open(self.habitos_path, "w", encoding="utf-8") as f:
                json.dump(self.habitos, f, ensure_ascii=False, indent=2)
            with open(self.registros_path, "w", encoding="utf-8") as f:
                json.dump(self.registros, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[HABITOS] Error guardando: {e}")

    def _hoy(self) -> str:
        return date.today().isoformat()

    def _fecha(self, dias_atras: int = 0) -> str:
        return (date.today() - timedelta(days=dias_atras)).isoformat()

    # ── Gestión de hábitos ────────────────────────────────────────────────────

    def agregar_habito(self, nombre: str, categoria: str = "general",
                       emoji: str = "✅", meta_dias: int = 21) -> dict:
        """
        Registra un nuevo hábito para seguimiento.

        Args:
            nombre: Nombre del hábito.
            categoria: Categoría (salud, aprendizaje, bienestar, trabajo).
            emoji: Emoji representativo.
            meta_dias: Meta de días consecutivos (por defecto 21 = formar hábito).

        Returns:
            El hábito creado.
        """
        habito_id = nombre.lower().replace(" ", "_")[:30]
        habito = {
            "id": habito_id,
            "nombre": nombre,
            "categoria": categoria,
            "emoji": emoji,
            "meta_dias": meta_dias,
            "creado": self._hoy(),
            "activo": True,
        }
        self.habitos[habito_id] = habito
        if habito_id not in self.registros:
            self.registros[habito_id] = []
        self._guardar()
        return habito

    def eliminar_habito(self, habito_id: str) -> bool:
        """Marca un hábito como inactivo."""
        if habito_id in self.habitos:
            self.habitos[habito_id]["activo"] = False
            self._guardar()
            return True
        return False

    # ── Registro diario ───────────────────────────────────────────────────────

    def registrar(self, habito_id: str, completado: bool = True,
                  nota: str = "") -> dict:
        """
        Registra si un hábito fue completado hoy.

        Args:
            habito_id: ID del hábito.
            completado: True si se completó, False si se falló.
            nota: Nota opcional sobre el registro.

        Returns:
            dict con estado, racha actual y si hay celebración.
        """
        if habito_id not in self.habitos:
            return {"error": f"Hábito '{habito_id}' no encontrado."}

        hoy = self._hoy()

        # Verificar si ya fue registrado hoy
        registros_habito = self.registros.get(habito_id, [])
        ya_registrado = any(r["fecha"] == hoy for r in registros_habito)

        if ya_registrado:
            # Actualizar el registro existente
            for r in registros_habito:
                if r["fecha"] == hoy:
                    r["completado"] = completado
                    r["nota"] = nota
                    break
        else:
            registros_habito.append({
                "fecha": hoy,
                "completado": completado,
                "nota": nota,
                "hora": datetime.now().strftime("%H:%M"),
            })

        self.registros[habito_id] = registros_habito
        self._guardar()

        racha = self.calcular_racha(habito_id)
        celebrar = completado and racha > 0 and racha % self.racha_premio == 0

        return {
            "habito": self.habitos[habito_id]["nombre"],
            "completado": completado,
            "racha_actual": racha,
            "celebrar": celebrar,
            "mensaje_racha": (
                f"¡{racha} días seguidos! ¡Eso es dedicación, Sara!" if celebrar
                else f"Racha: {racha} día{'s' if racha != 1 else ''}."
            ),
        }

    def registrar_varios(self, completados: list[str], fallidos: list[str] = None) -> list[dict]:
        """Registra múltiples hábitos de una vez."""
        resultados = []
        for h_id in completados:
            resultados.append(self.registrar(h_id, True))
        for h_id in (fallidos or []):
            resultados.append(self.registrar(h_id, False))
        return resultados

    # ── Estadísticas ──────────────────────────────────────────────────────────

    def calcular_racha(self, habito_id: str) -> int:
        """
        Calcula la racha actual de días consecutivos completados.
        """
        registros = self.registros.get(habito_id, [])
        completados = {
            r["fecha"] for r in registros if r["completado"]
        }

        racha = 0
        dia = date.today()
        while dia.isoformat() in completados:
            racha += 1
            dia -= timedelta(days=1)

        return racha

    def calcular_racha_maxima(self, habito_id: str) -> int:
        """Calcula la racha máxima histórica de un hábito."""
        registros = self.registros.get(habito_id, [])
        if not registros:
            return 0

        fechas_completadas = sorted(
            r["fecha"] for r in registros if r["completado"]
        )
        if not fechas_completadas:
            return 0

        max_racha = 1
        racha_actual = 1
        for i in range(1, len(fechas_completadas)):
            prev = date.fromisoformat(fechas_completadas[i - 1])
            curr = date.fromisoformat(fechas_completadas[i])
            if (curr - prev).days == 1:
                racha_actual += 1
                max_racha = max(max_racha, racha_actual)
            else:
                racha_actual = 1

        return max_racha

    def get_tasa_cumplimiento(self, habito_id: str, dias: int = 30) -> float:
        """Calcula el % de días completados en los últimos N días."""
        registros = self.registros.get(habito_id, [])
        fechas_objetivo = {
            self._fecha(i) for i in range(dias)
        }
        completados = sum(
            1 for r in registros
            if r["fecha"] in fechas_objetivo and r["completado"]
        )
        return round(completados / dias * 100, 1)

    def get_resumen_hoy(self) -> dict:
        """
        Resumen del día de hoy: hábitos pendientes, completados y rachas.
        """
        hoy = self._hoy()
        habitos_activos = [h for h in self.habitos.values() if h["activo"]]
        completados_hoy = []
        pendientes_hoy = []

        for habito in habitos_activos:
            h_id = habito["id"]
            registros_hoy = [
                r for r in self.registros.get(h_id, [])
                if r["fecha"] == hoy
            ]
            fue_completado = any(r["completado"] for r in registros_hoy)

            info = {
                **habito,
                "racha": self.calcular_racha(h_id),
                "completado_hoy": fue_completado,
            }

            if fue_completado:
                completados_hoy.append(info)
            else:
                pendientes_hoy.append(info)

        progreso = (
            round(len(completados_hoy) / len(habitos_activos) * 100)
            if habitos_activos else 0
        )

        return {
            "fecha": hoy,
            "total_habitos": len(habitos_activos),
            "completados": completados_hoy,
            "pendientes": pendientes_hoy,
            "progreso_pct": progreso,
            "mensaje": (
                f"Hoy completaste {len(completados_hoy)}/{len(habitos_activos)} hábitos ({progreso}%)."
            ),
        }

    def get_resumen_semanal(self) -> dict:
        """Resumen de rendimiento de los últimos 7 días."""
        habitos_activos = [h for h in self.habitos.values() if h["activo"]]
        reporte = []

        for habito in habitos_activos:
            h_id = habito["id"]
            racha = self.calcular_racha(h_id)
            tasa = self.get_tasa_cumplimiento(h_id, dias=7)
            reporte.append({
                "emoji": habito["emoji"],
                "nombre": habito["nombre"],
                "racha": racha,
                "tasa_7d": tasa,
                "meta_dias": habito["meta_dias"],
                "progreso_meta": round(racha / habito["meta_dias"] * 100, 1),
            })

        # Ordenar por tasa de cumplimiento descendente
        reporte.sort(key=lambda h: h["tasa_7d"], reverse=True)

        return {
            "semana": f"{self._fecha(6)} al {self._hoy()}",
            "habitos": reporte,
            "mejor_habito": reporte[0]["nombre"] if reporte else None,
            "habito_a_mejorar": reporte[-1]["nombre"] if len(reporte) > 1 else None,
        }

    def get_habitos_sugeridos(self) -> list[dict]:
        """Devuelve la lista de hábitos sugeridos que aún no han sido agregados."""
        nombres_actuales = {
            h["nombre"].lower() for h in self.habitos.values()
        }
        return [
            s for s in HABITOS_SUGERIDOS
            if s["nombre"].lower() not in nombres_actuales
        ]

    def listar_habitos(self) -> list[dict]:
        """Lista todos los hábitos activos con su racha actual."""
        resultado = []
        for habito in self.habitos.values():
            if habito["activo"]:
                resultado.append({
                    **habito,
                    "racha": self.calcular_racha(habito["id"]),
                    "tasa_30d": self.get_tasa_cumplimiento(habito["id"], 30),
                })
        resultado.sort(key=lambda h: h["racha"], reverse=True)
        return resultado
