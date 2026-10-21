# Foto de la web del curso (T10 de la clase 2 de Markov)

`enlaces_curso.tsv` es una **foto fija** de los enlaces entre las páginas de
`course/`, tomada el **2026-10-21** (antes de escribir las páginas de la clase 2
de Markov, cuyas seis páginas no aparecen como nodos). La página de PageRank
(`course/8_markov/2_a_la_larga/6_pagerank.md`) cita las cifras de esta foto, no
las del curso de hoy: si el curso crece, la foto no cambia y las cifras siguen
siendo ciertas.

Cómo se generó:

```bash
python3 tools/markov.py foto      # markov.escribir_foto() sobre markov.enlaces_curso()
```

- Nodos: cada `.md` de `course/` con `id` en su frontmatter, fuera de los
  directorios de soporte (`_*`).
- Enlaces: wikilinks `[[id|…]]` y `raya:id` entre esas páginas (por id o por
  alias), sin repetir y sin enlaces de una página a sí misma.
- Formato: un encabezado `tipo a b`; renglones `nodo<TAB>id<TAB>título` y
  `enlace<TAB>origen<TAB>destino`.

No la regeneres: `markov.pagerank_curso()` lee la foto (`markov.leer_foto()`),
y `tools/test_markov_c2.py` fija sus cifras (134 nodos, 506 enlaces, 5 sin
salidas). Regenerarla es una decisión que cambia las cifras de la página.
