# Módulo 2 — The Left Takes the Future Back

**Filosofía de la IA · La izquierda reclama el futuro**

Cuatro lecturas, 53 páginas, entre 3.5 y 4 horas. Siguen directo de las seis del
[Módulo 1](../clase_1/README.md): el manifiesto que reclama para la izquierda
lo que Land y Fisher dejaron planteado, y su aterrizaje en programa concreto e
infraestructura.

## Cuadernillo

**[`lecturas/filosofia_ia_clase_2_cuadernillo.pdf`](lecturas/filosofia_ia_clase_2_cuadernillo.pdf)**
— **53 páginas, las cuatro lecturas completas**, cada una con su portadilla y
la razón por la que se lee.

| # | Lectura | Autor | Año | Fuente | Estado |
|---|---|---|---|---|---|
| 1 | «#ACCELERATE: Manifesto for an Accelerationist Politics» | Williams y Srnicek | 2013 | [criticallegalthinking.com](https://criticallegalthinking.com/2013/05/14/accelerate-manifesto-for-an-accelerationist-politics/) | ✅ en el cuadernillo, completa |
| 2 | *Capitalist Realism*, cap. 4 | Fisher | 2009 | ed. Zero Books 2009, pp. 21–30 del impreso (pp. 25–34 del archivo) | ✅ en el cuadernillo |
| 3 | *Inventing the Future*, cap. 6 «Post-Work Imaginaries» | Srnicek y Williams | 2015 | ed. Verso 2015, conversión EPUB → PDF, pp. 77–93 de ese archivo | ✅ en el cuadernillo |
| 4 | «Red Stack Attack! Algorithms, Capital and the Automation of the Common» | Terranova | 2014 | [euronomade.info](http://www.euronomade.info/?p=2268) | ✅ en el cuadernillo, completa |

### Sobre las dos que llegaron como PDF

Ambas se reproducen de la edición que las tiene, y el pipeline las recorta por
página. Dos avisos que importan al citarlas en clase — uno de ellos es una
discrepancia de paginación real, no cosmética:

- **Fisher, *Capitalist Realism*.** El archivo es la edición Zero Books 2009
  completa, 86 páginas contando las preliminares. **Las pp. 25–34 que recorta
  el pipeline son internas de este archivo, no del impreso**: el índice del
  propio libro sitúa el capítulo 4, «Reflexive impotence, immobilization and
  liberal communism», en la p. 21 y el capítulo 5 en la p. 31, y en el archivo
  esos dos capítulos empiezan en las pp. 25 y 35 — un corrimiento constante de
  cuatro páginas. **En clase se cita pp. 21–30**, la paginación impresa —que
  además es la que hace cuadrar el libro con las 81 páginas que le da el
  catálogo, frente a las 86 del archivo. Verificado por el `debe_contener` de la entrada (`depressive hedonia`, que
  el pipeline exige encontrar en el recorte o aborta) y por lectura del cambio
  de capítulo en la página 35 del archivo.

- **Srnicek y Williams, *Inventing the Future*, cap. 6.** Este es el caso que
  hay que marcar con más cuidado, en la línea de lo que la contraparte de
  este README en el Módulo 1 documenta para Swarmachines y El Anti-Edipo: **el
  texto que tenemos no viene de una edición impresa.** La única fuente
  conseguida fue un EPUB, convertido a PDF para poder recortarlo por página
  con el mismo pipeline que las demás lecturas. Sus páginas 77–93 son
  **internas de este archivo** — no corresponden a la paginación de ningún
  impreso, ni siquiera aproximadamente. El temario cita pp. 107–128 de la
  edición Verso 2015 en papel; eso es lo que hay que citar en clase, no
  «pp. 77–93», que solo tiene sentido dentro de este PDF.

  El capítulo se localizó y verificó **por encabezado, no por número de
  página**: la p. 77 del archivo contiene, a media página, «Chapter 6 /
  Post-Work Imaginaries» (después de que el capítulo 5 termina con «…is
  precisely the political struggle before us.»); la p. 93 contiene, también a
  media página, «Chapter 7 / A New Common Sense» (después de que el capítulo 6
  termina con «…It is to these issues that we now turn.»). El texto es el
  mismo que el de la edición impresa; la numeración no lo es en absoluto.

Qué se versiona y qué no: los dos PDF conseguidos —los archivos completos en
`fuentes/`— están en `.gitignore` y viven solo en tu disco. Los recortes de los
capítulos (`lecturas/fisher-capitalist-realism-cap4.pdf`,
`lecturas/srnicek-williams-post-work.pdf`) y el cuadernillo que los contiene sí
están versionados, y el cuadernillo se publica en el sitio del curso.

## Sobre las dos que llegaron como texto completo

Ambas se descargaron íntegras de la fuente primaria abierta y no se recortan
— el pipeline las usa completas (`Recorte()` sin `desde`/`hasta`/`palabras_max`).

- **El manifiesto de Williams y Srnicek** son 3 814 palabras, de
  criticallegalthinking.com, publicado el 14 de mayo de 2013. El mismo texto
  se reimprimió en la antología *#Accelerate* (Urbanomic, 2014) que cita el
  Módulo 1; aquí se toma de la fuente original de los autores, no de la
  antología, así que **tampoco hay correspondencia de página con ninguna cita
  del temario que use la paginación de la antología** — es la misma clase de
  aviso que ya aplica a Marx, Swarmachines, Meltdown y la ideología
  californiana en el Módulo 1: el texto es idéntico, la numeración de página
  es la de la fuente, no la de la antología.
- **Terranova** son 5 489 palabras, de euronomade.info, y llega completa
  incluida la bibliografía final.

## Cómo se reconstruye

```bash
python3 tools/bajar_lecturas.py filosofia_ia/clase_2   # descarga y verifica
python3 tools/lecturas.py       filosofia_ia/clase_2    # recorta y maqueta
```

El descargador comprueba que cada archivo contenga lo que dice contener antes
de guardarlo. Agregar una lectura es agregar una entrada a `LECTURAS` o
`PDFS` en `tools/lecturas.py`, con su recorte (o rango de páginas) y la razón
por la que se lee.

Las fuentes de texto (`williams_srnicek_manifesto_en.txt`,
`terranova_red_stack_en.txt`) quedan en `fuentes/` tal como se descargaron,
para que el recorte sea auditable, y están versionadas. Los dos PDF en
derechos (`fisher_capitalist_realism.pdf`,
`srnicek_williams_inventing_the_future.pdf`) están en `fuentes/` pero
excluidos por `.gitignore`.

`introduccion.md` es la fuente de la introducción general del cuadernillo; la
página del curso (`course/2_filosofia_ia/2_aceleracionismo_de_izquierda/0_index.md`) es donde
vive la versión para el sitio de este módulo.
