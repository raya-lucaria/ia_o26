"""El linter de notación de la unidad 9 (contrato §4.7, D-005, D-015).

- Cada regla de la lista negra atrapa su caso y deja pasar la forma buena,
  y las dos notas únicas (λ en `ml-c3-def-lagrangeano-capacidad`, SMOTE en
  `ml-c4-obs-por-que-no-remuestrear`) solo valen dentro de su bloque.
- La lista blanca marca lo desconocido y lo que aparece antes de su clase.
- Cada línea de `tools/datos/notacion_ml/cN.txt` trae su fuente, y cada
  excepción su razón y un fragmento que de verdad está en su archivo.
- Ninguna página de la unidad ni ningún guion tiene hallazgos.
"""
from pathlib import Path

import pytest

import notacion_ml as nm

RAIZ = Path(__file__).resolve().parent.parent


def reglas(texto, clase=5, blanca=None):
    return [r for _, r, _ in nm.revisar_texto(texto, clase, blanca=blanca)]


# --- Lista negra ------------------------------------------------------------

@pytest.mark.parametrize("malo, regla", [
    (r"$\boldsymbol{\beta}$", "boldsymbol"),
    (r"$\hat{\beta}$", "hat"),
    (r"$\hat\beta$", "hat"),
    (r"la fuerza $\lambda$ de ridge", "lambda"),
    ("la fuerza λ de ridge", "lambda"),
    ("con alpha = 0.1 en sklearn", "alpha"),
    (r"$\alpha$", "alpha"),
    ("El lagrangiano de la capacidad.", "lagrangiano"),
    ("La Lagrangiana del problema.", "lagrangiano"),
    ("Ese ingreso es un outlier y se quita.", "outlier"),
    ("Usa SMOTE para balancear.", "smote"),
    ("El sobremuestreo arregla el desbalanceo.", "smote"),
    ("Un polinomio de grado 5 es un modelo no lineal.", "no-lineal"),
    ("El modelo es no lineal porque sube el grado.", "no-lineal"),
    (r"$\log n$", "log"),
])
def test_la_lista_negra_atrapa_cada_caso(malo, regla):
    assert regla in reglas(malo)


@pytest.mark.parametrize("bueno", [
    r"$\mathbf{\Phi}\widehat\beta$",
    "El lagrangeano $\\mathcal L$ con $\\mu\\ge0$.",
    "Ese ingreso no es un outlier: es la cola larga.",
    "Un polinomio en $x$ es curvo en $x$ y lineal en $\\beta$.",
    "La frontera es no lineal. Un polinomio de grado 2 es otra historia.",
    r"$\log_{10}\mu$ en el eje",
    r"$\ln(1+x)$",
])
def test_la_lista_negra_deja_pasar_la_forma_buena(bueno):
    assert [r for r in reglas(bueno) if r != "antes"] == []


def test_lambda_y_alpha_solo_valen_en_la_nota_unica():
    nota = ("::: remark {#ml-c3-def-lagrangeano-capacidad title=\"x\"}\n"
            "Los libros la llaman $\\lambda$ y sklearn `alpha`.\n"
            ":::\n")
    assert reglas(nota) == []
    afuera = nota + "Y aquí otra vez $\\lambda$.\n"
    assert reglas(afuera) == ["lambda"]
    otro = nota.replace("lagrangeano-capacidad", "otra-cosa")
    assert set(reglas(otro)) == {"lambda", "alpha"}


def test_smote_solo_vale_en_su_observacion():
    obs = ("::: remark {#ml-c4-obs-por-que-no-remuestrear}\n"
           "SMOTE inventa casos; no resuelve el desbalanceo.\n"
           ":::\n")
    assert reglas(obs) == []
    assert reglas(obs + "Luego usa SMOTE.\n") == ["smote"]


# --- Lista blanca -------------------------------------------------------------

def test_un_simbolo_antes_de_su_clase_falla():
    assert reglas("$\\rho$", clase=1) == ["antes"]
    assert reglas("$\\rho$", clase=3) == []
    assert reglas("la mezcla ρ", clase=2) == ["antes"]
    assert reglas("$L_{\\text{val}}$", clase=1) == ["antes"]
    assert reglas("$L_{\\text{val}}$", clase=2) == []
    assert reglas("$\\mathrm{MCC}$", clase=3) == ["antes"]


def test_lo_heredado_vale_desde_la_clase_0():
    texto = "$\\beta^\\star$, $\\Pr(y=1)$, $\\ell_i$, $\\mu\\ge0$, $\\phi(x)$"
    assert reglas(texto, clase=0) == []


def test_un_simbolo_desconocido_falla_hasta_que_entra_en_su_lista(tmp_path):
    # \varkappa no está en ninguna lista real: la prueba no depende de cN.txt
    assert reglas("$\\varkappa_h$", clase=5) == ["blanca"]
    (tmp_path / "c5.txt").write_text("\\varkappa | contrato §4.8 (prueba)\n",
                                     encoding="utf-8")
    blanca = nm.lista_blanca(tmp_path)
    assert reglas("$\\varkappa_h$", clase=5, blanca=blanca) == []
    assert reglas("$\\varkappa_h$", clase=4, blanca=blanca) == ["antes"]


def test_una_forma_comun_se_adelanta_con_la_lista_de_su_clase(tmp_path):
    cov = "$\\operatorname{cov}(x_1,x_2)$"
    assert reglas(cov, clase=3, blanca=nm.lista_blanca(tmp_path)) == ["antes"]
    (tmp_path / "c3.txt").write_text("re:\\\\operatorname\\*?\\{cov\\} | D-015\n",
                                     encoding="utf-8")
    blanca = nm.lista_blanca(tmp_path)
    assert reglas(cov, clase=3, blanca=blanca) == []
    assert reglas(cov, clase=2, blanca=blanca) == ["antes"]


def test_el_codigo_no_cuenta_para_la_lista_blanca():
    texto = "```python\nphi = polinomio(N=3)  # $\\gamma$\n```\n`$\\gamma$`\n"
    assert reglas(texto, clase=0) == []


def test_las_lineas_se_cuentan_bien():
    texto = "uno\n\ndos $\\hat y$\n"
    assert nm.revisar_texto(texto, 5)[0][0] == 3


# --- Datos: listas por clase y excepciones -----------------------------------

@pytest.mark.parametrize("linea", [
    "\\gamma", "\\gamma |", "\\gamma | porque sí", "| contrato §4.2",
])
def test_una_linea_sin_fuente_se_rechaza(linea):
    with pytest.raises(ValueError):
        nm.leer_lista_clase(linea)


def test_una_linea_con_fuente_se_acepta():
    filas = nm.leer_lista_clase(
        "# comentario\n\\gamma | contrato §4.8\nre:\\text{a|b} | D-015\n"
        "γ | plan-c5-10\n")
    assert filas == [("\\gamma", "contrato §4.8"), ("re:\\text{a|b}", "D-015"),
                     ("γ", "plan-c5-10")]


@pytest.mark.parametrize("clase", list(nm.CLASES))
def test_cada_lista_de_clase_existe_y_trae_fuentes(clase):
    ruta = nm.DATOS / f"c{clase}.txt"
    assert ruta.exists(), f"falta {ruta.relative_to(RAIZ)} (D-015)"
    nm.leer_lista_clase(ruta.read_text(encoding="utf-8"), ruta.name)


def test_las_excepciones_tienen_razon_y_su_fragmento_existe():
    for ruta, fragmento, regla, razon in nm.excepciones():
        archivo = RAIZ / ruta
        if archivo.exists():
            assert fragmento in archivo.read_text(encoding="utf-8"), (
                f"excepción vieja: «{fragmento}» ya no está en {ruta}")


def test_una_excepcion_sin_razon_se_rechaza():
    with pytest.raises(ValueError):
        nm.leer_excepciones("a.md | frag | outlier |")
    with pytest.raises(ValueError):
        nm.leer_excepciones("a.md | frag | inventada | razón")


def test_una_excepcion_declarada_silencia_solo_su_linea():
    exc = [("course/x.md", "es un outlier", "outlier", "cita textual")]
    texto = "Dice: es un outlier.\nY otra vez outlier.\n"
    hall = nm.revisar_texto(texto, 5, "course/x.md", excepcs=exc)
    assert [(n, r) for n, r, _ in hall] == [(2, "outlier")]


def test_la_clase_de_cada_archivo():
    u = nm.UNIDAD
    assert nm.clase_de_archivo(u / "1_que_es_aprender/1_repaso.md") == 0
    assert nm.clase_de_archivo(u / "3_separar_los_datos/0_index.md") == 2
    assert nm.clase_de_archivo(u / "A_notacion.md") == nm.UNIDAD_ENTERA
    assert nm.clase_de_archivo(u / "_drafts/x.md") is None
    assert nm.clase_de_archivo(nm.GUIONES / "06_leer_el_error.texto.md") == 3


# --- El repositorio -----------------------------------------------------------

ARCHIVOS = nm.archivos_por_revisar()


@pytest.mark.parametrize("ruta", ARCHIVOS,
                         ids=[r.relative_to(RAIZ).as_posix() for r in ARCHIVOS])
def test_ningun_archivo_de_la_unidad_tiene_hallazgos(ruta):
    hall = nm.revisar_archivo(ruta)
    assert not hall, "\n".join(f"{ruta.relative_to(RAIZ)}:{n}: [{r}] {m}"
                               for n, r, m in hall)
