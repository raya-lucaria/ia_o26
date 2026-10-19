# Corpus: *Don Quijote de la Mancha* (corte versionado)

`quijote.txt` es el texto que usa la unidad 8 (cadenas de Markov): cada cifra
del corpus que citan las páginas de `course/8_markov/` sale de este archivo
exacto, vía `tools/markov.py` (`cargar_corpus()`), y `tools/test_markov.py`
fija su SHA-256.

## Fuente

- **Obra:** Miguel de Cervantes Saavedra, *Don Quijote de la Mancha* (las dos
  partes).
- **Transcripción:** Project Gutenberg, libro #2000, acreditada a «an anonymous
  Project Gutenberg volunteer and Joaquin Cuenca Abela».
- **URL descargada:** https://www.gutenberg.org/cache/epub/2000/pg2000.txt
  (ficha: https://www.gutenberg.org/ebooks/2000).
- **Fecha de descarga:** 2026-10-18.
- **SHA-256 del original descargado** (UTF-8, fin de línea CRLF, 2 225 803 bytes):
  `534f41d59f7142163fa0964076ac6351845c006ea6433778be637fac6d5b04d7`

## Corte

Se conserva desde la primera línea que empieza con «Capítulo primero» hasta la
línea anterior a la que empieza con `*** END OF THE PROJECT GUTENBERG EBOOK`,
ambas buscadas en el original con el fin de línea ya normalizado a `\n`.

- **Primera línea conservada** (línea 1 069 del original):
  `Capítulo primero. Que trata de la condición y ejercicio del famoso hidalgo`
- **Línea de corte** (línea 37 709 del original; no se conserva, ni nada
  después):
  `*** END OF THE PROJECT GUTENBERG EBOOK DON QUIJOTE ***`

Se quitan así la cabecera y la licencia de Gutenberg y el paratexto inicial de
la primera parte (tasa, erratas, privilegio, dedicatoria, prólogo y versos
preliminares). Los títulos de capítulo y de parte se quedan. Las líneas
conservadas no se tocan: se unen con `\n` y el archivo termina en un `\n`
(los renglones en blanco previos a la línea de corte se quedan).

- **Codificación:** UTF-8 sin BOM; fin de línea `\n`.
- **SHA-256 del corte:**
  `7e40231809f16318113cbefbf58a8c271857c2e84b95260c6ff083927c657e92`
- **Tamaño:** 2 128 659 bytes, 36 640 líneas (bajo el tope de 12 MB por
  archivo de `tools/test_aceptacion.py`).
- **Comprobaciones:** ninguna mención a «Gutenberg» en el corte; contiene la
  frase ancla «En un lugar de la Mancha, de cuyo nombre no quiero acordarme» y
  la frase de la clase 1, «— Con la iglesia hemos dado, Sancho.» (segunda
  parte, capítulo IX).

Para rehacer el corte:

```python
raw = open("pg2000.txt", "rb").read().decode("utf-8")
lineas = raw.replace("\r\n", "\n").split("\n")
i = next(k for k, l in enumerate(lineas) if l.startswith("Capítulo primero"))
j = next(k for k, l in enumerate(lineas)
         if l.startswith("*** END OF THE PROJECT GUTENBERG EBOOK"))
open("quijote.txt", "w", encoding="utf-8", newline="\n").write(
    "\n".join(lineas[i:j]) + "\n")
```

## Derechos

- **La obra es de dominio público:** Cervantes murió en 1616.
- **La transcripción:** Project Gutenberg la publica como libro de dominio
  público en Estados Unidos: su cabecera es la de esos libros («This eBook is
  for the use of anyone anywhere in the United States and most other parts of
  the world at no cost and with almost no restrictions whatsoever»), sin aviso
  de derechos, y no es una edición crítica moderna con derechos propios.
- **Licencia de Project Gutenberg** (§1.C del pie del original): para una obra
  sin protección de derechos en Estados Unidos, no impide copiarla ni hacer
  obras derivadas «as long as all references to Project Gutenberg are
  removed» (https://www.gutenberg.org/policy/license.html). Por eso el corte
  no conserva la cabecera, el pie ni ninguna otra mención al proyecto; la
  procedencia queda registrada solo en este README.

## Normalizaciones (en `tools/markov.py`, no en el archivo)

El archivo se versiona tal cual; las normalizaciones las aplica el código:
`normalizar_vc` (solo letras a–z y ñ, vocales con diacrítico fundidas, sin
espacios: 1 620 532 letras), `normalizar_caracteres` (lo mismo con un espacio
entre palabras: 28 símbolos, 1 997 128 caracteres) y `normalizar_palabras`
(376 597 palabras, 22 164 distintas).
