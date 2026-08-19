# Módulo 4 — Moloch, Rationality & the Long Future

**Filosofía de la IA · El futuro como proyecto de ingeniería**

Seis lecturas, 78 páginas, entre 3 h y 3 h 30. Es el cuadernillo más largo
de la unidad: 78 páginas frente a las 57 del
[Módulo 1](../clase_1/README.md), que era el que lo era antes. Cambia de
terreno respecto de los tres anteriores: si el Módulo 1 preguntaba **acelerar
qué**, el 2 **quién lo construye** y el 3 **quién se queda**, este lee a quienes
contestan que antes de discutir la dirección hay que contar a quienes vendrán
después — y que hecha la cuenta, ella decide. La pregunta es **quién cuenta**.

## Cuadernillo

**[`lecturas/filosofia_ia_clase_4_cuadernillo.pdf`](lecturas/filosofia_ia_clase_4_cuadernillo.pdf)**
— **78 páginas, las seis lecturas**, cada una con su portadilla y la razón por
la que se lee. Cuatro van completas; del artículo de Greaves y MacAskill van las
secciones 1 a 4 y la 10, y la cuarta lectura es un apunte escrito para el curso.

| # | Lectura | Autor | Año | Fuente | Estado |
|---|---|---|---|---|---|
| 1 | «Meditations on Moloch» | Scott Alexander | 2014 | [slatestarcodex.com](https://slatestarcodex.com/2014/07/30/meditations-on-moloch/) | ✅ en el cuadernillo, completa (partes I–VIII) |
| 2 | «What Do We Mean By "Rationality"?» | Eliezer Yudkowsky | 2009 | [lesswrong.com](https://www.lesswrong.com/posts/RcZCwxFiZzE6X7nsv/what-do-we-mean-by-rationality-1) | ✅ en el cuadernillo, completa |
| 3 | «The Transhumanist Declaration» | Humanity+ | 1998/2009 | [humanityplus.org](https://www.humanityplus.org/the-transhumanist-declaration) | ✅ en el cuadernillo, las ocho proposiciones |
| 4 | «Genealogies of the Engineered Future» | Apunte del curso | 2026 | material propio | ✅ en el cuadernillo, escrito para este módulo |
| 5 | «Astronomical Waste» | Nick Bostrom | 2003 | [nickbostrom.com](https://nickbostrom.com/astronomical/waste) | ✅ en el cuadernillo, completa |
| 6 | «The Case for Strong Longtermism» | Greaves y MacAskill | 2021 | [globalprioritiesinstitute.org](https://globalprioritiesinstitute.org/wp-content/uploads/The-Case-for-Strong-Longtermism-GPI-Working-Paper-June-2021-2-2.pdf) | ✅ en el cuadernillo, **secciones 1–4 y 10** |

Como el Módulo 3, este se reconstruye entero en cualquier clon del repositorio:
no hay ninguna lectura que dependa de un PDF que viva solo en un disco, así que
`filosofia_ia/clase_4` no tiene entradas en `PDFS` ni en `ENLACES` de
`tools/lecturas.py`. El PDF del artículo de Greaves y MacAskill sí se descarga
—está en `fuentes/`, ignorado por git—, pero de él solo se conserva el texto
extraído, que sí se versiona.

### Abierto no es libre de derechos

Las seis están disponibles gratis y completas en la web, y **cinco siguen en
derechos de sus autores**; la sexta es material del curso. Ninguna de las cinco
declara licencia abierta. Se reproducen aquí como material de una clase cerrada,
con la fuente al pie de cada una, que es el mismo criterio de los módulos
anteriores: lo que su autor o su editor publican gratis y completo se reproduce;
lo que se vende como edición se enlaza. El campo `licencia` de cada `Fuente` lo
dice caso por caso.

El documento de Greaves y MacAskill es el que más se acerca a la frontera y cae
del lado abierto sin ambigüedad: es un *working paper* que el propio Global
Priorities Institute publica en su sitio para descarga libre, no una edición a
la venta.

## Dos formas de fuente nuevas, y por qué

Este módulo estrenó dos maneras de traer texto, las dos en
`tools/bajar_lecturas.py`, y las dos para material publicado en abierto:

- **`lesswrong=`** trae un ensayo por la API pública de LessWrong. El HTML del
  sitio devuelve `429 Too Many Requests` a un script, incluso a uno educado y con
  un solo intento; la API de GraphQL, que es la vía documentada, responde sin
  problema. Es la fuente canónica: el post del propio autor en su propio sitio.
- **`pdf=`** baja un PDF publicado en abierto y le saca el texto con
  `pdftotext -layout`. Toma una lista de cortes `(desde, hasta)` para poder
  sacar dos tramos del mismo archivo sin bajarlo dos veces, que es justo lo que
  pide la lectura 6. **No es la vía de los PDF de pago**: esos siguen sin
  descargarse y viven en `PDFS`, sin versionarse.

Hace falta `pdftotext` (paquete `poppler-utils`) para reconstruir este módulo.
Sin `-layout`, la extracción pega las palabras entre sí y el texto queda
inservible.

## Qué se recortó de cada fuente, y qué no

**1 · Alexander.** Completa. El corte de arriba empieza en «Allen Ginsberg's
famous poem on Moloch» y el de abajo en el pie del blog, donde empiezan el aviso
del podcast y el del NFT. Sin ese corte inferior entrarían los comentarios de la
entrada, que pesan seis veces más que el ensayo: la página cruda son 84 000
palabras y el ensayo 14 321.

**2 · Yudkowsky.** Completa, sin recorte: el post es exactamente la lectura.

**3 · La Declaración.** Completa, desde el párrafo que nombra a sus veintidós
redactores de 1998 hasta la octava proposición, que es donde termina la página.
Ese párrafo de procedencia se conserva a propósito: forma parte de lo que hay
que leer.

**5 · Bostrom.** Completa, desde el encabezado de la sección I. Se conservan las
notas al final, que son referencias.

**6 · Greaves y MacAskill.** Dos tramos: de «A striking fact about the history of
civilisation» (sección 1) hasta el encabezado de la sección 5, y luego la sección
10 completa hasta el apéndice. Quedan fuera las secciones 5 a 9 —individuos y
carrera, otras axiologías, *cluelessness*, fanatismo y la versión deóntica— y el
apéndice con la demostración. **El temario no especificaba páginas para esta
lectura**, así que el recorte es una decisión del curso: se conserva el argumento
positivo completo y sus conclusiones, y se dejan fuera las objeciones técnicas,
que no caben en una sesión de dos horas. La ficha de la lectura lo advierte, y
advierte también que la sección 10 resume secciones que el lector no vio.

Un efecto secundario del recorte que conviene conocer: al extraer el texto de un
PDF, las notas al pie caen **entre párrafos**, en el punto donde el original
cambiaba de página, y a veces parten una oración. No es un defecto reparable sin
reescribir el texto, así que se documenta en la ficha en vez de esconderse.

## Diferencias con la paginación y las fechas del temario

Tres, y ninguna es un error del temario:

- **Yudkowsky, 2012 en el temario, 2009 aquí.** El post en LessWrong es del 16 de
  marzo de 2009; 2012 es la fecha de la recopilación en libro. El cuadernillo
  cita la del post, que es de donde sale el texto.
- **Bostrom, pp. 308–314.** Es la paginación de *Utilitas* 15(3), 2003, y la
  propia página del autor la declara. El cuadernillo reproduce la versión que
  Bostrom aloja en su sitio: mismo texto, sin esos números de página.
- **Alexander, «14,955 words» en el temario.** El extracto limpio da 14 321
  palabras. La diferencia es el marcado y los pies de la página original, no
  texto faltante: van las ocho partes completas.

## La cuarta lectura la escribimos nosotros

«Genealogies of the Engineered Future» no es una fuente: es un apunte escrito
para este módulo, en español, **con ayuda de un modelo de lenguaje**, y lo dice
en su primera línea. Existe porque sin él la Declaración Transhumanista parece
caída del cielo: hay siglo y medio de esta idea antes de que llegara a un
laboratorio de IA, y ninguna de las otras cinco lecturas lo cuenta.

Recorre cinco linajes —el cosmismo ruso de Fiódorov, el extropianismo de Max
More, el singularitarianismo de Kurzweil, el cosmismo contemporáneo y el
altruismo eficaz— y de cada uno cita un fragmento breve de texto original, con
su fuente. Vive en `fuentes/apunte_genealogias_es.txt` y **no pasa por
`bajar_lecturas.py`**: no hay nada que descargar ni que verificar contra una
fuente externa, así que no tiene entrada en `FUENTES`. Si se edita, hay que
reconstruir el cuadernillo y volver a copiarlo.

## Cómo se reconstruye

```bash
python3 tools/bajar_lecturas.py filosofia_ia/clase_4   # descarga y verifica
python3 tools/lecturas.py       filosofia_ia/clase_4   # recorta y maqueta
```

Y para publicarlo, tres copias a mano —nada enlaza `lecturas/` con `course/`—:

```bash
cp lecturas/filosofia_ia/clase_4/lecturas/filosofia_ia_clase_4_cuadernillo.pdf \
   course/2_filosofia_ia/_assets/cuadernillo_modulo_4_long_future.pdf
pdftoppm -png -r 106 -f 1 -l 1 -singlefile \
   course/2_filosofia_ia/_assets/cuadernillo_modulo_4_long_future.pdf \
   course/2_filosofia_ia/_assets/cuadernillo_portada_modulo_4
python3 -m pytest tools/test_lecturas.py -q
```

La cifra de páginas aparece en seis lugares —la página del módulo, la tarea
oficial, el visor y tres veces en este README— y `test_lecturas.py` los compara
todos contra el PDF publicado. Léela del PDF ya copiado; no la estimes.

**Y no vuelvas a descargar las fuentes de los módulos 1 y 2.** El caso está
documentado en [el README del módulo 3](../clase_3/README.md): sus `.txt`
versionados ya no se reproducen desde la web, y volver a correr el descargador
sobre ellos ensucia el árbol sin arreglar nada.
