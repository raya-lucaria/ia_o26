"""La traza interactiva del arbol T muestra los pasos que juegos.py da hoy.

course/7_juegos/_assets/traza_arbol_t.html lleva incrustados, entre dos
marcas, los pasos de cada algoritmo que escribe tools/gen_traza_web.py desde
juegos.pasos_interactivos(). A diferencia de las pruebas de los generadores
de SVG, esta NO regenera: compara el bloque comiteado con lo que el
generador produciria hoy, asi que un cambio en juegos.py sin volver a correr
el generador falla aqui en vez de publicarse en silencio.
"""
import json
import re

import pytest

import gen_traza_web as g

HTML = g.HTML
TOPE_BYTES = 60_000


@pytest.fixture(scope="module")
def html():
    return HTML.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def incrustado(html):
    return json.loads(g.bloque_incrustado(html))


def test_el_bloque_incrustado_es_el_que_daria_hoy_pasos_interactivos(html):
    esperado = g.serializar(g.compactar(g.trazas_de_hoy()))
    assert g.bloque_incrustado(html) == esperado, (
        "el JSON de traza_arbol_t.html ya no coincide con juegos.pasos_interactivos(): "
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
