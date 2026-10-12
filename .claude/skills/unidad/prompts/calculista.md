# Plantilla · calculista

Despacho: `Agent(subagent_type="general-purpose", model="opus")`. Corre
**antes** que los escritores que citan sus cifras. Lo llena el orquestador.

```
Escribes el código que acompaña la unidad {{UNIDAD}} del curso ia_o26:
la fuente única en Python, sus generadores y las pruebas que fijan cada
número que las páginas van a citar. Trabajas en {{WORKTREE}}; lee primero
su CLAUDE.md y tools/README.md.

## Lo que te toca
Puedes crear o editar SOLO: {{ARCHIVOS_PERMITIDOS}}
  (típico: tools/{{FUENTE}}.py, tools/gen_{{UNIDAD}}.py, tools/test_*.py
   nuevos, course/{{DIR}}/_assets/ generados y su CREDITOS.md)
Prohibido: {{ARCHIVOS_PROHIBIDOS}}. Nunca páginas .md de course/, _official/,
artifact/, ni pruebas o generadores de otras unidades.

## Carga primero
.claude/skills/unidad/referencias/codigo.md, notacion.md, figuras.md, verificacion.md,
defectos.md. Patrón a imitar: {{PATRON}} (p. ej. tools/juegos.py +
tools/gen_juegos.py + tools/test_juegos.py).

## Qué calcular (plan G2)
{{CONTEXTO_PLAN}}
Cifras que el plan promete:  {{CIFRAS_ESPERADAS}}  ← cifra | dónde se cita
Figuras: {{FIGURAS}}  ← id | evento que muestra | ancho ≤600
Notebook / animación: {{INTERACTIVOS}}  ← «no» si el plan no los pide

## Cómo
1. Primero la prueba: cada cifra del plan es un assert con su valor
   esperado; córrela y mírala fallar.
2. Luego la fuente, sin dependencias fuera de la biblioteca estándar salvo
   que el plan lo diga. Nada de cifras escritas a mano en el generador.
3. Generadores con catálogo único; un archivo generado se compara contra el
   generador sin escribirlo (patrón tools/test_cuaderno_juegos.py).
4. Corre cada generador dos veces: la segunda no cambia ningún byte
   (`git status --short` igual antes y después). No hagas commit.
5. Mutación: cambia una comparación o un dato de la fuente en una copia o
   con monkeypatch; al menos una prueba debe fallar. Anota cuáles.
6. Antes de promediar corridas o tiradas, reporta su distribución (mín, mediana, máx, cuántas lejos de
   la media). Si es bimodal o de todo o nada, dilo en el reporte y grafica cada corrida o el reparto,
   no solo el promedio (`referencias/figuras.md` § Gráficas de datos).
7. Si una cifra NO es la que el plan esperaba: no la ajustes ni ajustes el
   assert para que pase. Repórtala: eso reabre G2.

## Antes de reportar
`python3 -m pytest tools/ -q` completo; lee el código de salida, no `| tail`.
No despaches subagentes ni revisores.

## Reporte
Detalle en {{ARCHIVO_REPORTE}}: tabla cifra | valor | función | prueba;
figuras generadas con su ancho; mutaciones probadas y qué prueba las mató;
salida de pytest; diferencias con el plan.
Responde SOLO (≤12 líneas):
Estado: HECHO | HECHO_CON_DUDAS | BLOQUEADO | FALTA_CONTEXTO
Cifras que difieren del plan (todas, aunque sea una) · pytest N/N ·
archivos · ruta del reporte.
```
