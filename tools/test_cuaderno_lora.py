"""El notebook 03 «Fine-tuning generativo con LoRA» sale de su generador y está sano.

course/10_deep_learning/_assets/03_finetuning_lora.ipynb sale de
tools/gen_cuaderno_lora.py (envoltorio del generador del notebook 02) a
partir de las fuentes sNN_* en tools/cuadernos_dl/03_finetuning_lora/. Las
reglas del formato (claves, guiones, `--integrar`) ya las prueba
test_cuaderno_entender_red.py sobre el mismo código; aquí se comprueba lo
propio del 03:

- el envoltorio no toca los globales del generador del 02 (corren en la
  misma sesión de pytest);
- el notebook generado abre como JSON, su primera celda trae el badge con
  la URL del 03, no queda «NOTA PARA SOL» y cada sección NN ≥ 1 abre su
  primera celda de texto con «## NN ·»;
- el notebook comiteado, si existe, tiene las mismas celdas que el
  generador (ignorando salidas) y pesa menos de 11 MB.

Mientras falte alguna sección s00…s13, las pruebas sobre las fuentes reales
se saltan con un mensaje que dice cuáles faltan.
"""
import json
from pathlib import Path

import pytest

import gen_cuaderno_entender_red as gen02
import gen_cuaderno_lora as gen

NB = gen.DESTINO
SECCIONES = range(14)
TOPE = 11 * 1024 * 1024  # mismo tope que el notebook 02; el del repo es 12 MB


def faltantes(base=gen.FUENTES):
    """Las secciones NN sin su par sNN_*.py + sNN_*.texto.md."""
    base = Path(base)
    return [f"s{nn:02d}" for nn in SECCIONES
            if not list(base.glob(f"s{nn:02d}_*.py"))
            or not list(base.glob(f"s{nn:02d}_*.texto.md"))]


@pytest.fixture(scope="module")
def generado(tmp_path_factory):
    faltan = faltantes()
    if faltan:
        pytest.skip("faltan secciones: " + ", ".join(faltan))
    ruta = tmp_path_factory.mktemp("nb03") / "03.ipynb"
    assert gen.main(["--salida", str(ruta)]) == 0   # sin --borrador
    return json.loads(ruta.read_text(encoding="utf-8"))


def test_envoltorio_no_toca_el_generador_del_02():
    assert gen02.FUENTES.name == "02_entender_una_red"
    assert "02_entender_una_red.ipynb" in gen02.BADGE
    assert gen.FUENTES.name == "03_finetuning_lora"
    assert gen.RUTA_NB == "course/10_deep_learning/_assets/03_finetuning_lora.ipynb"
    assert gen.URL_COLAB.endswith(gen.RUTA_NB)
    assert gen.URL_COLAB in gen.BADGE


def test_primera_celda_trae_la_url_del_03(generado):
    primera = generado["cells"][0]
    assert primera["cell_type"] == "markdown"
    texto = gen.fuente(primera)
    assert gen.URL_COLAB in texto
    assert "02_entender_una_red" not in texto


def test_metadata_gpu(generado):
    assert generado["metadata"]["accelerator"] == "GPU"
    assert generado["metadata"]["colab"]["gpuType"] == "T4"


def test_sin_nota_para_sol(generado):
    for celda in generado["cells"]:
        assert gen.g.NOTA not in gen.fuente(celda), celda["metadata"]["id"]


def test_cada_seccion_abre_con_su_encabezado(generado):
    primeras = {}
    for celda in generado["cells"]:
        if celda["cell_type"] != "markdown":
            continue
        nn = int(celda["metadata"]["id"][1:3])
        primeras.setdefault(nn, gen.fuente(celda))
    for nn in SECCIONES:
        if nn == 0:
            continue                           # la portada lleva «# Notebook 3»
        assert nn in primeras, f"s{nn:02d} no tiene celda de texto"
        primera_linea = primeras[nn].lstrip().split("\n")[0]
        assert primera_linea.startswith(f"## {nn:02d} · "), (
            f"s{nn:02d} abre con {primera_linea!r}, no con «## {nn:02d} · …»")


def test_comiteado_igual_al_generador(generado):
    if not NB.exists():
        pytest.skip(f"no existe {gen.RUTA_NB}: corre el generador")
    comiteado = json.loads(NB.read_text(encoding="utf-8"))
    a = [(c["cell_type"], c["metadata"]["id"], gen.fuente(c))
         for c in generado["cells"]]
    b = [(c["cell_type"], c["metadata"].get("id"), gen.fuente(c))
         for c in comiteado["cells"]]
    assert a == b, "el .ipynb no es el que arma el generador hoy"


def test_tamano_menor_11mb():
    if not NB.exists():
        pytest.skip(f"no existe {gen.RUTA_NB}")
    assert NB.stat().st_size <= TOPE, (
        f"{gen.RUTA_NB} pesa {NB.stat().st_size / 2**20:.1f} MB (> 11 MB)")
