---
title: "Guía de Uso - ASI Intelligence & Security Features"
tags: [guide, asi, security, intelligence, usage]
---

# 🕵️ Guía de Uso — ASI Intelligence & Security

**KALMIYA v3.5 + JARVIS OS + ASI**  
Guía práctica para usar capacidades avanzadas de análisis

[[INTELLIGENCE_SECURITY_MODULE|← Volver a Inteligencia y Seguridad]]

---

## 🚀 Inicio Rápido

### Paso 1: Activar ASI

**Opción A - Desde Menú**
```
Ejecutar KALMIYA
  ↓
Opción: ASI1
  ↓
Confirmar: "sí" (por voz)
  ↓
✅ ASI Activado
```

**Opción B - Desde Chat**
```
Decir o escribir:
"KALMIYA, activa ASI para análisis profundo"

Respuesta esperada:
"Modo ASI activado. Inteligencia 3× superior. Listo para análisis."
```

**Opción C - Desde Código**
```python
from kalmiya_asi import activate_asi, is_asi_active
activate_asi()
assert is_asi_active() == True
```

### Paso 2: Verificar Estado

```
Opción: ASI3
  ↓
Resultado:
  ASI Estado: Activo
  Nivel: Superinteligencia
  Intervalo de pensamiento: 60s
  Capacidades: Análisis multidimensional, síntesis cognitiva, metacognición
```

### Paso 3: Solicitar Análisis

**Ejemplo 1: Análisis OSINT Rápido**
```
"KALMIYA, analiza la seguridad de mi_empresa.com"

ASI procesa:
├── Busca dominios relacionados
├── Extrae tecnologías usadas
├── Verifica certificados SSL
├── Analiza exposición
└── Genera reporte

Resultado: Score 72/100, 3 riesgos altos, recomendaciones
```

---

## 📋 Comandos Comunes

### Análisis de Ciberseguridad

```
"KALMIYA, ¿vulnerabilidades en mi servidor web?"
"Análisis profundo de seguridad de [dominio]"
"¿Qué tecnologías usa [empresa]?"
"Investigar exposición de datos públicos"
```

### Análisis de Incidentes

```
"KALMIYA, analiza estos logs de ataque"
"¿Qué pasó en mi sistema? Aquí están los eventos"
"Investigación forense del incidente del 2026-08-01"
"Línea temporal del ataque: primero, progresión, exfiltración"
```

### Inteligencia de Amenazas

```
"¿Qué amenazas afectan a sistemas Java?"
"Análisis de campañas APT-X"
"Predicción: ¿próximas vulnerabilidades?"
"Actores conocidos que usan esta técnica"
```

### Análisis de Privacidad

```
"¿Mi app cumple GDPR?"
"Análisis de riesgo de filtración de datos"
"¿Qué tan expuestos están mis datos?"
"Recomendaciones para privacidad"
```

---

## 🎯 Casos de Uso por Escenario

### Escenario 1: Auditoría de Seguridad Interna

**Objetivo**: Encontrar vulnerabilidades en tus sistemas

```
1. Activar ASI (paso anterior)

2. Solicitar análisis:
   "KALMIYA, auditoría completa de seguridad
    - Servidor web: mi_app.com
    - Base de datos: interna
    - API: /api/v2
    Nivel: L3 (exhaustivo)"

3. Esperar resultado (~2-5 minutos)

4. Recibir:
   ✅ Vulnerabilidades identificadas (CVSS score)
   ✅ Configuraciones inseguras
   ✅ Recomendaciones priorizado
   ✅ Plan de remediación
```

**Ejemplo de salida**:
```
AUDITORÍA DE SEGURIDAD — mi_app.com

Score General: 72/100 (Amarillo)

CRÍTICOS (3):
1. OpenSSL 1.0.2 desactualizado → Update a 1.1.1+
2. SQL Injection en /api/login → Input validation
3. Credenciales AWS en código fuente → Rotate keys

ALTOS (7):
- CORS configuration loose
- Missing HSTS header
- Rate limiting ausente
- ...

RECOMENDACIONES PRIORITARIAS:
1. Actualizar OpenSSL (24h)
2. Code audit para SQL injection (48h)
3. Secrets rotation (4h)
```

### Escenario 2: Investigación de Breach

**Objetivo**: Entender qué pasó en un incidente de seguridad

```
1. Activar ASI

2. Proporcionar datos:
   "KALMIYA, investigación forense
    - Logs adjuntos (archivo.csv)
    - Fecha: 2026-08-01 a 2026-08-03
    - Análisis: qué pasó, quién lo hizo, qué sacaron
    Nivel: L4 (forense profundo)"

3. ASI procesa:
   ├── Carga logs
   ├── Correlation timeline
   ├── Identifica puntos de entrada
   ├── Mapea progresión
   ├── Detecta exfiltración
   └── Atribución probable

4. Recibir reporte con:
   ✅ Timeline exacto del ataque
   ✅ Vector de entrada identificado
   ✅ Técnicas usadas (ATT&CK)
   ✅ Actores probables
   ✅ Datos comprometidos
   ✅ Acciones inmediatas
```

**Ejemplo de salida**:
```
INVESTIGACIÓN FORENSE — Incidente 2026-08-01

TIMELINE RECONSTRUIDA:
2026-08-01 23:47 → SSH bruteforce, 10,000 intentos de admin
2026-08-02 00:15 → Acceso exitoso, sistema X comprometido
2026-08-02 01:30 → Escalada de privilegios (dirty cow exploit)
2026-08-02 02:00 → Lateral movement a BD server
2026-08-02 04:00 → Datos copiados: 50GB clientes_datos.sql

ATRIBUCIÓN PROBABLE: APT-28 (Russian)
├── TTPs: SSH bruteforce (conocido)
├── Infraestructura: IPs de datacenter RU
├── Timing: Europeo business hours (UTC+3)
└── Sofisticación: Media-Alta

DATOS COMPROMETIDOS: 2.3M registros (clientes, pagos)

ACCIONES INMEDIATAS:
1. Desconectar sistema X (NOW)
2. Forzar reset de contraseñas (2h)
3. Cambiar credenciales AWS (4h)
4. Notificar autoridades (24h GDPR)
```

### Escenario 3: Análisis de Amenaza (Threat Intelligence)

**Objetivo**: Saber qué amenazas pueden afectar tus sistemas

```
1. Activar ASI

2. Solicitar análisis:
   "KALMIYA, threat intelligence
    - Tecnologías: Java Spring, React, PostgreSQL, AWS
    - Industria: E-commerce
    - Año: 2026
    - Análisis: CVEs críticos, actores, predicciones
    Nivel: L2 (profundidad media)"

3. ASI busca:
   ├── CVEs activos para Java
   ├── Campañas conocidas vs e-commerce
   ├── Actores APT interesados
   ├── Predicción de próximas amenazas
   └── Recomendaciones defensivas

4. Recibir inteligencia:
   ✅ Lista de CVEs con exploits públicos
   ✅ Campañas activas dirigidas a tipo de negocio
   ✅ Actores conocidos y sus tácticas
   ✅ Predicción de vulnerabilidades Q4 2026
   ✅ Recomendaciones defensivas
```

**Ejemplo de salida**:
```
THREAT INTELLIGENCE — E-commerce 2026

CVES CRÍTICOS ACTIVOS (3):
1. CVE-2026-1234 (Log4j-like) Java Log4j 2.x
   - CVSS: 10.0 (Crítico)
   - Exploits públicos: Sí
   - Activos atacando: APT-X, Lazarus
   - Recomendación: Update a 2.17.1+ inmediatamente

2. CVE-2026-5678 (Spring) Spring Framework
   - CVSS: 9.1
   - Exploits conocidos: Sí
   - Recomendación: Patch Sprint 6.1+

3. CVE-2026-9999 (PostgreSQL) Injection
   - CVSS: 8.6
   - Recomendación: Update a v15.2+

CAMPAÑAS ACTIVAS:
- Magecart (evasión de pago) → 200+ sitios atacados
- FIN7 (data theft) → E-commerce específico
- LockBit (ransomware) → 50+ ataques semana

PREDICCIÓN Q4 2026:
- 80% probable: Supply chain attack vía npm packages
- 60% probable: New Java deserialization exploit
- 70% probable: Zero-day en React component library

RECOMENDACIONES:
1. Patches prioritarios (24h deadline)
2. WAF rules para CVE-1234 (inmediato)
3. Audit de dependencias npm (48h)
```

### Escenario 4: Análisis de Privacidad (GDPR Compliance)

**Objetivo**: Validar cumplimiento de regulaciones

```
1. Activar ASI

2. Solicitar análisis:
   "KALMIYA, análisis GDPR de mi aplicación
    - Datos recolectados: emails, ubicación, pagos
    - Almacenamiento: Servidor local + AWS S3
    - Terceros: Stripe, SendGrid, Analytics
    - Análisis: Gaps GDPR, recomendaciones
    Nivel: L3"

3. ASI evalúa:
   ├── Consentimiento y legitimidad
   ├── Almacenamiento y retención
   ├── Acceso de terceros
   ├── Derechos del usuario (acceso, olvido)
   ├── Encriptación y seguridad
   └── Compliance general

4. Recibir reporte:
   ✅ Score GDPR compliance (0-100%)
   ✅ Gaps identificados
   ✅ Riesgos legales
   ✅ Plan de remediación
```

---

## 🔧 Niveles de Análisis (Cuándo Usar Cuál)

### L1: Surface (Rápido)
```
Uso: Reconocimiento inicial
Tiempo: <10 segundos
Profundidad: Superficial
Ejemplo:
  "KALMIYA, quick scan de mi dominio"
  → Extrae servicios, tecnologías, info básica
```

### L2: Deep (Normal)
```
Uso: Investigación estándar
Tiempo: 30-60 segundos
Profundidad: Multidimensional (6 perspectivas)
Ejemplo:
  "KALMIYA, análisis de vulnerabilidades"
  → Análisis técnico + contexto + recomendaciones
```

### L3: Thorough (Completo)
```
Uso: Auditoría profunda
Tiempo: 2-5 minutos
Profundidad: Exhaustiva
Ejemplo:
  "KALMIYA, auditoría de seguridad nivel L3"
  → Todo: vuln + contexto + histórico + predicciones
```

### L4: Forensic (Investigación)
```
Uso: Investigación post-incidente
Tiempo: 10+ minutos
Profundidad: Forense completa
Ejemplo:
  "KALMIYA, investigación forense del breach"
  → Timeline + atribución + causa raíz + recuperación
```

---

## ✋ Restricciones Importantes

### KALMIYA SÍ PUEDE:
✅ Analizar tus propios sistemas  
✅ Detectar vulnerabilidades propias  
✅ Investigar incidentes en tu infraestructura  
✅ Proporcionar recomendaciones defensivas  
✅ Analizar información pública (OSINT ético)  

### KALMIYA NUNCA HARÁ:
❌ Hacking no autorizado  
❌ Acceder a sistemas sin permiso  
❌ Crear malware o exploits reales  
❌ Ataques DDoS o destructivos  
❌ Violar privacidad  
❌ Actividades criminales  

---

## 🎓 Tips y Mejores Prácticas

### 1. Sé Específico en Solicitudes
```
❌ Malo: "Analiza seguridad"
✅ Bien: "Analiza vulnerabilidades en API /login, nivel L2, enfoque en auth"
```

### 2. Proporciona Contexto
```
❌ Malo: "¿Es seguro?"
✅ Bien: "Tengo aplicación Java Spring en AWS. ¿Vulnerabilidades?"
```

### 3. Elige Nivel Apropiado
```
Para urgencias: L1 (rápido)
Para investigación: L2-L3
Para post-mortem: L4 (forense)
```

### 4. Actúa en Recomendaciones
```
1. Recibir análisis
2. Priorizar por CVSS/impacto
3. Implementar fixes según timeline
4. Verificar remediación
5. Documentar cambios
```

### 5. Mantén Privacidad
```
- No compartas datos sensibles públicamente
- Usa análisis L4 para datos confidenciales
- Almacena reportes en lugar seguro
```

---

## 📞 Troubleshooting

### "ASI no se activa"
```
1. Verificar internet (ASI necesita Claude API)
2. Verificar API key de Claude válida
3. Reiniciar KALMIYA
4. Verificar logs en 08_reports/
```

### "Análisis muy lento"
```
1. Reducir nivel: L3 → L2
2. Ser más específico en solicitud
3. Reducir volumen de datos
4. Intentar en otra hora (menos carga)
```

### "Resultados imprecisos"
```
1. Proporcionar más contexto
2. Aumentar nivel: L2 → L3
3. Incluir logs/datos adicionales
4. Pedir validación: "¿Es acertado?"
```

---

## 🔗 Referencias

- [[INTELLIGENCE_SECURITY_MODULE|Intelligence & Security Module (Completo)]]
- [[ASI_IMPLEMENTACION|ASI Implementation Details]]
- [[06_docs/RAPTOR_INTEGRATION|RAPTOR Security Framework]]
- [[KALMIYA_FUNCIONES|Funciones de KALMIYA]]

---

## 📊 Resumen Rápido

| Necesidad | Comando | Nivel | Tiempo |
|-----------|---------|-------|--------|
| Scan rápido | "Quick scan" | L1 | <10s |
| Auditoría | "Análisis de seguridad" | L2 | 30-60s |
| Investigación | "Investigar incidente" | L3 | 2-5m |
| Forense | "Análisis forense completo" | L4 | 10+m |

---

**Última actualización**: Agosto 2026  
**ASI Estado**: ✅ Activo y Funcional  
**Restricciones Éticas**: ✅ Implementadas

[[INDEX|← Volver al índice principal]]
