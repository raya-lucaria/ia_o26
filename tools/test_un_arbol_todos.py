"""«El mismo árbol, todos los algoritmos» muestra lo que juegos.py da hoy.

course/7_juegos/_assets/un_arbol_todos.html lleva incrustado, en
<script type="application/json" id="datos">, el JSON que tools/gen_un_arbol_todos.py
escribe desde juegos.datos_interactivo_tpm(). Esta prueba NO regenera:
compara el bloque comiteado con el que daría hoy la fuente, así que cambiar
juegos.py sin volver a correr el generador falla aquí.

Además: cada variante del selector apunta a un algoritmo que existe en el
JSON y a una fila de la tabla; la tabla incrustada tiene las cifras de
tabla_t_pm(); la página no carga nada de fuera, copia la paleta del skin, no
usa text-transform ni comentarios HTML, y pesa menos de TOPE_BYTES. Con
Chrome disponible (se salta sin él, como en CI), abre la página en varios
fragmentos y lee la tarjeta y la tabla que pintó el JavaScript.
"""
import json
import re
import shutil
import subprocess
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
    assert g.bloque_incrustado(html) == g.serializar(j.datos_interactivo_tpm()), (
        "el JSON de un_arbol_todos.html ya no coincide con juegos.datos_interactivo_tpm(): "
        "corre python3 tools/gen_un_arbol_todos.py y comitea el HTML")


def test_el_generador_es_idempotente(html):
    d = j.datos_interactivo_tpm()
    una = g.incrustar(html, d)
    assert g.incrustar(una, d) == una


def _variantes(html):
    return [dict(re.findall(r'data-([\w-]+)="([^"]*)"', m))
            for m in re.findall(r"<(?:button|span)[^>]*\sdata-v=[^>]*>", html)]


def test_cada_variante_del_selector_existe_en_los_datos(html, datos):
    vs = _variantes(html)
    filas = {f["algoritmo"] for f in datos["tabla"]}
    assert len(vs) == 15
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


def test_cada_familia_tiene_su_boton_y_sus_variantes(html):
    familias = re.findall(r'data-familia="([\w-]+)"', html)
    grupos = re.findall(r'class="variantes" data-de="([\w-]+)"', html)
    assert familias and sorted(familias) == sorted(grupos)


def test_la_tabla_incrustada_tiene_las_cifras_de_tabla_t_pm(datos):
    esperado = j.tabla_t_pm()
    assert [f["algoritmo"] for f in datos["tabla"]] == [f["algoritmo"] for f in esperado]
    for f, e in zip(datos["tabla"], esperado):
        assert f["jugada"] == e["jugada"], f["algoritmo"]
        assert f["valor"] == (j.fmt_t(e["valor"]) if isinstance(e["valor"], j.F) else e["valor"])
        assert (f["tipo"], f["escala"], f["nodos"], f["exacto"]) == \
               (e["tipo"], e["escala"], e["nodos"], e["exacto"]), f["algoritmo"]


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


# (fragmento, jugada, valor de la raíz, nodos mirados, ¿exacto?)
CASOS = [
    ("minimax", "centro", "0", "15 de 15", "sí"),
    ("alfa-beta-dado", "centro", "0", "12 de 15", "sí"),
    ("alfa-beta-al-reves", "centro", "0", "14 de 15", "sí"),
    ("dado", "der", "1/3", "15 de 15", "no"),
    ("corte-d1", "izq", "60", "4 de 15", "no"),
    ("corte-d2", "centro", "10", "11 de 15", "no"),
    ("corte-d3", "centro", "0", "15 de 15", "sí"),
    ("quietud", "centro", "20", "5 de 15", "no"),
    ("iterativa-d3", "centro", "0", "12 de 15", "sí"),
    ("mc-5", "der", "3/5", "15 de 15", "no"),
    ("uct", "centro", "0", "15 de 15", "no"),
]


@pytest.mark.parametrize("frag, jugada, valor, nodos, exacto", CASOS, ids=[c[0] for c in CASOS])
def test_la_tarjeta_dice_lo_que_dicen_los_datos(frag, jugada, valor, nodos, exacto):
    t = {k: _norm(v) for k, v in _leer(frag).por_id.items()}
    assert t["t-jugada"].startswith(jugada), t["t-jugada"]
    assert t["t-valor"].split()[0] == valor, t["t-valor"]
    assert t["t-nodos"].startswith(nodos), t["t-nodos"]
    assert t["t-exacto"].startswith(exacto), t["t-exacto"]
    assert ("✓" in t["t-jugada"]) == (jugada == j.minimax_tpm()[0])
    assert t["anuncio"], "el aria-live quedó vacío"


def test_la_tarjeta_coincide_con_la_tabla_de_la_fuente():
    """Los CASOS de arriba son las cifras de tabla_t_pm(), no otras."""
    filas = {f["algoritmo"]: f for f in j.tabla_t_pm()}
    por_frag = {"minimax": "minimax", "alfa-beta-dado": "alfa-beta, orden dado",
                "alfa-beta-al-reves": "alfa-beta, orden al revés",
                "dado": "expectiminimax, D es un dado", "corte-d1": "corte d = 1",
                "corte-d2": "corte d = 2", "corte-d3": "corte d = 3", "quietud": "quietud, d = 1",
                "mc-5": "Monte Carlo plano, 5 por jugada", "uct": "UCT, c = 1, 40 vueltas"}
    for frag, jugada, valor, nodos, exacto in CASOS:
        if frag not in por_frag:
            continue
        f = filas[por_frag[frag]]
        v = j.fmt_t(f["valor"]) if isinstance(f["valor"], j.F) else str(f["valor"])
        assert (jugada, valor, nodos, exacto) == \
               (f["jugada"], v, f"{f['nodos']} de 15", "sí" if f["exacto"] else "no"), frag


def test_la_tabla_pintada_tiene_las_cifras_de_tabla_t_pm():
    filas = _leer("minimax").filas
    esperado = j.tabla_t_pm()
    assert [f[0] for f in filas] == [e["algoritmo"] for e in esperado]
    for f, e in zip(filas, esperado):
        _, _, jugada, valor, nodos, exacto = (_norm(x) for x in f)
        v = j.fmt_t(e["valor"]) if isinstance(e["valor"], j.F) else str(e["valor"])
        assert jugada.split()[0] == e["jugada"], e["algoritmo"]
        assert valor.split()[0] == v.replace("-", "−"), e["algoritmo"]
        assert nodos == str(e["nodos"]), e["algoritmo"]
        assert exacto == ("sí" if e["exacto"] else "no"), e["algoritmo"]


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
    assert t["t-nodos"] == f"{c['nodos']} de 15"
    assert "registr" not in _dom(f"mc-{k}")


# vuelta, jugada, ū de la jugada (de juegos.uct_tpm con t vueltas)
VUELTAS = [(5, "centro", "0"), (18, "centro", "−1/7"), (40, "centro", "0")]


@pytest.mark.parametrize("t, jugada, ubarra", VUELTAS, ids=[f"uct-{v[0]}" for v in VUELTAS])
def test_el_deslizador_de_uct_muestra_u_barra_en_cada_vuelta(t, jugada, ubarra):
    u = j.uct_tpm(1, t, j.SEMILLA_TPM)
    h = (j.JUGADAS_RAIZ.index(jugada),)
    assert u["mas_simulada"][-1] == jugada
    assert j.fmt_t(j.F(u["S"][h], u["N"][h])).replace("-", "−") == ubarra
    p = _leer(f"uct-{t}")
    tx = {i: _norm(v) for i, v in p.por_id.items()}
    assert tx["t-jugada"].split()[0] == jugada
    assert tx["t-valor"].split()[0] == ubarra and "ū" in tx["t-valor"]
    assert f"U de la vuelta {t}" in tx["t-extra"]
    svg = _svg_textos(f"uct-{t}")
    nombre = j.ids_tpm()[h]
    assert _tras(svg, nombre, 3)[1:] == [f"N {u['N'][h]}", f"ū {ubarra}"]
