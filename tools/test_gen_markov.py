"""Guardas de los diagramas de la unidad de cadenas de Markov.

Clase de prueba «compara sin escribir» (.claude/skills/unidad/referencias/
codigo.md § 3): contenido(nombre) se compara byte a byte con el SVG
comiteado, sin escribirlo. Si alguien edita un SVG a mano, o cambia
markov.py sin volver a correr el generador, la prueba falla con «corre el
generador».

Ademas, las convenciones de test_gen_juegos.py con ANCHO = 300: prefijo,
raiz <svg> con viewBox/width/height/aria-label, fondo del skin, <title> y
<desc>, sin opacidades, XML valido, sin huerfanos, sin SVG que ninguna pagina
use, letra de 12 px o mas, nada fuera del lienzo y ningun rotulo encimado
sobre otro. Y que lo dibujado salga de markov.py.
"""
import html
import os
import re
import xml.etree.ElementTree as ET
from functools import lru_cache

import pytest

import gen_markov as gen
import markov as m

FONDO = "#211033"
ANCHO = 300
UNIDAD = gen.ASSETS.parent
NOMBRES = sorted(gen.DIAGRAMAS)
_DEJAVU = "/usr/share/fonts/truetype/dejavu/"

# Clase 3: las figuras propias del plan (§4) y las claves del manifiesto de
# ejemplo y contraejemplo (§5), escritas a mano para que el catalogo no pueda
# perder ni inventar una.
FIGURAS_C3 = (
    "punto-fijo", "escalera", "escalera-arbol-vs-grafo", "flujo-hacia-atras", "pasillo",
    "pasillo-mdp", "politica-elige-filas", "cuatro-cadenas", "flujo-evaluar",
    "cuatro-politicas-plano", "simular-politica", "bellman-1d", "fronteras", "flujo-valores",
    "iterar-valores", "residuo", "pasillo-largo", "flujo-politicas", "rondas-politicas",
    "region-lp", "mapa-decidir")
CLAVES_C3 = ("punto-fijo", "hacia-atras", "mdp", "termina", "evaluar", "bellman", "codiciosa",
             "paro", "empates", "lineal")


@lru_cache(maxsize=None)
def _svg(nombre):
    return gen.contenido(nombre)


def _aria(nombre):
    return html.unescape(re.search(r'aria-label="([^"]*)"', _svg(nombre)).group(1))


def _renglones(nombre):
    return [html.unescape(t) for t in re.findall(r">([^<>]+)</text>", _svg(nombre))]


# ------------------------------------------------------ el archivo ---

@pytest.mark.parametrize("nombre", NOMBRES)
def test_cada_svg_es_el_que_produce_el_generador(nombre):
    archivo = gen.ASSETS / f"{nombre}.svg"
    assert archivo.is_file(), f"falta {archivo.name}: corre python3 tools/gen_markov.py"
    assert archivo.read_text(encoding="utf-8") == _svg(nombre), (
        f"{archivo.name} no es el que produce el generador: corre "
        "python3 tools/gen_markov.py y revisa el diff")


def test_cada_diagrama_lleva_el_prefijo_de_la_clase():
    assert all(re.match(r"mkv-c[123]-", n) for n in NOMBRES)


def test_estan_las_figuras_de_prioridad_1_y_la_de_rachas():
    assert set(NOMBRES) == {
        "mkv-c1-flujo-muestrear", "mkv-c1-flujo-contar", "mkv-c1-flujo-predecir",
        "mkv-c1-flujo-generar", "mkv-c1-grafo-vc", "mkv-c1-arbol-2-pasos",
        "mkv-c1-mu-t", "mkv-c1-recuperar-p", "mkv-c1-ceros", "mkv-c1-rachas",
        "mkv-c2-grafo-clasificar", "mkv-c2-grafo-contraejemplos", "mkv-c2-mu-t-inicios",
        "mkv-c2-flujo-potencias", "mkv-c2-tablero-chico", "mkv-c2-flujo-absorcion",
        "mkv-c2-web-juguete"} | {f"mkv-c2-ej-{c}" for c in gen.EJEMPLOS} | {
        f"mkv-c3-{n}" for n in FIGURAS_C3} | {f"mkv-c3-ej-{c}" for c in CLAVES_C3}


def test_hay_un_ejemplo_por_definicion_y_teorema_de_las_paginas_2_y_3():
    """Cada definicion y teorema de clasificar-estados y la-estacionaria tiene
    su recuadro «Ejemplo y contraejemplo» y, debajo, su figura."""
    for pagina, n in (("2_clasificar_estados.md", 8), ("3_la_estacionaria.md", 6)):
        texto = (UNIDAD / "2_a_la_larga" / pagina).read_text(encoding="utf-8")
        assert texto.count("> **Ejemplo y contraejemplo.**") == n, pagina
        claves = [c for c, e in gen.EJEMPLOS.items() if e["pagina"] == pagina]
        assert len(claves) == n, pagina
        for c in claves:
            assert f"](../_assets/mkv-c2-ej-{c}.svg)" in texto, (pagina, c)


@pytest.mark.parametrize("clave", sorted(gen.EJEMPLOS))
def test_la_matriz_dibujada_es_la_del_recuadro(clave):
    """La figura no puede contar otra cadena que el texto: cada matriz finita
    que dibuja aparece, igual, en el recuadro de su pagina, justo arriba."""
    e = gen.EJEMPLOS[clave]
    texto = (UNIDAD / "2_a_la_larga" / e["pagina"]).read_text(encoding="utf-8")
    figura = texto.index(f"mkv-c2-ej-{clave}.svg")
    recuadro = texto[texto.rindex("> **Ejemplo y contraejemplo.**", 0, figura):figura]
    for lado in ("si", "no"):
        panel = e[lado][0]
        if isinstance(panel, dict):
            assert gen.matriz_latex(panel["P"]) in recuadro, (clave, lado)


@pytest.mark.parametrize("nombre", NOMBRES)
def test_la_raiz_svg_trae_sus_convenciones(nombre):
    texto = _svg(nombre)
    etiqueta = re.match(r"<svg\b[^>]*>", texto).group()
    for atributo in ('viewBox="', 'role="img"', "aria-label="):
        assert atributo in etiqueta, (nombre, atributo)
    assert re.search(r'\bwidth="\d', etiqueta) and re.search(r'\bheight="\d', etiqueta)
    assert f'fill="{FONDO}"' in texto
    assert "<title>" in texto and "<desc>" in texto
    assert "fill-opacity" not in texto and "stroke-opacity" not in texto
    ET.fromstring(texto)


@pytest.mark.parametrize("nombre", NOMBRES)
def test_todas_miden_300_de_ancho(nombre):
    """Plan de unidad §6: 300 px caben en un telefono de 390 sin deslizar."""
    etiqueta = re.match(r"<svg\b[^>]*>", _svg(nombre)).group()
    ancho = float(re.search(r'\bwidth="([\d.]+)"', etiqueta).group(1))
    caja = re.search(r'viewBox="0 0 ([\d.]+) ', etiqueta).group(1)
    assert ancho == ANCHO == float(caja), nombre


@pytest.mark.parametrize("nombre", NOMBRES)
def test_ninguna_letra_baja_de_12(nombre):
    chicas = [(t, c) for t, c in re.findall(
        r'<text [^>]*font-size="([\d.]+)"[^>]*>([^<]*)<', _svg(nombre)) if float(t) < 12]
    assert not chicas, (nombre, chicas)


def test_no_queda_ningun_svg_huerfano():
    en_disco = {p.stem for p in gen.ASSETS.glob("mkv-*.svg")}
    assert en_disco == set(gen.DIAGRAMAS)


def test_ningun_svg_sin_pagina_que_lo_use():
    paginas = "\n".join(
        p.read_text(encoding="utf-8") for p in UNIDAD.rglob("*.md")
        if not any(parte.startswith("_") for parte in p.relative_to(UNIDAD).parts))
    sin_usar = sorted(f"{n}.svg" for n in gen.DIAGRAMAS if f"{n}.svg" not in paginas)
    assert not sin_usar, f"SVG que ninguna pagina enlaza: {sin_usar}"


# ------------------------------------------------- nada se encima ---

_PATRON_TEXTO = (r'<text x="([\d.-]+)" y="([\d.-]+)"[^>]*font-family="([^"]*)" '
                 r'font-size="([\d.]+)" font-weight="(\w+)" text-anchor="(\w+)">([^<]*)</text>')


def _cajas_de_texto(nombre):
    """(x0, y0, x1, y1, texto) de cada <text> sin girar, medido con DejaVu (la
    letra con que el navegador de esta maquina resuelve system-ui)."""
    ImageFont = pytest.importorskip("PIL.ImageFont")
    if not os.path.isdir(_DEJAVU):
        pytest.skip("sin DejaVu")
    cajas = []
    for x, y, familia, tam, peso, anclaje, contenido in re.findall(_PATRON_TEXTO, _svg(nombre)):
        archivo = (("DejaVuSansMono" if "mono" in familia else "DejaVuSans")
                   + ("-Bold" if peso == "700" else "") + ".ttf")
        t = float(tam)
        s = html.unescape(contenido)
        w = ImageFont.truetype(_DEJAVU + archivo, round(t)).getlength(s)
        x, y = float(x), float(y)
        x0 = {"start": x, "middle": x - w / 2, "end": x - w}[anclaje]
        cajas.append((x0, y - 0.75 * t, x0 + w, y + 0.22 * t, s))
    return cajas


@pytest.mark.parametrize("nombre", NOMBRES)
def test_nada_se_sale_del_lienzo(nombre):
    alto = float(re.search(r'height="([\d.]+)"', _svg(nombre)).group(1))
    for x0, y0, x1, y1, s in _cajas_de_texto(nombre):
        assert 4 <= x0 and x1 <= ANCHO - 4, (nombre, s, round(x0), round(x1))
        assert 0 <= y0 and y1 <= alto, (nombre, s)


@pytest.mark.parametrize("nombre", NOMBRES)
def test_ningun_rotulo_se_encima_sobre_otro(nombre):
    """Se publico «el va▮lor» en juegos (defecto 6): aqui ningun par de
    rotulos sin girar comparte un pixel."""
    cajas = _cajas_de_texto(nombre)
    for i, a in enumerate(cajas):
        for b in cajas[i + 1:]:
            se_tocan = (a[0] < b[2] - 0.5 and b[0] < a[2] - 0.5
                        and a[1] < b[3] - 0.5 and b[1] < a[3] - 0.5)
            assert not se_tocan, (nombre, a[4], b[4])


# ------------------------------------- lo dibujado sale de markov.py ---

def _fr(x):
    return gen.fr(x)


def test_el_grafo_dibuja_la_matriz_de_la_frase():
    P = m.matriz_estimada(m.frase_vc())
    assert [[_fr(x) for x in f] for f in P] == [["2/11", "9/11"], ["2/3", "1/3"]]
    renglones = _renglones("mkv-c1-grafo-vc")
    for rot in ("2/11", "9/11", "2/3", "1/3"):
        assert rot in renglones, rot
    aria = _aria("mkv-c1-grafo-vc")
    assert "a V con 2/11" in aria and "a C con 9/11" in aria
    assert "a V con 2/3" in aria and "a C con 1/3" in aria


def test_el_arbol_dibuja_los_cuatro_caminos_y_su_suma():
    renglones = _renglones("mkv-c1-arbol-2-pasos")
    for hoja in ("4/33", "6/11", "2/9", "1/9"):
        assert hoja in renglones, hoja
    assert "4/33 + 2/9 = 34/99." in renglones
    assert "Pr(S₂ = V) = 4/33 + 2/9 = 34/99." in _aria("mkv-c1-arbol-2-pasos")


def test_mu_t_dibuja_la_cuenta_y_la_simulacion():
    datos = m.mu_t_corpus()
    aria = _aria("mkv-c1-mu-t")
    assert "10 000 réplicas" in aria
    # la cuenta desde C, a mano: 0, 0.710, 0.334, 0.533…
    assert "Desde C: cuenta 0.000, 0.710, 0.334, 0.533, 0.428, 0.484, 0.454, 0.470, 0.462" \
        in aria
    assert "Desde V: cuenta 1.000, 0.181, 0.615, 0.385, 0.507, 0.442, 0.476, 0.458, 0.468" \
        in aria
    for d in datos.values():
        assert ", ".join(gen.dec(p) for p in d["simulada"]) in aria
    assert "la mayor diferencia es 0.010, unos 2.0 errores estándar" in aria
    # una marca por paso y por inicio en cada panel: 9 x 2 x 2
    svg = _svg("mkv-c1-mu-t")
    assert svg.count("<circle") == 9 * 2 + 1 and svg.count('<rect x="') >= 9 * 2


def test_recuperar_p_dibuja_las_siete_longitudes():
    aria = _aria("mkv-c1-recuperar-p")
    for T in ("10", "30", "100", "300", "1 000", "3 000", "10 000"):
        assert f"T = {T}: mediana" in aria, T
    assert "T = 10: mediana 0.210, del 5 % al 95 % entre 0.069 y 0.319" in aria
    assert "T = 10 000: mediana 0.006, del 5 % al 95 % entre 0.002 y 0.013" in aria
    assert "Réplicas con un estado sin salidas: 0." in aria


def test_ceros_dibuja_las_cuatro_memorias():
    aria = _aria("mkv-c1-ceros")
    assert "memoria 0: 0 % (0 de 998 564)" in aria
    assert "memoria 1: 0.003 % (29 de 998 563), contextos vistos 27 de 28" in aria
    assert "memoria 2: 0.072 % (718 de 998 562), contextos vistos 379 de 784" in aria
    assert "memoria 3: 0.570 % (5 694 de 998 561), contextos vistos 3 328 de 21 952" in aria


def test_rachas_dibuja_reales_y_los_dos_modelos():
    aria = _aria("mkv-c1-rachas")
    assert "q = 0.290 (rombos)" in aria and "q = 0.536 (triángulos)" in aria
    assert "ℓ = 1: reales 384 971" in aria
    assert "ℓ = 4: reales 323" in aria and "ℓ = 5: reales 3," in aria
    reales = m.rachas_corpus()
    sim = m.rachas_simuladas("markov")
    for ell in range(1, 6):
        assert f"ℓ = {ell}: reales {gen.miles(reales.get(ell, 0))}, cadena " \
               f"{gen.miles(sim[ell][0])}" in aria
    # marcas distintas, no solo color, y que no son las de V y C (círculo y
    # cuadrado): rombo (cadena) y triángulo (independientes)
    svg = _svg("mkv-c1-rachas")
    assert svg.count("<circle") == 0
    assert svg.count("<polygon") == 2 * (5 + 1)


@pytest.mark.parametrize("clave", sorted(gen.FLUJOS))
def test_cada_flujo_tiene_rombo_y_salida_explicita(clave):
    """Cajas con verbos cortos, una decision por rombo, una sola salida (la
    caja de borde de acento) y al menos una vuelta. Excepcion: el tiempo
    medio de llegada (clase 2) resuelve un sistema de una vez: no da vueltas
    y tiene dos salidas (m, o el aviso de que desde algun estado no se
    llega), igual que evaluar una politica (clase 3). Y la iteracion de potencias (clase 2) tiene dos salidas porque
    distingue parar por tolerancia de llegar al tope sin parar."""
    f = gen.FLUJOS[clave]
    cajas = [p for p in f["pasos"] if "caja" in p]
    rombos = [p for p in f["pasos"] if "rombo" in p]
    sin_vuelta = clave in ("absorcion", "evaluar")
    assert 3 <= len(cajas) <= 6 and rombos and (f["vueltas"] or sin_vuelta)
    dos_salidas = sin_vuelta or clave == "potencias"
    assert [p.get("fin") for p in f["pasos"]].count(True) == (2 if dos_salidas else 1)
    assert f["pasos"][-1].get("fin")
    nombre = next(n for n in gen.DIAGRAMAS if n.endswith(f"-flujo-{clave}"))
    svg = gen.contenido(nombre)
    assert svg.count("<polygon") == len(rombos)


# ------------------------------------------------------------ clase 3 ---

NOMBRES_C3 = [n for n in NOMBRES if n.startswith("mkv-c3-")]


def test_el_manifiesto_de_la_clase_3_es_el_del_plan():
    assert set(gen.EJEMPLOS_C3) == set(CLAVES_C3)


@pytest.mark.parametrize("clave", CLAVES_C3)
def test_cada_ejemplo_de_la_clase_3_tiene_sus_dos_paneles(clave):
    renglones = _renglones(f"mkv-c3-ej-{clave}")
    assert renglones.count("✓ Lo cumple") == 1 and renglones.count("✗ No lo cumple") == 1
    aria = _aria(f"mkv-c3-ej-{clave}")
    assert aria.startswith("Lo cumple: ") and " No lo cumple: " in aria


@pytest.mark.parametrize("nombre", NOMBRES_C3)
def test_la_clase_3_respeta_la_notacion_del_plan(nombre):
    """Plan §2: V(1), nunca V con subindice; politicas en palabras, nunca
    CC/CR; ningun guion bajo de LaTeX en un rotulo."""
    texto = " ".join(_renglones(nombre)) + " " + _aria(nombre)
    for prohibido in ("V₁", "V₂", "V_", "r_", "P_", "CC", "CR", "\\"):
        assert prohibido not in texto, (nombre, prohibido)
    assert not re.search(r"V\(\d\)\s*=\s*-", texto), nombre    # menos tipografico


def test_el_mdp_dibuja_las_matrices_de_markov_py():
    J = m.pasillo()
    aria = _aria("mkv-c3-pasillo-mdp")
    for a in (m.CAMINAR, m.CORRER):
        filas = "; ".join(", ".join(gen._v(x) for x in f) for f in m.matriz_accion(J, a))
        assert filas in aria, a
    assert "en 1, correr (r = −6): se queda con 1/2, a 2 con 1/2" in aria


def test_las_cuatro_politicas_llevan_su_valor():
    J = m.pasillo()
    for figura in ("mkv-c3-cuatro-cadenas", "mkv-c3-cuatro-politicas-plano"):
        aria = _aria(figura)
        for nombre, pol in m.POLITICAS_J2.items():
            V = m.evaluar_politica(J, pol)
            assert nombre in aria
            assert f"({gen._v(V[1])}, {gen._v(V[2])})" in aria or \
                f"V(1) = {gen._v(V[1])}, V(2) = {gen._v(V[2])}" in aria, (figura, nombre)
    assert "(−5, −2)" in _aria("mkv-c3-cuatro-politicas-plano")


def test_el_paro_dice_cuantas_veces_el_residuo():
    """Correccion del plan: en el pasillo el error es igual al residuo desde
    la ronda 2; en el lazo 99/100 es 99 veces."""
    J = m.pasillo()
    Vs = m.evaluar_politica(J, m.POLITICAS_J2["caminar–correr"])
    traza = m.iterar_valores(J, rondas=10)
    err, res = m.errores(traza, Vs)[1:], m.residuos(traza)
    assert all(e == r for e, r in zip(err[1:], res[1:]))
    renglones = _renglones("mkv-c3-ej-paro")
    assert "el pasillo: error = residuo desde t = 2" in renglones
    assert "lazo 99/100: error = 99 × residuo" in renglones


def test_la_codiciosa_elige_lo_que_dice_markov_py():
    J = m.pasillo()
    aria = _aria("mkv-c3-ej-codiciosa")
    Vs = m.evaluar_politica(J, m.POLITICAS_J2["caminar–correr"])
    assert gen._nombre_pol(m.codiciosa(J, Vs)) == "caminar–correr"
    assert gen._nombre_pol(m.codiciosa(J, {1: -8, 2: -8})) == "caminar–caminar"
    assert "La codiciosa elige caminar–correr" in aria
    assert "La codiciosa elige caminar–caminar" in aria
    assert "en 1, caminar vale −11; en 1, correr vale −14" in aria


def test_el_programa_lineal_y_la_simulacion_salen_de_markov_py():
    assert "el mínimo: (−5, −2) = V*" in _renglones("mkv-c3-region-lp")
    aria = _aria("mkv-c3-ej-lineal")
    assert "V* = (0, 0)" in aria and "(−5, −2)" in aria
    media, ee = m.resumen_simulacion()
    aria = _aria("mkv-c3-simular-politica")
    assert f"Media {gen._vd(media)}, error estándar {gen._vd(ee)}" in aria
    assert "V(1) = −5" in aria
    d = m.pasillo_largo()
    assert f"V*(1) = {gen._aprox(d['v_inicio'])}" in _aria("mkv-c3-pasillo-largo")
    assert f"{gen.miles(d['rondas_vi'])} rondas" in _aria("mkv-c3-rondas-politicas")


def test_la_escalera_dibuja_las_cifras_de_markov_py():
    aria = _aria("mkv-c3-escalera")
    assert "4, 4, 2, 1, 1, 0" in aria
    assert "0 → 2 → 4 → 5 y paga 4" in aria and "0 → 1 → 2 → 4 → 5 y paga 5" in aria
    assert "8, 5, 3, 2, 1, 1" in _aria("mkv-c3-escalera-arbol-vs-grafo")
