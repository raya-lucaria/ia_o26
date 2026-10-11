---
name: unidad-auditar
description: Unidad o clase del curso ia_o26 — AUDITA (solo lectura) el contenido y el código que acompaña de una unidad, clase o página ya escrita contra el contrato de la skill `unidad` (anatomía, lectura medible, ejemplos, ejercicios, figuras, código, defectos conocidos) y entrega hallazgos agrupados en lotes para que el usuario elija cuáles arreglar. Úsala para «audita/revisa la unidad X», «¿cómo está la clase Y?». No edita nada.
---

# unidad-auditar — auditoría de solo lectura

**No edita ningún archivo del repo.** Notas y capturas van al scratchpad o a `.superpowers/unidad/<id>/auditoria-<fecha>.md` (gitignorado). Arreglar es trabajo de la skill `unidad`, solo con los lotes que el usuario elija.

Subagentes: **solo `model: opus`**, en paralelo (son de solo lectura). Las referencias viven en `.claude/skills/unidad/referencias/`; las plantillas de lente en `.claude/skills/unidad/prompts/`.

## Pasos

1. **Delimitar.** Unidad, clase o páginas. Si no está claro, una pregunta (AskUserQuestion, con opción recomendada). Registra el commit auditado (`git rev-parse --short HEAD`).
2. **Medir (mecánico, tú).**
   - `python3 tools/contrato_unidad.py <ruta-unidad> --json` → lectura, figuras, ejercicios, minutos.
   - Generadores de la unidad → `git status` limpio (`.claude/skills/unidad/scripts/generadores_limpios.sh`).
   - `python3 -m pytest tools/ -q` y `raya validate`/`build` (ver `referencias/verificacion.md`).
   - Capturas 390/1280 de las páginas (`scripts/capturas.sh`).
3. **Leer con criterio (paralelo, una lente por subagente, sin contexto previo).**
   - **Corrección:** números y prosa contra la fuente Python; hechos falsos; Python de página que no corre.
   - **Alumno:** `anatomia.md`, `pedagogia.md`, `ejercicios.md`, `lectura.md` — orden, definiciones antes de uso, ejemplo hilo y variantes, niveles de ejercicio, pistas que filtran, relleno.
   - **Render:** recibe las capturas, no el Markdown — desbordes, figuras cortadas, tablas ilegibles, contraste.
   - **Consistencia:** `figuras.md`, `codigo.md`, `defectos.md` — vocabulario de figuras, ids, títulos, notación vs `A_notacion`, notebook/Colab/animación enlazados y vigentes.
   Cada lente cita `archivo:línea` o captura; «sin hallazgos» exige la lista de lo comprobado.
4. **Calibrar.** Si la auditoría corre sobre algo con hallazgos ya conocidos (filas de `defectos.md` o una auditoría previa), cuenta cuántos encontró cada lente. Una lente que no halla un defecto conocido y presente se repite con el defecto como pista de dónde mirar, y se anota en el informe.
5. **Juntar.** Quita duplicados, clasifica, agrupa en lotes, estima esfuerzo.

## Clasificación

- **Severidad:** alta (enseña algo falso, rompe la página o el build), media (viola un DEBE o confunde), baja (DEBERÍA o estilo).
- **Regla:** DEBE / DEBERÍA / CRITERIO, citando la referencia.
- **Decisión de diseño vs defecto:** si el patrón es deliberado y documentado (p. ej. pistas y respuestas en páginas separadas de 6.4), repórtalo como «decisión a confirmar», no como defecto.
- **Fuera de alcance** (`_official`, `N_tarea.md`, calendario): solo aviso, en su propia sección; nunca en un lote.
- Unidades viejas no se juzgan contra todo el contrato: lo que no aplica a su tipo se omite.

## Salida (se muestra al usuario)

```markdown
## Auditoría · <unidad> · <commit> · <fecha>
**Resumen:** A altas · M medias · B bajas · decisiones a confirmar: D · guardas que faltan: G

| # | Sev | Regla | Evidencia | Arreglo propuesto | Lote |
|---|---|---|---|---|---|
| 1 | alta | DEBE dato correcto | `ruta.md:210` | … | L1 |

**Lotes** (cada uno es una rama posible):
- **L1 · <nombre>** — N hallazgos · ~X min · riesgo
- **L2 · …**
- **L3 · guardas nuevas** — qué prueba evita que vuelva

**Decisiones a confirmar:** …
**Fuera de alcance (solo aviso):** tareas / objetos oficiales afectados.
**Necesito de ti:** ¿qué lotes ejecuto? (recomiendo L1 + L3)
```

Explica la tabla en ≤5 líneas de prosa antes de preguntar. Cuando el usuario elige lotes, invoca la skill `unidad` empezando en su fase **2 · Plan** con esos lotes, y su G2 se muestra igual.
