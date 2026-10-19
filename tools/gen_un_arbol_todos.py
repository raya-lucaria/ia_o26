"""Incrusta en «El mismo árbol, todos los algoritmos» los datos del árbol de resultados.

course/7_juegos/_assets/un_arbol_todos.html es una pagina autocontenida: su
JavaScript solo pinta, no calcula ni sortea nada. Muestra los siete metodos
de la radiografia (minimax, alfa-beta, expectiminimax con el dado en D, el
corte con quietud e iterativa, Monte Carlo plano, Monte Carlo con
actualizacion minimax y UCT). Todo lo que muestra -que nodos miro cada
algoritmo, cuales podo, que jugada elige, el valor de la raiz y su tipo, las
corridas de Monte Carlo con la semilla de la pagina, y la tabla resumen-
sale de juegos.datos_interactivo_tpm() mas la corrida de juegos.mc_minimax
(datos_mmmc(), aqui: juegos.py no la trae en ese paquete), y este script lo
escribe dentro del HTML, en el bloque

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


CLAVE_MMMC = "actualización minimax"
# La fila de la tabla es la corrida de la radiografía (jue-c3-cmp-resultados):
# 10 partidas, 11 estados guardados, raíz aún provisional. El deslizador sigue
# llegando a VUELTAS_PAGINA_TPM, el presupuesto de UCT.
PARTIDAS_FILA_MMMC = j.ITERACIONES_MMMC_TPM
FILA_MMMC = f"actualización minimax, {PARTIDAS_FILA_MMMC} partidas"
GARANTIZA_MMMC = ("No (en un árbol finito, con todas las jugadas, finales reales y partidas "
                  "sin límite, converge a él)")

# «¿Garantiza V?» con la convención de la radiografía (plan §5.1): el corte que
# alcanza todos los finales da M·V, no V; UCT converge con sus condiciones
# completas. juegos.GARANTIZA_TPM conserva los textos viejos (los fija
# test_juegos.py); aquí se homologan para lo que ve el alumno.
GARANTIZA_HOMOLOGADA = {
    "No, salvo si llega a los finales":
        "No; si llega a todos los finales, da M·V (aquí M = 100)",
    "No, salvo si llega a los finales antes de cortar":
        "No; si llega a todos los finales antes de activar la quietud, da M·V (aquí M = 100)",
    "No (con tiempo sin límite converge a él, con cualquier c > 0)":
        "No (en un árbol finito, con c > 0 fija y vueltas sin límite, converge a él)",
}

# El orden de la radiografia (plan §5.2): la tabla de la pagina va asi, no en
# el de tabla_t_pm(), que pone expectiminimax antes que alfa-beta.
ORDEN_FAMILIAS = ("minimax", "alfa-beta", "expectiminimax", "corte", "quietud",
                  "profundización iterativa", "Monte Carlo plano", "actualización minimax", "UCT")


def _familia(algoritmo):
    return next(f for f in sorted(ORDEN_FAMILIAS, key=len, reverse=True)
                if algoritmo.startswith(f))


def datos_mmmc(arbol=j.ARBOL_TPM, partidas=j.VUELTAS_PAGINA_TPM, semilla=j.SEMILLA_TPM):
    """La corrida de Monte Carlo con actualizacion minimax del interactivo:
    juegos.mc_minimax con la semilla y el presupuesto de UCT (los tres Monte
    Carlo se comparan con las mismas partidas). Tras cada partida t, lo que
    hay guardado: {id: [N, V̂, exacto]} (V̂ como texto, «1/3»), Q̂ de cada
    jugada de la raiz (None = sin visitar), la jugada que entregaria y el
    camino y U de esa partida. mc_minimax con t partidas repite las primeras
    t de la corrida larga (misma semilla), asi que cada foto es una corrida
    real, no una reconstruccion."""
    ids = j.ids_tpm(arbol)
    s = lambda x: None if x is None else (j.fmt_t(x) if isinstance(x, j.F) else x)
    larga = j.mc_minimax(arbol, partidas, semilla)
    por_partida = []
    for t in range(1, partidas + 1):
        r = j.mc_minimax(arbol, t, semilla)
        por_partida.append({ids[c]: [r["N"][c], s(r["V"][c]), r["exacto"][c]]
                            for c in sorted(r["V"], key=lambda c: (len(c), c))})
    return dict(semilla=semilla,
                caminos=[[ids[h["camino"][:k]] for k in range(1, len(h["camino"]) + 1)]
                         for h in larga["historia"]],
                U=[h["U"] for h in larga["historia"]],
                Q=[[s(q) for q in h["Q"]] for h in larga["historia"]],
                jugada=[j.JUGADAS_RAIZ[h["jugada"]] for h in larga["historia"]],
                por_partida=por_partida)


def fila_mmmc(arbol=j.ARBOL_TPM, partidas=PARTIDAS_FILA_MMMC, semilla=j.SEMILLA_TPM):
    """Su fila de la tabla, con los campos de tabla_t_pm(): valor = Q̂ de la
    jugada entregada; nodos = los estados que guardo; da_v_aqui = si ese
    numero es V (0 en el arbol de resultados)."""
    r = j.mc_minimax(arbol, partidas, semilla)
    v = j.minimax_tpm(arbol)[1]
    q = r["Q"][r["jugada"]]
    exacta = r["exacto"][()]
    return dict(algoritmo=FILA_MMMC, jugada=j.JUGADAS_RAIZ[r["jugada"]],
                valor=j.fmt_t(q) if isinstance(q, j.F) else q, tipo="Q̂", escala="U",
                nodos=len(r["V"]), simulaciones=partidas, garantiza=GARANTIZA_MMMC,
                da_v_aqui=q == v,
                nota="raíz exacta: ya descubrió lo que decide" if exacta else "raíz provisional")


# juegos.py aun rotula con la notacion vieja (plan §5.1): un promedio es «ū»
# y el limite de Monte Carlo plano, «μ». La pagina dice Q̂ y Q_azar.
NOTACION = {"ū": "Q̂", "μ": "Q_azar"}


def _homologar(texto):
    for viejo, nuevo in NOTACION.items():
        texto = texto.replace(viejo, nuevo)
    return texto


def garantiza(texto):
    """El «¿Garantiza V?» de una fila, con la convención de la radiografía."""
    return GARANTIZA_HOMOLOGADA.get(texto, texto)


def datos_de_hoy():
    """juegos.datos_interactivo_tpm() con la actualizacion minimax agregada,
    la tabla en el orden de la radiografia y la notacion de §5.1 (Q̂ por ū,
    Q_azar por μ; «¿Garantiza V?» con M·V y condiciones completas) en los
    textos que trae la fuente."""
    d = j.datos_interactivo_tpm()
    d["tabla"] = [dict(f, tipo=_homologar(f["tipo"]), nota=_homologar(f["nota"]),
                       garantiza=garantiza(f["garantiza"])) for f in d["tabla"]]
    mc = d["algoritmos"]["Monte Carlo plano"]
    limite = mc["limite"]
    mc["limite"] = dict(jugada=limite["jugada"], q_azar=limite["mu"])
    algs = dict(d["algoritmos"])
    algs[CLAVE_MMMC] = datos_mmmc()
    d["algoritmos"] = {k: algs[k] for k in sorted(algs, key=lambda k: ORDEN_FAMILIAS.index(_familia(k)))}
    tabla = d["tabla"] + [fila_mmmc()]
    d["tabla"] = sorted(tabla, key=lambda f: ORDEN_FAMILIAS.index(_familia(f["algoritmo"])))
    return d


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
