"""Incrusta en el generador de texto de la unidad 8 las tablas del Quijote.

course/8_markov/_assets/generador_texto.html es una pagina autocontenida: el
alumno elige memoria h, semilla y largo, y la pagina escribe texto con
GENERAR y MUESTREAR-FILA, simbolo por simbolo, mostrando el contexto, la fila,
el u sorteado y donde cae en la fila acumulada. Los conteos que usa son los de
markov.conteos_caracteres(h), h = 0..MEMORIA_MAX, y este script los escribe
dentro del HTML, en el bloque

    <script type="application/json" id="tablas"> ... </script>

Todo lo demas del archivo (estilo, marcado y codigo) se escribe a mano y el
script no lo toca: solo reemplaza lo que hay entre esas dos marcas. Es
idempotente; tras correrlo, `git status` tiene que quedar limpio si nada
cambio en tools/markov.py ni en el corpus.

La regla dura es la reproducibilidad: con la misma semilla, la pagina escribe
el mismo texto que markov.generar(h, largo=..., semilla=...). Para eso:

- la suerte es el Mersenne Twister de Python (random.Random), reimplementado
  en el JS como en bandido_en_vivo.html, y cada paso gasta un random();
- la fila es la misma de markov.tabla_desde_conteos: el doble
  N(contexto z)/N(contexto), sumado en el orden de markov.ALFABETO con la
  comparacion u < acumulado de markov.muestrear_fila. Python y JS usan dobles
  IEEE-754 con division y suma correctamente redondeadas, asi que las mismas
  operaciones en el mismo orden dan los mismos bits. Los conteos 0 no se
  guardan: sumar 0.0 no mueve la suma;
- un contexto que no esta en la tabla usa la fila uniforme 1/28 (Laplace con
  conteos 0), como markov.generar_desde.

Ademas el bloque lleva AUTOPRUEBA: los textos que da markov.generar con las
semillas de la pagina (SEMILLAS["generar-h"]) y LARGO_AUTOPRUEBA simbolos. La
pagina los recalcula al cargar y dice «autoprueba: ok» o un aviso visible.
tools/test_generador_markov.py compara este bloque con el archivo sin
escribir, y corre la logica JS con node contra markov.generar.

Formato de una tabla (una cadena por memoria h): los contextos en el orden de
ALFABETO, separados por «;»; cada uno son sus h simbolos y luego pares
simbolo-conteo («a123b4…»), solo conteos > 0, en el orden de ALFABETO. El
espacio se escribe «_» (ningun simbolo es cifra ni «_» ni «;», asi que el
formato no es ambiguo). Memoria 3 cabe: las cuatro tablas pesan ~82 KB.

    python3 tools/gen_generador_markov.py
"""
import json
import re
import sys
from pathlib import Path

import markov as m

RAIZ = Path(__file__).resolve().parent.parent
HTML = RAIZ / "course/8_markov/_assets/generador_texto.html"

MEMORIA_MAX = 3
LARGO_AUTOPRUEBA = 60
ESPACIO = "_"

ABRE = '<script type="application/json" id="tablas">'
CIERRA = "</script>"


def _clave(ctx):
    return [m.ALFABETO.index(c) for c in ctx]


def tabla_texto(h):
    """La tabla de memoria h en el formato compacto del docstring."""
    conteos = m.conteos_caracteres(h)
    entradas = []
    for ctx in sorted(conteos, key=_clave):
        fila = conteos[ctx]
        pares = "".join(f"{z}{fila[z]}" for z in m.ALFABETO if fila[z])
        entradas.append(f"{ctx}{pares}".replace(" ", ESPACIO))
    return ";".join(entradas)


def leer_tabla(texto, h):
    """Inversa de tabla_texto: {contexto: {simbolo: conteo}}."""
    tabla = {}
    for entrada in texto.split(";"):
        entrada = entrada.replace(ESPACIO, " ")
        ctx, resto = entrada[:h], entrada[h:]
        tabla[ctx] = {z: int(n) for z, n in re.findall(r"(\D)(\d+)", resto)}
    return tabla


def semilla(h):
    return m.SEMILLAS[f"generar-{h}"]


def autoprueba():
    """Los textos de referencia: markov.generar con la semilla de la pagina."""
    return [{"h": h, "semilla": semilla(h), "largo": LARGO_AUTOPRUEBA,
             "texto": m.generar(h, largo=LARGO_AUTOPRUEBA, semilla=semilla(h))}
            for h in range(MEMORIA_MAX + 1)]


def _js(valor):
    return json.dumps(valor, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def serializar():
    """JSON del bloque, con un renglon por tabla y por texto de autoprueba."""
    r = ["{", f'"alfabeto":{_js(m.ALFABETO)},',
         f'"contexto_inicial":{_js(m.CONTEXTO_INICIAL)},', '"tablas":[']
    r.append(",\n".join(_js(tabla_texto(h)) for h in range(MEMORIA_MAX + 1)) + "],")
    r.append('"autoprueba":[')
    r.append(",\n".join(_js(e) for e in autoprueba()) + "]")
    r.append("}")
    return "\n".join(r)


def bloque_incrustado(html):
    """El texto entre las dos marcas, tal como esta en el archivo."""
    mm = re.search(re.escape(ABRE) + r"\n(.*?)\n" + re.escape(CIERRA), html, re.S)
    if not mm:
        raise ValueError(f"no se encontro el bloque {ABRE} ... {CIERRA}")
    return mm.group(1)


def incrustar(html, bloque):
    viejo = bloque_incrustado(html)
    return html.replace(f"{ABRE}\n{viejo}\n{CIERRA}", f"{ABRE}\n{bloque}\n{CIERRA}", 1)


def contenido():
    """El HTML como debe quedar hoy: el de disco con el bloque de datos al dia."""
    return incrustar(HTML.read_text(encoding="utf-8"), serializar())


def main():
    html = HTML.read_text(encoding="utf-8")
    nuevo = contenido()
    if nuevo != html:
        HTML.write_text(nuevo, encoding="utf-8")
        print(f"actualizado {HTML.relative_to(RAIZ)} ({len(nuevo.encode())} bytes)")
    else:
        print(f"sin cambios {HTML.relative_to(RAIZ)} ({len(html.encode())} bytes)")


if __name__ == "__main__":
    sys.exit(main())
