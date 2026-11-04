"""Pruebas propias de tools/figuras_ml_c0.py (clase 0, unidad 9; sin prosa).

Las guardas comunes (XML, titulo, aria, ancho, letra, opacidad,
determinismo, fila en CREDITOS, uso en una pagina) viven en
tools/test_gen_aprendizaje_maquina.py. Aqui va lo propio de la clase 0
(clase_0.md §10.8):

- cada SVG pasa test_9 de test_aceptacion.py, mide <=600 y su letra es >=12;
- el aria-label de F1a y F1b pone cada regla junto a su valor, tomado de
  ml_cifras_c0 (no escrito aqui); F1a no revela los tiempos reales (31, 33);
- el texto visible no nombra los roles (contrato §7.3);
- vistas, nuevas, la recta y el promedio llevan color y trazo del rol que
  exporta gen_aprendizaje_maquina (por import); F1a, F1b y F2 no llevan ni el
  color ni el cuadrado del rol «prueba»;
- F3 no dibuja circulos ni elipses (la IA no es una cebolla) y rotula las
  cinco ramas con el texto de v3-taxonomia.svg (D-015);
- F4 no escribe phi con subindice numerico en ninguna forma y la tira 4 dice
  «capa 1» y «capa 2» (contrato §4.4, r2-01).

Mutacion anotada en el commit de C0.T2: rotular la tira 4 con «φ_1» pone
roja test_f4_sin_phi_con_subindice_numerico.
"""
import re
from pathlib import Path

import pytest

import figuras_ml_c0 as fig
import gen_aprendizaje_maquina as gen
import ml_cifras_c0 as cifras
import test_aceptacion

RAIZ = Path(__file__).resolve().parent.parent
TAXONOMIA = RAIZ / "course/1_introduccion/2_historia_ia/_assets/v3-taxonomia.svg"
F1A = "ml-c0-tres-reglas-en-lo-visto"
F1B = "ml-c0-memorizar-contra-ajustar"
F2 = "ml-c0-con-y-sin-y"
F3 = "ml-c0-jerarquia"
F4 = "ml-c0-quien-elige-phi"
TRAMO_RAPIDO = (F1A, F1B, F2, F3, F4)
DATOS = (F1A, F1B, F2)


def _svg(ident):
    return fig.FIGURAS_C0[ident]()


def _aria(texto_svg):
    return re.search(r'aria-label="([^"]*)"', texto_svg).group(1)


def _textos(texto_svg):
    """Todo el texto visible: el contenido de cada <text> (con sus <tspan>)."""
    return [re.sub(r"<[^>]+>", "", m) for m in re.findall(r"<text\b[^>]*>(.*?)</text>",
                                                         texto_svg, re.S)]


def test_el_catalogo_trae_las_cinco_figuras_del_tramo_rapido():
    assert tuple(fig.FIGURAS_C0) == TRAMO_RAPIDO


@pytest.mark.parametrize("ident", TRAMO_RAPIDO)
def test_empieza_con_svg_y_pasa_test_9(ident, tmp_path, monkeypatch):
    texto = _svg(ident)
    assert texto.startswith("<svg")
    d = tmp_path / "assets"
    d.mkdir()
    (d / f"{ident}.svg").write_text(texto, encoding="utf-8")
    monkeypatch.setattr(test_aceptacion, "ASSETS_POR_UNIDAD", {"c0": d})
    test_aceptacion.test_9_los_diagramas_svg_son_legibles_sobre_el_fondo_oscuro_del_skin()


@pytest.mark.parametrize("ident", TRAMO_RAPIDO)
def test_ancho_y_letra(ident):
    texto = _svg(ident)
    raiz = re.match(r"<svg\b[^>]*>", texto).group()
    assert float(re.search(r'\bwidth="([\d.]+)"', raiz).group(1)) <= 600
    assert min(float(t) for t in re.findall(r'font-size="([\d.]+)"', texto)) >= 12


@pytest.mark.parametrize("ident", TRAMO_RAPIDO)
def test_determinista(ident):
    assert _svg(ident) == _svg(ident)


# ------------------------------------------------- F1a y F1b: cifras ---

C = cifras.cifras_c0_memorizar()
f = cifras.redondeo


def _junto(aria, rotulo, valor):
    """`rotulo` y luego `valor` en la misma frase (sin punto final ni punto y
    coma entre los dos; el punto decimal de «3.6x» no corta), con el valor
    como numero completo."""
    patron = (rf"{re.escape(rotulo)}(?:[^.;]|\.(?=\d))*?(?<![\d.])"
              rf"{re.escape(valor)}(?![\d]|\.\d)")
    return re.search(patron, aria, re.I) is not None


def test_f1a_pone_cada_regla_junto_a_su_error_en_lo_visto():
    aria = _aria(_svg(F1A))
    assert _junto(aria, "memorizar copia", f(C["memorizar"]["mae_vistas"]))
    assert _junto(aria, "la recta", f(C["recta"]["mae_vistas"]))
    assert _junto(aria, "el promedio fijo", f(C["promedio"]["mae_vistas"]))
    for regla, rot in (("memorizar", "memorizar "), ("promedio", "el promedio "),
                       ("recta", "la recta ")):
        a, b = (f(v) for v in C[regla]["anuncios_nuevas"])
        assert f"{rot}{a} y {b}" in aria, regla


def test_f1a_no_revela_los_tiempos_reales_de_las_nuevas():
    texto = _svg(F1A)
    for i in cifras.NUEVAS:
        real = str(cifras.ENTREGAS[i][1])
        assert not re.search(rf"(?<![\d.]){real}(?![\d])", _aria(texto))
        assert all(not re.search(rf"(?<![\d.]){real}(?![\d])", t) for t in _textos(texto))


def test_f1b_pone_cada_regla_junto_a_su_error_en_cada_conjunto():
    aria = _aria(_svg(F1B))
    izq, der = aria.split("Derecha:")
    assert _junto(izq, "memorizar", f(C["memorizar"]["mae_vistas"]))
    assert _junto(izq, "recta", f(C["recta"]["mae_vistas"]))
    assert _junto(izq, "promedio", f(C["promedio"]["mae_vistas"]))
    for regla in ("memorizar", "promedio", "recta"):
        clave = {"memorizar": "memorizar anuncia", "promedio": "el promedio anuncia",
                 "recta": "la recta anuncia"}[regla]
        frase = next(fr for fr in der.split(";") if clave in fr)
        assert re.search(rf"falla[^;]*?(?<![\d.]){re.escape(f(C[regla]['mae_nuevas']))}"
                         rf"(?![\d]|\.\d)", frase), regla
    for i in cifras.NUEVAS:
        assert str(cifras.ENTREGAS[i][1]) in der


def test_f1b_dibuja_los_mae_bajo_cada_panel_junto_a_su_regla():
    textos = _textos(_svg(F1B))
    for clave in ("mae_vistas", "mae_nuevas"):
        for regla in ("memorizar", "recta", "promedio"):
            valor = f(C[regla][clave])
            assert valor in textos, (regla, clave)


# ---------------------------------------------------------- roles ---

PROHIBIDAS = ("entrenamiento", "prueba", "observaciones nuevas", "benchmark", "f̂")


@pytest.mark.parametrize("ident", DATOS)
def test_el_texto_visible_no_nombra_los_roles(ident):
    for t in _textos(_svg(ident)):
        for palabra in PROHIBIDAS:
            assert palabra not in t.lower(), (ident, t)


def _circulos(texto, color):
    return re.findall(rf'<circle\b[^>]*fill="{re.escape(color)}"[^>]*/>', texto)


@pytest.mark.parametrize("ident", (F1A, F1B))
def test_roles_por_import_en_f1a_y_f1b(ident):
    texto = _svg(ident)
    r = gen.ROLES
    # vistas: circulo relleno del color de entrenamiento (cuatro + leyenda)
    assert len(_circulos(texto, r["entrenamiento"]["color"])) >= 4
    # nuevas: punto pequeno del rol observaciones nuevas (dos + leyenda)
    nuevas = _circulos(texto, r["observaciones_nuevas"]["color"])
    assert len(nuevas) >= 2
    assert all(float(re.search(r'r="([\d.]+)"', c).group(1)) <= 5 for c in nuevas)
    # la recta: trazo continuo del color de f estimada
    assert re.search(rf'<line\b[^>]*stroke="{r["f_estimada"]["color"]}"(?![^>]*dasharray)',
                     texto)
    # el promedio: color y raya-punto del rol benchmark
    assert re.search(rf'<line\b[^>]*stroke="{r["benchmark"]["color"]}"[^>]*'
                     rf'stroke-dasharray="{r["benchmark"]["guiones"]}"', texto)


@pytest.mark.parametrize("ident", DATOS)
def test_sin_el_color_ni_el_cuadrado_del_rol_prueba(ident):
    texto = _svg(ident)
    prueba = gen.ROLES["prueba"]
    assert prueba["color"].lower() not in texto.lower()
    assert prueba["simbolo"] not in texto


# ------------------------------------------------------------- F3 ---

def test_f3_no_es_una_cebolla():
    texto = _svg(F3)
    assert "<circle" not in texto and "<ellipse" not in texto


def test_f3_rotula_las_cinco_ramas_como_historia():
    historia = " ".join(re.sub(r"<[^>]+>", "", m) for m in
                        re.findall(r"<text\b[^>]*>(.*?)</text>",
                                   TAXONOMIA.read_text(encoding="utf-8"), re.S))
    nuestro = " ".join(_textos(_svg(F3)))
    for l1, l2 in fig.RAMAS:
        assert f"{l1} {l2}" in historia, (l1, l2)
        assert l1 in nuestro and l2 in nuestro
    # D-015: la caja hermana como historia, el zoom con «de»
    assert "Aprendizaje máquina" in historia
    assert "aprendizaje de máquina" in nuestro


# ------------------------------------------------------------- F4 ---

_PHI_NUMERO = re.compile(r"(φ|\\phi|ϕ)\s*(_\{?\s*)?[0-9₀-₉]")


def _texto_completo_f4(texto):
    partes = _textos(texto)
    partes += re.findall(r"<title>(.*?)</title>", texto, re.S)
    partes.append(_aria(texto))
    return partes


def test_f4_sin_phi_con_subindice_numerico():
    for parte in _texto_completo_f4(_svg(F4)):
        assert not _PHI_NUMERO.search(parte), parte
    assert not re.search(r"\bfi \d", _aria(_svg(F4)))


def test_f4_la_tira_4_dice_capa_1_y_capa_2():
    textos = _textos(_svg(F4))
    assert "capa 1" in textos and "capa 2" in textos


def test_la_guarda_de_phi_atrapa_las_formas_prohibidas():
    for malo in ("φ_1", "φ1", "\\phi_{2}", "φ₁", "\\phi_1"):
        assert _PHI_NUMERO.search(malo), malo
    assert not _PHI_NUMERO.search("φ(x)")
