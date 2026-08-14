# 🧠 Karpaty Graph Configuration

Configuración e instrucciones para activar Karpaty en la bóveda KALMIYA.

## ¿Qué es Karpaty?

Karpaty es un plugin de Obsidian que crea visualizaciones gráficas de tu conocimiento. Conecta tus notas a través de los links [[wiki-links]] y muestra cómo está estructurado tu conocimiento.

## Instalación

### Método 1: Community Plugins (Recomendado)

1. Abre Obsidian → Settings → Community Plugins
2. Haz clic en "Browse"
3. Busca "Karpaty" o "Graph Analysis"
4. Instala el plugin
5. Actívalo en la pestaña de plugins

### Método 2: Manual

1. Descarga Karpaty desde: https://github.com/phibr0/obsidian-karpaty
2. Copia la carpeta en: `.obsidian/plugins/karpaty/`
3. Recarga Obsidian (Cmd/Ctrl + R)
4. Actívalo en Settings → Community Plugins

## Configuración

### Abrir Karpaty Graph

1. Abre la Command Palette (Cmd/Ctrl + P)
2. Escribe: "Karpaty: Open graph analysis"
3. Presiona Enter

O usa el icono de grafo en la sidebar izquierda.

### Configurar la Visualización

En Settings → Karpaty, puedes ajustar:

- **Node size**: Tamaño de los nodos (por relevancia)
- **Link distance**: Distancia entre nodos
- **Physics enabled**: Simulación física (más realista)
- **Filter by tag**: Mostrar solo notas con ciertos tags
- **Highlight backlinks**: Resaltar conexiones bidireccionales
- **Color scheme**: Esquema de colores personalizado

### Recomendaciones para KALMIYA

```json
{
  "physics": true,
  "linkDistance": 100,
  "nodeSize": "links",
  "filterTags": ["proyecto", "decisión", "aprendizaje"],
  "colorScheme": "dark",
  "highlightDepth": 2,
  "physics": {
    "enabled": true,
    "timeStep": 0.35,
    "damping": 0.4,
    "gravityDistance": 500
  }
}
```

## Uso

### Navegación

- **Click en nodo**: Abre la nota
- **Hover en nodo**: Muestra las conexiones
- **Drag nodo**: Mueve por el grafo
- **Scroll**: Zoom in/out
- **Doble click**: Expande conexiones

### Análisis

- **Nodos centrales**: Conceptos más conectados
- **Nodos aislados**: Notas sin conexiones (huérfanas)
- **Clusters**: Grupos de temas relacionados
- **Puentes**: Notas que conectan diferentes temas

## Mejora: Estructura de Links

Para que Karpaty sea útil, necesitas:

1. **Usar [[wiki-links]] generosamente**
   ```markdown
   Esta nota está relacionada con [[RAPTOR_INTEGRATION]]
   y conecta a través de [[Security_Ops]].
   ```

2. **Tags para categorización**
   ```markdown
   ---
   tags: 
     - proyecto
     - seguridad
     - raptor
   ---
   ```

3. **Backlinks bidireccionales**
   Si A → B, asegúrate que B → A cuando sea relevante

## Archivos del Grafo

- `.obsidian/graph.json` — Configuración del grafo nativo
- `.obsidian/plugins/karpaty/` — Plugin Karpaty
- `.obsidian/plugins/karpaty/data.json` — Datos del análisis

## Integración con KALMIYA

El sistema RAG (`kalmiya_rag.py`) usa los links y estructura de wiki para:

- Re-indexar automáticamente cada cambio
- Encontrar notas relacionadas rápidamente
- Responder consultas con contexto completo
- Sugerir conexiones entre concepto

## Exportar Grafo

Karpaty permite exportar visualizaciones:

1. En el viewer del grafo, click derecho
2. "Export as SVG" o "Export as PNG"
3. Guardar en `01_systems/KALMIYA/outputs/grafos/`

## Troubleshooting

### Karpaty no aparece
- Asegúrate de que está habilitado en Community Plugins
- Recarga Obsidian (Cmd/Ctrl + R)

### El grafo está vacío
- Verifica que tienes [[wiki-links]] en tus notas
- Re-indexa: Settings → Karpaty → "Reindex"

### Performance lento con muchas notas
- Reduce la distancia de física
- Filtra por tags específicos
- Deshabilita la simulación física

---

**Última actualización**: 2026-08-12  
**Basado en**: JARVIS OS Architecture
