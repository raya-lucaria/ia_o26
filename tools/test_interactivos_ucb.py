"""Los dos interactivos de la clase 7.3, «De dónde sale el bono».

`hoeffding_en_vivo.html` y `bandido_en_vivo.html` son páginas autocontenidas
de `course/7_juegos/_assets/`: JS plano, sin red. Su lógica vive en un
`<script id="logica">` sin DOM, que esta prueba corre con node (si está
instalado; si no, se salta) y compara con `tools/juegos.py`:

- las constantes (las Q_azar de x, y, z, el c de la teoría, el 10 % al azar,
  la semilla que atora) se leen del JS con expresiones regulares;
- el generador es el Mersenne Twister de Python, sembrado igual que
  `juegos.bandido` y `juegos.frecuencia_desvio`, así que las elecciones del
  bandido y los conteos de la cola tienen que coincidir **exactamente**, no
  solo en distribución. Si alguien cambia la siembra en un lado, esto falla.
  La cola de arriba (la de MIN) y el modo «δ fijo» de Hoeffding se cotejan
  con la misma cuenta hecha aquí en Python y con juegos.margen_hoeffding.

Notación (plan de homologación §5.1): Q_azar, Q̂(s,a), N(s), N(s,a); nada
de μ, ū, N(s′) ni G/N en ninguna de las dos páginas.

Si falta la página del bono, la prueba que la lee falla (no se salta).
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
PAGINA_BONO = RAIZ / "course/7_juegos/3_cuando_no_cabe/5_de_donde_sale_el_bono.md"


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


def test_la_pagina_del_bono_enlaza_los_dos_interactivos():
    assert PAGINA_BONO.exists(), f"falta la página del bono: {PAGINA_BONO}"
    texto = _texto(PAGINA_BONO)
    for ruta in PAGINAS:
        assert f"../_assets/{ruta.name}" in texto, f"la página del bono no enlaza {ruta.name}"


# ------------------------------------------- constantes contra juegos ---

def test_las_q_azar_del_bandido_son_las_del_hilo():
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
    for ident, lo, hi in (("mu", "-0.8", "0.8"), ("n", "1", "200"), ("eps", "0.05", "0.8"),
                          ("delta", "0.005", "0.5")):
        m = re.search(rf'<input type="range" id="{ident}" min="([^"]+)" max="([^"]+)"', html)
        assert m and m.groups() == (lo, hi), ident
    # los dos modos: qué se fija (ε o δ) y qué cola se cuenta (MAX abajo, MIN arriba)
    for nombre, valores in (("fijo", ("eps", "delta")), ("cola", ("abajo", "arriba"))):
        for v in valores:
            assert re.search(rf'<label><input type="radio" name="{nombre}" value="{v}"', html), (nombre, v)


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


def _cola_arriba_en_python(mu, n, eps, reps, semilla):
    """La cuenta de juegos.frecuencias_desvio, pero en la otra cola:
    Q̂ ≥ Q_azar + ε, es decir, total de U ≥ ⌈(Q_azar + ε)·n⌉."""
    import random
    from fractions import Fraction as F
    rng = random.Random(semilla)
    p = float(juegos.prob_gana(F(mu, 100)))
    tope = math.ceil((F(mu, 100) + F(eps, 100)) * n)
    return sum(sum(juegos._resultado(rng, p) for _ in range(n)) >= tope for _ in range(reps))


@pytest.mark.parametrize("mu, n, eps, reps, semilla",
                         [(30, 100, 20, 5000, 1), (-50, 37, 15, 3000, 7), (80, 3, 5, 2000, 3),
                          (30, 10, 20, 4000, 2)])
def test_la_cola_de_arriba_cuenta_lo_que_cuenta_python(tmp_path, mu, n, eps, reps, semilla):
    datos = _correr(HOEFFDING, f"""
const c = new L.Corrida({mu}, {n}, {eps}, {semilla}, "arriba");
c.promedios({reps});
console.log(JSON.stringify([c.enCola, c.hechos, L.umbralArriba({mu}, {eps}, {n})]));
""", tmp_path)
    from fractions import Fraction as F
    assert datos[0] == _cola_arriba_en_python(mu, n, eps, reps, semilla)
    assert datos[1] == reps
    assert datos[2] == math.ceil((F(mu, 100) + F(eps, 100)) * n)


def test_con_delta_fijo_el_margen_es_el_de_juegos_y_la_cota_es_delta(tmp_path):
    casos = [(0.05, 10), (0.05, 100), (0.005, 100), (0.5, 1), (0.2, 200)]
    datos = _correr(HOEFFDING, f"""
const casos = {json.dumps(casos)};
console.log(JSON.stringify(casos.map(([d, n]) => {{
  const e = L.margenDelta(n, d); return [e, L.cotaHoeffding(n, e)]; }})));
""", tmp_path)
    for (d, n), (e, cota) in zip(casos, datos):
        assert math.isclose(e, juegos.margen_hoeffding(d, n), rel_tol=1e-12)
        assert math.isclose(cota, d, rel_tol=1e-9)
    # con 100 muestras: 0.245 y 0.326, las de la figura de la página
    assert [round(datos[i][0], 3) for i in (1, 2)] == [0.245, 0.326]


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
def test_escribe_la_notacion_de_la_unidad_y_sin_vocabulario_ajeno(ruta):
    """Plan de homologación §5.1: Q_azar (la esperanza si todos juegan al
    azar), Q̂(s,a) (el promedio), N(s) y N(s,a). μ, ū, N(s′) y G/N ya no
    existen en la unidad: ni en rótulos, ni en ayudas, ni en el JavaScript que
    los escribe. Y nada de «arrepentimiento», que la página no define (r1,
    alumno H11)."""
    html = _texto(ruta)
    for viejo in ("μ", "ū", "s′", "(s')", "G/N", "T±"):
        assert viejo not in html, (ruta.name, viejo)
    assert "arrepent" not in html.lower()
    assert "Q<sub>azar</sub>" in html and "Q̂" in html
    visible = re.sub(r"<script.*?</script>|<style.*?</style>", "", html, flags=re.S)
    assert "Q<sub>azar</sub>" in visible and "Q̂" in visible


def test_el_bandido_usa_n_de_s_a_y_puntaje():
    """N(s,a) cuenta las vueltas de cada jugada; Q̂ + bono es un puntaje, no
    una cota del pago (§5.1: el puntaje no es un pago)."""
    html = _texto(BANDIDO)
    assert "N(s,a) de cada jugada contra N(s)" in html
    assert "c·√(ln N(s) / N(s,a))" in html
    assert "UCB: Q̂(s,a) + bono" in html
    assert "cota optimista" not in html


def test_el_bandido_entrega_la_mas_visitada_y_cuenta_vueltas():
    """Plan §5.2: se entrega «la más visitada», no «la más simulada» (ola 4,
    r2: la r1 solo lo corrigió en un_arbol_todos.html); y N(s,a) cuenta
    vueltas también en el aria-label de las barras."""
    html = _texto(BANDIDO)
    assert "más simulada" not in html and "masSimulada" not in html
    assert "se entregaría la más visitada:" in html
    assert "${n} vueltas, promedio" in html


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


def test_el_estado_dice_la_vuelta_actual_tambien_corriendo():
    """«Vuelta N» se congelaba mientras corría (decía «Vuelta 0» junto a
    barras de 7 554 vueltas), y tras el tope Correr reiniciaba sin repintar:
    «Vuelta 10 000» junto a la corrida nueva (ronda 1 de render, H5)."""
    html = _texto(BANDIDO)
    cuerpo = re.search(r"function pintarJugadas\(\)\{(.*?)\n\}", html, re.S).group(1)
    assert '$("estado").innerHTML = estado;' in cuerpo
    assert "corriendo ?" not in cuerpo, "el estado no debe congelarse al correr"
    # Correr tras el tope reinicia y repinta antes de arrancar.
    correr = re.search(r'\$\("b-correr"\)\.addEventListener\("click", \(\) => \{(.*?)\n\}\);',
                       html, re.S).group(1)
    assert re.search(r"reiniciar\(\);\s*pintar\(\);", correr)
    # Al correr se apaga aria-live (no se lee cada cuadro) y al parar se prende.
    assert '$("estado").setAttribute("aria-live", si ? "off" : "polite");' in html


def test_las_figuras_y_tablas_que_cita_existen_en_la_pagina():
    """La leyenda citaba «UCB empieza abajo y termina arriba», un título que
    ya no existía (ronda 1 de render, H6), y luego «Cuánto gana cada regla»,
    una figura que la homologación quitó (sus cifras pasaron a una tabla).
    Toda figura o tabla citada por título tiene que ser el title de una
    figura o tabla de la página del bono, y el bandido cita al menos una."""
    texto = _texto(PAGINA_BONO)
    titulos = {k: set(re.findall(rf'^::: {k} \{{#[^ ]+ title="([^"]+)"\}}', texto, re.M))
               for k in ("figure", "table")}
    for ruta in PAGINAS:
        for clase, c in re.findall(r"(figura|tabla) «([^»]+)»", _texto(ruta)):
            assert c in titulos["figure" if clase == "figura" else "table"], (ruta.name, c)
    assert re.findall(r"(?:figura|tabla) «([^»]+)»", _texto(BANDIDO))
    assert "Cuánto gana cada regla" not in _texto(BANDIDO)
