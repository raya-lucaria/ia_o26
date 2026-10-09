"""Incrusta en la traza interactiva del arbol T los pasos de cada algoritmo.

course/7_juegos/_assets/traza_arbol_t.html es una pagina autocontenida: su
JavaScript solo pinta, no calcula nada. Los pasos que pinta salen de
juegos.pasos_interactivos(modo, variante), la misma fuente que el cuaderno de
la unidad, y este script los escribe dentro del HTML, en el bloque

    <script type="application/json" id="trazas"> ... </script>

Todo lo demas del archivo (estilo, marcado y codigo) se escribe a mano y el
script no lo toca: solo reemplaza lo que hay entre esas dos marcas. Es
idempotente: correrlo dos veces deja el archivo igual, y tras correrlo
`git status` tiene que quedar limpio si nada cambio en tools/juegos.py.

Los datos van compactados para que la pagina pese poco (sin compactar, las
ocho trazas suman unos 230 KB, casi todo el estado de cada nodo repetido en
cada paso). Se deja fuera solo un campo que la pagina no pinta, `evento`
(se lee ya en la frase); todo lo demas se guarda sin perdida:
expandir(compactar(x)) == x sin ese campo, y
tools/test_traza_web.py lo comprueba para cada modo. Lo que cambia:

- pseudo, renglones y arbol se guardan una sola vez y cada traza los nombra
  por indice (alfa-beta T y T1 comparten pseudocodigo; corte d = 1, 2, 3
  tambien; el arbol T sirve a cinco trazas).
- cada paso es un par de listas planas [campos, estado]. `campos` trae solo
  los campos que cambiaron respecto del paso anterior, como pares
  (indice en `claves` de la traza, valor); `estado`, solo los nodos que
  cambiaron, como pares (id, valor), y el valor de un nodo es
  [estado, v, alfa, beta, cota] con el estado por indice en ESTADOS.
- cada valor de esos pares es un indice en `valores`, la lista de todos los
  valores distintos de las ocho trazas (pilas, frases, «−∞»...): la misma
  pila o la misma frase se repite en varias trazas y se guarda una vez.
- n no se guarda: es la posicion del paso.

El JavaScript de la pagina hace la misma expansion que expandir() aqui.

    python3 tools/gen_traza_web.py
"""
import json
import re
import sys
from pathlib import Path

import juegos as j

RAIZ = Path(__file__).resolve().parent.parent
HTML = RAIZ / "course/7_juegos/_assets/traza_arbol_t.html"

# (clave en la pagina, modo, variante). La clave es la que usa el JavaScript;
# el fragmento de URL se traduce a ella (#alfa-beta → alfa-beta-T).
MODOS = [
    ("minimax", "minimax", None),
    ("azar", "azar", None),
    ("alfa-beta-T1", "alfa-beta", "T1"),
    ("alfa-beta-T", "alfa-beta", "T"),
    ("corte-1", "corte", 1),
    ("corte-2", "corte", 2),
    ("corte-3", "corte", 3),
    ("iterativa", "iterativa", None),
]

ESTADOS = ["pormirar", "pila", "devuelto", "evaluado", "podado"]
CLAVES_ESTADO = ["estado", "v", "alfa", "beta", "cota"]
CLAVES_NODO = ["id", "nombre", "tipo", "padre", "jugada", "hoja", "valor", "prob", "eval"]
DERIVADAS = {"n", "estado"}
FUERA = {"evento"}   # la pagina no lo pinta

ABRE = '<script type="application/json" id="trazas">'
CIERRA = "</script>"


def _indice(lista, valor):
    if valor not in lista:
        lista.append(valor)
    return lista.index(valor)


def _nodo_compacto(e):
    if sorted(e) != sorted(CLAVES_ESTADO):
        raise ValueError(f"estado de nodo con claves inesperadas: {sorted(e)}")
    return [ESTADOS.index(e["estado"]), e["v"], e["alfa"], e["beta"], 1 if e["cota"] else 0]


def compactar(trazas):
    """trazas: {clave: pasos_interactivos(...)} → el dict que va en el HTML."""
    pseudos, arboles, salida, valores_, vistos = [], [], {}, [], {}

    def interna(v):
        k = json.dumps(v, ensure_ascii=False, sort_keys=True)
        if k not in vistos:
            vistos[k] = len(valores_)
            valores_.append(v)
        return vistos[k]

    for clave, d in trazas.items():
        if sorted(d) != sorted(["arbol", "modo", "pagina", "pasos", "pseudo", "renglones",
                                "resultado", "titulo", "variante"]):
            raise ValueError(f"{clave}: claves inesperadas {sorted(d)}")
        arbol = [[n[k] for k in CLAVES_NODO] for n in d["arbol"]["nodos"]]
        if any(sorted(n) != sorted(CLAVES_NODO) for n in d["arbol"]["nodos"]):
            raise ValueError(f"{clave}: nodo del arbol con claves inesperadas")
        todas = sorted(set().union(*(p.keys() for p in d["pasos"])) - DERIVADAS)
        claves = [c for c in todas if c not in FUERA]
        pasos, antes, previos = [], {}, None
        for k, p in enumerate(d["pasos"], 1):
            if p["n"] != k:
                raise ValueError(f"{clave}, paso {k}: n no es la posicion del paso")
            if sorted(p) != sorted(todas + sorted(DERIVADAS)):
                raise ValueError(f"{clave}, paso {k}: claves distintas a las de la traza")
            cambio = []
            for i, e in p["estado"].items():
                if antes.get(i) != e:
                    cambio += [i, interna(_nodo_compacto(e))]
            antes = p["estado"]
            valores = [p[c] for c in claves]
            campos = []
            for c, v in enumerate(valores):
                if previos is None or previos[c] != v:
                    campos += [c, interna(v)]
            previos = valores
            pasos.append([campos, cambio])
        salida[clave] = {
            "modo": d["modo"], "variante": d["variante"], "titulo": d["titulo"],
            "pagina": d["pagina"], "resultado": d["resultado"],
            "pseudo": _indice(pseudos, [d["pseudo"], d["renglones"]]),
            "arbol": _indice(arboles, arbol),
            "claves": claves, "pasos": pasos,
        }
    return {"estados": ESTADOS, "claves_estado": CLAVES_ESTADO, "claves_nodo": CLAVES_NODO,
            "pseudos": pseudos, "arboles": arboles, "valores": valores_, "trazas": salida}


def expandir(datos):
    """El inverso de compactar(): {clave: pasos_interactivos(...)}."""
    res = {}
    for clave, t in datos["trazas"].items():
        pseudo, renglones = datos["pseudos"][t["pseudo"]]
        nodos = [dict(zip(datos["claves_nodo"], n)) for n in datos["arboles"][t["arbol"]]]
        val = datos["valores"]
        estado, pasos, valores = {}, [], [None] * len(t["claves"])
        for k, (campos, cambio) in enumerate(t["pasos"], 1):
            valores = list(valores)
            for c, v in zip(campos[::2], campos[1::2]):
                valores[c] = val[v]
            estado = dict(estado)
            for i, c in zip(cambio[::2], cambio[1::2]):
                e = dict(zip(datos["claves_estado"], val[c]))
                e["estado"] = datos["estados"][e["estado"]]
                e["cota"] = bool(e["cota"])
                estado[i] = e
            p = dict(zip(t["claves"], valores))
            p.update(n=k, estado=estado)
            pasos.append(p)
        res[clave] = {"modo": t["modo"], "variante": t["variante"], "titulo": t["titulo"],
                      "pagina": t["pagina"], "pseudo": pseudo, "renglones": renglones,
                      "arbol": {"nodos": nodos}, "pasos": pasos, "resultado": t["resultado"]}
    return res


def sin_fuera(trazas):
    """Las trazas tal como las devuelve juegos, sin los campos FUERA."""
    return {c: dict(d, pasos=[{k: v for k, v in p.items() if k not in FUERA}
                              for p in d["pasos"]]) for c, d in trazas.items()}


def trazas_de_hoy():
    return {clave: j.pasos_interactivos(modo, variante) for clave, modo, variante in MODOS}


def _js(valor):
    texto = json.dumps(valor, ensure_ascii=False, separators=(",", ":"))
    return texto.replace("</", "<\\/")


def serializar(datos):
    """JSON compacto, con un renglon por paso para que el diff se lea."""
    r = ["{"]
    for k in ("estados", "claves_estado", "claves_nodo"):
        r.append(f'"{k}":{_js(datos[k])},')
    r.append('"pseudos":[')
    r.append(",\n".join(_js(p) for p in datos["pseudos"]) + "],")
    r.append('"arboles":[')
    r.append(",\n".join(_js(a) for a in datos["arboles"]) + "],")
    r.append('"valores":[')
    r.append(",\n".join(_js(v) for v in datos["valores"]) + "],")
    r.append('"trazas":{')
    bloques = []
    for clave, t in datos["trazas"].items():
        cabeza = {k: v for k, v in t.items() if k != "pasos"}
        bloques.append(f"{_js(clave)}:{_js(cabeza)[:-1]},\"pasos\":[\n"
                       + ",\n".join(_js(p) for p in t["pasos"]) + "]}")
    r.append(",\n".join(bloques) + "}}")
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
    nuevo = incrustar(html, compactar(trazas_de_hoy()))
    if nuevo != html:
        HTML.write_text(nuevo, encoding="utf-8")
        print(f"actualizado {HTML.relative_to(RAIZ)} ({len(nuevo.encode())} bytes)")
    else:
        print(f"sin cambios {HTML.relative_to(RAIZ)} ({len(html.encode())} bytes)")


if __name__ == "__main__":
    sys.exit(main())
