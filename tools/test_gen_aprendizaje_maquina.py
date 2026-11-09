"""Guardas comunes del generador de figuras de la unidad 9 (contrato §7.1).

Dos grupos:

1. **Sin la unidad** (corren siempre, tambien en la subrama de U.T3): el
   catalogo (seis modulos de clase, prefijos, ids unicos), las convenciones
   de cada SVG que produce el generador (raiz <svg> sin prologo que pasa
   **la misma** guarda test_9 de test_aceptacion.py, importada y no copiada;
   XML valido; ancho <= 600; letra >= 12 px; sin opacidades; determinista),
   el posproceso de matplotlib, los roles de §7.3, la CLI con ML_CLASES y la
   importacion perezosa de ml_lab.
2. **Con la unidad** (se SALTAN si no existe course/9_aprendizaje_maquina/ o
   su _assets/CREDITOS.md; contrato §8.3, plan maestro §3 F2(i)): compara
   sin escribir, sin huerfanos, fila en CREDITOS.md, y que cada figura del
   catalogo la use alguna pagina dentro de un `::: figure` con el mismo id
   (esta ultima lee prosa: en una rama de clase solo pasa en S2).

Con ML_CLASES puesta (p. ej. ML_CLASES=2 en S2 de la clase 2), el grupo 2
se restringe a esas clases, igual que el generador.
"""
import html
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

import gen_aprendizaje_maquina as gen
import test_aceptacion

TOOLS = Path(__file__).resolve().parent
NOMBRES = sorted(gen.figuras())
CREDITOS = gen.ASSETS_ML / "CREDITOS.md"


def _guarda_test_9(tmp_path, monkeypatch, nombre, texto):
    """Pasa un SVG por test_9 de test_aceptacion.py tal cual: se le da un
    ASSETS_POR_UNIDAD con un solo directorio que contiene solo ese SVG."""
    d = tmp_path / "assets"
    d.mkdir(exist_ok=True)
    (d / f"{nombre}.svg").write_text(texto, encoding="utf-8")
    monkeypatch.setattr(test_aceptacion, "ASSETS_POR_UNIDAD", {"aprendizaje-maquina": d})
    test_aceptacion.test_9_los_diagramas_svg_son_legibles_sobre_el_fondo_oscuro_del_skin()


# ------------------------------------------------------------ catalogo ---

def test_los_seis_modulos_de_clase_estan_en_la_lista_fija():
    assert gen.MODULOS_FIGURAS == [f"figuras_ml_c{n}" for n in range(6)]
    for n in range(6):
        assert (TOOLS / f"figuras_ml_c{n}.py").is_file(), f"falta figuras_ml_c{n}.py"


def test_cada_modulo_de_clase_exporta_su_catalogo():
    catalogos = gen.figuras_por_clave()
    assert set(catalogos) == {"u", 0, 1, 2, 3, 4, 5}
    for clave, catalogo in catalogos.items():
        assert isinstance(catalogo, dict), clave


def test_un_modulo_que_falta_es_un_error_no_un_catalogo_vacio():
    with pytest.raises(ModuleNotFoundError):
        gen.cargar_catalogos(["figuras_ml_c0", "figuras_ml_c7"])


def test_un_id_repetido_entre_catalogos_falla():
    f = lambda: ""  # noqa: E731
    with pytest.raises(ValueError, match="repetido"):
        gen.unir_catalogos({"u": {}, 1: {"ml-c1-x": f}, 2: {"ml-c1-x": f}})


def test_un_id_sin_el_prefijo_de_su_clase_falla():
    f = lambda: ""  # noqa: E731
    with pytest.raises(ValueError, match="empieza por"):
        gen.unir_catalogos({3: {"ml-c2-x": f}})
    with pytest.raises(ValueError, match="empieza por"):
        gen.unir_catalogos({"u": {"ml-c0-x": f}})


def test_el_mapa_de_la_unidad_esta_en_figuras_u():
    assert "ml-u-mapa" in gen.FIGURAS_U
    assert "ml-u-mapa" in gen.FIGURAS


def test_cada_id_lleva_el_prefijo_de_su_catalogo():
    for clave, catalogo in gen.figuras_por_clave().items():
        for ident in catalogo:
            assert ident.startswith(gen.prefijo(clave)), ident
            assert gen.clave_de(ident) == clave, ident


# ------------------------------------------------- convenciones del SVG ---

@pytest.mark.parametrize("nombre", NOMBRES)
def test_cada_svg_pasa_la_guarda_test_9(nombre, tmp_path, monkeypatch):
    _guarda_test_9(tmp_path, monkeypatch, nombre, gen.contenido(nombre))


@pytest.mark.parametrize("nombre", NOMBRES)
def test_cada_svg_es_xml_valido_y_trae_titulo_y_aria(nombre):
    texto = gen.contenido(nombre)
    assert texto.startswith("<svg"), f"{nombre}: el archivo no empieza con <svg"
    raiz = ET.fromstring(texto)
    assert raiz.tag.endswith("svg")
    assert raiz.get("role") == "img"
    assert raiz.get("aria-label", "").strip(), f"{nombre}: aria-label vacio"
    ns = "{http://www.w3.org/2000/svg}"
    assert raiz.find(f"{ns}title") is not None, f"{nombre}: sin <title>"


@pytest.mark.parametrize("nombre", NOMBRES)
def test_cada_svg_mide_a_lo_mas_600_y_cuadra_con_su_viewbox(nombre):
    raiz = re.match(r"<svg\b[^>]*>", gen.contenido(nombre)).group()
    ancho = float(re.search(r'\bwidth="([\d.]+)"', raiz).group(1))
    alto = float(re.search(r'\bheight="([\d.]+)"', raiz).group(1))
    _, _, vw, vh = (float(v) for v in re.search(r'viewBox="([^"]+)"', raiz).group(1).split())
    assert ancho <= gen.ANCHO_MAX, f"{nombre}: {ancho} px de ancho"
    assert abs(ancho / alto - vw / vh) < 0.01, f"{nombre}: width/height no guardan la proporcion"


@pytest.mark.parametrize("nombre", NOMBRES)
def test_la_letra_efectiva_es_de_12_px_o_mas(nombre):
    texto = gen.contenido(nombre)
    raiz = re.match(r"<svg\b[^>]*>", texto).group()
    ancho = float(re.search(r'\bwidth="([\d.]+)"', raiz).group(1))
    vw = float(re.search(r'viewBox="([^"]+)"', raiz).group(1).split()[2])
    escala = ancho / vw
    tams = [float(t) for t in re.findall(r'font-size="([\d.]+)', texto)]
    tams += [float(t) for t in re.findall(r"font(?:-size)?:\s*(?:[a-z ]*\s)?([\d.]+)px", texto)]
    assert tams, f"{nombre}: sin texto"
    assert min(tams) * escala >= gen.LETRA_MIN - 1e-9, (
        f"{nombre}: letra de {min(tams) * escala:.1f} px a {ancho:.0f} px de ancho")


@pytest.mark.parametrize("nombre", NOMBRES)
def test_ningun_svg_usa_opacidad(nombre):
    # La transparencia se hornea con gen.mezclar (contrato §7.3).
    assert not re.search(r"opacity", gen.contenido(nombre)), f"{nombre}: usa opacidad"


@pytest.mark.parametrize("nombre", NOMBRES)
def test_cada_svg_es_determinista(nombre):
    assert gen.contenido(nombre) == gen.contenido(nombre)


def test_el_mapa_no_lleva_fechas():
    # D-008: sin fechas en el contenido.
    svg = gen.contenido("ml-u-mapa")
    aria = re.search(r'aria-label="([^"]*)"', svg).group(1)
    texto = html.unescape(" ".join([aria] + re.findall(r">([^<>]+)<", svg)))
    assert not re.search(r"\b20\d\d\b|\b\d{1,2} de [a-z]+", texto)
    meses = ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
             "agosto", "septiembre", "octubre", "noviembre", "diciembre")
    assert not any(m in texto.lower() for m in meses)


def test_el_mapa_nombra_las_seis_clases_en_orden():
    renglones = [html.unescape(t) for t in re.findall(r">([^<>]+)</text>",
                                                       gen.contenido("ml-u-mapa"))]
    numeros = [r for r in renglones if re.fullmatch(r"Clase \d", r)]
    assert numeros == [f"Clase {n}" for n in range(6)]


# ----------------------------------------------------------- posproceso ---

_PROLOGO_MPL = (
    '<?xml version="1.0" encoding="utf-8" standalone="no"?>\n'
    '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n'
    '  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
    '<!-- Created with matplotlib (https://matplotlib.org/) -->\n'
    '<svg xmlns:xlink="http://www.w3.org/1999/xlink" width="460.8pt" height="345.6pt" '
    'viewBox="0 0 460.8 345.6" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'
    ' <g id="figure_1"><text x="10" y="20" style="font: 13px \'DejaVu Sans\'">a</text></g>\n'
    '</svg>\n'
)


def test_el_posproceso_quita_el_prologo_y_pasa_test_9(tmp_path, monkeypatch):
    salida = gen.posprocesar_svg(_PROLOGO_MPL, aria="una prueba", ancho=480)
    assert salida.startswith("<svg ")
    assert "<?xml" not in salida and "DOCTYPE" not in salida and "<!--" not in salida
    raiz = re.match(r"<svg\b[^>]*>", salida).group()
    assert 'width="480"' in raiz and 'height="360"' in raiz
    assert 'viewBox="0 0 460.8 345.6"' in raiz
    assert 'xmlns:xlink=' in raiz
    ET.fromstring(salida)
    _guarda_test_9(tmp_path, monkeypatch, "ml-u-prueba", salida)


def test_el_posproceso_rechaza_un_ancho_mayor_a_600():
    with pytest.raises(ValueError):
        gen.posprocesar_svg(_PROLOGO_MPL, aria="x", ancho=601)


def test_una_figura_de_matplotlib_sale_determinista_y_pasa_test_9(tmp_path, monkeypatch):
    matplotlib = pytest.importorskip("matplotlib")
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def dibujar():
        with matplotlib.rc_context(gen.RC_SITIO):
            fig, ax = plt.subplots(figsize=(5, 3.5))
            r = gen.ROLES["entrenamiento"]
            ax.plot([0, 1, 2], [1, 3, 2], linestyle="none", marker=r["marcador"],
                    color=r["color"], label=r["nombre"])
            b = gen.ROLES["benchmark"]
            ax.axhline(2, linestyle=b["linea"], color=b["color"], label=b["nombre"])
            ax.legend()
            ax.set_xlabel("x")
            return gen.svg_de_matplotlib(fig, aria="humo", ancho=500)

    uno, dos = dibujar(), dibujar()
    assert uno == dos, "el SVG de matplotlib cambia entre corridas"
    assert uno.startswith("<svg")
    assert "opacity" not in uno, "la leyenda o un trazo salio con opacidad"
    ET.fromstring(uno)
    _guarda_test_9(tmp_path, monkeypatch, "ml-u-humo", uno)


# ---------------------------------------------------------------- roles ---

def _luminancia(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def _contraste(a, b):
    la, lb = sorted([_luminancia(a), _luminancia(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


ROLES_ESPERADOS = {
    # rol: (marcador, linea, color del sitio) de la tabla del contrato §7.3
    "entrenamiento": ("o", None, "#64dce3"),
    "validacion": ("^", None, "#ffd166"),
    "prueba": ("s", None, "#ff87ad"),
    "realidad": (None, "--", "#fff8ed"),
    "f_verdadera": (None, "-", "#a9e88f"),
    "f_estimada": (None, "-", "#64dce3"),
    "piso_bayes": (None, ":", "#dfd0e8"),
    "observaciones_nuevas": (".", None, None),
    "benchmark": (None, "-.", "#f04cff"),
}


def test_los_roles_son_los_de_la_tabla_del_contrato():
    assert set(gen.ROLES) == set(ROLES_ESPERADOS)
    for rol, (marcador, linea, color) in ROLES_ESPERADOS.items():
        r = gen.ROLES[rol]
        assert r["marcador"] == marcador, rol
        assert r["linea"] == linea, rol
        if color is not None:
            assert r["color"] == color, rol


def test_cada_rol_lleva_marca_o_trazo_ademas_del_color():
    for rol, r in gen.ROLES.items():
        assert r["marcador"] or r["linea"], f"{rol}: el color seria la unica senal"


def test_las_marcas_de_los_roles_de_puntos_no_se_repiten():
    marcas = [r["marcador"] for r in gen.ROLES.values() if r["marcador"]]
    assert len(marcas) == len(set(marcas))


def test_las_dos_lineas_continuas_se_distinguen_por_grosor():
    assert gen.ROLES["f_verdadera"]["grosor"] >= 2 * gen.ROLES["f_estimada"]["grosor"]


def test_observaciones_nuevas_es_crema_horneada_contra_el_fondo():
    assert gen.ROLES["observaciones_nuevas"]["color"] == gen.mezclar("#fff8ed", 0.6)
    assert re.fullmatch(r"#[0-9a-f]{6}", gen.ROLES["observaciones_nuevas"]["color"])


@pytest.mark.parametrize("rol", sorted(ROLES_ESPERADOS))
def test_cada_color_de_rol_pasa_3_a_1_contra_el_panel_y_el_fondo(rol):
    color = gen.ROLES[rol]["color"]
    assert _contraste(color, gen.PANEL) >= 3, f"{rol}: {_contraste(color, gen.PANEL):.2f}:1"
    assert _contraste(color, gen.FONDO) >= 3


def test_el_magenta_del_benchmark_se_distingue_del_rosa_de_prueba():
    # Comprobado tambien en Chrome (U.T3). Tono a mas de 30 grados, y el
    # benchmark es una raya-punto mientras la prueba es un cuadrado.
    d = abs(gen.tono(gen.ROLES["benchmark"]["color"]) - gen.tono(gen.ROLES["prueba"]["color"]))
    assert min(d, 360 - d) >= 30
    assert gen.ROLES["benchmark"]["color"] != gen.ROLES["validacion"]["color"]


def test_el_fondo_es_el_surface_del_skin():
    skin = (TOOLS.parent / "skins/eva-cyberpunk.yaml").read_text(encoding="utf-8")
    assert re.search(r'surface:\s*"#211033"', skin)
    assert gen.FONDO == "#211033"


# ------------------------------------------------------------------ CLI ---

def test_sin_argumentos_ni_ml_clases_genera_todo():
    assert gen.claves_pedidas([], {}) == ["u", 0, 1, 2, 3, 4, 5]


def test_ml_clases_restringe_la_corrida_sin_argumentos():
    assert gen.claves_pedidas([], {"ML_CLASES": "2"}) == [2]
    assert gen.claves_pedidas([], {"ML_CLASES": "1, 3,u"}) == [1, 3, "u"]


def test_un_argumento_explicito_manda_sobre_ml_clases():
    assert gen.claves_pedidas(["--clase", "4"], {"ML_CLASES": "2"}) == [4]
    assert gen.claves_pedidas(["--unidad"], {"ML_CLASES": "2"}) == ["u"]


@pytest.mark.parametrize("valor", ["7", "dos", "2,,3", ","])
def test_ml_clases_invalida_falla_en_vez_de_generar_todo(valor):
    with pytest.raises(ValueError):
        gen.claves_pedidas([], {"ML_CLASES": valor})


def test_con_ml_clases_2_no_escribe_nada_de_otra_clase(tmp_path, monkeypatch):
    def fig(ident):
        return lambda: gen.svg(100, 50, ident, ident, [])

    falsos = {"u": {"ml-u-mapa": fig("u")}, 0: {}, 1: {"ml-c1-a": fig("1")},
              2: {"ml-c2-a": fig("2a"), "ml-c2-b": fig("2b")}, 3: {"ml-c3-a": fig("3")},
              4: {}, 5: {}}
    monkeypatch.setattr(gen, "figuras_por_clave", lambda: falsos)
    monkeypatch.setattr(gen, "ASSETS_ML", tmp_path)
    gen.main([], {"ML_CLASES": "2"})
    assert sorted(p.name for p in tmp_path.iterdir()) == ["ml-c2-a.svg", "ml-c2-b.svg"]


def test_ml_clases_invalida_en_main_sale_con_error(tmp_path, monkeypatch):
    monkeypatch.setattr(gen, "ASSETS_ML", tmp_path)
    with pytest.raises(SystemExit):
        gen.main([], {"ML_CLASES": "9"})
    assert not any(tmp_path.iterdir())


def test_el_generador_nombra_la_ruta_de_la_unidad():
    # generadores_limpios.sh detecta el generador de una unidad buscando
    # «course/9_aprendizaje_maquina» en su texto.
    texto = (TOOLS / "gen_aprendizaje_maquina.py").read_text(encoding="utf-8")
    assert re.search(r"course/9_aprendizaje_maquina\b", texto)


# -------------------------------------------------- importacion perezosa ---

def test_importar_y_generar_el_mapa_no_importa_ml_lab_ni_matplotlib():
    codigo = (
        "import sys, gen_aprendizaje_maquina as g\n"
        "g.contenido('ml-u-mapa')\n"
        "import figuras_ml_c0\n"
        "[g.contenido(i) for i in figuras_ml_c0.FIGURAS_C0]\n"
        "print('aprendizaje_maquina' in sys.modules, 'matplotlib' in sys.modules)\n"
    )
    salida = subprocess.run([sys.executable, "-c", codigo], cwd=TOOLS,
                            capture_output=True, text=True, check=True)
    assert salida.stdout.split() == ["False", "False"], salida.stdout + salida.stderr


# ---------------------------------------------------- con la unidad ---

def _claves_de_ml_clases():
    valor = os.environ.get("ML_CLASES", "").strip()
    return None if not valor else set(gen.parsear_ml_clases(valor))


def _nombres_de_la_corrida():
    claves = _claves_de_ml_clases()
    return [n for n in NOMBRES if claves is None or gen.clave_de(n) in claves]


requiere_unidad = pytest.mark.skipif(
    not gen.UNIDAD_ML.is_dir() or not CREDITOS.is_file(),
    reason="no existe course/9_aprendizaje_maquina/ o su _assets/CREDITOS.md (U.T1)")


@requiere_unidad
@pytest.mark.parametrize("nombre", _nombres_de_la_corrida())
def test_cada_svg_es_el_que_produce_el_generador(nombre):
    archivo = gen.ASSETS_ML / f"{nombre}.svg"
    assert archivo.is_file(), (
        f"falta {archivo.name}: corre python3 tools/gen_aprendizaje_maquina.py")
    comiteado, generado = archivo.read_text(encoding="utf-8"), gen.contenido(nombre)
    parecido = (_misma_estructura if nombre in FIGURAS_QUE_DEPENDEN_DE_LA_CPU
                else _mismo_svg_salvo_redondeo)
    assert comiteado == generado or parecido(comiteado, generado), (
        f"{archivo.name} no es el que produce el generador: corre "
        "python3 tools/gen_aprendizaje_maquina.py y revisa el diff")


# Matplotlib escribe floats con todos sus dígitos y nombra cada clipPath con un hash
# de sus coordenadas. En CI (otra CPU, mismo numpy) cuatro SVG salieron distintos solo
# en el último dígito: «9.999999999999999e-05» contra «0.0001», y por eso con otro id
# de clipPath (run 42686844702). La figura es la misma; la comparación tolera eso y
# nada más: texto, colores y estructura deben coincidir carácter por carácter.
_NUMERO = re.compile(r"-?\d+(?:\.\d+)?(?:e[-+]?\d+)?")
_CLIP = re.compile(r"\bp[0-9a-f]{10}\b")


# Figuras cuyos datos salen de ajustes que cambian con la CPU, no solo en el último
# dígito: en CI (run 42691939001) los ejes de estas tres se movieron varios píxeles
# (mínimos cuadrados no convexos, CV de un ajuste mal condicionado). Para ellas la
# guarda exige el mismo SVG salvo las coordenadas: mismos elementos, textos, rótulos
# y colores. Las cifras que la prosa cita de esos cálculos las vigilan las pruebas
# de cifras y prosa, redondeadas, y esas sí pasan en CI.
FIGURAS_QUE_DEPENDEN_DE_LA_CPU = {"ml-c2-reparto", "ml-c3-mu-cv", "ml-c5-cybenko"}


def _misma_estructura(a, b):
    """Mismos elementos SVG, en la misma cantidad, y los mismos textos no numéricos."""
    def firma(texto):
        raiz = ET.fromstring(texto)
        etiquetas = sorted(e.tag for e in raiz.iter())
        textos = sorted(t.strip() for e in raiz.iter() for t in [e.text or ""]
                        if t.strip() and not _NUMERO.fullmatch(t.strip().replace("−", "-")))
        return etiquetas, textos
    return firma(a) == firma(b)


def _mismo_svg_salvo_redondeo(a, b, absoluta=1e-3, relativa=1e-6):
    def ids_en_orden(texto):
        vistos = {}
        return _CLIP.sub(lambda m: vistos.setdefault(m.group(), f"clip{len(vistos)}"), texto)

    a, b = ids_en_orden(a), ids_en_orden(b)
    if _NUMERO.split(a) != _NUMERO.split(b):
        return False
    na, nb = _NUMERO.findall(a), _NUMERO.findall(b)
    return len(na) == len(nb) and all(
        abs(float(x) - float(y)) <= max(absoluta, relativa * abs(float(x)))
        for x, y in zip(na, nb))


def test_la_tolerancia_de_redondeo_no_deja_pasar_un_cambio_visible():
    base = '<g id="anotar-0.07880462815669911"><path clip-path="url(#pc7f070eaf2)" d="M 10.5 2"/></g>'
    ruido = '<g id="anotar-0.07880462815669913"><path clip-path="url(#p822f8dad43)" d="M 10.5 2"/></g>'
    assert _mismo_svg_salvo_redondeo(base, ruido)
    assert not _mismo_svg_salvo_redondeo(base, base.replace("10.5", "10.6"))
    assert not _mismo_svg_salvo_redondeo(base, base.replace("anotar", "anotad"))
    assert not _mismo_svg_salvo_redondeo(base, base.replace('d="M', 'd="L'))


@requiere_unidad
def test_no_hay_figuras_huerfanas_en_assets():
    claves = _claves_de_ml_clases()
    catalogo = set(NOMBRES)
    huerfanas = []
    for archivo in sorted(gen.ASSETS_ML.iterdir()):
        if archivo.suffix not in (".svg", ".png") or not archivo.name.startswith("ml-"):
            continue
        ident = archivo.stem
        if claves is not None and gen.clave_de(ident) not in claves:
            continue
        if ident not in catalogo:
            huerfanas.append(archivo.name)
    assert not huerfanas, f"figuras que ningun catalogo produce: {huerfanas}"


@requiere_unidad
@pytest.mark.parametrize("nombre", _nombres_de_la_corrida())
def test_cada_figura_tiene_su_fila_en_creditos(nombre):
    from unidades import filas_de_creditos
    filas = filas_de_creditos(gen.ASSETS_ML)
    assert f"{nombre}.svg" in filas, f"{nombre}.svg sin fila en CREDITOS.md"


_BLOQUE_FIGURA = re.compile(r"^:::\s*figure\s*\{#([\w-]+)[^}]*\}\s*$(.*?)^:::\s*$",
                            re.M | re.S)


def _bloques_de_figura():
    bloques = {}
    for pagina in sorted(gen.UNIDAD_ML.rglob("*.md")):
        if any(parte.startswith("_") for parte in pagina.relative_to(gen.UNIDAD_ML).parts):
            continue
        for m in _BLOQUE_FIGURA.finditer(pagina.read_text(encoding="utf-8")):
            bloques.setdefault(m.group(1), []).append((pagina, m.group(2)))
    return bloques


@requiere_unidad
@pytest.mark.parametrize("nombre", _nombres_de_la_corrida())
def test_cada_figura_la_usa_una_pagina_dentro_de_un_figure_con_su_id(nombre):
    bloques = _bloques_de_figura().get(nombre, [])
    assert bloques, f"ninguna pagina tiene ::: figure {{#{nombre} ...}}"
    assert any(re.search(rf"_assets/{re.escape(nombre)}\.(svg|png)\)", cuerpo)
               for _, cuerpo in bloques), (
        f"el ::: figure {{#{nombre}}} no enlaza _assets/{nombre}.svg")
