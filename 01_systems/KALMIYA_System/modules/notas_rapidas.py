"""
notas_rapidas.py - Sistema de notas persistentes para KALMIYA
=============================================================
Permite crear, buscar, etiquetar y gestionar notas rápidas
desde voz o texto. Se guardan en JSON en disco.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional


class NotasRapidas:
    """
    Sistema de notas rápidas con etiquetas, búsqueda y persistencia.
    Las notas se almacenan en un archivo JSON local.
    """

    def __init__(self, data_dir: str = None):
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            # Usar variable de entorno si existe, o carpeta por defecto
            env_dir = os.environ.get("NOTAS_DIR", "")
            if env_dir:
                self.data_dir = Path(env_dir)
            else:
                self.data_dir = Path(__file__).parent.parent / "data" / "notas"

        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.notas_path = self.data_dir / "notas.json"
        self.notas: dict[str, dict] = self._cargar_notas()

    # ── Persistencia ──────────────────────────────────────────────────────────

    def _cargar_notas(self) -> dict:
        if self.notas_path.exists():
            try:
                with open(self.notas_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _guardar_notas(self):
        try:
            with open(self.notas_path, "w", encoding="utf-8") as f:
                json.dump(self.notas, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[NOTAS] Error guardando: {e}")

    def _generar_id(self) -> str:
        """Genera un ID único para la nota."""
        return f"nota_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:20]}"

    # ── CRUD ──────────────────────────────────────────────────────────────────

    def agregar(self, contenido: str, etiquetas: list[str] = None, titulo: str = "") -> dict:
        """
        Crea una nueva nota.

        Args:
            contenido: El texto de la nota.
            etiquetas: Lista de etiquetas opcionales (ej: ['trabajo', 'urgente']).
            titulo: Título corto opcional.

        Returns:
            La nota creada como dict.
        """
        if not contenido.strip():
            return {"error": "La nota no puede estar vacía."}

        nota_id = self._generar_id()
        nota = {
            "id": nota_id,
            "titulo": titulo or contenido[:40].strip(),
            "contenido": contenido.strip(),
            "etiquetas": [e.lower().strip() for e in (etiquetas or [])],
            "creada": datetime.now().isoformat(),
            "modificada": datetime.now().isoformat(),
            "favorita": False,
            "archivada": False,
        }
        self.notas[nota_id] = nota
        self._guardar_notas()
        return nota

    def editar(self, nota_id: str, nuevo_contenido: str = None,
               nuevo_titulo: str = None, nuevas_etiquetas: list[str] = None) -> dict:
        """Edita una nota existente."""
        if nota_id not in self.notas:
            return {"error": f"Nota '{nota_id}' no encontrada."}

        nota = self.notas[nota_id]
        if nuevo_contenido:
            nota["contenido"] = nuevo_contenido.strip()
        if nuevo_titulo:
            nota["titulo"] = nuevo_titulo.strip()
        if nuevas_etiquetas is not None:
            nota["etiquetas"] = [e.lower().strip() for e in nuevas_etiquetas]
        nota["modificada"] = datetime.now().isoformat()
        self._guardar_notas()
        return nota

    def eliminar(self, nota_id: str) -> bool:
        """Elimina una nota permanentemente."""
        if nota_id in self.notas:
            del self.notas[nota_id]
            self._guardar_notas()
            return True
        return False

    def archivar(self, nota_id: str) -> bool:
        """Archiva una nota (la oculta del listado principal)."""
        if nota_id in self.notas:
            self.notas[nota_id]["archivada"] = True
            self.notas[nota_id]["modificada"] = datetime.now().isoformat()
            self._guardar_notas()
            return True
        return False

    def marcar_favorita(self, nota_id: str) -> bool:
        """Marca/desmarca una nota como favorita."""
        if nota_id in self.notas:
            self.notas[nota_id]["favorita"] = not self.notas[nota_id]["favorita"]
            self._guardar_notas()
            return self.notas[nota_id]["favorita"]
        return False

    # ── Búsqueda y filtros ────────────────────────────────────────────────────

    def buscar(self, query: str, incluir_archivadas: bool = False) -> list[dict]:
        """
        Busca notas por texto en título, contenido o etiquetas.

        Returns:
            Lista de notas que coinciden, ordenadas por fecha de modificación.
        """
        query_lower = query.lower()
        resultados = []

        for nota in self.notas.values():
            if nota["archivada"] and not incluir_archivadas:
                continue
            # Buscar en título, contenido y etiquetas
            if (query_lower in nota["titulo"].lower() or
                    query_lower in nota["contenido"].lower() or
                    any(query_lower in e for e in nota["etiquetas"])):
                resultados.append(nota)

        # Ordenar por fecha de modificación (más reciente primero)
        resultados.sort(key=lambda n: n["modificada"], reverse=True)
        return resultados

    def por_etiqueta(self, etiqueta: str) -> list[dict]:
        """Devuelve todas las notas con una etiqueta específica."""
        etiqueta = etiqueta.lower().strip()
        return [
            n for n in self.notas.values()
            if etiqueta in n["etiquetas"] and not n["archivada"]
        ]

    def listar(self, limite: int = 10, solo_favoritas: bool = False) -> list[dict]:
        """
        Devuelve las notas más recientes.

        Args:
            limite: Máximo de notas a devolver.
            solo_favoritas: Si True, solo muestra favoritas.

        Returns:
            Lista de notas ordenadas por fecha de creación.
        """
        notas_activas = [
            n for n in self.notas.values()
            if not n["archivada"]
        ]
        if solo_favoritas:
            notas_activas = [n for n in notas_activas if n["favorita"]]

        notas_activas.sort(key=lambda n: n["creada"], reverse=True)
        return notas_activas[:limite]

    def get_etiquetas_disponibles(self) -> list[str]:
        """Devuelve todas las etiquetas únicas en uso."""
        etiquetas = set()
        for nota in self.notas.values():
            etiquetas.update(nota["etiquetas"])
        return sorted(etiquetas)

    # ── Estadísticas ──────────────────────────────────────────────────────────

    def get_resumen(self) -> dict:
        """Resumen general del sistema de notas."""
        total = len(self.notas)
        activas = sum(1 for n in self.notas.values() if not n["archivada"])
        archivadas = total - activas
        favoritas = sum(1 for n in self.notas.values() if n["favorita"])
        etiquetas = self.get_etiquetas_disponibles()

        return {
            "total": total,
            "activas": activas,
            "archivadas": archivadas,
            "favoritas": favoritas,
            "etiquetas": etiquetas,
            "mensaje": (
                f"Tienes {activas} notas activas"
                + (f" y {favoritas} favoritas." if favoritas else ".")
            ),
        }

    def nota_del_dia(self) -> Optional[dict]:
        """Devuelve una nota aleatoria de las más recientes (como recordatorio)."""
        import random
        recientes = self.listar(limite=20)
        if not recientes:
            return None
        return random.choice(recientes)

    def exportar_txt(self, ruta_destino: str = None) -> str:
        """Exporta todas las notas activas a un archivo .txt."""
        notas_activas = self.listar(limite=9999)
        if not notas_activas:
            return "No hay notas para exportar."

        if not ruta_destino:
            ruta_destino = str(self.data_dir / f"notas_export_{datetime.now().strftime('%Y%m%d')}.txt")

        with open(ruta_destino, "w", encoding="utf-8") as f:
            f.write(f"NOTAS KALMIYA — Exportadas el {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            f.write("=" * 60 + "\n\n")
            for nota in notas_activas:
                f.write(f"[{nota['creada'][:10]}] {nota['titulo']}\n")
                if nota["etiquetas"]:
                    f.write(f"Etiquetas: {', '.join(nota['etiquetas'])}\n")
                f.write(f"{nota['contenido']}\n")
                f.write("-" * 40 + "\n\n")

        return ruta_destino
