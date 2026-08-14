---
title: "Todos los Nodos Conectados"
tags: [graph, nodes, connections, obsidian]
created: 2026-07-26
---

# ✅ Todos los Nodos Conectados en Obsidian

[[INDEX|← Índice]] | [[08_reports/graphify-out/GRAPH_REPORT|📊 Reporte del Grafo]]

> **Última actualización:** 26 julio 2026  
> **Estado:** Todos los archivos markdown conectados ✅

---

## 📊 RESUMEN

Todos los archivos `.md` del proyecto ahora tienen enlaces wikilink que los conectan al grafo de Obsidian.

### Estadísticas
- **Archivos conectados:** 20+
- **Hub central:** [[INDEX]]
- **Nodos aislados restantes:** 0 (solo archivos no-markdown)

---

## ✅ ARCHIVOS CONECTADOS

### 📖 Raíz del Proyecto

| Archivo | Estado | Conectado a |
|---------|--------|-------------|
| [[INDEX\|INDEX.md]] | ✅ | Hub central |
| [[README\|README.md]] | ✅ | INDEX, WELCOME, DASHBOARD |
| [[WELCOME\|WELCOME.md]] | ✅ | INDEX, DASHBOARD, MODULOS |
| [[KALMIYA_DASHBOARD\|KALMIYA_DASHBOARD.md]] | ✅ | INDEX, README, ROOT_STRUCTURE |
| `LICENSE` | ⚠️ | Sin enlaces (archivo de texto plano) |

### 📦 06_docs/ — Documentación

| Archivo | Estado | Conectado a |
|---------|--------|-------------|
| [[06_docs/MODULOS_IMPLEMENTADOS\|MODULOS_IMPLEMENTADOS.md]] | ✅ | INDEX |
| [[06_docs/KALMIYA_FUNCIONES\|KALMIYA_FUNCIONES.md]] | ✅ | INDEX |
| [[06_docs/FUNCIONES_IMPLEMENTACION\|FUNCIONES_IMPLEMENTACION.md]] | ✅ | INDEX |
| [[06_docs/ASI_IMPLEMENTACION\|ASI_IMPLEMENTACION.md]] | ✅ | INDEX, MODULOS_IMPLEMENTADOS |
| [[06_docs/CHAT_GUIA\|CHAT_GUIA.md]] | ✅ | INDEX, WELCOME |
| [[06_docs/OBSIDIAN_SETUP\|OBSIDIAN_SETUP.md]] | ✅ | INDEX |
| [[06_docs/OPEN_VAULT\|OPEN_VAULT.md]] | ✅ | INDEX |
| [[06_docs/RAPTOR_INTEGRATION\|RAPTOR_INTEGRATION.md]] | ✅ | INDEX, README |
| [[06_docs/ESTRUCTURA_VISUAL\|ESTRUCTURA_VISUAL.md]] | ✅ | INDEX |
| [[06_docs/CONTRIBUTING\|CONTRIBUTING.md]] | ✅ | INDEX, README |
| [[06_docs/ISSUES\|ISSUES.md]] | ✅ | INDEX, README |
| [[06_docs/ROOT_STRUCTURE\|ROOT_STRUCTURE.md]] | ✅ | INDEX, ESTRUCTURA_VISUAL |
| [[06_docs/PR_BODY\|PR_BODY.md]] | ✅ | INDEX, CONTRIBUTING |
| [[06_docs/GRAPH_CONNECTIONS\|GRAPH_CONNECTIONS.md]] | ✅ | INDEX, GRAPH_REPORT |
| [[06_docs/ORGANIZACION_COMPLETA\|ORGANIZACION_COMPLETA.md]] | ✅ | INDEX, ROOT_STRUCTURE |
| [[06_docs/NODOS_CONECTADOS\|NODOS_CONECTADOS.md]] | ✅ | Este documento |

### 📁 Proyecto SENA (06_docs/OneDrive_Docs/GitHub/proyecto_elementos/)

| Archivo | Estado | Conectado a |
|---------|--------|-------------|
| [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/README\|README.md]] | ✅ | INDEX, CHECKLIST, INSTRUCCIONES |
| [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/CHECKLIST_GITHUB\|CHECKLIST_GITHUB.md]] | ✅ | INDEX, README, INSTRUCCIONES |
| [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/INSTRUCCIONES_GITHUB\|INSTRUCCIONES_GITHUB.md]] | ✅ | INDEX, README, CHECKLIST |
| [[06_docs/OneDrive_Docs/GitHub/proyecto_elementos/examples/README\|examples/README.md]] | ✅ | INDEX, README proyecto |

### 🗒️ 07_notes/ — Notas del Sistema

| Archivo | Estado | Conectado a |
|---------|--------|-------------|
| [[07_notes/README\|README.md]] | ✅ | INDEX |
| [[07_notes/KALMIYA_Biometria_y_Audio\|KALMIYA_Biometria_y_Audio.md]] | ✅ | INDEX, README notes |

### 📊 08_reports/ — Reportes

| Archivo | Estado | Conectado a |
|---------|--------|-------------|
| [[08_reports/README\|README.md]] | ✅ | INDEX |
| [[08_reports/graphify-out/GRAPH_REPORT\|graphify-out/GRAPH_REPORT.md]] | ✅ | INDEX, README reports |

---

## 🔗 PATRÓN DE CONEXIÓN

Todos los documentos siguen este patrón:

```markdown
---
title: "Título del Documento"
tags: [tag1, tag2, tag3]
---

# 📄 Título

[[INDEX|← Índice]] | [[OTRO_DOC|🔗 Otro]] | [[TERCER_DOC|📦 Tercero]]

Contenido del documento...

---

[[INDEX|← Volver al índice]]
```

### Elementos Clave
1. **Frontmatter** con title y tags
2. **Enlace al INDEX** en el header
3. **Enlaces cruzados** a documentos relacionados
4. **Enlace de regreso** al INDEX en el footer

---

## 🎯 NODOS QUE NO SON MARKDOWN

Estos archivos NO pueden tener enlaces wikilink pero son parte del proyecto:

### Archivos de Código
- `*.py` — Scripts Python (referencias en docstrings)
- `*.js`, `*.jsx` — Código JavaScript/React
- `*.json` — Configuración
- `*.html` — Templates

### Archivos de Sistema
- `.gitignore`, `.gitmodules`
- `.env`, `.env.example`
- `LICENSE` (texto plano)
- `package.json`, `requirements.txt`

### Directorios de Sistema
- `.git/`, `.github/`, `.obsidian/`
- `.venv/`, `__pycache__/`, `.pytest_cache/`
- `node_modules/` (si existe)

**Nota:** Estos archivos aparecerán en el explorador de Obsidian pero NO en el grafo porque no son markdown.

---

## 📈 IMPACTO EN OBSIDIAN

### Vista de Grafo (`Ctrl+G`)

**Antes:**
```
[INDEX] ●

[README] ●       [WELCOME] ●

[MODULOS] ●          [CHECKLIST] ●

         [ASI] ●
```
Muchos nodos aislados sin conexiones.

**Después:**
```
           [MODULOS]
              │
     [WELCOME]─[INDEX]─[README]
         │       │        │
    [DASHBOARD] [ASI] [CHECKLIST]
         │       │        │
    [FUNCIONES] [ISSUES] [INSTRUCCIONES]
```
Todos conectados formando una red cohesiva.

### Búsqueda Mejorada

Obsidian ahora puede:
- ✅ Encontrar documentos por enlaces
- ✅ Navegar entre documentos relacionados
- ✅ Mostrar backlinks (quién enlaza a este documento)
- ✅ Sugerir documentos relacionados

---

## 🔍 VERIFICAR EN OBSIDIAN

### 1. Abrir Vista de Grafo
```
Presiona: Ctrl+G
```

### 2. Buscar Nodos Aislados
En el grafo, busca puntos sin líneas conectándolos:
- Si encuentras alguno, agrégalo a [[INDEX]]
- Asegúrate de que tiene wikilinks

### 3. Ver Backlinks
Abre cualquier documento y mira el panel derecho:
- **Outgoing links:** A quién enlaza este doc
- **Backlinks:** Quién enlaza a este doc

### 4. Filtrar por Tags
```
tag:#documentation
tag:#project
tag:#implementation
```

---

## 🚀 MANTENER CONEXIONES

### Al Crear un Nuevo Documento

1. **Agregar frontmatter:**
   ```markdown
   ---
   title: "Nombre del Doc"
   tags: [categoria, tipo]
   ---
   ```

2. **Enlazar al INDEX:**
   ```markdown
   [[INDEX|← Índice]]
   ```

3. **Agregar al INDEX:**
   Edita [[INDEX]] y agrega enlace al nuevo doc.

4. **Enlaces cruzados:**
   Enlaza a 2-3 documentos relacionados.

---

## 📚 DOCUMENTOS RELACIONADOS

- [[INDEX|← Índice Principal]]
- [[06_docs/GRAPH_CONNECTIONS|✅ Conexiones del Grafo]]
- [[06_docs/ORGANIZACION_COMPLETA|📁 Organización Completa]]
- [[08_reports/graphify-out/GRAPH_REPORT|📊 Reporte del Grafo]]

---

## ✅ CHECKLIST FINAL

- [x] Todos los `.md` en raíz conectados
- [x] Todos los `.md` en 06_docs/ conectados
- [x] Archivos del proyecto SENA conectados
- [x] Notas en 07_notes/ conectadas
- [x] Reportes en 08_reports/ conectados
- [x] INDEX como hub central funcional
- [x] Enlaces bidireccionales implementados
- [x] Frontmatter en todos los documentos
- [x] Vista de grafo sin nodos aislados grandes

---

**Estado:** ✅ **Grafo de Obsidian completamente conectado**

[[INDEX|← Volver al índice]]
