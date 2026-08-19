# Módulo 3 — Exit, NRx & Dark Enlightenment

**Filosofía de la IA · La salida como programa político**

Cuatro lecturas, 45 páginas, entre 1 h 35 y 1 h 50. Sigue siendo el cuadernillo
más corto de la unidad: 45 páginas frente a las 53 del
[Módulo 2](../clase_2/README.md), y alrededor de la mitad de su tiempo de
lectura (1 h 35–1 h 50 frente a 3 h 30–4 h).
Cierra el arco que
abrieron los otros dos: si el Módulo 1 preguntaba **acelerar qué** y el Módulo 2
**quién lo construye**, este lee a quienes contestan que la pregunta está mal
planteada porque de la política hay que salirse.

## Cuadernillo

**[`lecturas/filosofia_ia_clase_3_cuadernillo.pdf`](lecturas/filosofia_ia_clase_3_cuadernillo.pdf)**
— **45 páginas, las cuatro lecturas**, cada una con su portadilla y la razón por
la que se lee. Tres van completas; de *Patchwork* va la segunda mitad del
capítulo, que es lo que pide el temario.

| # | Lectura | Autor | Año | Fuente | Estado |
|---|---|---|---|---|---|
| 1 | «A Formalist Manifesto» | Yarvin (como «Mencius Moldbug») | 2007 | [unqualified-reservations.org](https://www.unqualified-reservations.org/2007/04/formalist-manifesto-originally-posted/) | ✅ en el cuadernillo, completa |
| 2 | *Patchwork*, cap. 1 «A Positive Vision» | Yarvin (como «Mencius Moldbug») | 2008 | [unqualified-reservations.org](https://www.unqualified-reservations.org/2008/11/patchwork-positive-vision-part-1/) | ✅ en el cuadernillo, **segunda mitad del capítulo** |
| 3 | «The Education of a Libertarian» | Thiel | 2009 | [cato-unbound.org](https://www.cato-unbound.org/2009/04/13/peter-thiel/education-libertarian/) | ✅ en el cuadernillo, completa |
| 4 | *The Dark Enlightenment*, partes 1 y 4a | Land | 2012 | [thedarkenlightenment.com](https://www.thedarkenlightenment.com/the-dark-enlightenment-by-nick-land/) | ✅ en el cuadernillo, las dos partes completas |

**Ninguna de las cuatro llegó como PDF.** Es el primer módulo de la unidad en el
que todas las lecturas salen de la web, así que `filosofia_ia/clase_3` no tiene
entradas en `PDFS` ni en `ENLACES` de `tools/lecturas.py`, y el cuadernillo se
puede reconstruir entero en cualquier clon del repositorio, sin archivos que
vivan solo en un disco. Es también por eso que pesa 182 KB y no un megabyte: no
lleva dentro ninguna página escaneada.

### Abierto no es libre de derechos

Conviene decirlo sin rodeos, porque el encabezado de `tools/bajar_lecturas.py`
hablaba durante un tiempo solo de dominio público y este módulo no lo es:
**las cuatro lecturas siguen en derechos de sus autores.** Ninguna de las
páginas declara licencia abierta —lo comprobamos buscando `creative commons`,
`CC BY` y `licen[cs]e` en el HTML de todas ellas: nada—. Lo que hay es que las
cuatro se pueden leer gratis y completas en la web, y se reproducen aquí como
material de un curso, con la fuente al pie de cada lectura en el cuadernillo.

No es un caso nuevo del repositorio: el manifiesto de Williams y Srnicek y el
ensayo de Terranova, en el Módulo 2, están en la misma situación. Lo nuevo es
que aquí se dice. El criterio que el repositorio aplica de hecho, y que ahora
está escrito en el encabezado del descargador, es este: **se reproduce lo que
su autor o su editor publican gratis y completo en la web; lo que se vende
como edición o vive tras un muro de pago se enlaza o se recorta de un PDF que
no se versiona.** Si esa política tiene que ser más estricta, la decisión es de
quien lleva el curso, y el lugar para cambiarla es `CLAUDE.md`.

## Qué se recortó de cada fuente, y qué no

Tres de las cuatro se toman completas y lo único que se les recorta es el sitio
alrededor del texto; *Patchwork* es la excepción, y por eso va primero. Cuatro
avisos que importan al citarlas:

- **Yarvin, *Patchwork*. Es el único recorte parcial del módulo.** El temario
  pide el capítulo 1, «A Positive Vision», pp. 7–18 de la recopilación en PDF
  que circula como libro — es decir, **no el capítulo entero**, sino desde su
  página 7. El texto se toma de la entrada de blog original, del 13 de
  noviembre de 2008, que es la publicación primaria y está en abierto; el
  propio sitio la titula ya «Chapter 1: A Positive Vision | Patchwork: A
  Political System for the 21st Century», así que la numeración de capítulos no
  es un invento de la recopilación. El corte de inicio es la frase con la que
  el temario empieza («Anyway. Enough anecdotes and generalities…»), que es
  también donde el texto deja la parte publicitaria y se pone a diseñar; lo que
  queda fuera son anécdotas y un rodeo por los valores cívicos de 1911, y **la
  introducción del cuadernillo y la ficha de la lectura avisan de que empieza a
  media pieza**. El corte final es el segundo del repositorio que se apoya en
  navegación del sitio y no en una frase del texto: el capítulo termina en su
  segunda nota al pie y lo siguiente ya es la barra de capítulos. Las notas al
  pie sí van dentro.

  Una advertencia para quien cite: el capítulo **remite al capítulo 2** para
  resolver el problema con el que cierra —a dónde van los residentes que no
  pueden pagar—, y ese capítulo 2 no está en el cuadernillo. La página de la
  hora 2 de la sesión (`course/2_filosofia_ia/3_aceleracionismo_de_derecha/2_discutir_la_salida.md`)
  reproduce lo esencial de esa respuesta, verificado contra la fuente, y lo
  marca como material fuera del cuadernillo.

- **Yarvin, «A Formalist Manifesto».** Se toma la entrada completa del 24 de abril de 2007, desde su
  primera frase («The other day I was tinkering around in my garage…») hasta el
  enlace `next »` con el que el archivo del blog pasa a la entrada siguiente.
  Dos notas sobre esos dos cortes. El de inicio empezaba antes, en la línea de
  autoría del sitio (`MENCIUS MOLDBUG · APRIL 24, 2007`), y se movió: el
  cuadernillo ya pone el título en su portadilla, así que arrancar ahí lo
  imprimía dos veces, la segunda raspado del blog. La fecha no se pierde —va en
  la línea de fuente que el cuadernillo imprime al pie de la lectura—. El de
  final es uno de los dos cortes del repositorio que se apoyan en un elemento de
  navegación del sitio y no en una frase del texto —el otro es el de
  *Patchwork*, aquí arriba—; el ensayo simplemente termina y viene el enlace. Falla ruidosamente si el sitio cambia,
  que es lo que hace tolerable la dependencia.

  `unqualified-reservations.org` es el archivo estático que hoy sirve esas
  entradas; el blog se escribió en otra plataforma y Yarvin dejó de
  actualizarlo hacia 2013. La paginación no aplica: es una entrada de blog, se
  cita por fecha y título. Y es **anterior** a *Patchwork* (noviembre de 2008),
  que es la lectura siguiente de este mismo cuadernillo.

- **Thiel.** Se toma el ensayo tal como Cato Unbound lo publicó el 13 de abril
  de 2009, desde su primera línea hasta la última. **Lo que queda fuera a
  propósito es la «Editor's Note»** que Cato añadió después de esa última línea,
  con una elaboración posterior del propio Thiel sobre el pasaje del voto
  femenino. No es parte del ensayo —es un texto distinto y posterior, «Your
  Suffrage Isn't in Danger. Your Other Rights Are.»— y colarlo dentro del
  ensayo lo haría pasar por su final. Se enlaza desde la página del módulo, en
  la misma URL, en vez de reproducirse.

- **Land.** El ensayo tiene **diez partes** —1, 2, 3, 4 y las subpartes 4a a
  4f(inal); se contaron los encabezados de la propia página— y se publica entero
  en una sola URL. Aquí van dos: la parte 1 («Neo-reactionaries head for the
  exit») completa, y la parte 4a («A multi-part sub-digression into racial
  terror») completa. Se recortan por encabezado de parte, no por número de
  página: el descargador corta la parte 1 entre su título y el de la parte 2, y
  la 4a entre su título y el de la 4b. El encabezado de cada parte queda dentro
  del texto, así que en el cuadernillo se ve dónde empieza cada una — pero
  **entre las dos faltan la 2, la 3 y la 4 y el cuerpo no lo advierte**: eso lo
  dicen la introducción del cuadernillo y la ficha de la lectura, no el texto.

  **De dónde sale el texto, que no es un detalle.** *xenosystems.net*, el sitio
  donde el ensayo se publicó, ya no existe (el dominio hoy redirige a otra
  cosa). El único alojamiento completo y estable que queda es
  `thedarkenlightenment.com`, que **no es de Land**: lo mantiene un tercero que
  firma como «Charon» y que en su propia página lo describe como «little more
  than an oft-linked placeholder for three seminal NRx documents», añadiendo que
  ni Land ni Yarvin han tenido nunca participación en el sitio y que **Land
  publicó un deslinde** al respecto. El dominio está además monetizado con
  enlaces de casinos que no tienen nada que ver con el ensayo. Nada de eso afecta
  la integridad del texto —se comparó palabra por palabra contra el HTML de
  origen—, pero sí a cómo se cita: la página del módulo lo explica a los
  alumnos en vez de presentar el sitio como si fuera la publicación del autor.

  El `debe_contener` de esta fuente apunta a una frase de la **parte 4a**
  («its sub-political character: all exit and no voice»), no a una de la parte
  1. La razón es concreta: con `concatenar`, la guarda se evalúa sobre el texto
  unido, y una frase de la parte 1 tomada de su propio encabezado sería un
  subconjunto literal del ancla `desde` y no podría fallar nunca. Apuntando al
  segundo recorte, la guarda comprueba algo que las anclas no comprueban.

## Sobre la parte 4a

La parte 4a de Land discute el despido de John Derbyshire de *National Review* y
se pone del lado de Derbyshire; lee la *fuga blanca* de las ciudades
estadounidenses como un caso de salida; y trata la herencia biológica como una
de las explicaciones disponibles de las diferencias de conducta entre
poblaciones, con la que explica que unas ciudades sean seguras y otras se hayan
deteriorado. Es material sobre raza que este curso
**no comparte y no suaviza**. Se reproduce porque es fuente primaria de la posición que la unidad
estudia, y porque omitirla dejaría el módulo cómodo y falso: no es un desvío del
ensayo, es su continuación numerada, y es donde el argumento abstracto de la
salida aterriza en un caso concreto. Tanto la introducción del cuadernillo como
la página del curso lo advierten antes de que el lector llegue ahí, y las
páginas de repaso lo tratan como lo que es: un argumento que hay que poder
reconstruir para poder decir en qué paso se rompe.

## Cómo se reconstruye

```bash
python3 tools/bajar_lecturas.py filosofia_ia/clase_3   # descarga y verifica
python3 tools/lecturas.py       filosofia_ia/clase_3   # recorta y maqueta
```

El descargador comprueba que cada archivo contenga lo que dice contener antes de
guardarlo. Agregar una lectura es agregar una entrada a `LECTURAS` en
`tools/lecturas.py`, con su recorte y la razón por la que se lee.

Las cuatro fuentes (`yarvin_formalist_manifesto_en.txt`,
`yarvin_patchwork_cap1_en.txt`, `thiel_education_libertarian_en.txt`,
`land_dark_enlightenment_en.txt`) quedan en `fuentes/` tal como se descargaron,
para que el recorte sea auditable, y están versionadas.

## Un arreglo del descargador salió de este módulo, y no es inocuo

`_limpiar` pegaba toda inicial mayúscula suelta a la palabra siguiente —la regla
que convierte «T he» en «The»—, y las lecturas de aquí están escritas en
primera persona: el ensayo de Thiel empezaba «Iremain committed» y el de Yarvin,
«Idecided to build a new ideology». Ahora «I» y «A» quedan excluidos de esa
regla, por ser palabras enteras del inglés y no iniciales sueltas. El defecto era
además invisible: la misma regla que lo producía hacía que el texto ya no
calzara con el patrón de `PROHIBIDO` que debía detectarlo.

**El arreglo cambia también lo que produciría volver a descargar los módulos 1 y
2, y esos no se regeneraron.** Se comprobó corriendo el descargador de antes y el
de ahora contra las mismas páginas, en el mismo momento:

| Archivo | Con el código anterior | Con el arreglo |
|---|---|---|
| `clase_1/land_meltdown_en.txt` | `Aconvergent anti-authoritarianism` | `A convergent anti-authoritarianism` |
| `clase_1/ccru_swarmachines_en.txt` | `Apost-spectacular immersive tactility` | `A post-spectacular immersive tactility` |
| `clase_2/terranova_red_stack_en.txt` | `Iquaderni`, `Iwould`, `Acall`, `Adeeper` | separados |
| `clase_2/williams_srnicek_manifesto_en.txt` | `Avanishingly`, `Apositive`, `Aform` | separados |

Con el código anterior, los cuatro `.txt` de `clase_1` se reproducen byte a byte
desde la web; con el arreglo, dos difieren. Esas palabras pegadas **están hoy en
los cuadernillos publicados de los módulos 1 y 2**, y se quedan ahí por ahora.
Regenerarlos no es gratis: la numeración de páginas de los dos cuadernillos es la
que citan, página por página, las tablas de verificación de cinco páginas del
curso (`docs/verificacion/filosofia_ia/`), y un carácter de más puede correr un
salto de página. Cambiar dos palabras en 57 páginas no justifica rehacer y
revalidar esas tablas hoy; cuando alguno de los dos módulos se regenere por otra
razón, esto se arregla solo y hay que volver a comprobar las páginas de sus
citas.

**Y un aviso para quien lo intente:** las fuentes de `clase_2` ya **no** se
reproducen desde la web ni con el código anterior. El HTML de origen cambió
—`terranova_red_stack_en.txt` difiere en cientos de líneas— por razones ajenas a
este arreglo. Volver a descargar ese módulo no restaura nada: produce un texto
distinto.

`introduccion.md` es la fuente de la introducción general del cuadernillo; la
página del curso (`course/2_filosofia_ia/3_aceleracionismo_de_derecha/0_index.md`) es donde vive la versión
para el sitio de este módulo.
