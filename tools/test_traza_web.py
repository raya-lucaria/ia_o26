"""La traza interactiva del arbol T muestra los pasos que juegos.py da hoy.

course/7_juegos/_assets/traza_arbol_t.html lleva incrustados, entre dos
marcas, los pasos de cada algoritmo que escribe tools/gen_traza_web.py desde
juegos.pasos_por_linea(): un paso por cada linea del pseudocodigo que se
ejecuta. A diferencia de las pruebas de los generadores de SVG, esta NO
regenera: compara el bloque comiteado con lo que el generador produciria
hoy, asi que un cambio en juegos.py sin volver a correr el generador falla
aqui en vez de publicarse en silencio.

El tope de peso (TOPE_BYTES, 150 KB) existe para que la pagina siga cargando
al instante en un telefono. Era de 80 KB cuando un paso era una fila de la
tabla (~60 KB); al pasar a un paso por linea (777 pasos en vez de 145, cada
uno con su pila de llamadas) la pagina pesa ~128 KB aun compactada: ~92 KB de
datos y ~36 KB de estilo y codigo. Si un dia se llena, la salida no es subir
el tope a ciegas: es sacar el JSON a un archivo aparte en _assets/
(traza_arbol_t.json) que la pagina lea con fetch, y que esta prueba compare
igual que hoy compara el bloque incrustado. Ojo: fetch no funciona abriendo
el HTML como file://, por eso hoy los datos van dentro.

Las ultimas pruebas abren la pagina en un Chrome/Chromium sin pantalla
(--dump-dom) y leen lo que el JavaScript pinto en varios pasos, incluidos los
que enlazan las paginas (#alfa-beta-fila-12, #alfa-beta-fila-8: -fila-N
abre en el paso que cierra la fila N; -paso-K es el paso K). Se saltan si
no hay navegador, como en CI.
"""
import html as html_mod
import json
import re
import shutil
import subprocess

import pytest

import gen_traza_web as g

HTML = g.HTML
TOPE_BYTES = 150_000


@pytest.fixture(scope="module")
def html():
    return HTML.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def incrustado(html):
    return json.loads(g.bloque_incrustado(html))


def test_el_bloque_incrustado_es_el_que_daria_hoy_pasos_por_linea(html):
    esperado = g.serializar(g.compactar(g.trazas_de_hoy()))
    assert g.bloque_incrustado(html) == esperado, (
        "el JSON de traza_arbol_t.html ya no coincide con juegos.pasos_por_linea(): "
        "corre python3 tools/gen_traza_web.py y comitea el HTML"
    )


def test_la_compactacion_no_pierde_nada_de_lo_que_la_pagina_usa(incrustado):
    assert g.expandir(incrustado) == g.sin_fuera(g.trazas_de_hoy())


@pytest.mark.parametrize("clave,modo,variante", g.MODOS)
def test_cada_modo_y_variante_esta_en_la_pagina(incrustado, clave, modo, variante):
    t = incrustado["trazas"][clave]
    assert t["modo"] == modo
    assert t["variante"] == variante
    assert t["pasos"], f"{clave} no tiene pasos"


def test_cada_fragmento_de_url_lleva_a_una_traza_que_existe(html, incrustado):
    de_frag = json.loads(re.search(r"const DE_FRAG = (\{.*?\});", html, re.S).group(1))
    for frag in ("minimax", "azar", "alfa-beta", "alfa-beta-t1", "corte", "corte-d1",
                 "corte-d3", "iterativa"):
        assert de_frag.get(frag) in incrustado["trazas"], frag
    assert set(de_frag.values()) == set(incrustado["trazas"])


def test_no_carga_nada_de_fuera(html):
    assert not re.search(r"""(?:src|href)\s*=\s*["']?\s*(?:https?:)?//""", html, re.I)
    assert not re.search(r"@import|url\(\s*['\"]?(?:https?:)?//", html, re.I)
    for cdn in ("cdn", "unpkg", "jsdelivr", "googleapis", "cloudflare"):
        assert cdn not in html.lower(), cdn


def test_pesa_menos_que_el_tope(html):
    peso = len(html.encode("utf-8"))
    assert peso < TOPE_BYTES, f"traza_arbol_t.html pesa {peso} bytes (tope {TOPE_BYTES})"


def test_copia_la_paleta_del_skin_y_declara_idioma_y_titulo(html):
    assert "--surface:#211033" in html
    assert '<html lang="es">' in html
    assert re.search(r"<title>[^<]+</title>", html)


def test_el_generador_es_idempotente(html):
    datos = g.compactar(g.trazas_de_hoy())
    una = g.incrustar(html, datos)
    assert g.incrustar(una, datos) == una


NAVEGADOR = next((shutil.which(n) for n in ("google-chrome", "google-chrome-stable",
                                            "chromium", "chromium-browser", "chrome")
                  if shutil.which(n)), None)

def _filas(t):
    return max([p["fila"] for p in t["pasos"]] + [x for p in t["pasos"] for x in p["filas_x"]])


def _paso_de_fila(pasos, fila):
    """El paso de linea en que se cierra la fila `fila` de la tabla."""
    return max(k for k, p in enumerate(pasos, 1) if p["fila"] == fila or fila in p["filas_x"])


# (fragmento, clave de la traza, paso de linea que debe abrir, texto que
# debe aparecer en la frase)
CASOS_DOM = [
    # los dos enlaces de 5_alfa_beta_como_algoritmo: -fila-N
    ("alfa-beta-fila-12", "alfa-beta-T", ("fila", 12), "corte beta"),
    ("alfa-beta-fila-8", "alfa-beta-T", ("fila", 8), "α ← max(3, 5) = 5"),
    # una fila ✗ abre en el return del corte que la deja fuera
    ("iterativa-fila-34", "iterativa", ("fila", 34), "corte alfa"),
    # -paso-K: el paso K, la K-esima linea que corre (-linea-K es su alias)
    ("alfa-beta-paso-2", "alfa-beta-T", ("paso", 2), "α ← −∞"),
    ("alfa-beta-linea-5", "alfa-beta-T", ("paso", 5), "Entra a ALFA-BETA"),
    ("corte-d1-paso-10", "corte-1", ("paso", 10), None),
    # el ultimo paso: la frase lleva el resultado dentro
    ("azar-paso-108", "azar", ("paso", 108), "return mejor_jugada = der"),
]


def _dom(fragmento):
    salida = subprocess.run(
        [NAVEGADOR, "--headless=new", "--disable-gpu", "--no-sandbox", "--dump-dom",
         f"{HTML.as_uri()}#{fragmento}"],
        capture_output=True, text=True, timeout=60, check=True)
    return salida.stdout


def test_los_enlaces_de_las_paginas_abren_lo_que_prometen():
    """5_alfa_beta_como_algoritmo promete «el corte beta de C2» y «C y C1 a
    la vez en la pila, C1 sube su α en la línea 15»."""
    pagina = (g.RAIZ / "course/7_juegos/2_mirar_todo_y_podar/5_alfa_beta_como_algoritmo.md"
              ).read_text(encoding="utf-8")
    enlaces = re.findall(r"traza_arbol_t\.html#([\w-]+)\)", pagina)
    assert "alfa-beta-fila-12" in enlaces and "alfa-beta-fila-8" in enlaces
    # -paso-N ya no es fila: ningun enlace de la unidad debe usarlo como tal
    for md in (g.RAIZ / "course/7_juegos").rglob("*.md"):
        assert not re.search(r"traza_arbol_t\.html#[\w-]+-paso-\d", md.read_text(encoding="utf-8")), md
    pasos = g.trazas_de_hoy()["alfa-beta-T"]["pasos"]
    p = pasos[_paso_de_fila(pasos, 12) - 1]
    assert p["nodo"] == "C2" and p["linea"] == 14 and "corte beta" in p["frase"]
    p = pasos[_paso_de_fila(pasos, 8) - 1]
    assert p["linea"] == 15 and [m["nodo"] for m in p["marco"]] == ["R", "C", "C1"]


@pytest.mark.skipif(NAVEGADOR is None, reason="no hay Chrome ni Chromium")
@pytest.mark.parametrize("fragmento,clave,cual,frase", CASOS_DOM)
def test_la_pagina_pinta_el_paso_pedido(fragmento, clave, cual, frase):
    t = g.trazas_de_hoy()[clave]
    n = _paso_de_fila(t["pasos"], cual[1]) if cual[0] == "fila" else cual[1]
    p = t["pasos"][n - 1]
    dom = _dom(fragmento)

    cuenta = re.search(r'id="cuenta"[^>]*>([^<]*)<', dom).group(1)
    assert cuenta == f"Paso {n} de {len(t['pasos'])} · fila {p['fila']} de {_filas(t)}"

    texto_frase = dom[dom.index('id="frase"'):dom.index('id="col-pseudo"')]
    assert f">línea {p['linea']}<" in texto_frase
    assert html_mod.escape(p["frase"], quote=False) in texto_frase
    if frase:
        assert html_mod.escape(frase, quote=False) in texto_frase

    # una sola linea del pseudocodigo marcada: la que corre (con `parcial`,
    # solo su primer renglon impreso)
    marcadas = [int(r) for r in re.findall(r'<div class="lin aqui" data-r="(\d+)"', dom)]
    assert set(marcadas) == {p["linea"]}
    assert len(marcadas) == (1 if p["parcial"] else t["renglones"].count(p["linea"]))

    # la pila: una tarjeta por marco, la actual con su tabla de variables
    pila = dom[dom.index('id="pila"'):dom.index('id="col-arbol"')]
    assert pila.count('<li class="marco') == len(p["marco"])
    assert pila.count('<li class="marco actual"') == 1
    locales = dict(p["marco"][-1]["locales"])
    for k in locales:
        assert f"<td>{html_mod.escape(k, quote=False)}" in pila
    # una fila marcada por variable que la linea cambio de verdad; reasignar
    # el mismo valor se dice («se reasignó, igual») pero no se marca
    cambiadas = [k for i, k, antes in p["cambia"]
                 if i == len(p["marco"]) - 1 and k in locales and antes != locales[k]]
    assert pila.count('<tr class="cambia">') == len(cambiadas)
    for k in cambiadas:
        assert re.search(r'<tr class="cambia"><td>' + re.escape(k) + " <span", pila), k

    arbol = dom[dom.index('id="arbol"'):dom.index('id="leyenda"')]
    podados = sum(1 for e in p["estado"].values() if e["estado"] == "podado")
    assert arbol.count(">?</text>") == podados
