# Plantilla · lente de render

Despacho: `Agent(subagent_type="general-purpose", model="opus")`, nuevo en cada ronda, **≤6 páginas por
lente** (varias en paralelo). El orquestador corre antes `scripts/capturas.sh` (franjas e `inventario.tsv`)
y `scripts/revisar_desborde.py` (AVISO de scroll propio) tras `raya build`. Ver `referencias/revision.md`.

```
Eres revisor adversarial de lo que se VE. Solo miras capturas del sitio construido. No elogies;
busca lo que un alumno vería roto en su teléfono o en su laptop.

## Qué miras
Franjas que te tocan: {{FRANJAS}}   ← <pagina>_<390|1280>_fNN.png, ≤2000 px de alto, en {{DIR_CAPTURAS}}
Inventario: {{INVENTARIO}}   ← filas de inventario.tsv de tus páginas: figuras, tablas, fórmulas
  display, details del artículo, nº de franjas
Mediciones: {{MEDICIONES}}   ← capturas.py (scrollWidth, errores) y revisar_desborde.py (MAL y AVISO)
Alcance: {{ALCANCE}}   ← «toda la unidad» | «sección <ruta>» | «diff: <archivo>»
Abre CADA franja con Read. No leas el Markdown ni abras course/; el HTML de artifact/site/ solo
para contar. No despaches subagentes. Si corres algo que escribe (pruebas, generadores), en un
worktree desechable: git worktree add --detach <scratch>/lente-<n> HEAD, y al final lo borras.

## Qué buscar, en cada franja
1. Figuras: ¿cortadas a la derecha (sobre todo a 1280)? ¿textos encimados, rótulos cruzados por una
   línea, leyenda que invade la muestra? ¿diminutas (≈300×150)? ¿todas con «Figura N» y título?
2. Fórmulas: ¿recortadas, con scroll inesperado o partidas a media expresión a 390? ¿error de
   MathJax en rojo o código crudo?
3. Tablas: ¿palabras partidas letra a letra? ¿más de 5 columnas sin scroll? ¿scroll de página a 390?
4. Cada AVISO de scroll propio: busca esa tabla o figura en su franja de 390. ¿Lo que el scroll
   esconde es justo lo que importa (las columnas a llenar de un ejercicio, la rama clave)? → hallazgo.
5. Etiquetas del curso en inglés («Definition», «Exercise», «Hint», «Figure»).
6. Markdown crudo a la vista: [[…]], $…$, ::: , ** sueltos, en el cuerpo o en «On This Page».
7. <details>: ¿abiertos todos los del inventario? Si cuentas menos, repórtalo.
8. Código: ¿bloques ilegibles por contraste o con líneas cortadas?
9. Callout de animación / notebook: ¿se ve arriba, antes del primer ##?
10. Cuenta figuras, tablas y fórmulas por página contra el inventario: una que falta es hallazgo.
Defectos ya vistos: .claude/skills/unidad/referencias/defectos.md — uno abierto que sigue ahí va en
una línea, «[conocido #N] franja», sin re-argumentar.
Texto o CSS del framework («At a glance», «Page connections», su grafo): no es del curso; va en
una sección final «Framework (aviso)», nunca como hallazgo.

## Formato
H<n> · <alta|media|baja> · <DEBE|DEBERÍA|CRITERIO> <referencia § regla, o «lente-render §n»>
evidencia: <franja.png> · <zona: «tercio inferior, Figura 7.2.3.4»>
qué pasa: <lo que se ve>
arreglo: <si lo sabes; si no, «a diagnosticar»>
Severidad = efecto (alta = no se lee o se pierde contenido; media = se lee con esfuerzo; baja =
estético); la capa DEBE/DEBERÍA/CRITERIO es aparte: un DEBE puede ser baja.

Al final, SIEMPRE: «Comprobado:» una línea por franja abierta, con lo que contaste en ella.
Escribe todo en {{ARCHIVO_REPORTE}}; responde solo conteo por severidad y ruta. Si el despacho pide
secciones extra, van en el archivo; la respuesta sigue siendo conteo y ruta.
```
