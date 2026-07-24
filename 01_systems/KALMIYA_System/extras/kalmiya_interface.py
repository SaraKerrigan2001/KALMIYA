import time

class KalmiyaInterface:
    def __init__(self):
        self.identity = "KALMIYA"
        self.classification = "Clase S"

    def verificar_actualizaciones(self):
        print(f"[{self.identity}]: Iniciando escaneo de red...")
        time.sleep(1)

        actualizaciones = {
            "Seguridad": "Parche de protección familiar v4.9 (CRÍTICO) disponible.",
            "Nuevas Tecnologías": "Módulos de análisis de datos e IA v6.0 listos para descarga.",
            "Hardware": "Sin cambios detectados en el hardware local. Estado: Óptimo."
        }

        self.mostrar_reporte_actualizaciones(actualizaciones)
        return actualizaciones

    def mostrar_reporte_actualizaciones(self, actualizaciones):
        print("\n--- REPORTE DE ACTUALIZACIONES ---")
        for area, estado in actualizaciones.items():
            print(f"[*] Área: {area} -> {estado}")

        print("\n[SISTEMA]: ¿Desea iniciar la descarga e instalación de los parches críticos? [S/N]")

    def descargar_parches(self, actualizaciones):
        print(f"[{self.identity}]: Iniciando descarga de parches...")
        descargado = []

        for area, estado in actualizaciones.items():
            if "disponible" in estado.lower() or "listos para descarga" in estado.lower():
                print(f"- Descargando parche para {area}...")
                time.sleep(1)
                descargado.append(area)
                print(f"  ✅ {area} descargado.")

        if not descargado:
            print("No se encontraron parches listos para descarga.")
            return False

        print(f"[{self.identity}]: Descarga completada para {len(descargado)} parche(s).")
        return True

    def instalar_parches(self, actualizaciones):
        print(f"[{self.identity}]: Iniciando instalación de parches...")
        instalado = []

        for area, estado in actualizaciones.items():
            if "disponible" in estado.lower() or "listos para descarga" in estado.lower():
                print(f"- Instalando parche para {area}...")
                time.sleep(1)
                instalado.append(area)
                print(f"  ✅ {area} instalado.")

        if not instalado:
            print("No había parches pendientes de instalación.")
            return False

        print(f"[{self.identity}]: Instalación completada para {len(instalado)} parche(s).")
        return True

    def ejecutar_actualizacion(self):
        actualizaciones = self.verificar_actualizaciones()
        respuesta = self._solicitar_confirmacion()

        if respuesta:
            if self.descargar_parches(actualizaciones):
                if self.instalar_parches(actualizaciones):
                    print(f"[{self.identity}]: Todos los parches críticos se han instalado correctamente.")
                    return True
                print(f"[{self.identity}]: La instalación no pudo completarse.")
            else:
                print(f"[{self.identity}]: No se descargaron parches.")
            return False

        print(f"[{self.identity}]: Operación cancelada por el usuario.")
        return False

    def _solicitar_confirmacion(self):
        while True:
            opcion = input("Ingresa S para sí o N para no: ").strip().lower()
            if opcion in ("s", "si"):
                return True
            if opcion in ("n", "no"):
                return False
            print("Respuesta inválida. Usa S o N.")


if __name__ == "__main__":
    kalmiya = KalmiyaInterface()
    kalmiya.ejecutar_actualizacion()
