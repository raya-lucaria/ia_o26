# Notación: una sola, con sentido, bien definida

Para quién: planear, escribir, calcular (nombres en el código), lentes alumno y consistencia.
Las hojas de notación del curso: `course/3_computabilidad/A_notacion.md`, `course/4_complejidad/A_notacion.md`,
`course/7_juegos/A_notacion.md` (y la de cada unidad nueva).

## Unificar
- **DEBE** buscar antes de inventar: `grep` del símbolo y del concepto en **todas** las `A_notacion.md` y en las
  páginas de la unidad. Si el concepto ya tiene símbolo, se reusa tal cual; si la letra ya significa otra cosa,
  la nueva cede (`course/7_juegos/A_notacion.md:88`: $w$ es «lo que devuelve un hijo», por eso MCTS usa $G(s')$).
- **DEBE** una letra, una cosa, en la unidad y en las unidades que la unidad cita (defectos #19). Choque
  inevitable → aviso en la primera aparición y en `A_notacion` («Esta $N$ no es Negras», `A_notacion.md:100`).
- **DEBE** traducir a la notación del curso cualquier material externo (libro, artículo, esbozo del usuario)
  **antes** de escribir: $Q(s,a)$ → $\bar u(s')$, $N(s,a)$ → $N(s')$. Una línea lo dice si el alumno lo verá
  distinto fuera: «en otros textos verás $Q(s,a)$; aquí es $\bar u(s')$».
- **DEBERÍA** seguir la convención de Russell y Norvig (el libro del curso) salvo choque con lo ya enseñado.

## Que el símbolo diga lo que es
- **DEBE** símbolos mnemónicos y distintos para cosas distintas: $\mathrm{Pl}$ jugador y $\Pr$ probabilidad,
  nunca dos $P$ (`tools/test_juegos.py::test_la_unidad_escribe_pl_y_no_p`; `A_notacion.md:94`); $G$ de
  ganadas, $N$ de número de simulaciones; procedimientos en MAYÚSCULAS con guion (DECIDIR-CON-CORTE).
- **CRITERIO** palabra en vez de letra si el símbolo se usaría una o dos veces: «tiempo», no $T$
  (`course/7_juegos/3_cuando_no_cabe/2_minimax_con_corte.md:530`), porque $T$ ya es la transición.
- **DEBE** en código, los mismos nombres que en la página (`mejor_jugada`, `mejor_valor`), con el símbolo en
  el comentario si difiere.

## Definir correctamente
- **DEBE** cada símbolo, en su primera aparición: **qué es** (tipo: número, conjunto, función, procedimiento),
  **cómo se lee** en palabras, **su dominio o escala** (¿$\pm1$? ¿$[0,1]$? ¿$\pm100$?) y **desde qué lado**
  se mide (de MAX, del que mueve). Antes de usarse, nunca después (`lectura.md`).
- **DEBE** fila en la `A_notacion.md` de la unidad, con «Se presenta en», en el mismo commit que la página.
- **DEBE** una fórmula importada nombra sus supuestos (acotado en $[0,1]$, independientes…) y qué cambia al
  pasarla a la escala del curso; si cambia una constante, se dice y se calcula (p. ej. $c$ al pasar de $[0,1]$ a $\pm1$).
- **DEBERÍA** distinguir en la definición lo que se parece y no es (bloque «Qué no es»: $\mathrm{EVAL}$ no es $V$).

## Quién lo vigila
- Escritor: busca y traduce antes de escribir; pide la fila de `A_notacion` en su reporte.
- Lente de consistencia § 5 y lente del alumno § 3: símbolo sin fila, letra con dos sentidos, símbolo que ya
  existía con otro nombre en otra unidad, escala no declarada.
- Guardas existentes: `test_la_unidad_escribe_pl_y_no_p`. Un choque que se repita 2 veces → guarda nueva (`revision.md`).
