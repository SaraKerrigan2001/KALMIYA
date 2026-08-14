# SKILL: Bóveda (Memory + RAG)

[[INDEX|← Índice]] | [[06_docs/JARVIS_OS/SKILLS_CATALOG|📘 Catálogo de Skills]] | [[06_docs/JARVIS_OS/README|🌟 JARVIS OS]]

Consulta tu memoria depurada. Si no está en la bóveda, no pasó.

## Descripción
El skill **Bóveda** es tu consultor de memoria. Accede a todo lo que sabes (notas, decisiones, aprendizajes, contexto) para informar acciones presentes y futuras. Funciona con Obsidian + Karpaty Graph.

## Qué Hace
- 🧠 Retrieval-Augmented Generation (RAG) sobre tu bóveda
- 🔗 Navega grafo de conocimiento (Karpaty)
- 📚 Busca en notas enlazadas
- 💾 Integra contexto histórico
- 📖 Lee y escribe en Markdown

## Parámetros de Activación
```python
"¿qué sé sobre X?"
"consulta bóveda"
"qué decidimos sobre..."
"dame contexto de..."
"recuerda cuando..."
```

## Flujo de Trabajo
1. **Recibe pregunta** → Interpreta intención
2. **Consulta RAG** → Busca en bóveda + grafo
3. **Recupera contexto** → Notas relacionadas
4. **Sintetiza** → Genera respuesta coherente
5. **Actualiza** → Registra nueva información si aplica

## Entrada
- Bóveda Obsidian: `01_systems/KALMIYA/`
- Grafo: `01_systems/KALMIYA/.obsidian/graph.json`
- Base de datos RAG: `01_systems/KALMIYA_System/rag_db/`
- Consulta: Pregunta en lenguaje natural

## Salida
```
### 📖 RESULTADO DE BÓVEDA

**Pregunta**: ¿Qué sé sobre RAPTOR?

**Respuesta Sintetizada**:
RAPTOR es nuestro framework de seguridad autónoma...

**Notas Relacionadas**:
- [[RAPTOR_INTEGRATION]] - Implementación técnica
- [[Security_Ops]] - Protocolos de seguridad
- [[Threat_Analysis]] - Análisis de amenazas recientes

**Última actualización**: 2026-08-10
**Confianza**: 0.92 (Muy alta)
```

## Archivos Relacionados
- `01_systems/KALMIYA_System/kalmiya_rag.py` — Motor RAG
- `01_systems/KALMIYA_System/obsidian_bridge.py` — Integración Obsidian
- `01_systems/LLM_Wiki/` — Wiki estructurada

## Notas
- RAG se re-indexa diariamente a las 4:00 AM
- Mantener estructura Markdown limpia en bóveda
- Links [[doble corchete]] son consultables
- YAML frontmatter para metadatos

---
**Creado:** 2026-08-12  
**Estado:** Implementado ✅
