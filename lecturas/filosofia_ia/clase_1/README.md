# Clase 1 — ¿Puede pensar una máquina?

**Filosofía de la IA · La pregunta antes de la computadora**

La pregunta que Turing formula en 1950 es tres siglos más vieja que la máquina
que la volvió urgente. Estas cuatro lecturas la muestran formándose: Hobbes
define razonar como calcular, Descartes propone la prueba que ninguna máquina
pasaría, Leibniz nos hace caminar dentro del mecanismo, y La Mettrie quita la
excepción que Descartes había dejado para el alma.

Encadena con el hilo **esencia contra comportamiento** que abre la unidad de
[historia de la IA](../../../course/1_introduccion/2_historia_ia/0_index.md).

## Cuadernillo

**[`lecturas/filosofia_ia_clase_1_cuadernillo.pdf`](lecturas/filosofia_ia_clase_1_cuadernillo.pdf)**
— 25 páginas, las cuatro lecturas en un solo archivo, con su portadilla y la
razón de cada una. Todo dominio público: se puede imprimir, repartir y publicar
sin pedir permiso a nadie.

| # | Lectura | Autor | Año | Fuente |
|---|---|---|---|---|
| 1 | Leviatán, I.5 — De la razón y la ciencia | Hobbes | 1651 | [Gutenberg 3207](https://www.gutenberg.org/ebooks/3207) |
| 2 | Discurso del método, Quinta parte | Descartes | 1637 | [Wikisource ES](https://es.wikisource.org/wiki/Discurso_del_método_(Wikisource_tr.)/Quinta_parte) |
| 3 | Monadología, §17 — El argumento del molino | Leibniz | 1714 | [Wikisource EN, tr. Duncan](https://en.wikisource.org/wiki/Monadology_(Leibniz,_tr._Duncan)) |
| 4 | El hombre máquina (extracto) | La Mettrie | 1747 | [Gutenberg 52090](https://www.gutenberg.org/ebooks/52090) |

## Además, en línea

Estos dos siguen en derechos, así que **no se reproducen aquí**: se enlazan a
copias abiertas que universidades publican para sus cursos. Si prefieres
repartirlos como archivo, ese es el lugar del LMS, no de un sitio abierto.

- **Turing (1950), «Computing Machinery and Intelligence»**, *Mind* LIX(236) —
  [PDF (UMBC)](https://redirect.cs.umbc.edu/courses/471/papers/turing.pdf).
  Declara mal planteada la pregunta y la sustituye por un juego de imitación.
  Léelo justo después de Descartes: es la misma prueba del lenguaje, con el
  veredicto invertido.
- **Searle (1980), «Minds, Brains, and Programs»**, *BBS* 3(3) —
  [PDF (CSULB)](https://home.csulb.edu/~cwallis/382/readings/482/searle.minds.brains.programs.bbs.1980.pdf).
  El cuarto chino: manipular símbolos según reglas no es entender. Es el molino
  de Leibniz reescrito para la era del software.

## Cómo se reconstruye

```bash
python3 tools/bajar_lecturas.py filosofia_ia/clase_1   # descarga y verifica
python3 tools/lecturas.py       filosofia_ia/clase_1   # recorta y maqueta
```

El descargador comprueba que cada archivo contenga lo que dice contener antes de
guardarlo. No es paranoia: el ebook 17147 de Gutenberg, que parecía ser la
*Monadología*, resultó ser la *Teodicea* — la guarda lo detectó.

Agregar una lectura es agregar una entrada a `LECTURAS` en `tools/lecturas.py`,
con su recorte y la razón por la que se lee. No hay que tocar código.

## Qué se versiona y qué no

`fuentes/` guarda los textos de dominio público tal como se descargaron, para
que el recorte sea auditable. Los PDF con derechos vigentes están en
`.gitignore`: viven en tu disco para preparar clase, no en el repositorio.
