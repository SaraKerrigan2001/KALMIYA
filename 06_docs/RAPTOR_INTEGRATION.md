# RAPTOR Security Integration para KALMIYA

![RAPTOR](https://img.shields.io/badge/RAPTOR-Security%20Agent-red?style=flat-square) ![Status](https://img.shields.io/badge/Status-Integrated-success?style=flat-square)

## Descripción General

RAPTOR (Recursive Autonomous Penetration Testing and Observation Robot) es un framework autónomo de investigación de seguridad construido por [gadievron](https://github.com/gadievron) que ha sido integrado en KALMIYA para proporcionar capacidades avanzadas de seguridad ofensiva y defensiva.

### ¿Qué es RAPTOR?

RAPTOR es un sistema autónomo que:
- **Analiza código estáticamente** para encontrar vulnerabilidades
- **Analiza binarios** en busca de fallos de seguridad
- **Valida vulnerabilidades** usando IA (Claude)
- **Genera exploits** para vulnerabilidades confirmadas
- **Escribe patches** automáticos para vulnerabilidades

## Características en KALMIYA

Con RAPTOR integrado en KALMIYA obtienes:

### 1. Análisis Autónomo de Seguridad
```python
from modules.raptor_security_agent import RaptorSecurityAgent

agent = RaptorSecurityAgent()
result = agent.analyze_codebase("./01_systems/KALMIYA_System")
```

### 2. Análisis de Amenazas
```python
threat_analysis = agent.analyze_threat(
    "Posible inyección SQL en módulo de base de datos"
)
```

### 3. Generación de Reportes
```python
report = agent.generate_security_report([result])
print(report)
```

### 4. Búsqueda de Vulnerabilidades
- Análisis estático automático
- Búsqueda de patrones de seguridad débiles
- Validación de exploitabilidad
- Sugereencias de remediación

## Instalación y Configuración

### Requisitos Previos
- Python 3.12+
- Git
- Claude API Key (para análisis con IA)
- (Opcional) Herramientas binarias (objdump, radare2, etc.)

### Instalación

El submódulo RAPTOR ya está incluido. Para actualizarlo:

```powershell
cd C:\Users\maria\env
git submodule update --remote 01_systems/RAPTOR
```

### Configuración de API

Asegúrate de que tu Claude API key está configurada:

```powershell
$env:CLAUDE_API_KEY = "tu_clave_aqui"
```

O en tu archivo `.env`:
```
CLAUDE_API_KEY=tu_clave_aqui
```

## Casos de Uso

### 1. Auditoría de Seguridad del Código
```python
from modules.raptor_security_agent import RaptorSecurityAgent

agent = RaptorSecurityAgent()

# Analiza KALMIYA buscando vulnerabilidades
result = agent.analyze_codebase(
    "01_systems/KALMIYA_System",
    analysis_type="comprehensive"
)

print(f"Vulnerabilidades encontradas: {len(result.vulnerabilities)}")
print(f"Nivel de riesgo: {result.risk_level}")
```

### 2. Análisis de Amenazas Específicas
```python
# Analiza vectores de ataque para una amenaza específica
threat = agent.analyze_threat(
    "Acceso no autorizado a bases de datos de usuario"
)

print("Estrategias ofensivas:")
for strategy in threat["offensive_strategies"]:
    print(f"  - {strategy}")

print("\nEstrategias defensivas:")
for defense in threat["defensive_strategies"]:
    print(f"  - {defense}")
```

### 3. Reporte de Seguridad Automatizado
```python
# Genera reporte ejecutivo
analyses = [
    agent.analyze_codebase("01_systems/KALMIYA_System"),
    agent.analyze_codebase("01_systems/KALMIYA_System/modules"),
]

report = agent.generate_security_report(analyses)

# Guarda el reporte
with open("08_reports/security_report.md", "w") as f:
    f.write(report)
```

## Estructura de Directorio

```
KALMIYA/
├── 01_systems/
│   ├── KALMIYA_System/
│   │   └── modules/
│   │       └── raptor_security_agent.py (⭐ Nuevo)
│   └── RAPTOR/ (⭐ Nuevo - Submódulo de Git)
│       ├── raptor.py
│       ├── analysis/
│       ├── exploits/
│       └── ...
├── 06_docs/
│   └── RAPTOR_INTEGRATION.md (⭐ Nuevo)
└── 08_reports/
    └── security_reports/ (Reportes generados)
```

## Comandos Útiles

### Actualizar RAPTOR
```powershell
cd C:\Users\maria\env
git submodule update --remote
```

### Ejecutar Test de RAPTOR
```powershell
cd 01_systems/RAPTOR
python -m pytest tests/
```

### Generar Reporte de Seguridad
```python
# En Python
from modules.raptor_security_agent import RaptorSecurityAgent
import logging

logging.basicConfig(level=logging.INFO)
agent = RaptorSecurityAgent()
report = agent.generate_security_report([
    agent.analyze_codebase("01_systems/KALMIYA_System")
])
print(report)
```

## Documentación de RAPTOR

Para información completa sobre RAPTOR, consulta:
- [RAPTOR en GitHub](https://github.com/gadievron/raptor)
- [README de RAPTOR](../RAPTOR/README.md)
- [Documentación de Análisis](../RAPTOR/docs/)

## Seguridad y Privacidad

⚠️ **IMPORTANTE:**

1. **Uso Autorizado**: RAPTOR solo debe usarse en sistemas y código que poseas o tengas permiso explícito de auditar.

2. **Datos Sensibles**: Los análisis se envían a Claude API. No analices código con credenciales hardcodeadas.

3. **Cumplimiento Legal**: Respeta las leyes de tu jurisdicción sobre testing de penetración y análisis de seguridad.

4. **Divulgación Responsable**: Si encuentras vulnerabilidades en sistemas de terceros, reportalas de manera responsable.

## Integración Futura

Planes para mejorar la integración de RAPTOR en KALMIYA:

- [ ] Dashboard de seguridad en tiempo real
- [ ] Alertas automáticas de vulnerabilidades criticas
- [ ] Integración con módulo de Telegram para reportes
- [ ] Análisis programado automático
- [ ] Integración con CI/CD pipeline
- [ ] Caché de resultados para análisis más rápidos

## Contribuir

¿Quieres mejorar la integración de RAPTOR? 

1. Fork el repositorio
2. Crea una rama: `git checkout -b feature/raptor-enhancement`
3. Commit cambios: `git commit -am 'Add RAPTOR feature'`
4. Push: `git push origin feature/raptor-enhancement`
5. Envía un Pull Request

Para más detalles, consulta [CONTRIBUTING.md](../06_docs/CONTRIBUTING.md)

## Licencia

- **KALMIYA**: MIT (ver [LICENSE](../LICENSE))
- **RAPTOR**: MIT (ver [01_systems/RAPTOR/LICENSE](../RAPTOR/LICENSE))

## Créditos

- **RAPTOR Framework**: [gadievron](https://github.com/gadievron), [danielcuthbert](https://github.com/danielcuthbert), [thomasdullien](https://github.com/thomasdullien), [mbrg](https://github.com/mbrg), [grokjc](https://github.com/grokjc)
- **KALMIYA Integration**: María (SaraKerrigan2001)

## Soporte

Si encuentras problemas:

1. Revisa los logs: `05_tests/audit_results.txt`
2. Consulta la documentación de RAPTOR
3. Abre un issue en [GitHub](https://github.com/SaraKerrigan2001/KALMIYA/issues)
4. Contacta al equipo de desarrollo

---

**Última actualización:** 2026-08-08  
**Versión:** 1.0.0  
**Estado:** ✅ Integrado
