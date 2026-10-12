"""Los dos interactivos de la clase 7.3, «De dónde sale el bono».

`hoeffding_en_vivo.html` y `bandido_en_vivo.html` son páginas autocontenidas
de `course/7_juegos/_assets/`: JS plano, sin red. Su lógica vive en un
`<script id="logica">` sin DOM, que esta prueba corre con node (si está
instalado; si no, se salta) y compara con `tools/juegos.py`:

- las constantes (los μ de x, y, z, el c de la teoría, el 10 % al azar, la
  semilla que atora) se leen del JS con expresiones regulares;
- el generador es el Mersenne Twister de Python, sembrado igual que
  `juegos.bandido` y `juegos.frecuencia_desvio`, así que las elecciones del
  bandido y los conteos de la cola tienen que coincidir **exactamente**, no
  solo en distribución. Si alguien cambia la siembra en un lado, esto falla.

Lo que no mira: el dibujo. Eso se revisó a mano en Chrome a 390 y 1280 px.
"""
import glob
import json
import math
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

import juegos

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "course/7_juegos/_assets"
HOEFFDING = ASSETS / "hoeffding_en_vivo.html"
BANDIDO = ASSETS / "bandido_en_vivo.html"
PAGINAS = (HOEFFDING, BANDIDO)
PAGINA_P6 = RAIZ / "course/7_juegos/3_cuando_no_cabe/6_de_donde_sale_el_bono.md"


def _texto(ruta):
    return ruta.read_text(encoding="utf-8")


def _logica(ruta):
    m = re.search(r'<script id="logica">(.*?)</script>', _texto(ruta), re.S)
    assert m, f"{ruta.name} no trae <script id=\"logica\">"
    return m.group(1)


def _node():
    """node del PATH, o el más nuevo de nvm (en zsh, node es una función de nvm)."""
    encontrado = shutil.which("node")
    if encontrado:
        return encontrado
    candidatos = glob.glob(os.path.expanduser("~/.nvm/versions/node/*/bin/node"))
    def version(ruta):
        v = Path(ruta).parent.parent.name.lstrip("v")
        return tuple(int(x) for x in v.split(".") if x.isdigit())
    return max(candidatos, key=version) if candidatos else None


NODE = _node()


def _correr(ruta, programa, tmp_path):
    """Corre `programa` en node con la lógica de `ruta` cargada como `L`."""
    if not NODE:
        pytest.skip("node no está instalado")
    modulo = tmp_path / f"{ruta.stem}_logica.js"
    modulo.write_text(_logica(ruta), encoding="utf-8")
    guion = tmp_path / "prueba.js"
    guion.write_text(f"const L = require({json.dumps(str(modulo))});\n{programa}",
                     encoding="utf-8")
    salida = subprocess.run([NODE, str(guion)], capture_output=True, text=True, timeout=120)
    assert salida.returncode == 0, salida.stderr
    return json.loads(salida.stdout)


# ------------------------------------------------------------- forma ---

@pytest.mark.parametrize("ruta", PAGINAS, ids=lambda r: r.name)
def test_existe_declara_idioma_titulo_y_paleta(ruta):
    html = _texto(ruta)
    assert '<html lang="es">' in html
    assert re.search(r"<title>[^<]+</title>", html)
    assert 'name="viewport"' in html
    assert re.search(r":root\s*\{[^}]*--surface:#211033", html), "sin la paleta del skin en :root"
    assert "aria-live" in html, "el resultado tiene que anunciarse"


@pytest.mark.parametrize("ruta", PAGINAS, ids=lambda r: r.name)
def test_no_carga_nada_de_fuera(ruta):
    html = _texto(ruta)
    assert not re.search(r"""(?:src|href)\s*=\s*["']?\s*(?:https?:)?//""", html, re.I)
    assert not re.search(r"@import|url\(\s*['\"]?(?:https?:)?//", html, re.I)
    assert not re.search(r"<script[^>]*\ssrc=", html, re.I), "nada de scripts externos"
    assert not re.search(r"<link[^>]*stylesheet", html, re.I), "nada de hojas externas"
    for cdn in ("cdn", "unpkg", "jsdelivr", "googleapis", "cloudflare", "fetch(", "XMLHttpRequest"):
        assert cdn not in html, cdn


@pytest.mark.parametrize("ruta", PAGINAS, ids=lambda r: r.name)
def test_cada_control_tiene_su_etiqueta(ruta):
    html = _texto(ruta)
    for ident in re.findall(r'<(?:input|select)[^>]*\sid="([^"]+)"', html):
        assert re.search(rf'<label[^>]*for="{ident}"', html), f"#{ident} sin <label for>"


def test_la_pagina_6_enlaza_los_dos_interactivos():
    if not PAGINA_P6.exists():
        pytest.skip("la página 6 aún no está escrita")
    texto = _texto(PAGINA_P6)
    for ruta in PAGINAS:
        assert f"../_assets/{ruta.name}" in texto, f"la página 6 no enlaza {ruta.name}"


# ------------------------------------------- constantes contra juegos ---

def test_los_mu_del_bandido_son_los_del_hilo():
    m = re.search(r"const MUS = \{([^}]*)\}", _logica(BANDIDO))
    assert m
    mus = {k: float(v) for k, v in re.findall(r"(\w+):\s*(-?[\d.]+)", m.group(1))}
    assert mus == {k: float(v) for k, v in juegos.MUS_HILO.items()}


def test_c_por_defecto_azar_y_semilla_son_los_de_juegos():
    js = _logica(BANDIDO)
    assert re.search(r"const C_TEORIA = 2 \* Math\.SQRT2;", js)
    assert math.isclose(2 * math.sqrt(2), juegos.C_TEORIA)
    assert float(re.search(r"const AL_AZAR = ([\d.]+);", js).group(1)) == juegos.AL_AZAR
    assert int(re.search(r"const SEMILLA_INICIAL = (\d+);", js).group(1)) == juegos.SEMILLA_ATORA
    html = _texto(BANDIDO)
    assert re.search(r'id="semilla"[^>]*value="36"', html)
    assert re.search(r'id="c"[^>]*value="2.83"', html)
    assert 'data-c="teoria"' in html and 'data-c="1"' in html and 'data-c="0"' in html


def test_los_deslizadores_de_hoeffding_tienen_el_rango_pedido():
    html = _texto(HOEFFDING)
    for ident, lo, hi in (("mu", "-0.8", "0.8"), ("n", "1", "200"), ("eps", "0.05", "0.8")):
        m = re.search(rf'<input type="range" id="{ident}" min="([^"]+)" max="([^"]+)"', html)
        assert m and m.groups() == (lo, hi), ident


# --------------------------------------------- la lógica, con node ---

def test_el_generador_es_el_de_python(tmp_path):
    import random
    datos = _correr(HOEFFDING, """
const r = new L.PyRandom(1), s = new L.PyRandom(36002), t = new L.PyRandom(2 ** 40 + 5);
console.log(JSON.stringify([[r.random(), r.random(), r.random()], s.random(), t.random()]));
""", tmp_path)
    r = random.Random(1)
    assert datos[0] == [r.random() for _ in range(3)]
    assert datos[1] == random.Random(36002).random()
    assert datos[2] == random.Random(2 ** 40 + 5).random()


def test_la_cota_y_el_umbral_son_los_de_juegos(tmp_path):
    casos = [(1, 20), (50, 20), (100, 20), (200, 5), (30, 45)]
    datos = _correr(HOEFFDING, f"""
const casos = {json.dumps(casos)};
console.log(JSON.stringify({{
  cota: casos.map(([n, e]) => L.cotaHoeffding(n, e / 100)),
  umbral: [[30, 20, 100], [30, 20, 7], [-50, 15, 37], [80, 5, 3], [-80, 80, 10]].map(a => L.umbral(...a)),
  p: [30, -50, 80].map(L.probGana)
}}));
""", tmp_path)
    from fractions import Fraction as F
    for (n, e), v in zip(casos, datos["cota"]):
        assert math.isclose(v, juegos.cota_hoeffding(n, e / 100), rel_tol=1e-12)
    esperado = [juegos._umbral(F(m, 100), F(e, 100), n)
                for m, e, n in [(30, 20, 100), (30, 20, 7), (-50, 15, 37), (80, 5, 3), (-80, 80, 10)]]
    assert datos["umbral"] == esperado
    assert datos["p"] == [float(juegos.prob_gana(F(m, 100))) for m in (30, -50, 80)]


@pytest.mark.parametrize("mu, n, eps, reps, semilla",
                         [(30, 100, 20, 20000, 1), (30, 10, 20, 5000, 1), (-50, 37, 15, 3000, 7),
                          (80, 1, 80, 2000, 3)])
def test_la_cola_cuenta_lo_mismo_que_frecuencia_desvio(tmp_path, mu, n, eps, reps, semilla):
    from fractions import Fraction as F
    datos = _correr(HOEFFDING, f"""
const c = new L.Corrida({mu}, {n}, {eps}, {semilla});
c.promedios({reps});
const suma = Array.from(c.hist).reduce((a, b) => a + b, 0);
console.log(JSON.stringify([c.enCola, c.hechos, suma]));
""", tmp_path)
    esperado = juegos.frecuencia_desvio(F(mu, 100), n, F(eps, 100), reps, semilla) * reps
    assert datos == [esperado, reps, reps]


CASOS_BANDIDO = [(regla, semilla, None) for regla in juegos.REGLAS_BANDIDO
                 for semilla in (36, 1, 7)] + \
                [("ucb", semilla, c) for semilla in (36, 1, 7) for c in (0, 1, 5)]


@pytest.mark.parametrize("regla, semilla, c", CASOS_BANDIDO)
def test_el_bandido_elige_lo_mismo_que_juegos(tmp_path, regla, semilla, c):
    vueltas = 400
    cjs = "L.C_TEORIA" if c is None else str(c)
    datos = _correr(BANDIDO, f"""
const b = new L.Bandido({json.dumps(regla)}, {semilla}, {cjs});
for (let t = 0; t < {vueltas}; t++) b.paso();
console.log(JSON.stringify({{e: b.elecciones.join(""), N: b.N, n: b.nPadre,
  hN: [0, 1, 2].map(i => b.historiaN[i][{vueltas}]),
  fx: [10, 100, {vueltas}].map(k => b.fraccionEnX(k))}}));
""", tmp_path)
    py = juegos.bandido(regla, juegos.MUS_HILO, vueltas, semilla, c)
    assert datos["e"] == "".join(py["elecciones"])
    assert datos["N"] == [py["N"][a] for a in "xyz"] == datos["hN"]
    assert datos["n"] == vueltas
    # la segunda gráfica: la fracción de vueltas en x, la de la figura
    for k, f in zip((10, 100, vueltas), datos["fx"]):
        assert math.isclose(f, py["elecciones"][:k].count("x") / k, rel_tol=1e-12)


def test_con_la_semilla_36_el_mejor_promedio_se_atora_en_z(tmp_path):
    datos = _correr(BANDIDO, """
const b = new L.Bandido("mejor_promedio", L.SEMILLA_INICIAL, 0);
for (let t = 0; t < 1000; t++) b.paso();
const u = new L.Bandido("ucb", L.SEMILLA_INICIAL, L.C_TEORIA);
for (let t = 0; t < 12; t++) u.paso();
console.log(JSON.stringify({N: b.N, doce: b.elecciones.slice(0, 12).join(""),
  ucb: u.elecciones.join(""), N12: u.N}));
""", tmp_path)
    assert datos["N"] == [1, 1, 998]
    assert datos["doce"] == "xyzzzzzzzzzz"
    assert datos["ucb"] == "xyzzzxyxyxyx"
    assert datos["N12"] == [5, 4, 3]


def test_el_bono_es_el_de_juegos(tmp_path):
    casos = [(100, 10), (100, 30), (100, 60), (5, 1), (50, 30)]
    datos = _correr(BANDIDO, f"""
const casos = {json.dumps(casos)};
console.log(JSON.stringify({{t: casos.map(([p, n]) => L.bonoUcb(p, n, L.C_TEORIA)),
  uno: casos.map(([p, n]) => L.bonoUcb(p, n, 1)), cero: L.bonoUcb(100, 0, 1) === Infinity}}));
""", tmp_path)
    for (p, n), v, u in zip(casos, datos["t"], datos["uno"]):
        assert math.isclose(v, juegos.bono_ucb(p, n), rel_tol=1e-12)
        assert math.isclose(u, juegos.bono_ucb(p, n, c=1), rel_tol=1e-12)
    assert datos["cero"]


# ------------------------------------------- lo que el alumno lee ---

@pytest.mark.parametrize("ruta", PAGINAS, ids=lambda r: r.name)
def test_los_numeros_van_con_el_formato_del_curso(ruta):
    """Punto decimal y espacio de miles, como la página («10 000»): nada de
    toLocaleString (pone coma de miles), ni notación e-9, ni «10 mil»."""
    html = _texto(ruta)
    assert "toLocaleString" not in html
    assert "toPrecision" not in html and "toExponential" not in html
    assert '" mil"' not in html
    assert "const miles = " in html


@pytest.mark.parametrize("ruta", PAGINAS, ids=lambda r: r.name)
def test_escribe_n_de_s_con_prima_y_sin_vocabulario_ajeno(ruta):
    """N(s′) con la prima de la página, nunca con apóstrofo recto; y nada de
    «arrepentimiento» ni μ*, que la página no define (r1, alumno H11)."""
    html = _texto(ruta)
    assert "(s')" not in html
    assert "arrepent" not in html.lower() and "μ*" not in html


@pytest.mark.parametrize("ruta", PAGINAS, ids=lambda r: r.name)
def test_miles_pone_espacio_de_miles(ruta, tmp_path):
    linea = re.search(r"^const miles = .*?;(?=\s*(?://.*)?$)", _texto(ruta), re.M).group(0)
    datos = _correr(ruta, f"""
{linea}
console.log(JSON.stringify([7, 1000, 9468, 10000, 369600].map(miles)));
""", tmp_path)
    assert [d.replace("\u00a0", " ") for d in datos] == ["7", "1 000", "9 468", "10 000", "369 600"]
    assert all(" " not in d for d in datos), "el espacio de miles no debe partirse"


def test_el_control_de_c_dice_que_solo_es_de_ucb_y_que_reinicia():
    html = _texto(BANDIDO)
    etiqueta = re.search(r'<label for="c">(.*?)</label>', html, re.S).group(1)
    assert "solo UCB" in etiqueta and "reinicia" in etiqueta
    assert 'id="aviso-c"' in html
