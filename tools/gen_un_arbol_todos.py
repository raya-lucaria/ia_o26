"""Incrusta en «El mismo árbol, todos los algoritmos» los datos de T±.

course/7_juegos/_assets/un_arbol_todos.html es una pagina autocontenida: su
JavaScript solo pinta, no calcula ni sortea nada. Todo lo que muestra -que
nodos miro cada algoritmo, cuales podo, que jugada elige, el valor de la
raiz y su tipo, las corridas de Monte Carlo plano y de UCT con la semilla de
la pagina, y la tabla resumen- sale de juegos.datos_interactivo_tpm(), y este
script lo escribe dentro del HTML, en el bloque

    <script type="application/json" id="datos"> ... </script>

El navegador no muestra ese bloque (no es un comentario HTML ni texto de la
pagina). Todo lo demas del archivo (estilo, marcado y codigo) se escribe a
mano y el script no lo toca: solo reemplaza lo que hay entre esas dos
marcas. Es idempotente, y tras correrlo `git status` tiene que quedar limpio
si nada cambio en tools/juegos.py. tools/test_un_arbol_todos.py compara el
bloque comiteado con el que daria hoy la fuente, sin escribir.

    python3 tools/gen_un_arbol_todos.py
"""
import json
import re
import sys
from pathlib import Path

import juegos as j

RAIZ = Path(__file__).resolve().parent.parent
HTML = RAIZ / "course/7_juegos/_assets/un_arbol_todos.html"

ABRE = '<script type="application/json" id="datos">'
CIERRA = "</script>"


def datos_de_hoy():
    return j.datos_interactivo_tpm()


def _js(valor):
    texto = json.dumps(valor, ensure_ascii=False, separators=(",", ":"))
    return texto.replace("</", "<\\/")


def serializar(datos):
    """JSON compacto, un renglon por nodo, por algoritmo y por fila de la
    tabla, para que el diff se lea."""
    r = ["{", '"nodos":[', ",\n".join(_js(n) for n in datos["nodos"]) + "],",
         f'"jugadas_raiz":{_js(datos["jugadas_raiz"])},', '"algoritmos":{']
    r.append(",\n".join(f"{_js(k)}:{_js(v)}" for k, v in datos["algoritmos"].items()) + "},")
    r.append('"tabla":[')
    r.append(",\n".join(_js(f) for f in datos["tabla"]) + "]}")
    resto = set(datos) - {"nodos", "jugadas_raiz", "algoritmos", "tabla"}
    if resto:
        raise ValueError(f"claves que serializar() no conoce: {sorted(resto)}")
    return "\n".join(r)


def bloque_incrustado(html):
    """El texto entre las dos marcas, tal como esta en el archivo."""
    m = re.search(re.escape(ABRE) + r"\n(.*?)\n" + re.escape(CIERRA), html, re.S)
    if not m:
        raise ValueError(f"no se encontro el bloque {ABRE} ... {CIERRA}")
    return m.group(1)


def incrustar(html, datos):
    viejo = bloque_incrustado(html)
    return html.replace(f"{ABRE}\n{viejo}\n{CIERRA}", f"{ABRE}\n{serializar(datos)}\n{CIERRA}", 1)


def main():
    html = HTML.read_text(encoding="utf-8")
    nuevo = incrustar(html, datos_de_hoy())
    if nuevo != html:
        HTML.write_text(nuevo, encoding="utf-8")
        print(f"actualizado {HTML.relative_to(RAIZ)} ({len(nuevo.encode())} bytes)")
    else:
        print(f"sin cambios {HTML.relative_to(RAIZ)} ({len(html.encode())} bytes)")


if __name__ == "__main__":
    sys.exit(main())
