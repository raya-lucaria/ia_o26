"""«El mismo árbol, todos los algoritmos» muestra lo que juegos.py da hoy.

course/7_juegos/_assets/un_arbol_todos.html lleva incrustado, en
<script type="application/json" id="datos">, el JSON que tools/gen_un_arbol_todos.py
escribe desde juegos.datos_interactivo_tpm() más la corrida de
juegos.mc_minimax (gen_un_arbol_todos.datos_de_hoy()). Esta prueba NO
regenera: compara el bloque comiteado con el que daría hoy la fuente, así que
cambiar juegos.py sin volver a correr el generador falla aquí.

Los siete métodos de la radiografía (minimax, alfa-beta, expectiminimax con
el dado en D, el corte con quietud e iterativa, Monte Carlo plano, la
actualización minimax y UCT) tienen cada uno su botón, y el texto visible usa
la notación de la homologación (§5.1): «árbol de resultados», Q̂, V̂, Q_azar,
N(s,a); nada de μ, ū, T±, G/N ni N(s′).

Además: cada variante del selector apunta a un algoritmo que existe en el
JSON y a una fila de la tabla; la tabla incrustada tiene las cifras de
tabla_t_pm() (y la de la actualización minimax, las de mc_minimax); la página no carga nada de fuera, copia la paleta del skin, no
usa text-transform ni comentarios HTML, y pesa menos de TOPE_BYTES. Con
Chrome disponible (se salta sin él, como en CI), abre la página en varios
fragmentos y lee la tarjeta y la tabla que pintó el JavaScript.
"""
import json
import re
import shutil
import subprocess
from html import unescape as html_unescape
from html.parser import HTMLParser

import pytest

import gen_un_arbol_todos as g
import juegos as j

HTML = g.HTML
TOPE_BYTES = 150_000


@pytest.fixture(scope="module")
def html():
    return HTML.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def datos(html):
    return json.loads(g.bloque_incrustado(html))


def test_el_bloque_incrustado_es_el_que_daria_hoy_la_fuente(html):
    assert g.bloque_incrustado(html) == g.serializar(g.datos_de_hoy()), (
        "el JSON de un_arbol_todos.html ya no coincide con gen_un_arbol_todos.datos_de_hoy(): "
        "corre python3 tools/gen_un_arbol_todos.py y comitea el HTML")


def test_el_generador_es_idempotente(html):
    d = g.datos_de_hoy()
    una = g.incrustar(html, d)
    assert g.incrustar(una, d) == una


def _variantes(html):
    return [dict(re.findall(r'data-([\w-]+)="([^"]*)"', m))
            for m in re.findall(r"<(?:button|span)[^>]*\sdata-v=[^>]*>", html)]


def test_cada_variante_del_selector_existe_en_los_datos(html, datos):
    vs = _variantes(html)
    filas = {f["algoritmo"] for f in datos["tabla"]}
    assert len(vs) == 16
    assert len({v["v"] for v in vs}) == len(vs), "fragmentos repetidos"
    for v in vs:
        assert v["clave"] in datos["algoritmos"], v
        assert v["fila"] in filas, v
        assert v.get("nombre"), v
        if "k" in v:
            assert v["k"] in datos["algoritmos"]["Monte Carlo plano"]["corridas"], v
        if "iter" in v:
            assert int(v["iter"]) < len(datos["algoritmos"][v["clave"]]), v
    # y todo algoritmo de los datos tiene al menos un botón
    assert {v["clave"] for v in vs} == set(datos["algoritmos"])
    assert {v["k"] for v in vs if "k" in v} == {str(k) for k in j.SIMS_MC_TPM}


SIETE = [("minimax", "Minimax"), ("alfa-beta", "Alfa-beta"), ("dado", "Expectiminimax (dado en D)"),
         ("corte", "Minimax con corte"), ("mc", "Monte Carlo plano"),
         ("mmmc", "Monte Carlo con actualización minimax"),
         ("uct", "UCT")]


def test_cada_familia_tiene_su_boton_y_sus_variantes(html):
    familias = re.findall(r'data-familia="([\w-]+)"', html)
    grupos = re.findall(r'class="variantes" data-de="([\w-]+)"', html)
    assert familias and sorted(familias) == sorted(grupos)


def test_los_siete_metodos_de_la_radiografia_en_su_orden(html):
    """Siete botones, en el orden de las fichas; quietud e iterativa son
    variantes del corte, no familias aparte."""
    botones = re.findall(r'<button type="button" data-familia="([\w-]+)">([^<]+)</button>', html)
    assert botones == SIETE
    corte = re.search(r'class="variantes" data-de="corte".*?\n    </div>\n', html, re.S).group(0)
    for v in ("corte-d1", "corte-d2", "corte-d3", "quietud", "iterativa-d1", "iterativa-d2",
              "iterativa-d3"):
        assert f'data-v="{v}"' in corte, v


def test_la_tabla_incrustada_tiene_las_cifras_de_tabla_t_pm(datos):
    """Las filas de tabla_t_pm() con sus cifras, en el orden de la
    radiografía y con «ū» rotulado Q̂; más la de la actualización minimax."""
    esperado = {e["algoritmo"]: e for e in j.tabla_t_pm()}
    orden = [f["algoritmo"] for f in datos["tabla"]]
    assert set(orden) == set(esperado) | {g.FILA_MMMC}
    assert sorted(orden, key=lambda a: g.ORDEN_FAMILIAS.index(g._familia(a))) == orden
    assert orden.index("alfa-beta, orden al revés") < orden.index("expectiminimax, D es un dado")
    assert orden[-2:] == [g.FILA_MMMC, "UCT, c = 1, 40 vueltas"]
    for f in datos["tabla"]:
        if f["algoritmo"] == g.FILA_MMMC:
            continue
        e = esperado[f["algoritmo"]]
        assert f["jugada"] == e["jugada"], f["algoritmo"]
        assert f["valor"] == (j.fmt_t(e["valor"]) if isinstance(e["valor"], j.F) else e["valor"])
        tipo = "Q̂" if e["tipo"] == "ū" else e["tipo"]
        assert (f["tipo"], f["escala"], f["nodos"], f["garantiza"], f["da_v_aqui"]) == \
               (tipo, e["escala"], e["nodos"], g.garantiza(e["garantiza"]),
                e["da_v_aqui"]), f["algoritmo"]


def test_la_actualizacion_minimax_es_la_de_mc_minimax(datos):
    """Cada foto del deslizador es mc_minimax con t partidas (semilla 0); la
    fila de la tabla, la de la radiografía (10 partidas): centro, Q̂ = 0 = V,
    11 estados guardados, raíz aún provisional."""
    m = datos["algoritmos"][g.CLAVE_MMMC]
    ids = j.ids_tpm()
    assert len(m["por_partida"]) == j.VUELTAS_PAGINA_TPM
    for t in (1, 10, 17, 40):
        r = j.mc_minimax(j.ARBOL_TPM, t, j.SEMILLA_TPM)
        assert m["por_partida"][t - 1] == {ids[c]: [r["N"][c], r["V"][c], r["exacto"][c]]
                                           for c in r["V"]}, t
        assert m["jugada"][t - 1] == j.JUGADAS_RAIZ[r["jugada"]]
        assert m["Q"][t - 1] == r["Q"]
    assert m["Q"][9] == [None, 0, -1] and len(m["por_partida"][9]) == 11
    fila = next(f for f in datos["tabla"] if f["algoritmo"] == g.FILA_MMMC)
    assert g.FILA_MMMC == f"actualización minimax, {j.ITERACIONES_MMMC_TPM} partidas"
    assert (fila["jugada"], fila["valor"], fila["nodos"], fila["da_v_aqui"]) == ("centro", 0, 11, True)
    assert fila["nota"] == "raíz provisional"
    assert fila["garantiza"] == g.GARANTIZA_MMMC


def test_los_nodos_mirados_coinciden_con_la_cuenta_de_la_tabla(datos):
    """La tarjeta cuenta los nodos iluminados; la tabla, los generados."""
    a, filas = datos["algoritmos"], {f["algoritmo"]: f for f in datos["tabla"]}
    pares = [("minimax", "minimax"), ("alfa-beta, dado", "alfa-beta, orden dado"),
             ("alfa-beta, al revés", "alfa-beta, orden al revés"),
             ("quietud d = 1", "quietud, d = 1")] + \
            [(f"corte d = {d}", f"corte d = {d}") for d in (1, 2, 3)]
    for clave, fila in pares:
        assert len(a[clave]["visitados"]) == filas[fila]["nodos"], clave
    it = a["profundización iterativa"]
    assert [len(x["visitados"]) for x in it] == [x["nodos"] for x in it]
    assert sum(x["nodos"] for x in it) == filas["profundización iterativa, d = 1, 2, 3"]["nodos"]


def test_la_corrida_de_uct_cuadra_consigo_misma(datos):
    """La página reconstruye N en cada vuelta contando los caminos: al final
    tiene que dar los N que guarda la corrida."""
    u = datos["algoritmos"]["UCT"]
    assert len(u["caminos"]) == len(u["mas_simulada"]) == j.VUELTAS_PAGINA_TPM
    n = {"R": len(u["caminos"])}
    for cm in u["caminos"]:
        for x in cm:
            n[x] = n.get(x, 0) + 1
    assert n == u["N"]
    assert re.search(r'id="vuelta" min="1" max="40"', HTML.read_text(encoding="utf-8"))


def test_forma_paleta_y_accesibilidad(html):
    assert '<html lang="es">' in html
    assert re.search(r"<title>[^<]+</title>", html)
    assert 'name="viewport"' in html
    assert re.search(r":root\s*\{[^}]*--surface:#211033", html), "sin la paleta del skin en :root"
    assert 'aria-live="polite"' in html
    for ident in re.findall(r'<(?:input|select)[^>]*\sid="([^"]+)"', html):
        assert re.search(rf'<label[^>]*for="{ident}"', html), f"#{ident} sin <label for>"


def test_sin_text_transform_ni_comentarios_html(html):
    assert "text-transform" not in html, "convierte N(s′) en N(S′)"
    assert "<!--" not in html


def test_no_carga_nada_de_fuera(html):
    assert not re.search(r"""(?:src|href)\s*=\s*["']?\s*(?:https?:)?//""", html, re.I)
    assert not re.search(r"@import|url\(\s*['\"]?(?:https?:)?//", html, re.I)
    assert not re.search(r"<script[^>]*\ssrc=", html, re.I)
    assert not re.search(r"<link[^>]*stylesheet", html, re.I)
    for x in ("cdn", "unpkg", "jsdelivr", "googleapis", "fetch(", "XMLHttpRequest"):
        assert x not in html, x


def test_nada_de_azar_en_el_navegador(html):
    assert "Math.random" not in html and "crypto" not in html


def test_pesa_menos_que_el_tope(html):
    peso = len(html.encode("utf-8"))
    assert peso < TOPE_BYTES, f"un_arbol_todos.html pesa {peso} bytes (tope {TOPE_BYTES})"


# ------------------------------------------------- con un navegador ---

NAVEGADOR = next((shutil.which(n) for n in ("google-chrome", "google-chrome-stable",
                                            "chromium", "chromium-browser", "chrome")
                  if shutil.which(n)), None)


def _dom(fragmento):
    if not NAVEGADOR:
        pytest.skip("no hay Chrome/Chromium")
    salida = subprocess.run(
        [NAVEGADOR, "--headless=new", "--disable-gpu", "--no-sandbox", "--dump-dom",
         f"{HTML.as_uri()}#{fragmento}"], capture_output=True, text=True, timeout=60, check=True)
    return salida.stdout


class _Texto(HTMLParser):
    """El texto de cada elemento con id, y las filas de la tabla."""
    def __init__(self):
        super().__init__()
        self.pila, self.por_id, self.filas = [], {}, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.pila.append((tag, a.get("id")))
        if tag == "tr" and "data-algoritmo" in a:
            self.filas.append([a["data-algoritmo"]])
        if tag == "td" and self.filas and any(t == "tbody" for t, _ in self.pila):
            self.filas[-1].append("")

    def handle_endtag(self, tag):
        while self.pila:
            t, _ = self.pila.pop()
            if t == tag:
                break

    def handle_data(self, data):
        for _, i in self.pila:
            if i:
                self.por_id[i] = self.por_id.get(i, "") + data
        if self.filas and any(t == "td" for t, _ in self.pila) and len(self.filas[-1]) > 1:
            self.filas[-1][-1] += data


def _leer(fragmento):
    p = _Texto()
    p.feed(_dom(fragmento))
    return p


def _norm(s):
    return re.sub(r"\s+", " ", s).strip()


# «¿Garantiza V?» y «¿y aquí da V?» vienen de tabla_t_pm() (campos
# `garantiza` y `da_v_aqui`); la página no los deduce. La tabla pintada solo
# abrevia tres textos para caber a 390 px (ABREVIA del JavaScript).
ABREVIA = {
    "Sí, el V del juego con dado": "Sí, el del juego con dado",
    "No; si llega a todos los finales, da M·V (aquí M = 100)": "No; con finales, M·V",
    "No; si llega a todos los finales antes de activar la quietud, da M·V (aquí M = 100)":
        "No; con finales, M·V",
    "No (en un árbol finito, con c > 0 fija y vueltas sin límite, converge a él)": "No; converge",
    g.GARANTIZA_MMMC: "No; converge",
}

# (fragmento, jugada, valor de la raíz, nodos mirados, ¿garantiza V?, ¿y aquí da V?)
CASOS = [
    ("minimax", "centro", "0", "15 de 15", "Sí", "sí"),
    ("alfa-beta-dado", "centro", "0", "12 de 15", "Sí, en la raíz", "sí"),
    ("alfa-beta-al-reves", "centro", "0", "14 de 15", "Sí, en la raíz", "sí"),
    ("dado", "der", "1/3", "15 de 15", "Sí, el V del juego con dado", "sí: 1/3 es el V del juego con dado"),
    ("corte-d1", "izq", "60", "4 de 15", "No; si llega a todos los finales, da M·V (aquí M = 100)", "no"),
    ("corte-d2", "centro", "10", "11 de 15", "No; si llega a todos los finales, da M·V (aquí M = 100)", "no"),
    ("corte-d3", "centro", "0", "15 de 15", "No; si llega a todos los finales, da M·V (aquí M = 100)", "sí: 0 = 100·V (M·V con M = 100), porque esta vez llegó a los finales en todas sus ramas"),
    ("quietud", "centro", "20", "5 de 15", "No; si llega a todos los finales antes de activar la quietud, da M·V (aquí M = 100)", "no"),
    ("iterativa-d1", "izq", "60", "4 de 15", "No; si llega a todos los finales, da M·V (aquí M = 100)", "no"),
    ("iterativa-d3", "centro", "0", "12 de 15", "No; si llega a todos los finales, da M·V (aquí M = 100)", "sí: 0 = 100·V (M·V con M = 100), porque esta vez llegó a los finales en todas las ramas que no podó"),
    ("mc-5", "der", "3/5", "15 de 15", "No", "no"),
    ("mc-50", "der", "12/25", "15 de 15", "No", "no"),
    ("uct", "centro", "0", "15 de 15", "No (en un árbol finito, con c > 0 fija y vueltas sin límite, converge a él)", "sí, por casualidad"),
    ("uct-18", "centro", "−1/7", "14 de 15", "No (en un árbol finito, con c > 0 fija y vueltas sin límite, converge a él)", "no"),
    ("mmmc", "centro", "0", "11 de 15", "No (en un árbol finito, con todas las jugadas, finales reales y partidas sin límite, converge a él)", "sí, por ahora"),
    ("mmmc-10", "centro", "0", "11 de 15", "No (en un árbol finito, con todas las jugadas, finales reales y partidas sin límite, converge a él)", "sí, por ahora"),
    ("mmmc-40", "centro", "0", "15 de 15", "No (en un árbol finito, con todas las jugadas, finales reales y partidas sin límite, converge a él)", "sí: 0 es V, y ya es exacto"),
]


@pytest.mark.parametrize("frag, jugada, valor, nodos, garantiza, aqui", CASOS, ids=[c[0] for c in CASOS])
def test_la_tarjeta_dice_lo_que_dicen_los_datos(frag, jugada, valor, nodos, garantiza, aqui):
    t = {k: _norm(v) for k, v in _leer(frag).por_id.items()}
    assert t["t-jugada"].startswith(jugada), t["t-jugada"]
    assert t["t-valor"].split()[0] == valor, t["t-valor"]
    assert t["t-nodos"].startswith(nodos), t["t-nodos"]
    assert t["t-garantiza"] == garantiza, t["t-garantiza"]
    assert t["t-aqui"].startswith(aqui), t["t-aqui"]
    assert ("✓" in t["t-jugada"]) == (jugada == j.minimax_tpm()[0])
    assert t["anuncio"], "el aria-live quedó vacío"


def test_la_tarjeta_coincide_con_la_tabla_de_la_fuente():
    """Los CASOS de arriba son las cifras de tabla_t_pm(), no otras: la
    garantía es su `garantiza` y «¿y aquí da V?» su `da_v_aqui`."""
    filas = {f["algoritmo"]: f for f in j.tabla_t_pm()}
    por_frag = {"minimax": "minimax", "alfa-beta-dado": "alfa-beta, orden dado",
                "alfa-beta-al-reves": "alfa-beta, orden al revés",
                "dado": "expectiminimax, D es un dado", "corte-d1": "corte d = 1",
                "corte-d2": "corte d = 2", "corte-d3": "corte d = 3", "quietud": "quietud, d = 1",
                "mc-5": "Monte Carlo plano, 5 por jugada",
                "mc-50": "Monte Carlo plano, 50 por jugada", "uct": "UCT, c = 1, 40 vueltas"}
    iterativa = filas["profundización iterativa, d = 1, 2, 3"]
    filas[g.FILA_MMMC] = g.fila_mmmc()
    por_frag["mmmc"] = g.FILA_MMMC
    for frag, jugada, valor, nodos, garantiza, aqui in CASOS:
        if frag in ("mmmc-10", "mmmc-40"):
            assert garantiza == g.GARANTIZA_MMMC
            continue
        if frag.startswith("iterativa") or frag == "uct-18":
            fam = iterativa if frag.startswith("iterativa") else filas["UCT, c = 1, 40 vueltas"]
            assert garantiza == g.garantiza(fam["garantiza"]), frag
            continue
        f = filas[por_frag[frag]]
        v = j.fmt_t(f["valor"]) if isinstance(f["valor"], j.F) else str(f["valor"])
        assert (jugada, valor, nodos) == (f["jugada"], v, f"{f['nodos']} de 15"), frag
        assert garantiza == g.garantiza(f["garantiza"]), frag
        assert aqui.startswith("sí") == f["da_v_aqui"], frag
    # la última búsqueda de la iterativa es la fila de la tabla
    assert ("centro", "0") == (iterativa["jugada"], str(iterativa["valor"])) and iterativa["da_v_aqui"]


def test_la_tabla_pintada_va_en_el_orden_de_la_fuente_con_sus_cifras():
    """El orden de la radiografía lo da gen_un_arbol_todos; la página no reordena."""
    filas = _leer("minimax").filas
    esperado = g.datos_de_hoy()["tabla"]
    assert [f[0] for f in filas] == [e["algoritmo"] for e in esperado]
    for f, e in zip(filas, esperado):
        _, _, jugada, valor, nodos, garantiza = (_norm(x) for x in f)
        v = str(e["valor"])
        assert jugada.split()[0] == e["jugada"], e["algoritmo"]
        assert valor == v.replace("-", "−"), e["algoritmo"]
        assert nodos == str(e["nodos"]), e["algoritmo"]
        assert garantiza == ABREVIA.get(e["garantiza"], e["garantiza"]), e["algoritmo"]


def _fila_actual(fragmento):
    dom = _dom(fragmento)
    filas = re.findall(r'<tr data-algoritmo="([^"]+)"([^>]*)>(.*?)</tr>', dom, re.S)
    actuales = [(a, [_norm(html_unescape(re.sub(r"<[^>]+>", "", c))) for c in re.findall(r"<td[^>]*>(.*?)</td>", cuerpo, re.S)])
                for a, atr, cuerpo in filas if 'class="actual"' in atr]
    assert len(actuales) == 1, fragmento
    return actuales[0]


@pytest.mark.parametrize("k", [5, 10, 50])
def test_la_fila_marcada_de_monte_carlo_es_la_corrida_elegida(k, datos):
    """Alumno H8: con 50, la fila marcada no puede decir 5 y 3/5."""
    c = datos["algoritmos"]["Monte Carlo plano"]["corridas"][str(k)]
    _, celdas = _fila_actual(f"mc-{k}")
    assert celdas[0] == f"Monte Carlo plano, {k} por jugada"
    assert celdas[1].split()[0] == c["jugada"]
    assert celdas[2] == j.fmt_t(j.F(c["sumas"][c["jugada"]], k)).replace("-", "−")
    assert celdas[3] == str(c["nodos"])


@pytest.mark.parametrize("t", [10, 40])
def test_la_fila_marcada_de_la_actualizacion_minimax_es_la_partida_del_deslizador(t):
    r = j.mc_minimax(j.ARBOL_TPM, t, j.SEMILLA_TPM)
    jug = j.JUGADAS_RAIZ[r["jugada"]]
    _, celdas = _fila_actual(f"mmmc-{t}")
    assert celdas[0] == f"Act. minimax, partida {t} de {j.VUELTAS_PAGINA_TPM}"
    assert celdas[1].split()[0] == jug
    assert celdas[2] == str(r["Q"][r["jugada"]]).replace("-", "−")
    assert celdas[3] == str(len(r["V"]))


def test_la_actualizacion_minimax_marca_exacto_y_provisional():
    """Partida 10: izq sin visitar («?»), D y C2 exactos (✓), C y R
    provisionales (~); la tarjeta da Q̂ de la raíz con la desconocida."""
    t = _svg_textos("mmmc-10")
    assert _tras(t, "R", 3)[1:] == ["N 10", "V̂ 0 ~"]
    assert _tras(t, "D", 3)[1:] == ["N 5", "V̂ −1 ✓"]
    assert _tras(t, "C", 3)[1:] == ["N 5", "V̂ 0 ~"]
    assert _tras(t, "I", 1) == ["MIN · ?"]
    extra = _norm(_leer("mmmc-10").por_id["t-extra"])
    assert "Q̂(s, a) en la raíz: izq ? (sin visitar) · centro 0 · der −1" in extra
    assert "Exactos (✓): D y C2" in extra


VIEJOS = ("μ", "ū", "T±", "G/N", "s′", "DADO")


def test_ni_el_marcado_ni_el_codigo_usan_la_notacion_vieja(html):
    for viejo in VIEJOS:
        assert viejo not in html, viejo
    assert "árbol de resultados" in html


def test_los_nombres_y_la_garantia_son_los_de_la_radiografia(html):
    """Plan §5.2: «la más visitada», no «la más simulada»; y §5.1: el corte que
    alcanza los finales da M·V, no V (la radiografía, jue-c3-rx-tab-juega)."""
    visible = re.sub(r'<script type="application/json".*?</script>', "", html, flags=re.S)
    assert "Entrega la más visitada" in visible and "más simulada" not in visible
    assert "salvo si llega a los finales" not in html
    assert "con cualquier c > 0" not in html
    for nombre in ('data-nombre="Expectiminimax (dado en D)"', 'data-nombre="Minimax con corte, d = 1"',
                   'data-nombre="Búsqueda de quietud, d = 1"',
                   'data-nombre="Profundización iterativa, búsqueda d = 1"',
                   'data-nombre="Monte Carlo con actualización minimax"'):
        assert nombre in html, nombre


@pytest.mark.parametrize("frag", ["minimax", "dado", "mc-50", "mmmc-10", "uct-18", "corte-d2"])
def test_lo_que_pinta_el_javascript_usa_la_notacion_de_la_unidad(frag):
    dom = _dom(frag)
    visible = re.sub(r"<script.*?</script>|<style.*?</style>", "", dom, flags=re.S)
    for viejo in VIEJOS:
        assert viejo not in visible, (frag, viejo)
    if frag in ("mc-50", "mmmc-10", "uct-18"):
        assert "Q̂" in visible
    if frag == "mc-50":
        assert "Q<sub>azar</sub>" in visible
    if frag == "dado":
        assert "AZAR" in visible and "Pr(a | s)" in visible


@pytest.mark.parametrize("t", [18, 40])
def test_la_fila_marcada_de_uct_es_la_vuelta_del_deslizador(t):
    """Render H10: a la vuelta 18 la fila marcada no puede traer los números de la 40."""
    u = j.uct_tpm(1, t, j.SEMILLA_TPM)
    jug = u["mas_simulada"][-1]
    h = (j.JUGADAS_RAIZ.index(jug),)
    _, celdas = _fila_actual(f"uct-{t}")
    assert celdas[0] == f"UCT, c = 1, vuelta {t} de {j.VUELTAS_PAGINA_TPM}"
    assert celdas[1].split()[0] == jug
    assert celdas[2] == j.fmt_t(j.F(u["S"][h], u["N"][h])).replace("-", "−")
    assert celdas[3] == str(len(u["N"]))


def test_uct_agrega_a_lo_mas_un_nodo_por_vuelta(datos):
    """Alumno H11: tras 18 vueltas hay 14 nodos, no 19; la tarjeta dice cuáles
    vueltas no agregaron (bajaron a un final que ya estaba en el árbol)."""
    pv = datos["algoritmos"]["UCT"]["por_vuelta"]
    tamanos = [1] + [len(x) for x in pv]
    assert all(b - a in (0, 1) for a, b in zip(tamanos, tamanos[1:]))
    sin = [k for k in range(1, 19) if tamanos[k] == tamanos[k - 1]]
    assert tamanos[18] == 14 and sin == [9, 10, 11, 15, 18]
    extra = _norm(_leer("uct-18").por_id["t-extra"])
    assert "Nodos en el árbol (a lo más uno nuevo por vuelta): R + 13 en 18 vueltas; " \
        "no agregaron las vueltas 9, 10, 11, 15 y 18" in extra


def test_la_nota_de_uct_dice_cuando_un_nodo_elige_por_puntaje(datos):
    """Corrección H14: elige por puntaje solo con todos sus hijos en el árbol."""
    tras = datos["algoritmos"]["UCT"]["por_vuelta"][17]
    hijos = {}
    for n in datos["nodos"]:
        if n["padre"]:
            hijos.setdefault(n["padre"], []).append(n["id"])
    completos = [i for i in hijos if i in tras and all(x in tras for x in hijos[i])]
    assert completos == ["R", "I", "C", "D", "C1"]
    nota = _norm(_leer("uct-18").por_id["t-nota"])
    assert "solo cuando ya los tiene todos" in nota
    assert "ya eligen por puntaje: R, I, C, D y C1." in nota


def _podados_por_cota(visitados, valores, nodos):
    """La regla del JavaScript: hijos sin mirar de un nodo que quedó con cota."""
    vis = set(visitados)
    return sorted(n["id"] for n in nodos if n["padre"] in valores
                  and valores[n["padre"]][0] in ("≤", "≥") and n["id"] not in vis)


def test_los_podados_de_la_iterativa_vienen_de_la_fuente(datos):
    """La iterativa trae `podados` como alfa-beta (los hijos sin generar de
    cada nodo que cortó, no lo que quedó bajo el horizonte). Contraprueba:
    la regla «hijo sin mirar de un nodo con cota» da lo mismo en las tres."""
    a = datos["algoritmos"]
    for clave in ("alfa-beta, dado", "alfa-beta, al revés"):
        assert _podados_por_cota(a[clave]["visitados"], a[clave]["valores"], datos["nodos"]) \
            == sorted(a[clave]["podados"]), clave
    it = a["profundización iterativa"]
    assert [x["podados"] for x in it] == [[], ["d2", "d3"], ["c2b", "d2", "d3"]]
    assert [_podados_por_cota(x["visitados"], x["valores"], datos["nodos"]) for x in it] == \
        [sorted(x["podados"]) for x in it]


@pytest.mark.parametrize("frag, podados", [("iterativa-d1", ""), ("iterativa-d2", "podó d2, d3; "),
                                           ("iterativa-d3", "podó c2b, d2, d3; ")])
def test_la_iterativa_tacha_lo_que_podo(frag, podados):
    """Render H8: una marca, un significado; lo podado va tachado también aquí."""
    titulo = _norm(_leer(frag).por_id["arbol-titulo"])
    assert ("podó" in titulo) == bool(podados)
    if podados:
        assert podados.strip() in titulo


def test_la_vuelta_18_de_uct_entrega_centro_y_la_17_no():
    """Brief: centro queda arriba desde la 18 (empate 7–7 en la 18)."""
    t18 = _norm(_leer("uct-18").por_id["t-jugada"])
    t17 = _norm(_leer("uct-17").por_id["t-jugada"])
    mas = j.uct_tpm(1, j.VUELTAS_PAGINA_TPM, j.SEMILLA_TPM)["mas_simulada"]
    assert t18.split()[0] == mas[17] == "centro"
    assert t17.split()[0] == mas[16] != "centro"


def _svg_textos(fragmento):
    """Los textos del árbol pintado, en orden de nodo (id del nodo, luego sus
    renglones de valor)."""
    dom = _dom(fragmento)
    svg = re.search(r'<svg[^>]*id="arbol".*?</svg>', dom, re.S).group(0)
    return [_norm(t) for t in re.findall(r"<text[^>]*>([^<]*)</text>", svg)]


def _tras(textos, nodo, n=2):
    """Los n textos que siguen al nombre de un nodo interno (tipo y valores)."""
    i = textos.index(nodo)
    return textos[i + 1:i + 1 + n]


def test_minimax_y_alfa_beta_pintan_el_valor_de_cada_nodo_interno(datos):
    t = _svg_textos("minimax")
    for n, (_, v) in datos["algoritmos"]["minimax"]["valores"].items():
        esperado = f"V {v}" if n == "R" else str(v)
        assert _tras(t, n)[1] == esperado.replace("-", "−"), n
    t = _svg_textos("alfa-beta-dado")
    assert _tras(t, "D")[1] == "≤ −1" and _tras(t, "C2")[1] == "≥ 1"
    t = _svg_textos("quietud")
    assert _tras(t, "I", 3)[1:] == ["EVAL 60", "→ −100"]


@pytest.mark.parametrize("k", [10, 50])
def test_mc_plano_cuenta_los_nodos_de_cada_corrida(k, datos):
    t = {i: _norm(v) for i, v in _leer(f"mc-{k}").por_id.items()}
    c = datos["algoritmos"]["Monte Carlo plano"]["corridas"][str(k)]
    sims = next(f["simulaciones"] for f in datos["tabla"]
                if f["algoritmo"] == f"Monte Carlo plano, {k} por jugada")
    assert sims == k * len(j.JUGADAS_RAIZ)
    assert t["t-nodos"] == f"{c['nodos']} de 15 distintos, tocados por {sims} simulaciones"
    assert "registr" not in _dom(f"mc-{k}")


@pytest.mark.parametrize("t", [18, 40])
def test_uct_cuenta_los_nodos_de_su_arbol_y_sus_vueltas(t):
    """Brief r2 W3-4: los nodos de UCT son los guardados en el árbol, no los
    generados de una búsqueda; la tarjeta lo rotula y da las vueltas. N(R)
    cuenta vueltas, no simulaciones: una vuelta que llega a un final no
    simula (plan §5.2; ola 4, r2)."""
    u = j.uct_tpm(1, t, j.SEMILLA_TPM)
    tx = _norm(_leer(f"uct-{t}").por_id["t-nodos"])
    assert tx == f"{len(u['N'])} de 15 en el árbol, tras {u['N'][()]} vueltas"
    assert u["N"][()] == t


def test_la_nota_de_la_tabla_dice_que_los_nodos_no_miden_lo_mismo(html):
    nota = _norm(re.sub(r"<[^>]+>", "", html.split('id="tabla"', 1)[1].split("</p>", 1)[0]))
    assert "Nodos: no miden el mismo trabajo en todas las filas." in nota
    assert "en UCT, los que quedaron en su árbol" in nota


# vuelta, jugada, Q̂ de la jugada (de juegos.uct_tpm con t vueltas)
VUELTAS = [(5, "centro", "0"), (18, "centro", "−1/7"), (40, "centro", "0")]


@pytest.mark.parametrize("t, jugada, ubarra", VUELTAS, ids=[f"uct-{v[0]}" for v in VUELTAS])
def test_el_deslizador_de_uct_muestra_q_gorro_en_cada_vuelta(t, jugada, ubarra):
    u = j.uct_tpm(1, t, j.SEMILLA_TPM)
    h = (j.JUGADAS_RAIZ.index(jugada),)
    assert u["mas_simulada"][-1] == jugada
    assert j.fmt_t(j.F(u["S"][h], u["N"][h])).replace("-", "−") == ubarra
    p = _leer(f"uct-{t}")
    tx = {i: _norm(v) for i, v in p.por_id.items()}
    assert tx["t-jugada"].split()[0] == jugada
    assert tx["t-valor"].split()[0] == ubarra and "Q̂" in tx["t-valor"]
    assert f"U de la vuelta {t}" in tx["t-extra"]
    svg = _svg_textos(f"uct-{t}")
    nombre = j.ids_tpm()[h]
    assert _tras(svg, nombre, 3)[1:] == [f"N {u['N'][h]}", f"Q̂ {ubarra}"]
