# Plantilla · escritor

Despacho: `Agent(subagent_type="general-purpose", model="opus")`, uno por
página o por conjunto disjunto de páginas. El orquestador llena cada `{{…}}`.

```
Escribes {{PAGINAS}} de la unidad {{UNIDAD}} del curso ia_o26.
Trabajas en {{WORKTREE}}. Antes de nada lee CLAUDE.md de ese worktree.

## Lo que te toca
Puedes crear o editar SOLO: {{ARCHIVOS_PERMITIDOS}}
Prohibido tocar (otro agente es dueño o está fuera de alcance):
{{ARCHIVOS_PROHIBIDOS}}
Nunca: course/**/_official/, *_tarea.md, artifact/, calendario, ilustraciones.
Si necesitas cambiar un archivo que no es tuyo, NO lo cambies: pídelo en el reporte.

## Carga primero
.claude/skills/unidad/referencias/: anatomia.md, lectura.md, pedagogia.md,
ejercicios.md, figuras.md, {{REFERENCIAS_EXTRA}}
Modelo de tono y forma: {{PAGINAS_MODELO}}

## Plan aprobado (G2) para tus páginas
{{CONTEXTO_PLAN}}
Ejemplo hilo: {{EJEMPLO_HILO}} · Prefijo de ids: {{PREFIJO}}
Cifras que puedes citar (de la fuente, no las recalcules a mano):
{{TABLA_CIFRAS}}   ← cifra | función de {{FUENTE_PY}} | prueba que la fija
Figuras disponibles: {{FIGURAS}}   ← id del SVG | qué estado muestra

## Reglas que más se rompen (detalle en defectos.md)
- Ninguna cifra que no esté en la tabla. Si te falta una, escribe
  <!-- CIFRA: qué falta --> y repórtalo; no la inventes ni la estimes.
- Ningún símbolo, término o algoritmo antes de presentarlo en esta página
  o en una anterior de la navegación.
- Todo ejercicio lleva pista(s) y respuesta; la pista no nombra la respuesta.
- Toda imagen va en ::: figure; wikilinks con etiqueta y en una sola línea;
  nada de enlaces ni $…$ en encabezados; \mathbf, nunca \boldsymbol.
- Afirmaciones de hecho («todas distintas», «siempre»): compruébalas contra
  la fuente o no las escribas.

## Antes de reportar
1. Relee tu diff entero. Cada reemplazo que hiciste, ¿cambió algo? (grep)
2. Corre: {{COMANDOS_ENFOQUE}} (pytest de lo tuyo + raya validate).
   Lee el código de salida; no entubes pytest a tail.
3. No hagas commit. No despaches subagentes ni revisores: la revisión ya
   está agendada y la hace el orquestador con lentes nuevas.

## Reporte
Escribe el detalle en {{ARCHIVO_REPORTE}}:
- archivos tocados; minutos estimados por página y cómo los contaste;
- cada cifra citada → fila de la tabla; cada <!-- CIFRA --> pendiente;
- desviaciones del plan y por qué; dudas.
Responde SOLO (≤12 líneas):
Estado: HECHO | HECHO_CON_DUDAS | BLOQUEADO | FALTA_CONTEXTO
Archivos · comandos corridos y su salida (una línea) · dudas · ruta del reporte.
Si es BLOQUEADO o FALTA_CONTEXTO, di exactamente qué necesitas.
Una decisión de qué se enseña (no de cómo se dice) es FALTA_CONTEXTO.
```
