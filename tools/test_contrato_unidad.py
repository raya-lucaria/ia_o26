"""El contrato de lectura medible (`contrato_unidad.py`) mide lo que dice.

Cuatro grupos:

- (a) El parser y cada regla, con fragmentos Markdown sintéticos: cada regla
  detecta su violación y calla en el caso limpio.
- (b) Las unidades de `UNIDADES_CONTRATO` (opt-in) dan cero hallazgos alta o
  media. La lista arranca vacía, así que hoy este grupo no genera casos.
- (c) Humo: el CLI corre sobre dos unidades reales y cada hallazgo apunta a un
  `archivo:línea` que existe.
- (d) Cada ruta `tools/…` o `.claude/skills/…` citada en las skills existe. Se
  salta mientras falte alguna pieza de `ESQUELETO` (las dos `SKILL.md` y las
  nueve referencias).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import contrato_unidad as cu  # noqa: E402

RAIZ = cu.RAIZ


def reglas(texto, **umbrales):
    u = dict(cu.UMBRALES, **umbrales)
    return [h.regla for h in cu.medir_pagina(texto, "x.md", u)]


def pagina(cuerpo, tiempo="10m"):
    return f"---\nid: x\ntitle: X\nestimated_time: {tiempo}\n---\n\n# X\n\n{cuerpo}\n"


# --------------------------------------------------------------------------
# (a) Parser
# --------------------------------------------------------------------------

def test_el_parser_deja_fuera_frontmatter_codigo_formulas_tablas_y_figuras():
    texto = pagina(
        "Uno dos tres.\n\n"
        "```python\nesto no es prosa = 1\n```\n\n"
        "$$\nx = y\n$$\n\n"
        "$$a+b$$\n\n"
        "| a | b |\n|---|---|\n| 1 | 2 |\n\n"
        "::: figure {#f title=\"Una figura\"}\n![alt largo](f.svg)\n:::\n\n"
        "<!-- comentario\nde dos renglones -->\n\n"
        "Cuatro cinco."
    )
    pag = cu.parsear(texto)
    assert [u.texto for u in pag.unidades] == ["Uno dos tres.", "Cuatro cinco."]
    assert pag.frontmatter["estimated_time"] == "10m"
    assert len(pag.tablas) == 1 and pag.tablas[0].columnas == 2
    assert [i.en_figure for i in pag.imagenes] == [True]


def test_cada_item_de_lista_es_su_propia_unidad_con_su_continuacion():
    pag = cu.parsear(pagina("Intro.\n\n- Uno\n  sigue uno.\n- Dos.\n  - Anidado.\n1. Tres."))
    assert [(u.tipo, u.texto) for u in pag.unidades] == [
        ("parrafo", "Intro."),
        ("lista", "Uno sigue uno."),
        ("lista", "Dos."),
        ("lista", "Anidado."),
        ("lista", "Tres."),
    ]


def test_las_directivas_se_anidan_y_dan_contexto():
    pag = cu.parsear(pagina(
        '::: answer {#r of="e" title="R"}\nDentro.\n\n'
        '::: figure {#f title="F"}\n![a](b.svg)\n:::\n\nTambién dentro.\n:::\n\nFuera.'))
    assert [(u.texto, u.contexto) for u in pag.unidades] == [
        ("Dentro.", ("answer",)), ("También dentro.", ("answer",)), ("Fuera.", ())]
    d = pag.directivas[0]
    assert (d.nombre, d.id, d.of, d.title) == ("answer", "r", "e", "R")


def test_las_palabras_cuentan_formulas_y_enlaces_como_se_leen():
    assert cu.palabras("Sea $x_{cs}\\in\\{0,1\\}$ la **variable** de [[pag|la página]].") == 7
    assert cu.palabras("Ver `f(x)` y [el sitio](https://a.b/c) — @teo-1.") == 6


def test_las_frases_no_se_cortan_en_abreviaturas_ni_decimales():
    assert len(cu.frases("Vale 0.5 en la p. 3 del texto. Luego sube.")) == 2
    assert len(cu.frases("¿Quién mueve? Blancas. «Sí», dijo.")) == 3


@pytest.mark.parametrize("valor, esperado", [
    ("20m", 20), ("1h", 60), ("8h", 480), ("2h25m", 145), ("90min", 90), (45, 45),
    ("pronto", None), (None, None)])
def test_los_minutos_se_leen_en_los_formatos_del_curso(valor, esperado):
    assert cu.minutos(valor) == esperado


def test_un_frontmatter_con_1h_da_su_tope_de_palabras_por_minuto():
    texto = pagina(" ".join(["palabra"] * 9) + ".\n\n" + "\n\n".join(["Uno dos tres cuatro cinco."] * 20), "1h")
    assert "palabras-por-minuto" not in reglas(texto, ppm_max=2)
    assert "palabras-por-minuto" in reglas(texto, ppm_max=1)


# --------------------------------------------------------------------------
# (a) Reglas
# --------------------------------------------------------------------------

def test_frase_larga_se_detecta_y_la_corta_no():
    larga = " ".join(["palabra"] * 41) + "."
    assert "frase-larga" in reglas(pagina(larga, "1h"))
    assert "frase-larga" not in reglas(pagina("Una frase corta. Otra más.", "1h"))


def test_el_p90_de_las_frases_se_mide_por_pagina():
    media = " ".join(["palabra"] * 25) + "."
    corta = "Corta y clara."
    assert "frases-p90" in reglas(pagina("\n\n".join([media] * 3 + [corta] * 7), "1h"))
    assert "frases-p90" not in reglas(pagina("\n\n".join([media] + [corta] * 9), "1h"))


def test_negrita_excesiva_en_un_parrafo_y_en_la_media():
    cargado = "**a** b **c** d **e** f **g** h."
    assert "negrita-parrafo" in reglas(pagina(cargado, "1h"))
    assert "negrita-media" in reglas(pagina("**a** y **b**.\n\nUno **dos**.", "1h"))
    limpio = pagina("**Idea clave:** el resto.\n\nSin negrita.\n\nTampoco.", "1h")
    assert not {"negrita-parrafo", "negrita-media"} & set(reglas(limpio))


def test_parrafo_largo_y_item_largo():
    largo = " ".join(["uno dos tres cuatro cinco seis siete."] * 11)
    assert "parrafo-largo" in reglas(pagina(largo, "1h"))
    assert "parrafo-largo" in reglas(pagina("- " + largo, "1h"))
    lista = "\n".join(["- uno dos tres cuatro cinco seis siete ocho nueve diez."] * 10)
    assert "parrafo-largo" not in reglas(pagina(lista, "1h"))


# Excepciones de `referencias/lectura.md`: «Lo que traes», «Lo que hay que
# llevarse» y `**Piensa: …?**`.

LARGO = " ".join(["uno dos tres cuatro cinco seis siete ocho nueve diez"] * 8) + "."  # 80 palabras
CARGADO = "**a** b **c** d **e** f **g** h."
PROSA_TOPES = ("frase-larga", "frases-p90", "parrafo-largo",
               "negrita-parrafo", "negrita-media", "palabras-por-minuto")


def _excesos(cuerpo):
    """Las reglas de prosa que dispara `cuerpo`, con ppm_max=1 para que 10 palabras basten."""
    return {r for r in reglas(pagina(cuerpo, "10m"), ppm_max=1) if r in PROSA_TOPES}


@pytest.mark.parametrize("encabezado", [
    "## Lo que traes de la clase 1",
    "### Lo que traes",
    "## Lo que hay que llevarse",
    "#### Lo que hay que llevarse de esta página",
])
def test_la_seccion_lo_que_traes_o_llevarse_no_cuenta_para_ningun_tope(encabezado):
    cuerpo = f"{encabezado}\n\n{LARGO}\n\n{CARGADO}\n\n- {LARGO}\n\n**x** **y**."
    assert _excesos(cuerpo) == set()
    pag = cu.parsear(pagina(cuerpo))
    assert pag.unidades and all(u.excluida for u in pag.unidades)


def test_la_misma_prosa_en_una_seccion_ordinaria_si_cuenta():
    cuerpo = f"## Lo que sigue\n\n{LARGO}\n\n{CARGADO}\n\n**x** **y**."
    assert _excesos(cuerpo) == set(PROSA_TOPES)
    assert not any(u.excluida for u in cu.parsear(pagina(cuerpo)).unidades)


def test_la_seccion_excluida_termina_en_un_encabezado_de_igual_o_mayor_nivel():
    # Un ### dentro sigue excluido; el ## siguiente vuelve a contar; un # también.
    cuerpo = (f"## Lo que hay que llevarse\n\n{LARGO}\n\n### Detalle\n\n{LARGO}\n\n"
              f"## Siguiente\n\n{LARGO}")
    pag = cu.parsear(pagina(cuerpo))
    assert [u.excluida for u in pag.unidades] == [True, True, False]
    hallados = reglas(pagina(cuerpo, "1h"))
    assert hallados.count("parrafo-largo") == 1
    cuerpo = f"### Lo que traes\n\n{LARGO}\n\n# Otra parte\n\n{LARGO}"
    assert [u.excluida for u in cu.parsear(pagina(cuerpo)).unidades] == [True, False]


def test_la_tarjeta_en_cita_lo_que_traes_no_cuenta_y_la_prosa_de_despues_si():
    tarjeta = (f"> **Lo que traes de [[minimax|Minimax]].**\n>\n> - {LARGO}\n"
               f">   {CARGADO}\n>\n> {LARGO}\n> **x** **y** **z** **w**.")
    assert _excesos(tarjeta) == set()
    pag = cu.parsear(pagina(tarjeta + f"\n\n{LARGO}"))
    assert [u.excluida for u in pag.unidades] == [True, True, True, False]
    assert "parrafo-largo" in reglas(pagina(tarjeta + f"\n\n{LARGO}", "1h"))


def test_una_cita_ordinaria_si_cuenta():
    cita = f"> **Nota.** Algo.\n>\n> {LARGO}\n>\n> **Lo que traes** aquí ya no abre tarjeta."
    pag = cu.parsear(pagina(cita))
    assert not any(u.excluida for u in pag.unidades)
    assert "parrafo-largo" in reglas(pagina(cita, "1h"))


def test_las_tablas_dentro_de_lo_que_traes_se_siguen_midiendo():
    tabla = "| a | b | c | d | e | f |\n|---|---|---|---|---|---|\n| 1 | 2 | 3 | 4 | 5 | 6 |"
    assert "tabla-ancha" in reglas(pagina(f"## Lo que traes\n\n{tabla}"))


def test_piensa_no_cuenta_para_la_negrita_del_parrafo_ni_para_la_media():
    # Tres negritas + Piensa = 4 pares, pero solo 3 cuentan: no rebasa negrita_max=3.
    parrafo = "**Piensa: ¿qué sigue?** Luego **a**, **b** y **c**."
    assert cu.negritas(parrafo) == 4
    assert cu.negritas(parrafo, con_piensa=False) == 3
    assert "negrita-parrafo" not in reglas(pagina(parrafo, "1h"))
    # Una página hecha de preguntas «Piensa» y prosa sin negrita: media 0.
    preguntas = "\n\n".join(["**Piensa: con las siete piezas, ¿ya está decidido\ncuántos nodos hay?**",
                              "Sin negrita.", "**Piensa: ¿y luego?**", "Tampoco."])
    assert "negrita-media" not in reglas(pagina(preguntas, "1h"))
    # Una unidad que solo es «Piensa» no diluye la media de las demás.
    diluida = "\n\n".join(["**Piensa: ¿uno?**"] * 4 + ["**a** y **b**."])
    assert "negrita-media" in reglas(pagina(diluida, "1h"))


def test_una_negrita_ordinaria_o_un_piensa_sin_pregunta_si_cuentan():
    assert cu.negritas("**Piensa en esto.** **a** **b** **c**", con_piensa=False) == 4
    assert cu.negritas("**Piensa: sin signo.** **a** **b** **c**", con_piensa=False) == 4
    assert "negrita-parrafo" in reglas(pagina("**Piensa: sin signo.** **a** **b** **c**.", "1h"))


def test_piensa_si_cuenta_como_frase_y_como_palabras():
    larga = "**Piensa: " + " ".join(["palabra"] * 41) + "?**"
    assert "frase-larga" in reglas(pagina(larga, "1h"))


def test_imagen_suelta_contra_imagen_dentro_de_figure_y_contra_insignia():
    assert "imagen-fuera-de-figure" in reglas(pagina("![alt](a.svg)"))
    dentro = '::: figure {#f title="T"}\n![alt](a.svg)\n:::'
    assert "imagen-fuera-de-figure" not in reglas(pagina(dentro))
    insignia = "[![Abrir en Colab](badge.svg)](https://colab.example/x.ipynb)"
    assert "imagen-fuera-de-figure" not in reglas(pagina(insignia))


def test_tabla_ancha_y_la_excepcion_de_las_trazas():
    seis = "| a | b | c | d | e | f |\n|---|---|---|---|---|---|\n| 1 | 2 | 3 | 4 | 5 | 6 |"
    assert "tabla-ancha" in reglas(pagina(seis))
    traza = "| # | b | c | d | e | f | g |\n|---|---|---|---|---|---|---|\n| 1 | 2 | 3 | 4 | 5 | 6 | 7 |"
    assert "tabla-ancha" not in reglas(pagina(traza))
    en_directiva = '::: table {#t title="Traza de A"}\n' + seis + "\n:::"
    assert "tabla-ancha" not in reglas(pagina(en_directiva))
    ocho = "| # |" + " x |" * 7 + "\n|" + "---|" * 8
    assert "tabla-ancha" in reglas(pagina(ocho))


def ejercicio(pistas=1, respuestas=1, of="e", orden="ehr"):
    bloques = {
        "e": '::: exercise {#e title="Haz"}\nEnunciado.\n:::',
        "h": "\n\n".join(f'::: hint {{#p{i} of="{of}" title="Pista"}}\nPista.\n:::' for i in range(pistas)),
        "r": "\n\n".join(f'::: answer {{#r{i} of="{of}"}}\nRespuesta.\n:::' for i in range(respuestas)),
    }
    return pagina("\n\n".join(bloques[c] for c in orden if bloques[c]))


def test_el_ejercicio_completo_no_da_hallazgos():
    assert reglas(ejercicio(pistas=2)) == []


def test_ejercicio_sin_pista():
    assert reglas(ejercicio(pistas=0)) == ["ejercicio-sin-pista"]
    # Media, no alta: un micro de un paso puede ir sin pista (ejercicios.md §
    # Excepciones) y el script no sabe distinguirlo; la lente decide.
    assert cu.SEVERIDAD["ejercicio-sin-pista"] == "media"


def test_ejercicio_sin_respuesta_o_con_dos():
    assert "ejercicio-respuestas" in reglas(ejercicio(respuestas=0))
    assert "ejercicio-respuestas" in reglas(ejercicio(respuestas=2))


def test_answer_con_of_equivocado():
    r = reglas(ejercicio(of="otro"))
    assert {"of-sin-ejercicio", "ejercicio-sin-pista", "ejercicio-respuestas"} <= set(r)


def test_orden_exercise_hint_answer():
    assert "orden-ejercicio" in reglas(ejercicio(orden="erh"))
    assert "orden-ejercicio" in reglas(ejercicio(orden="hre"))


def test_minutos_que_no_suman_dan_aviso(tmp_path):
    def escribe(ruta, tiempo):
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(pagina("Texto.", tiempo), encoding="utf-8")

    escribe(tmp_path / "0_index.md", "1h")
    escribe(tmp_path / "1_clase/0_index.md", "45m")
    escribe(tmp_path / "1_clase/1_a.md", "20m")
    escribe(tmp_path / "1_clase/2_b.md", "20m")
    escribe(tmp_path / "1_clase/3_tarea.md", "50m")     # no cuenta
    escribe(tmp_path / "2_clase/0_index.md", "15m")
    escribe(tmp_path / "2_clase/1_c.md", "15m")
    avisos = [h for h in cu.sumas_de_minutos(tmp_path)]
    assert [(h.regla, h.severidad) for h in avisos] == [("suma-minutos", "aviso")]
    assert "40 min" in avisos[0].valor and "45 min" in avisos[0].valor

    escribe(tmp_path / "1_clase/0_index.md", "40m")
    escribe(tmp_path / "0_index.md", "55m")
    assert cu.sumas_de_minutos(tmp_path) == []


def test_una_clase_sola_se_cuadra_contra_su_propio_indice(tmp_path):
    for nombre, t in [("0_index.md", "30m"), ("1_a.md", "10m"), ("2_b.md", "10m")]:
        (tmp_path / nombre).write_text(pagina("Texto.", t), encoding="utf-8")
    assert [h.regla for h in cu.sumas_de_minutos(tmp_path)] == ["suma-minutos"]


def test_se_excluyen_tareas_y_directorios_de_soporte(tmp_path):
    for rel in ["1_a.md", "2_tarea.md", "_drafts/x.md", "_official/y.md", "_assets/z.md"]:
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(pagina("Texto."), encoding="utf-8")
    assert [p.name for p in cu.paginas_de(tmp_path)] == ["1_a.md"]


def test_los_umbrales_se_sobreescriben_por_unidad(monkeypatch):
    monkeypatch.setitem(cu.UMBRALES_POR_UNIDAD, "course/9_x", {"ppm_max": 150})
    assert cu.umbrales_para(RAIZ / "course/9_x")["ppm_max"] == 150
    assert cu.umbrales_para(RAIZ / "course/9_x")["frase_max"] == cu.UMBRALES["frase_max"]
    assert cu.umbrales_para(RAIZ / "course/7_juegos")["ppm_max"] == cu.UMBRALES["ppm_max"]


def test_cada_regla_tiene_severidad_conocida():
    assert set(cu.SEVERIDAD.values()) <= set(cu.ORDEN_SEVERIDAD)


# --------------------------------------------------------------------------
# (b) Unidades con contrato obligatorio
# --------------------------------------------------------------------------

@pytest.mark.parametrize("unidad", cu.UNIDADES_CONTRATO)
def test_la_unidad_con_contrato_no_tiene_hallazgos_alta_ni_media(unidad):
    graves = [str(h) for h in cu.auditar_unidad(RAIZ / unidad) if h.severidad in ("alta", "media")]
    assert not graves, "\n".join(graves)


# --------------------------------------------------------------------------
# (c) Humo del CLI
# --------------------------------------------------------------------------

@pytest.mark.parametrize("unidad", ["course/7_juegos", "course/6_optimizacion"])
def test_el_cli_corre_y_cada_hallazgo_apunta_a_un_renglon_real(unidad):
    if not (RAIZ / unidad).is_dir():
        pytest.skip(f"{unidad} no existe en este árbol")
    r = subprocess.run([sys.executable, str(RAIZ / "tools/contrato_unidad.py"), unidad, "--json"],
                       cwd=RAIZ, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, r.stderr
    datos = json.loads(r.stdout)
    assert datos["hallazgos"], "una unidad real sin un solo hallazgo es sospechosa"
    for h in datos["hallazgos"]:
        archivo = RAIZ / h["archivo"]
        assert archivo.is_file(), h
        assert 1 <= h["linea"] <= len(archivo.read_text(encoding="utf-8").splitlines()), h
        assert h["severidad"] == cu.SEVERIDAD[h["regla"]]


def test_el_cli_detecta_los_errores_sembrados_conocidos(tmp_path):
    """6.5 tiene 19 imágenes sin ::: figure. Los ejercicios sin pista se siembran
    en una unidad sintética de dos clases: la semilla real de juegos (las clases 1
    y 4) desapareció al sacar «Cuando no hay turnos» a `_drafts/`, que no se mide,
    y la homologación deja la clase 1 sin hallazgos medios."""
    practica = RAIZ / "course/6_optimizacion/5_practica_de_modelado"
    if not practica.is_dir():
        pytest.skip("falta la unidad de referencia")
    imagenes = [h for h in cu.auditar_unidad(practica) if h.regla == "imagen-fuera-de-figure"]
    assert len(imagenes) >= 19

    unidad = tmp_path / "9_unidad"
    for rel, texto in [
        ("1_clase/1_con_ejercicio.md", ejercicio(pistas=0)),
        ("2_clase/1_otra.md", ejercicio(pistas=0)),
        ("2_clase/2_imagen.md", pagina("Texto.\n\n![suelta](x.svg)")),
        ("2_clase/3_completo.md", ejercicio(pistas=1)),
        ("_drafts/1_no_se_mide.md", ejercicio(pistas=0)),
    ]:
        (unidad / rel).parent.mkdir(parents=True, exist_ok=True)
        (unidad / rel).write_text(texto, encoding="utf-8")
    hallazgos = cu.auditar_unidad(unidad)
    clase = lambda h: Path(h.archivo).relative_to(unidad).parts[0]
    sin_pista = {clase(h) for h in hallazgos if h.regla == "ejercicio-sin-pista"}
    assert sin_pista == {"1_clase", "2_clase"}
    assert [Path(h.archivo).name for h in hallazgos if h.regla == "imagen-fuera-de-figure"] == ["2_imagen.md"]


# --------------------------------------------------------------------------
# (d) Rutas citadas en las skills
# --------------------------------------------------------------------------

SKILLS = RAIZ / ".claude/skills"
RE_RUTA = re.compile(r"(?<![\w/.-])((?:tools|\.claude/skills)/[\w./<>*{}…-]+)")


def rutas_citadas():
    for md in sorted(SKILLS.rglob("*.md")):
        for n, renglon in enumerate(md.read_text(encoding="utf-8").splitlines(), start=1):
            for m in RE_RUTA.finditer(renglon):
                ruta = m.group(1).rstrip(".,;:)")
                if re.search(r"[<>*{}…]", ruta):
                    continue            # plantilla (tools/gen_<unidad>.py), no ruta
                yield md.relative_to(RAIZ), n, ruta


# Mientras falte alguna pieza del esqueleto las skills están a medio escribir y
# sus referencias cruzadas todavía no pueden resolverse: la prueba se salta.
ESQUELETO = ["unidad/SKILL.md", "unidad-auditar/SKILL.md"] + [
    f"unidad/referencias/{n}.md" for n in (
        "anatomia", "lectura", "pedagogia", "ejercicios", "figuras",
        "codigo", "verificacion", "revision", "defectos")]


def test_cada_ruta_citada_en_las_skills_existe():
    faltan_piezas = [p for p in ESQUELETO if not (SKILLS / p).is_file()]
    if faltan_piezas:
        pytest.skip(f".claude/skills incompleta, falta: {', '.join(faltan_piezas)}")
    faltan = [f"{md}:{n} → {ruta}" for md, n, ruta in rutas_citadas() if not (RAIZ / ruta).exists()]
    assert not faltan, "\n".join(faltan)
