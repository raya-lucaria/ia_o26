"""El notebook 02 «Entender una red» es el que arma su generador, y está sano.

course/10_deep_learning/_assets/02_entender_una_red.ipynb sale de
tools/gen_cuaderno_entender_red.py a partir de las fuentes sNN_* en
tools/cuadernos_dl/02_entender_una_red/. Esta prueba ata las dos cosas:

- el generador rechaza claves duplicadas, faltantes o sobrantes, «NOTA PARA
  SOL» e ilustraciones sin aviso (fixtures sintéticos, corren siempre);
- `--integrar` conserva las salidas de código, deja ganar al markdown del
  generador y borra la metadata de la cuenta de Colab (sintético);
- el notebook comiteado tiene el badge, metadata de GPU T4, las mismas
  celdas que el generador (ignorando salidas), ninguna nota, cada imagen con
  su aviso y su crédito en ilustraciones.json, y pesa menos de 11 MB;
- si trae salidas: ninguna es un error, la tabla maestra no repite IDs y la
  línea «EXPERIMENTOS COMPLETOS: <n>» está;
- la prueba de humo corre todo el código con RAPIDO=1 en CPU (se salta sin
  torch o sin MNIST).

Mientras falte alguna sección s00…s19, las pruebas sobre el notebook real se
saltan con un mensaje que dice cuáles faltan. Las pruebas de la caja de
herramientas (s01–s03) viven en test_caja_entender_red.py.
"""
import copy
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

import gen_cuaderno_entender_red as gen

NB = gen.DESTINO
SECCIONES = range(20)
TOPE = 11 * 1024 * 1024  # la corrida en T4 con 73 figuras pesa ~10 MB; el tope del repo es 12 MB
ID = re.compile(r"^s\d\d-[a-z0-9-]+$")
EXPERIMENTOS = re.compile(r"EXPERIMENTOS COMPLETOS:\s*(\d+)")


# --- utilidades --------------------------------------------------------------

def faltantes(base=gen.FUENTES):
    """Las secciones NN sin su par sNN_*.py + sNN_*.texto.md."""
    base = Path(base)
    faltan = []
    for nn in SECCIONES:
        py = list(base.glob(f"s{nn:02d}_*.py"))
        md = list(base.glob(f"s{nn:02d}_*.texto.md"))
        if not py or not md:
            faltan.append(f"s{nn:02d}")
    return faltan


def requiere_secciones():
    faltan = faltantes()
    if faltan:
        pytest.skip("faltan secciones: " + ", ".join(faltan))


@pytest.fixture(scope="module")
def nb():
    requiere_secciones()
    if not NB.exists():
        pytest.skip(f"no existe {gen.RUTA_NB}: corre el generador")
    return json.loads(NB.read_text(encoding="utf-8"))


def fuente(celda):
    return gen.fuente(celda)


def textos_de_salida(celda):
    """Todo el texto de las salidas de una celda (stream, text/plain, html)."""
    partes = []
    for s in celda.get("outputs", []):
        if "text" in s:
            t = s["text"]
            partes.append("".join(t) if isinstance(t, list) else t)
        for mime in ("text/plain", "text/html"):
            t = s.get("data", {}).get(mime)
            if t is not None:
                partes.append("".join(t) if isinstance(t, list) else t)
    return "\n".join(partes)


def con_salidas(nb):
    return any(c.get("outputs") for c in nb["cells"] if c["cell_type"] == "code")


def escribir(base, nombre, texto):
    (base / nombre).write_text(texto, encoding="utf-8")


@pytest.fixture
def fuentes(tmp_path):
    """Un juego mínimo y válido: portada, una sección con código y plegada."""
    escribir(tmp_path, "s00_portada.py", "# %% [texto] s00-portada\n")
    escribir(tmp_path, "s00_portada.texto.md",
             "### celda: s00-portada\n# Entender una red\n")
    escribir(tmp_path, "s01_arranque.py",
             "# %% [texto] s01-intro\n\n# %% [codigo] s01-a\nX = 1\n"
             "print(X)\n# %% [plegada] s01-resp\n")
    escribir(tmp_path, "s01_arranque.texto.md",
             "### celda: s01-intro\n## 01 · Arranque\n\n"
             "### celda: s01-resp\nPorque sí.\n")
    escribir(tmp_path, "s02_datos.py", "# %% [codigo] s02-b\nprint(X + 1)\n")
    return tmp_path


def falla_con(base, *palabras, **kw):
    with pytest.raises(SystemExit) as e:
        gen.cuaderno(base, **kw)
    mensaje = str(e.value)
    for p in palabras:
        assert p in mensaje, mensaje
    return mensaje


# --- el generador, sobre fixtures sintéticos -----------------------------------

def test_claves_unicas_y_completas(fuentes):
    nb = gen.cuaderno(fuentes)
    assert [c["metadata"]["id"] for c in nb["cells"]] == [
        "s00-portada", "s01-intro", "s01-a", "s01-resp", "s02-b"]
    plegada = fuente(nb["cells"][3])
    assert plegada.startswith("<details><summary>Respuesta</summary>\n\n")
    assert plegada.endswith("\n\n</details>")

    # duplicada dentro de un archivo
    escribir(fuentes, "s02_datos.py",
             "# %% [codigo] s02-b\nA = 1\n# %% [codigo] s02-b\nB = 2\n")
    falla_con(fuentes, "duplicada", "s02-b", "s02_datos.py")
    # duplicada entre secciones (con el prefijo de otra sección)
    escribir(fuentes, "s02_datos.py", "# %% [codigo] s01-a\nA = 1\n")
    falla_con(fuentes, "s01-a", "s02_datos.py")
    escribir(fuentes, "s02_datos.py", "# %% [codigo] s02-b\nprint(X + 1)\n")
    # faltante en el guion
    escribir(fuentes, "s01_arranque.texto.md",
             "### celda: s01-intro\n## 01 · Arranque\n")
    falla_con(fuentes, "falta", "s01-resp", "s01_arranque.texto.md")
    # sobrante en el guion
    escribir(fuentes, "s01_arranque.texto.md",
             "### celda: s01-intro\nA\n### celda: s01-resp\nB\n"
             "### celda: s01-sobra\nC\n")
    falla_con(fuentes, "sobrante", "s01-sobra", "s01_arranque.texto.md")
    # duplicada en el guion
    escribir(fuentes, "s01_arranque.texto.md",
             "### celda: s01-intro\nA\n### celda: s01-resp\nB\n"
             "### celda: s01-resp\nC\n")
    falla_con(fuentes, "duplicada", "s01-resp")
    # un guion sin su .py
    escribir(fuentes, "s01_arranque.texto.md",
             "### celda: s01-intro\nA\n### celda: s01-resp\nB\n")
    escribir(fuentes, "s05_huerfano.texto.md", "### celda: s05-x\nA\n")
    falla_con(fuentes, "sobrante", "s05_huerfano.texto.md")


def test_nota_para_sol_solo_en_borrador(fuentes):
    escribir(fuentes, "s01_arranque.texto.md",
             "### celda: s01-intro\n- NOTA PARA SOL: explicar\n"
             "### celda: s01-resp\nB\n")
    falla_con(fuentes, "NOTA PARA SOL", "s01-intro")
    with pytest.raises(SystemExit):
        gen.script(fuentes)
    assert "NOTA PARA SOL" in json.dumps(gen.cuaderno(fuentes, borrador=True))


def test_ilustracion_exige_aviso_y_png(fuentes):
    escribir(fuentes, "s01_arranque.texto.md",
             "### celda: s01-intro\n![una pelota](ilustracion:pelota)\n\n"
             "Otra cosa.\n### celda: s01-resp\nB\n")
    falla_con(fuentes, "pelota", "Ilustración generada", borrador=True)
    escribir(fuentes, "s01_arranque.texto.md",
             "### celda: s01-intro\n![una pelota](ilustracion:pelota)\n\n"
             f"{gen.AVISO}\n### celda: s01-resp\nB\n")
    falla_con(fuentes, "pelota")                       # falta el PNG
    md = fuente(gen.cuaderno(fuentes, borrador=True)["cells"][1])
    assert "ilustración pendiente: pelota" in md
    (fuentes / "ilustraciones").mkdir()
    (fuentes / "ilustraciones" / "pelota.png").write_bytes(b"\x89PNG\r\n\x1a\n")
    md = fuente(gen.cuaderno(fuentes)["cells"][1])
    assert "![una pelota](data:image/png;base64,iVBORw0KGgo" in md


def test_script_sin_portada_y_corre(fuentes, tmp_path_factory):
    ruta = tmp_path_factory.mktemp("humo") / "humo.py"
    assert gen.main(["--fuentes", str(fuentes), "--script", str(ruta)]) == 0
    texto = ruta.read_text(encoding="utf-8")
    assert "# ==== s01-a ====" in texto and "s00" not in texto
    r = subprocess.run([sys.executable, str(ruta)], capture_output=True,
                       text=True, timeout=60)
    assert r.returncode == 0, r.stderr
    assert r.stdout.split() == ["1", "2"]
    # --secciones filtra; la sección 0 entra al notebook aunque no se pida
    nb = gen.cuaderno(fuentes, secciones={2})
    assert [c["metadata"]["id"] for c in nb["cells"]] == ["s00-portada", "s02-b"]
    assert "s01-a" not in gen.script(fuentes, secciones={2})


def test_generador_es_determinista_y_sin_salidas(fuentes):
    a = gen.serializar(gen.cuaderno(fuentes))
    assert a == gen.serializar(gen.cuaderno(fuentes)) and a.endswith("}\n")
    nb = json.loads(a)
    assert nb["nbformat"] == 4
    for c in nb["cells"]:
        if c["cell_type"] == "code":
            assert c["outputs"] == [] and c["execution_count"] is None


def test_integrar_conserva_salidas_y_limpia_metadata(fuentes, tmp_path_factory):
    generado = gen.cuaderno(fuentes)
    descarga = copy.deepcopy(generado)
    descarga["metadata"]["colab"]["provenance"] = [
        {"file_id": "abc", "timestamp": 1, "user": {"email": "x@y.mx"}}]
    descarga["metadata"]["colab"]["authorship_tag"] = "ABX9"
    salida = {"output_type": "stream", "name": "stdout", "text": ["1\n"],
              "metadata": {"outputId": "zz", "colab": {"user_email": "x@y"}}}
    for c in descarga["cells"]:
        c["metadata"].update(outputId="o1", executionInfo={"user": {"x": 1}})
        if c["cell_type"] == "code":
            c["outputs"] = [salida]
            c["execution_count"] = 7
            c["source"] = "".join(c["source"])          # Colab a veces une
        else:
            c["source"] = ["texto viejo de Colab"]
    ruta_d = tmp_path_factory.mktemp("d") / "descarga.ipynb"
    ruta_d.write_text(json.dumps(descarga), encoding="utf-8")
    ruta = ruta_d.parent / "salida.ipynb"
    assert gen.main(["--fuentes", str(fuentes), "--integrar", str(ruta_d),
                     "--salida", str(ruta)]) == 0
    nb = json.loads(ruta.read_text(encoding="utf-8"))
    texto = json.dumps(nb)
    for prohibido in ("outputId", "authorship_tag", "executionInfo", "email",
                      "x@y", "file_id"):
        assert prohibido not in texto, prohibido
    assert nb["metadata"]["colab"]["provenance"] == []
    assert nb["metadata"]["accelerator"] == "GPU"
    codigo = [c for c in nb["cells"] if c["cell_type"] == "code"]
    assert all(c["outputs"][0]["text"] == ["1\n"] for c in codigo)
    assert all(c["execution_count"] == 7 for c in codigo)
    for g, i in zip(generado["cells"], nb["cells"]):
        assert fuente(g) == fuente(i)                # gana el markdown nuestro
        assert i["metadata"] == {"id": g["metadata"]["id"]}

    # una celda de código distinta obliga a reejecutar
    codigo_d = [c for c in descarga["cells"] if c["cell_type"] == "code"][0]
    codigo_d["source"] = "X = 2\n"
    with pytest.raises(SystemExit) as e:
        gen.integrar(generado, descarga)
    assert "s01-a" in str(e.value)
    # y una celda de menos también
    descarga["cells"].pop()
    with pytest.raises(SystemExit):
        gen.integrar(generado, descarga)


def test_badge_y_metadata_en_el_sintetico(fuentes):
    nb = gen.cuaderno(fuentes)
    primera = nb["cells"][0]
    assert primera["cell_type"] == "markdown"
    assert fuente(primera).startswith(gen.BADGE + "\n\n# Entender una red")
    assert nb["metadata"] == gen.METADATA


# --- el notebook comiteado ------------------------------------------------------

def test_primera_celda_es_badge(nb):
    primera = nb["cells"][0]
    assert primera["cell_type"] == "markdown"
    texto = fuente(primera)
    assert texto.startswith("[![Abrir en Colab](https://colab.research.google"
                            ".com/assets/colab-badge.svg)]")
    assert ("https://colab.research.google.com/github/raya-lucaria/ia_o26/"
            "blob/main/course/10_deep_learning/_assets/02_entender_una_red.ipynb"
            in texto)


def test_metadata_gpu(nb):
    assert nb["metadata"]["accelerator"] == "GPU"
    assert nb["metadata"]["colab"]["gpuType"] == "T4"
    assert nb["nbformat"] == 4


def test_celdas_iguales_al_generador_ignorando_salidas(nb):
    esperado = gen.cuaderno()
    vistas = [(c["cell_type"], c["metadata"].get("id"), fuente(c))
              for c in nb["cells"]]
    generadas = [(c["cell_type"], c["metadata"]["id"], fuente(c))
                 for c in esperado["cells"]]
    assert len(vistas) == len(generadas), "corre el generador o --integrar"
    for v, g in zip(vistas, generadas):
        assert v == g, f"celda {g[1]} distinta: corre el generador o --integrar"
    assert nb["metadata"] == esperado["metadata"]


def test_sin_nota_para_sol(nb):
    assert gen.NOTA not in json.dumps(nb, ensure_ascii=False)
    for md in sorted(gen.FUENTES.glob("s*.texto.md")):
        assert gen.NOTA not in md.read_text(encoding="utf-8"), md.name


def test_imagenes_con_aviso_y_credito():
    """Cada ilustración usada tiene su aviso y su entrada con crédito.

    Corre sobre las fuentes que existan (no espera a las veinte); sobre el
    notebook comiteado, si existe, cada data URI va seguida del aviso.
    """
    usadas = {}
    for md in sorted(gen.FUENTES.glob("s*.texto.md")):
        for m in gen.IMAGEN.finditer(md.read_text(encoding="utf-8")):
            usadas.setdefault(m.group(2), md.name)
    ruta_json = gen.FUENTES / "ilustraciones.json"
    if usadas:
        datos = json.loads(ruta_json.read_text(encoding="utf-8"))
        if isinstance(datos, dict):
            datos = datos.get("ilustraciones", list(datos.values()))
        por_nombre = {d.get("nombre"): d for d in datos}
        sin_entrada = sorted(set(usadas) - set(por_nombre))
        if sin_entrada and faltantes():
            pytest.skip("notebook en obra; aún sin entrada en "
                        "ilustraciones.json: " + ", ".join(sin_entrada))
        for nombre, donde in usadas.items():
            entrada = por_nombre.get(nombre)
            assert entrada, f"{donde}: {nombre!r} no está en ilustraciones.json"
            for campo in ("prompt", "modelo", "fecha", "credito"):
                assert str(entrada.get(campo, "")).strip(), (nombre, campo)
    if NB.exists() and not faltantes():
        nb = json.loads(NB.read_text(encoding="utf-8"))
        for c in nb["cells"]:
            if c["cell_type"] != "markdown":
                continue
            lineas = fuente(c).split("\n")
            for i, linea in enumerate(lineas):
                if "](data:image/png;base64," in linea:
                    sig = next((l for l in lineas[i + 1:] if l.strip()), "")
                    assert sig.strip() == gen.AVISO, c["metadata"]["id"]
    elif not usadas:
        pytest.skip("ninguna fuente usa ilustraciones todavía")


def test_tamano_menor_8mb():
    if not NB.exists():
        pytest.skip(f"no existe {gen.RUTA_NB}")
    assert NB.stat().st_size <= TOPE, f"{NB.stat().st_size / 1e6:.1f} MB"


# --- las salidas de la corrida en Colab -----------------------------------------

@pytest.fixture(scope="module")
def ejecutado(nb):
    if not con_salidas(nb):
        pytest.skip("el notebook no tiene salidas (aún no se integra Colab)")
    return nb


def test_salidas_sin_error_si_ejecutado(ejecutado):
    for c in ejecutado["cells"]:
        for s in c.get("outputs", []):
            assert s.get("output_type") != "error", (
                f"{c['metadata'].get('id')}: {s.get('ename')}: {s.get('evalue')}")


def ids_de_tabla(texto):
    """IDs `sNN-…` como celdas completas de la tabla (HTML o texto plano)."""
    celdas = re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", texto, flags=re.S)
    if celdas:
        return [html.unescape(t).strip() for t in celdas
                if ID.match(html.unescape(t).strip())]
    return [t for t in texto.split() if ID.match(t)]


def test_tabla_maestra_ids_unicos(ejecutado):
    finales = [c for c in ejecutado["cells"] if c["cell_type"] == "code"
               and c["metadata"].get("id", "").startswith("s19-")
               and c.get("outputs")]
    assert finales, "§19 no tiene salidas"
    salidas = finales[-1]["outputs"]
    html_ = [s["data"]["text/html"] for s in salidas
             if "text/html" in s.get("data", {})]
    texto = "\n".join("".join(h) if isinstance(h, list) else h for h in html_)
    ids = ids_de_tabla(texto or textos_de_salida(finales[-1]))
    assert ids, "la última celda de §19 no muestra IDs de la tabla maestra"
    repetidos = sorted({i for i in ids if ids.count(i) > 1})
    assert not repetidos, f"IDs repetidos en la tabla maestra: {repetidos}"


def test_experimentos_completos(ejecutado):
    todo = "\n".join(textos_de_salida(c) for c in ejecutado["cells"]
                     if c["cell_type"] == "code")
    cuentas = EXPERIMENTOS.findall(todo)
    assert cuentas, "falta la línea «EXPERIMENTOS COMPLETOS: <n>»"
    assert int(cuentas[-1]) > 0


# --- la prueba de humo ------------------------------------------------------------

def directorio_mnist():
    for d in (os.environ.get("MNIST_DIR"),
              str(Path.home() / ".cache" / "mnist_torchvision")):
        if d and (Path(d) / "MNIST").is_dir():
            return d
    return None


def test_humo_rapido(tmp_path):
    """Todo el código del notebook corre en CPU con RAPIDO=1 (obligatoria
    localmente antes de publicar; CI no instala torch y se salta)."""
    pytest.importorskip("torch")
    mnist = directorio_mnist()
    if mnist is None:
        pytest.skip("no hay MNIST en $MNIST_DIR ni en ~/.cache/mnist_torchvision")
    requiere_secciones()
    ruta = tmp_path / "humo.py"
    assert gen.main(["--script", str(ruta)]) == 0
    entorno = dict(os.environ, RAPIDO="1", MPLBACKEND="Agg", MNIST_DIR=mnist)
    r = subprocess.run([sys.executable, str(ruta)], cwd=tmp_path, env=entorno,
                       capture_output=True, text=True, timeout=900)
    assert r.returncode == 0, r.stdout[-3000:] + "\n" + r.stderr[-3000:]
    assert EXPERIMENTOS.search(r.stdout), "el humo no imprimió EXPERIMENTOS"
