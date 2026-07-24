"""
weather_integration.py — Integración de clima real con Open-Meteo
==================================================================
Usa get_real_weather() del módulo principal para obtener datos reales.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class WeatherIntegration:

    def __init__(self):
        self.location = None
        self.current_weather = {}

    def get_current_weather(self, location: str = "Cúcuta") -> dict:
        """Obtiene el clima actual real vía Open-Meteo."""
        from kalmiya_nuevas_funciones import get_real_weather
        self.location = location
        self.current_weather = get_real_weather(location)
        return self.current_weather

    def get_forecast(self, days: int = 7) -> dict:
        """Obtiene el pronóstico de los próximos días."""
        if not self.current_weather:
            self.get_current_weather(self.location or "Cúcuta")
        forecast = self.current_weather.get("pronostico", [])[:days]
        return {
            "location": self.current_weather.get("ciudad", self.location),
            "days":     days,
            "forecast": forecast,
        }

    def get_weather_alerts(self) -> dict:
        """Revisa alertas de clima — lluvia intensa o tormenta."""
        if not self.current_weather:
            self.get_current_weather(self.location or "Cúcuta")
        alerts = []
        for day in self.current_weather.get("pronostico", []):
            if day.get("lluvia", 0) > 10:
                alerts.append(f"Lluvia intensa el {day['dia']}: {day['lluvia']} mm")
            if "tormenta" in day.get("cond", "").lower():
                alerts.append(f"Tormenta el {day['dia']}")
        return {"alerts": alerts}

    def suggest_activities(self, weather_type: str = "") -> list:
        """Sugiere actividades según el clima actual."""
        if not weather_type and self.current_weather:
            cond = self.current_weather.get("condicion", "").lower()
            if any(w in cond for w in ["lluvia", "tormenta", "llovizna"]):
                weather_type = "rainy"
            elif any(w in cond for w in ["despejado", "soleado"]):
                weather_type = "sunny"
            else:
                weather_type = "cloudy"

        suggestions = {
            "sunny":  ["Salir a caminar", "Hacer deporte al aire libre", "Fotografía"],
            "rainy":  ["Programar y estudiar ADSO", "Dibujar", "Ver series", "Cocinar"],
            "cloudy": ["Pasear", "Leer", "Explorar nuevos lugares"],
        }
        return suggestions.get(weather_type, suggestions["cloudy"])
