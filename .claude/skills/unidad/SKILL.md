---
name: unidad
description: Unidad o clase del curso ia_o26 — escribe el CONTENIDO de una unidad, clase o página del curso (prosa, ejemplos, ejercicios, figuras) y el código que lo acompaña (fuente Python, generadores, notebook con Open in Colab, animación), con plan maestro aprobado por el usuario, subagentes Opus en paralelo y revisión adversarial. Úsala para «escribe/arma/rehaz la clase o unidad X», o para aplicar lotes elegidos de una auditoría de unidad-auditar. No crea tareas ni objetos oficiales.
---

# unidad — orquestador de contenido del curso

Eres el **único orquestador**. Los subagentes no lanzan subagentes: tú repartes, integras y verificas.
Esta skill **sustituye** en este repo a brainstorming, writing-plans y subagent-driven-development de superpowers: no las invoques para unidades.

## Reglas fijas

- **Subagentes: solo `model: opus`.** Paralelo cuando sus archivos son disjuntos; serie en lo compartido.
- **Alcance:** contenido (índices de unidad y clase, páginas, `A_notacion`) + código que acompaña.
  **Fuera:** `_official/`, páginas `N_tarea.md`, calendario de `course/0_index.md`, cuadernillos, ilustraciones generadas (cuestan dinero). En el recorrido de la clase, la tarea es una fila «aparte» **sin enlace** con `<!-- TAREA: la dispara el usuario -->`. Una tarea que ya exista es de solo lectura: si sus números cambian, se avisa en G3.
- **Git:** worktree `.worktrees/<rama-en-español>`; commits en inglés con cuerpo que explica el porqué; nunca `git add -A` en el checkout principal (el usuario tiene cambios sin commit); nunca editar `artifact/` ni archivos generados a mano.
- **Commits los haces tú,** al cerrar cada fase verde; los subagentes no hacen commit (comparten worktree) ni despachan subagentes.
- **Contrato de Raya y del repo:** `CLAUDE.md` (Authoring contract, unidades) y `tools/README.md`. No lo repitas: cárgalo.

## Referencias (cárgalas solo cuando tocan)

| Archivo en `referencias/` | Para quién |
|---|---|
| `anatomia.md`, `lectura.md` | planear, escribir, lente alumno |
| `pedagogia.md`, `ejercicios.md` | planear, escribir, lente alumno |
| `figuras.md`, `codigo.md` | calcular, generar, lente corrección |
| `verificacion.md` | tú, al cerrar cada fase |
| `revision.md`, `defectos.md` | tú y las lentes |

Plantillas de prompt en `prompts/` (escritor, calculista, lente-correccion, lente-alumno, lente-render). Scripts en `scripts/`.

## Capas de reglas

- **DEBE** (no negociable, verificable): alcance; ids únicos con prefijo de unidad; wikilinks `[[id|texto]]` en una línea y nunca en celdas; sin enlaces ni LaTeX en encabezados; `summary` con dos puntos entre comillas; `\mathbf`, nunca `\boldsymbol`; toda imagen en `::: figure`; todo número citado sale de una función y una prueba lo fija; generadores → `git status` limpio; todo ejercicio con pista(s) y respuesta; minutos que cuadran; pytest + validate + build verdes; capturas 390/1280 miradas; plan aprobado en G2.
- **DEBERÍA:** lo que dicen las referencias con esa etiqueta; lo vigilan las lentes.
- **CRITERIO:** guía con ejemplos del repo; decides tú y lo anotas.

## Estado (sobrevive a la compactación)

`.superpowers/unidad/<id-unidad>/estado.json` (gitignorado): fase, gates aprobados (fecha + resumen), rama, plan, tareas con dueño y estado, decisiones tomadas, ronda adversarial, hallazgos abiertos. Léelo al arrancar; actualízalo en cada transición. Si no existe, reconstrúyelo con `git log` de la rama.

## Fases

```
G1 intención ─► 1 leer ─► 2 plan ─► G2 aprobación ─► 3 calcular ─► 4 escribir ─► 5 código que acompaña
            ─► 6 revisar (≤3 rondas) ─► 7 verificar ─► G3 publicar ─► 8 aprender
```

**G1 · Intención.** Una sola llamada a AskUserQuestion, ≤4 preguntas, cada una con opción recomendada: alcance (unidad/clase/páginas), ejemplo hilo, número de clases, ¿animación/notebook? Omite lo que ya dijo el usuario.

**1 · Leer** (paralelo, solo lectura). Unidades modelo (`course/7_juegos`, `course/6_optimizacion/5_practica_de_modelado`), la unidad previa (qué trae el alumno), fuentes externas con fecha, lo que ya existe. Salida: notas con `archivo:línea`.

**2 · Plan.** Escribe el plan completo en `.superpowers/unidad/<id>/plan.md` y prepara la versión de una pantalla (plantilla abajo). Cada número que citarán las páginas se nombra como «lo calcula `f()`», sin valor todavía.

**G2 · Aprobación.** Muestra la plantilla, explícala en ≤6 líneas de prosa y pregunta. **No se toca un archivo sin el sí.** Cambios pedidos → nuevo plan → G2 otra vez.

**3 · Calcular** (si la unidad tiene algo ejecutable; si no, sáltala, nunca inventes un `<unidad>.py`). Un subagente `calculista`: fuente única, pruebas que fijan cada número, generadores. Si un número contradice el plan → vuelve a G2.

**4 · Escribir** (paralelo: un subagente `escritor` por página o grupo disjunto de páginas, si son ≥4; si son menos, escribe tú). Lo compartido (`A_notacion`, índices, `CREDITOS.md`, `tools/unidades.py`, listas de `test_aceptacion.py`) lo editas tú, en serie, después de la ola. Tras la ola: `git diff --name-only` contra los archivos permitidos; un generado tocado a mano se revierte.

**5 · Código que acompaña** (paralelo tras calcular): figuras, notebook con Open in Colab (solo si la unidad tiene algoritmo ejecutable), animación (solo algoritmos). Ver `codigo.md`. Los generadores corren una vez, al final, desde ti.

**6 · Revisar.** `revision.md`: tres lentes en paralelo, sin contexto previo, con errores sembrados; evidencia `archivo:línea` o captura; ≤3 rondas; rondas 2–3 solo sobre el diff. Arreglas, y lo que se repite se vuelve prueba.

**7 · Verificar.** `verificacion.md`, en orden. Corre también `python3 tools/contrato_unidad.py <unidad>`; si la unidad está en `UNIDADES_CONTRATO`, 0 altas y medias.

**G3 · Publicar.** Resume qué cambió, qué se verificó (con cifras) y qué queda abierto; pregunta si hace merge `--no-ff` a main, push y deploy. Tras el deploy: CI verde y comprobación en vivo (Colab incluido). Propón `git worktree remove`.

**8 · Aprender.** ¿Apareció un defecto o patrón nuevo? Agrega la fila a `referencias/defectos.md` (y la regla a su referencia) en la misma rama. Repetido 2 veces → propone una guarda.

## Cuándo preguntar (lista cerrada)

Fuera de G1–G3, solo preguntas si:
1. No está claro qué unidad o clase, o sus objetivos.
2. Hay que elegir o cambiar el ejemplo hilo.
3. Una clase tendría que enseñar dos cosas nuevas.
4. Una cifra calculada contradice el plan aprobado.
5. Una página excede su tiempo en >20 % y hay que recortar contenido.
6. Habría que tocar algo fuera de alcance.
7. Habría que editar una tarea existente, otra unidad o algo compartido (`juegos.py` de otra unidad, skin, `raya.yaml`, workflow).
8. Habría que renombrar un directorio (rompe URLs).
9. Un hecho citado no está verificado.
10. Quedan hallazgos altos tras 3 rondas.

Todo lo demás: **qué se enseña → pregunta; cómo se dice → decide, anótalo en el estado y verifícalo.**

## Plantilla G2 (una pantalla)

```markdown
## Plan · <unidad> · <fecha>
**Qué se lleva el alumno:** <1 frase>. **Ejemplo hilo:** <objeto, tamaño>. **No cubre:** <lista>.

| Clase | Cambia una sola cosa | Páginas (min) · tipo | Ejemplo | Números que fija el código |
|---|---|---|---|---|
| 1 | … | 1·… (20) concepto · 2·… (35) algoritmo | … | `f()` → 7 cifras |
| Tarea | la dispara el usuario | fila «aparte», sin enlace | — | — |

**Código:** `tools/<u>.py` → N figuras · notebook + Colab: sí/no (por qué) · animación: sí/no

    fuente ─┬─► figuras ──┐
            ├─► notebook ─┼─► páginas (paralelo por clase) ─► 3 lentes ─► verificar ─► G3
            └─► pruebas ──┘

| En paralelo | En serie | Dueño de lo compartido |
|---|---|---|

**Decisiones que tomé (y por qué):** 1… 2…
**Riesgos:** …   **Costo:** ~N subagentes Opus, ≤3 rondas.
**Necesito de ti:** ¿apruebas? · ¿A o B en <punto>? (recomiendo A)
```

## Entrada desde una auditoría

Si el usuario eligió lotes de `unidad-auditar`, salta G1 y la fase 1: el plan son esos lotes (cada lote, una rama posible). Muestra G2 igual.
