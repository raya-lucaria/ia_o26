"""El generador de texto de la unidad 8 escribe lo que escribe markov.py.

course/8_markov/_assets/generador_texto.html lleva incrustadas, entre dos
marcas, las tablas de conteos del Quijote (memoria 0 a 3) y tres o más textos
de autoprueba; las escribe tools/gen_generador_markov.py. Como
test_traza_web.py, esta prueba NO regenera: compara el archivo comiteado con
lo que el generador produciria hoy, asi que un cambio en markov.py o en el
corpus sin volver a correr el generador falla aqui.

La regla dura es que, con la misma semilla, la pagina escriba el mismo texto
que markov.generar. Se ata de tres formas:

- los textos de autoprueba incrustados son los de markov.generar con las
  semillas de la pagina; la pagina los recalcula al cargar y dice
  «autoprueba: ok» o un aviso visible (eso se mira en Chrome con
  tools/gen_vista_generador.py, que no corre en CI);
- el muestreador del JS tiene la forma de MUESTREAR-FILA (suma en el orden de
  ALFABETO, u < acumulado), leido del codigo;
- la logica del JS (<script id="logica">, sin DOM) se corre con node contra
  markov.generar con varias semillas y memorias, incluida la fila uniforme de
  un contexto nunca visto. Se salta si no hay node.

Y la captura mkv-c1-generador.png queda atada al HTML por su huella en
tools/vista_generador.json.
"""
import json
import re

import pytest
from PIL import Image

import gen_generador_markov as g
import gen_vista_generador as v
import markov as m
from test_interactivos_ucb import NODE

HTML = g.HTML
TOPE_BYTES = 150_000
FONDO_PAGINA = (0x12, 0x06, 0x1F)   # --page del interactivo (skin eva-cyberpunk)


@pytest.fixture(scope="module")
def html():
    return HTML.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def datos(html):
    return json.loads(g.bloque_incrustado(html))


def _logica(html):
    mm = re.search(r'<script id="logica">(.*?)</script>', html, re.S)
    assert mm, 'generador_texto.html no trae <script id="logica">'
    return mm.group(1)


# ------------------------------------------------------- el generador ---

def test_el_html_es_el_que_escribiria_hoy_el_generador(html):
    assert g.contenido() == html, (
        "generador_texto.html ya no coincide con markov.py: corre "
        "python3 tools/gen_generador_markov.py y comitea el HTML")


def test_las_tablas_incrustadas_son_los_conteos_del_corpus(datos):
    assert datos["alfabeto"] == m.ALFABETO
    assert datos["contexto_inicial"] == m.CONTEXTO_INICIAL
    assert len(datos["tablas"]) == g.MEMORIA_MAX + 1
    for h, texto in enumerate(datos["tablas"]):
        esperado = {ctx: dict(c) for ctx, c in m.conteos_caracteres(h).items()}
        assert g.leer_tabla(texto, h) == esperado, f"memoria {h}"


def test_la_autoprueba_es_lo_que_escribe_markov_generar(datos):
    pruebas = datos["autoprueba"]
    assert {e["h"] for e in pruebas} >= {0, 1, 2}
    for e in pruebas:
        assert e["semilla"] == m.SEMILLAS[f"generar-{e['h']}"]
        assert e["largo"] == 60
        assert e["texto"] == m.generar(e["h"], largo=e["largo"], semilla=e["semilla"])
        assert len(e["texto"]) == 60


def test_ningun_contexto_al_que_se_llega_queda_sin_fila():
    """La pagina afirma que con el libro completo la fila uniforme no llega a
    usarse con memoria 0 a 3: todo contexto alcanzable tiene conteos."""
    for h in range(1, g.MEMORIA_MAX + 1):
        c = m.conteos_caracteres(h)
        alcanzables = {(ctx + z)[1:] for ctx, fila in c.items() for z in fila}
        alcanzables.add(m.CONTEXTO_INICIAL[:h])
        assert alcanzables <= set(c), f"memoria {h}: {sorted(alcanzables - set(c))[:5]}"


# ------------------------------------------------------------- la forma ---

def test_pesa_menos_del_tope():
    assert HTML.stat().st_size < TOPE_BYTES


def test_declara_idioma_titulo_y_la_paleta_del_skin(html):
    assert '<html lang="es">' in html
    assert re.search(r"<title>[^<]+</title>", html)
    assert 'name="viewport"' in html
    raiz = re.search(r":root\s*\{([^}]*)\}", html)
    assert raiz, "sin bloque :root"
    for token in ("--page:#12061f", "--surface:#211033", "--text:#f7f2ff",
                  "--muted:#c8b9d8", "--accent:#f04cff"):
        assert token in raiz.group(1), token
    assert "aria-live" in html


def test_no_carga_nada_de_fuera(html):
    assert not re.search(r"""(?:src|href)\s*=\s*["']?\s*(?:https?:)?//""", html, re.I)
    assert "http://" not in html and "https://" not in html
    assert not re.search(r"@import|url\(", html, re.I)
    assert not re.search(r"<script[^>]*\ssrc=", html, re.I)
    assert not re.search(r"<link\b", html, re.I)
    assert "Math.random" not in html, "la suerte es la de random.Random, no Math.random"
    for cosa in ("fetch(", "XMLHttpRequest", "import("):
        assert cosa not in html, cosa


def test_sin_text_transform(html):
    """Convierte «u» en «U» y «h» en «H», que el curso no tiene."""
    assert "text-transform" not in html


def test_cada_control_tiene_su_etiqueta(html):
    for ident in re.findall(r'<input[^>]*\sid="([^"]+)"', html):
        assert re.search(rf'<label[^>]*for="{ident}"', html), f"#{ident} sin <label for>"
    assert html.count('name="memoria"') == g.MEMORIA_MAX + 1


def test_la_pagina_corre_la_autoprueba_y_lo_dice(html):
    assert "autoprueba: <b>ok</b>" in html
    assert "autoprueba: FALLA" in html
    assert re.search(r"for \(const e of DATOS\.autoprueba", html)


def test_el_muestreador_es_muestrear_fila(html):
    """Misma forma que markov.muestrear_fila: suma p = N/N(contexto) en el
    orden de la fila y devuelve la primera posicion con u < acumulado."""
    logica = _logica(html)
    cuerpo = re.search(r"function muestrearFila\(fila, u\)\{(.*?)\n\}", logica, re.S)
    assert cuerpo, "no se encontro muestrearFila"
    cuerpo = cuerpo.group(1)
    assert "let acumulado = 0;" in cuerpo
    assert "acumulado += fila.n[k] / fila.total;" in cuerpo
    assert "if (u < acumulado) return" in cuerpo
    assert re.search(r'const ALFABETO = "abcdefghijklmnñopqrstuvwxyz ";', logica)
    assert m.ALFABETO == "abcdefghijklmnñopqrstuvwxyz "


# ------------------------------------------------ la logica, con node ---

def _correr(html, programa, tmp_path):
    if not NODE:
        pytest.skip("node no está instalado")
    import subprocess
    modulo = tmp_path / "generador_logica.js"
    modulo.write_text(_logica(html), encoding="utf-8")
    datos = tmp_path / "datos.json"
    datos.write_text(g.bloque_incrustado(html), encoding="utf-8")
    guion = tmp_path / "prueba.js"
    guion.write_text(
        f"const L = require({json.dumps(str(modulo))});\n"
        f"const D = JSON.parse(require('fs').readFileSync({json.dumps(str(datos))}, 'utf8'));\n"
        f"const T = L.leerTablas(D);\n{programa}", encoding="utf-8")
    salida = subprocess.run([NODE, str(guion)], capture_output=True, text=True, timeout=300)
    assert salida.returncode == 0, salida.stderr
    return json.loads(salida.stdout)


CASOS_NODE = [(h, s, largo) for h in range(g.MEMORIA_MAX + 1)
              for s, largo in ((m.SEMILLAS[f"generar-{h}"], m.LARGO_GENERAR), (0, 80),
                               (1, 80), (2 ** 40 + 7, 80), (123456789, 400))]


def test_el_js_escribe_lo_mismo_que_markov_generar(html, tmp_path):
    casos = [list(c) for c in CASOS_NODE]
    textos = _correr(html, f"console.log(JSON.stringify({json.dumps(casos)}.map("
                           "([h, s, n]) => L.generar(T, h, s, n).texto)));", tmp_path)
    for (h, s, largo), texto in zip(CASOS_NODE, textos):
        assert texto == m.generar(h, largo=largo, semilla=s), (h, s, largo)


def test_el_js_sortea_igual_que_random_random(html, tmp_path):
    import random
    numeros = _correr(html, "const r = new L.PyRandom(2034); const a = [];"
                            "for (let i = 0; i < 1000; i++) a.push(r.random());"
                            "console.log(JSON.stringify(a));", tmp_path)
    rng = random.Random(2034)
    assert numeros == [rng.random() for _ in range(1000)]


def test_un_contexto_nunca_visto_usa_la_fila_uniforme(html, tmp_path):
    """Con una tabla de memoria 2 vacia, todo contexto es nunca visto: el JS
    tiene que escribir lo mismo que markov.generar_desde con la tabla vacia
    (fila uniforme 1/28, sin reiniciar)."""
    import random
    salida = _correr(html, "const vacias = [T[0], T[1], new Map()];"
                           "const c = L.generar(vacias, 2, 99, 120);"
                           "console.log(JSON.stringify([c.texto, c.pasos.every(p => !p.fila.vista)]));",
                     tmp_path)
    esperado = m.generar_desde({}, m.ALFABETO, m.CONTEXTO_INICIAL[:2], 118, random.Random(99))
    assert salida == [esperado, True]


# ---------------------------------------------------------- la captura ---

def test_la_captura_es_del_html_de_hoy():
    huella = json.loads(v.HUELLA.read_text(encoding="utf-8"))
    assert huella["sha256"] == v.huella_html(), (
        "generador_texto.html cambió desde la última captura: corre "
        "`uv run --python 3.12 --with playwright --with pillow python tools/gen_vista_generador.py`")
    assert (huella["vista"]["archivo"], huella["vista"]["fragmento"]) == v.VISTA
    assert huella["html"] == str(HTML.relative_to(g.RAIZ))


def test_la_captura_tiene_la_forma_esperada():
    ruta = HTML.parent / v.VISTA[0]
    img = Image.open(ruta)
    assert img.width == v.ANCHO and 400 <= img.height <= v.ALTO
    assert img.mode == "P", "sin reducir a 256 colores pesa el triple"
    assert ruta.stat().st_size < 150_000
    assert img.convert("RGB").getpixel((2, 2)) == FONDO_PAGINA


def test_el_fragmento_de_la_captura_lo_entiende_la_pagina(html):
    fragmento = v.VISTA[1]
    claves = dict(p.split("=") for p in fragmento.split("&"))
    assert set(claves) == {"h", "semilla", "largo", "paso"}
    assert 0 <= int(claves["h"]) <= g.MEMORIA_MAX
    assert int(claves["semilla"]) == m.SEMILLAS[f"generar-{claves['h']}"]
    for clave in claves:
        assert f'q.get("{clave}")' in html or f'q.has("{clave}")' in html, clave
