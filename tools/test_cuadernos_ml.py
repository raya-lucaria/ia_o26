"""Los notebooks de la unidad 9 son los que arma gen_cuadernos_ml.py hoy.

Contrato §6.6 (U.T4, D-003, D-005, D-006). Todas las pruebas van
parametrizadas por stem, con id `c<N>-<stem>`, y respetan `ML_CLASES` (lista
de clases separadas por comas; sin la variable, todas). Nunca se filtran
con `-k`. Las reglas:

1. compara sin escribir: `_assets/<stem>.ipynb` = `serializar(cuaderno(stem))`;
2. claves completas y anatomía de §6.2 en orden;
3. de punta a punta, en un proceso aparte, con el cargador real y
   `ML_LAB_PRUEBA=1` (solo si existe tools/aprendizaje_maquina.py);
4. el cargador en sus escenarios (descarga, sin red, copia local obsoleta ya
   importada, copia de otra X, copia local más nueva de la misma X);
5. forma: badge, `cellView: form`, sin salidas, celdas cortas, `REQUIERE` y
   respaldo incrustado byte-idéntico a la fuente (DECISIÓN
   prog-lab-cuadernos-1 sobre D-006);
6. notación del guion con tools/notacion_ml.py;
7. los `tarea_*` no traen `-explica` ni `<details>`;
8. solo las celdas autorizadas leen `.prueba`.

El notebook de humo (`tools/cuadernos_ml/_humo.*`) prueba el generador y el
cargador sin depender de ml_lab: corre siempre contra un ml_lab mínimo de
prueba (D-021) y, si la fuente real existe, también contra ella.
"""
import base64
import json
import os
import re
import subprocess
import sys
import zlib
from pathlib import Path

import pytest

import gen_cuadernos_ml as gen
import notacion_ml

RAIZ = Path(__file__).resolve().parent.parent
HAY_LAB = gen.LAB.exists()
SIN_LAB = "tools/aprendizaje_maquina.py aún no existe en esta rama (U.T2a)"
MAX_LINEAS, MAX_ANCHO = 40, 88
TOPE_KB = 300

STUB = '''"""ml_lab mínimo de prueba: solo lo que usa la celda de arranque."""
VERSION = "{version}"


def requiere(version_minima):
    x, y = (int(p) for p in VERSION.split("."))
    x0, y0 = (int(p) for p in version_minima.split("."))
    if x != x0 or y < y0:
        raise RuntimeError(f"cargó ml_lab {{VERSION}} y el notebook pide "
                           f"{{version_minima}}: vuelve a correr la celda de "
                           "arranque")


def tema(nombre="claro"):
    return None
'''

# §6.6 regla 8: lista CERRADA de celdas que pueden abrir la prueba. Un número
# es «cualquier celda de código de ese bloque»; una cadena, la clave exacta.
# Otra celda entra por SOLICITUD a coord.
AUTORIZADAS = {
    "03_entrenamiento_y_prueba": {3, 4},
    "tarea_2_separar_y_elegir": {6, "bloque-4-juega"},  # el reporte final abre
                                    # la prueba una vez (clase_2 §10.6)
    "07_el_lagrangeano_en_accion": {"bloque-5-prueba"},
    "tarea_3_cincuenta_variables": {6},
    "tarea_4_desbalanceo_multiclase": {6},
    "tarea_5b_fugas": {5},          # + la celda que siembra la separación mal
                                    # hecha: la confirma la clase 5 (§10.6)
}
LEE_PRUEBA = re.compile(r"\.prueba\b|\[\s*['\"]prueba['\"]\s*\]"
                        r"|getattr\([^)]*['\"]prueba['\"]")


# --- Qué stems ---------------------------------------------------------------

def _stems():
    clases = gen.clases_de_entorno(os.environ.get("ML_CLASES"))
    return gen.seleccion(clases)


STEMS = _stems()
IDS = [f"c{gen.clase_de(s)}-{s}" for s in STEMS]
HUMO = "_humo"


@pytest.fixture(scope="session")
def stub(tmp_path_factory):
    ruta = tmp_path_factory.mktemp("stub") / "ml_lab.py"
    ruta.write_text(STUB.format(version="1.0"), encoding="utf-8")
    return ruta


def _labs():
    return ["stub"] + (["real"] if HAY_LAB else [])


def _lab(nombre, stub):
    return stub if nombre == "stub" else gen.LAB


def _celdas_py(stem):
    return gen.leer_celdas(gen.fuente_py(stem), f"{stem}.py")


def _guion(stem):
    return gen.leer_guion(gen.fuente_guion(stem), f"{stem}.texto.md")


def _texto(celda):
    return "".join(celda["source"])


# --- 1. Compara sin escribir ---------------------------------------------------

@pytest.mark.skipif(not HAY_LAB, reason=SIN_LAB)
@pytest.mark.parametrize("stem", STEMS, ids=IDS)
def test_1_el_notebook_comiteado_es_el_que_genera_hoy(stem):
    ruta = gen.destino(stem)
    assert ruta.exists(), f"falta {ruta.relative_to(RAIZ)}: corre tools/gen_cuadernos_ml.py"
    hoy = gen.serializar(gen.cuaderno(stem))
    assert ruta.read_text(encoding="utf-8") == hoy, (
        f"{ruta.relative_to(RAIZ)} no es el que genera hoy: corre "
        "tools/gen_cuadernos_ml.py (nunca se edita a mano)")


# --- 2. Claves y anatomía ------------------------------------------------------

PARTES = re.compile(r"^bloque-(\d+)-(predice|juega|prueba|mira|explica)$")


def errores_de_anatomia(stem, celdas):
    """Lo que viola la anatomía de §6.2 en [(tipo, clave, cuerpo)]."""
    tarea, errores = gen.es_tarea(stem), []
    claves = [c for _, c, _ in celdas]
    if len(set(claves)) != len(claves):
        dup = sorted({c for c in claves if claves.count(c) > 1})
        errores.append(f"claves repetidas: {dup}")
    sec = [(t, c) for t, c, _ in celdas]
    i = 0

    def toma(clave, tipos, opcional=False):
        nonlocal i
        if i < len(sec) and sec[i][1] == clave:
            if sec[i][0] not in tipos:
                errores.append(f"{clave} es [{sec[i][0]}], se esperaba {tipos}")
            i += 1
            return True
        if not opcional:
            vista = sec[i][1] if i < len(sec) else "(fin)"
            errores.append(f"se esperaba {clave} y viene {vista}")
        return False

    toma("portada", {"texto"})
    toma("idea", {"texto"})
    k = 0
    while i < len(sec) and re.match(r"bloque-\d+-", sec[i][1]):
        k += 1
        juega = {"codigo", "codigo-visible"} if tarea else {"codigo"}
        toma(f"bloque-{k}-predice", {"texto"})
        toma(f"bloque-{k}-juega", juega)
        toma(f"bloque-{k}-prueba", {"codigo"}, opcional=True)
        toma(f"bloque-{k}-mira", {"texto"})
        if tarea:
            if toma(f"bloque-{k}-explica", {"texto"}, opcional=True):
                errores.append(f"bloque-{k}-explica: una tarea no explica")
            toma(f"entrega-{k}", {"texto"})
        else:
            toma(f"bloque-{k}-explica", {"texto"})
        if errores:
            return errores
    if not gen.es_herramienta(stem) and not 3 <= k <= 6:
        errores.append(f"{k} bloques; van de 3 a 6")
    if toma("taller-intro", {"texto"}, opcional=True):
        toma("taller", {"codigo-visible"})
    if toma("galeria-intro", {"texto"}, opcional=True):
        toma("galeria", {"codigo"})
    while i < len(sec) and sec[i][1].startswith("ejercicio-"):
        clave = sec[i][1]
        if clave.endswith("-respuesta"):
            errores.append(f"{clave} sin su ejercicio justo antes")
            i += 1
            continue
        toma(clave, {"texto"})
        if toma(f"{clave}-respuesta", {"texto"}, opcional=True) and tarea:
            errores.append(f"{clave}-respuesta: una tarea no trae respuestas")
    toma("cierre", {"texto"})
    if i < len(sec):
        errores.append(f"sobra o está fuera de lugar: {sec[i][1]}")
    for tipo, clave, cuerpo in celdas:
        cuerpo = gen.titulo_primero(cuerpo)
        if tipo == "codigo" and not cuerpo.startswith("#@title"):
            errores.append(f"[codigo] {clave}: va colapsada, con #@title "
                           "en su primera línea")
        if tipo == "codigo-visible" and cuerpo.startswith("#@title"):
            errores.append(f"[codigo-visible] {clave}: va visible, sin #@title")
    return errores


def errores_de_claves(celdas, guion):
    errores = []
    texto_py = [c for t, c, _ in celdas if t == "texto"]
    claves_guion = [c for c, _ in guion]
    if len(set(claves_guion)) != len(claves_guion):
        errores.append("el guion repite una sección")
    if set(texto_py) - set(claves_guion):
        errores.append(f"sin sección en el guion: {sorted(set(texto_py) - set(claves_guion))}")
    if set(claves_guion) - set(texto_py):
        errores.append(f"sección huérfana del guion: {sorted(set(claves_guion) - set(texto_py))}")
    for clave, md in guion:
        if not md.strip():
            errores.append(f"la sección {clave} está vacía")
        titulos = re.findall(r"^# \S", md, re.M)
        if clave == "portada" and len(titulos) != 1:
            errores.append("la portada lleva un solo título «# …»")
        if clave != "portada" and titulos:
            errores.append(f"{clave}: el «# » de nivel 1 va solo en la portada")
        if re.search(r"^###", md, re.M):
            errores.append(f"{clave}: dentro de una celda no hay «###»")
        if "colab-badge" in md:
            errores.append(f"{clave}: el badge lo escribe el generador")
    return errores


@pytest.mark.parametrize("stem", STEMS + [HUMO], ids=IDS + [f"humo-{HUMO}"])
def test_2_claves_completas_y_anatomia_en_orden(stem):
    celdas = _celdas_py(stem)
    errores = errores_de_claves(celdas, _guion(stem))
    errores += errores_de_anatomia(stem, celdas)
    assert not errores, f"{stem}:\n  " + "\n  ".join(errores)


def test_2_la_anatomia_rechaza_lo_que_debe():
    def py(*pares):
        return [(t, c, "#@title x" if t == "codigo" else "") for t, c in pares]
    base = [("texto", "portada"), ("texto", "idea")]
    bloque = lambda k: [("texto", f"bloque-{k}-predice"),
                        ("codigo", f"bloque-{k}-juega"),
                        ("texto", f"bloque-{k}-mira"),
                        ("texto", f"bloque-{k}-explica")]
    bueno = base + bloque(1) + bloque(2) + bloque(3) + [("texto", "cierre")]
    assert errores_de_anatomia("01_que_es_f", py(*bueno)) == []
    dos = base + bloque(1) + bloque(2) + [("texto", "cierre")]
    assert errores_de_anatomia("01_que_es_f", py(*dos))
    salto = base + bloque(1) + bloque(3) + bloque(4) + [("texto", "cierre")]
    assert errores_de_anatomia("01_que_es_f", py(*salto))
    assert errores_de_anatomia("tarea_1_proponer_phi", py(*bueno))
    sin_titulo = [(t, c, "") for t, c in bueno]
    assert errores_de_anatomia("01_que_es_f", sin_titulo)
    guion = [(c, "texto") for t, c in bueno if t == "texto"]
    assert errores_de_claves(py(*bueno), guion[1:])        # falta portada
    assert errores_de_claves(py(*bueno), guion + [("extra", "x")])


# --- 5. Forma -------------------------------------------------------------------

def errores_de_forma(stem, nb, texto_lab):
    errores, celdas = [], nb["cells"]
    url = gen.URL_COLAB.format(stem=stem)
    primera = _texto(celdas[0]).split("\n")[0]
    if primera != gen.BADGE.format(url=url):
        errores.append(f"la primera línea no es el badge de {url}")
    for n, c in enumerate(celdas):
        texto = _texto(c)
        if c["cell_type"] == "code":
            if c.get("outputs") or c.get("execution_count") is not None:
                errores.append(f"celda {n}: tiene salidas")
            if texto.startswith("#@title") != (c["metadata"].get("cellView") == "form"):
                errores.append(f"celda {n}: #@title y cellView: form van juntos")
            if n == 1:
                continue
            lineas = texto.split("\n")
            if len(lineas) > MAX_LINEAS:
                errores.append(f"celda {n}: {len(lineas)} líneas (> {MAX_LINEAS})")
            largas = [r for r in lineas if len(r) > MAX_ANCHO]
            if largas:
                errores.append(f"celda {n}: líneas de más de {MAX_ANCHO} columnas: "
                               f"{largas[0]!r}")
    arranque = _texto(celdas[1])
    if not arranque.startswith("#@title ▶ Corre esta celda primero"):
        errores.append("la segunda celda no es la de arranque")
    req = re.search(r'^REQUIERE = "([\d.]+)"', arranque, re.M)
    resp = re.search(r'^_RESPALDO = "([A-Za-z0-9+/=]+)"', arranque, re.M)
    if not req or req.group(1) != gen.version_de(texto_lab):
        errores.append("REQUIERE no es la VERSION de la fuente")
    if not resp or zlib.decompress(base64.b64decode(resp.group(1))).decode(
            "utf-8") != texto_lab:
        errores.append("el respaldo no es byte-idéntico a la fuente: corre "
                       "tools/gen_cuadernos_ml.py")
    if "ml.requiere(REQUIERE)" not in arranque:
        errores.append("el arranque no llama ml.requiere(REQUIERE)")
    peso = len(gen.serializar(nb).encode("utf-8")) / 1024
    if peso > TOPE_KB:
        errores.append(f"pesa {peso:.0f} KB (> {TOPE_KB}): avisar en la bitácora")
    return errores


@pytest.mark.skipif(not HAY_LAB, reason=SIN_LAB)
@pytest.mark.parametrize("stem", STEMS, ids=IDS)
def test_5_forma(stem):
    errores = errores_de_forma(stem, gen.cuaderno(stem),
                               gen.LAB.read_text(encoding="utf-8"))
    assert not errores, f"{stem}:\n  " + "\n  ".join(errores)


@pytest.mark.parametrize("lab", _labs())
def test_5_forma_del_humo(lab, stub):
    ruta = _lab(lab, stub)
    nb = gen.cuaderno(HUMO, lab=ruta)
    errores = errores_de_forma(HUMO, nb, ruta.read_text(encoding="utf-8"))
    assert not errores, "\n  ".join(errores)


def test_5_la_forma_atrapa_un_respaldo_viejo(stub, tmp_path):
    nb = gen.cuaderno(HUMO, lab=stub)
    otro = tmp_path / "ml_lab.py"
    otro.write_text(STUB.format(version="1.1"), encoding="utf-8")
    errores = errores_de_forma(HUMO, nb, otro.read_text(encoding="utf-8"))
    assert any("REQUIERE" in e for e in errores)
    assert any("respaldo" in e for e in errores)


def test_el_generador_es_determinista_y_sin_guion_deja_las_claves(stub):
    a = gen.serializar(gen.cuaderno(HUMO, lab=stub))
    assert a == gen.serializar(gen.cuaderno(HUMO, lab=stub))
    solo = gen.cuaderno(HUMO, lab=stub, solo_codigo=True)
    textos = [_texto(c) for c in solo["cells"] if c["cell_type"] == "markdown"]
    claves = [c for t, c, _ in _celdas_py(HUMO) if t == "texto"]
    assert textos[0].endswith(f"`{claves[0]}`")
    assert textos[1:] == [f"`{c}`" for c in claves[1:]]


def test_abre_prueba_queda_bajo_el_titulo():
    cuerpo = "# abre-prueba: elige con la prueba a propósito\n#@title Juega\nx = 1"
    assert gen.titulo_primero(cuerpo).split("\n")[:2] == [
        "#@title Juega", "# abre-prueba: elige con la prueba a propósito"]


# --- ML_CLASES ------------------------------------------------------------------

def test_ml_clases_restringe_la_corrida_sin_argumentos(tmp_path, monkeypatch,
                                                       stub):
    fuentes, assets = tmp_path / "fuentes", tmp_path / "assets"
    fuentes.mkdir()
    for stem in ("01_que_es_f", "03_entrenamiento_y_prueba", "06_leer_el_error"):
        for ext in (".py", ".texto.md"):
            (fuentes / f"{stem}{ext}").write_text(
                (gen.FUENTES / f"{HUMO}{ext}").read_text(encoding="utf-8"),
                encoding="utf-8")
    monkeypatch.setattr(gen, "FUENTES", fuentes)
    monkeypatch.setattr(gen, "ASSETS_ML", assets)
    monkeypatch.setattr(gen, "LAB", stub)
    monkeypatch.setattr(gen, "RAIZ", tmp_path)
    gen.main([], entorno={"ML_CLASES": "2"})
    assert sorted(p.name for p in assets.iterdir()) == [
        "03_entrenamiento_y_prueba.ipynb"]
    gen.main(["--clase", "3"], entorno={"ML_CLASES": "2"})
    assert sorted(p.name for p in assets.iterdir()) == [
        "03_entrenamiento_y_prueba.ipynb", "06_leer_el_error.ipynb"]
    gen.main([], entorno={})
    assert len(list(assets.iterdir())) == 3


def test_ml_clases_se_lee_bien():
    assert gen.clases_de_entorno(None) is None
    assert gen.clases_de_entorno("") is None
    assert gen.clases_de_entorno("2") == {2}
    assert gen.clases_de_entorno("1, 3,u") == {1, 3}
    with pytest.raises(ValueError):
        gen.clases_de_entorno("dos")


def test_cada_stem_tiene_su_clase():
    for clase, stems in gen.CUADERNOS.items():
        for stem in stems:
            assert gen.clase_de(stem) == clase
    assert set(AUTORIZADAS) <= {s for v in gen.CUADERNOS.values() for s in v}


# --- 3 y 4. Ejecución en un proceso aparte ---------------------------------------

CORREDOR = '''import json, os, sys, traceback
celdas = json.load(open(sys.argv[1], encoding="utf-8"))
g = {"__name__": "__main__"}
for clave, fuente in celdas:
    try:
        exec(compile(fuente, f"<celda {clave}>", "exec"), g)
    except BaseException:
        traceback.print_exc()
        print(f"FALLÓ la celda {clave}", file=sys.stderr)
        sys.exit(1)
'''

VERIFICA = '''import os, sys
assert sys.modules["ml_lab"] is ml, "ml no es el ml_lab de sys.modules"
assert ml.VERSION == os.environ["ESPERA_VERSION"], ml.VERSION
assert os.path.abspath(ml.__file__) == os.path.abspath("ml_lab.py"), ml.__file__
with open("ml_lab.py", encoding="utf-8") as f:
    assert f.read() == open(os.environ["ESPERA_TEXTO"], encoding="utf-8").read()
print("VERIFICADO", ml.VERSION)
'''


def correr(celdas, directorio, entorno_extra, timeout=120):
    """Corre [(clave, fuente)] en orden en un proceso aparte, en `directorio`."""
    directorio = Path(directorio)
    (directorio / "_corredor.py").write_text(CORREDOR, encoding="utf-8")
    (directorio / "_celdas.json").write_text(json.dumps(celdas), encoding="utf-8")
    entorno = dict(os.environ, ML_LAB_PRUEBA="1", MPLBACKEND="Agg",
                   **entorno_extra)
    return subprocess.run([sys.executable, "_corredor.py", "_celdas.json"],
                          cwd=directorio, env=entorno, capture_output=True,
                          text=True, timeout=timeout)


def celdas_de_codigo(nb):
    salida = []
    for n, c in enumerate(nb["cells"]):
        if c["cell_type"] != "code":
            continue
        lineas = [r for r in _texto(c).split("\n")
                  if not r.lstrip().startswith(("!", "%"))]
        salida.append((f"#{n}", "\n".join(lineas)))
    return salida


def _de_punta_a_punta(nb, lab, tmp_path):
    r = correr(celdas_de_codigo(nb), tmp_path,
               {"ML_LAB_URL": Path(lab).resolve().as_uri()})
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-4000:]
    assert "Listo: ml_lab" in r.stdout


@pytest.mark.skipif(not HAY_LAB, reason=SIN_LAB)
@pytest.mark.parametrize("stem", STEMS, ids=IDS)
def test_3_corre_de_punta_a_punta(stem, tmp_path):
    _de_punta_a_punta(gen.cuaderno(stem), gen.LAB, tmp_path)


@pytest.mark.parametrize("lab", _labs())
def test_3_el_humo_corre_de_punta_a_punta(lab, stub, tmp_path):
    ruta = _lab(lab, stub)
    _de_punta_a_punta(gen.cuaderno(HUMO, lab=ruta), ruta, tmp_path)


def _variante(directorio, nombre, texto_lab, version):
    ruta = Path(directorio) / nombre
    texto = re.sub(r'^VERSION\s*=\s*"[\d.]+"', f'VERSION = "{version}"',
                   texto_lab, count=1, flags=re.M)
    ruta.write_text(texto, encoding="utf-8")
    return ruta


ESCENARIOS = ["descarga", "sin-red", "local-obsoleta-importada", "otra-X",
              "local-mas-nueva"]


@pytest.mark.parametrize("lab", _labs())
@pytest.mark.parametrize("escenario", ESCENARIOS)
def test_4_el_cargador(escenario, lab, stub, tmp_path):
    fuente = _lab(lab, stub).resolve()
    texto_lab = fuente.read_text(encoding="utf-8")
    nb = gen.cuaderno(HUMO, lab=fuente)
    arranque = _texto(nb["cells"][1])
    trabajo, aparte = tmp_path / "trabajo", tmp_path / "aparte"
    trabajo.mkdir(), aparte.mkdir()
    rota = (aparte / "no-existe.py").as_uri()
    version = gen.version_de(texto_lab)
    x, y = version.split(".")
    previas, url, espera = [], rota, fuente
    if escenario == "descarga":
        url = fuente.as_uri()
    elif escenario == "local-obsoleta-importada":
        _variante(trabajo, "ml_lab.py", texto_lab, "0.0")
        previas = [("previa", "import ml_lab\nassert ml_lab.VERSION == '0.0'")]
    elif escenario == "otra-X":
        url = _variante(aparte, "ml_lab.py", texto_lab, f"{int(x) + 1}.0").as_uri()
    elif escenario == "local-mas-nueva":
        espera = _variante(aparte, "nueva.py", texto_lab, f"{x}.{int(y) + 7}")
        (trabajo / "ml_lab.py").write_text(espera.read_text(encoding="utf-8"),
                                           encoding="utf-8")
    r = correr(previas + [("arranque", arranque), ("verifica", VERIFICA)],
               trabajo, {"ML_LAB_URL": url,
                         "ESPERA_VERSION": gen.version_de(
                             espera.read_text(encoding="utf-8")),
                         "ESPERA_TEXTO": str(espera)})
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-4000:]
    assert "VERIFICADO" in r.stdout


# --- 6, 7 y 8. Guion y código -------------------------------------------------------

@pytest.mark.parametrize("stem", STEMS + [HUMO], ids=IDS + [f"humo-{HUMO}"])
def test_6_notacion_del_guion(stem):
    ruta = gen.FUENTES / f"{stem}.texto.md"
    hall = notacion_ml.revisar_archivo(ruta, clase=gen.clase_de(stem))
    assert not hall, "\n".join(f"{ruta.name}:{n}: [{r}] {m}" for n, r, m in hall)


@pytest.mark.parametrize("stem", [s for s in STEMS if gen.es_tarea(s)],
                         ids=[i for s, i in zip(STEMS, IDS) if gen.es_tarea(s)])
def test_7_las_tareas_no_traen_respuestas(stem):
    guion = _guion(stem)
    assert not [c for c, _ in guion if c.endswith("-explica")]
    assert not [c for c, md in guion if "<details" in md]


def autorizada(stem, clave):
    for regla in AUTORIZADAS.get(stem, ()):
        if regla == clave or (isinstance(regla, int)
                              and clave.startswith(f"bloque-{regla}-")):
            return True
    return False


def errores_de_prueba(stem, celdas):
    errores = []
    for tipo, clave, cuerpo in celdas:
        if tipo == "texto":
            continue
        marcada = bool(gen.ABRE_PRUEBA.match(cuerpo.split("\n")[0]))
        codigo = "\n".join(r.split("#")[0] for r in cuerpo.split("\n"))
        if marcada and not autorizada(stem, clave):
            errores.append(f"{clave}: marcada «abre-prueba» pero no está en la "
                           "lista cerrada de §6.6 regla 8 (SOLICITUD a coord)")
        if LEE_PRUEBA.search(codigo) and not marcada:
            errores.append(f"{clave}: lee .prueba sin «# abre-prueba: <razón>» "
                           "en la línea siguiente al marcador")
    return errores


@pytest.mark.parametrize("stem", STEMS + [HUMO], ids=IDS + [f"humo-{HUMO}"])
def test_8_solo_las_celdas_autorizadas_leen_la_prueba(stem):
    errores = errores_de_prueba(stem, _celdas_py(stem))
    assert not errores, f"{stem}:\n  " + "\n  ".join(errores)


def test_8_la_guarda_de_la_prueba_atrapa_lo_que_debe():
    lee = "#@title J\nR = riesgo(datos.prueba)"
    marcada = "# abre-prueba: por contrato\n" + lee
    assert errores_de_prueba("01_que_es_f", [("codigo", "bloque-1-juega", lee)])
    assert errores_de_prueba("01_que_es_f",
                             [("codigo", "bloque-1-juega", marcada)])
    assert not errores_de_prueba("03_entrenamiento_y_prueba",
                                 [("codigo", "bloque-4-juega", marcada)])
    assert errores_de_prueba("03_entrenamiento_y_prueba",
                             [("codigo", "bloque-4-juega", lee)])
    assert not errores_de_prueba("07_el_lagrangeano_en_accion",
                                 [("codigo", "bloque-5-prueba", marcada)])
    assert errores_de_prueba("07_el_lagrangeano_en_accion",
                             [("codigo", "bloque-5-juega", marcada)])
    alias = "#@title J\nd = datos\nx = d['prueba']"
    assert errores_de_prueba("01_que_es_f", [("codigo", "bloque-1-juega", alias)])
