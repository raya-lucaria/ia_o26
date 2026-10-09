"""Los minutos de la unidad de juegos suman lo que dicen.

Cada pagina declara su `estimated_time`, la tabla de su clase (`jue-ruta-N`)
lo repite, el indice de la clase declara la suma, la tabla de la unidad
(`jue-clases`) la repite, y el indice de la unidad declara el total en el
frontmatter y en la prosa («El recorrido de lectura suma **…**»). Nada
ataba esas cinco copias: la clase 2 llego a declarar 145m cuando sus
paginas sumaban 155m. Las filas marcadas «aparte» en la tabla de una clase
(las tareas de refuerzo) no cuentan en la suma; su total va en la frase de
las tareas («Las cuatro tareas suman unas **N horas más**»), redondeado.
"""
import re
from pathlib import Path

import pytest

UNIDAD = Path(__file__).resolve().parent.parent / "course/7_juegos"
CLASES = sorted(p for p in UNIDAD.iterdir() if p.is_dir() and re.match(r"\d+_", p.name))


def minutos(texto):
    """'8h', '7h20m', '145m', '45m, aparte' -> minutos."""
    m = re.fullmatch(r"\s*(?:(\d+)h)?\s*(?:(\d+)m)?\s*(?:,\s*aparte)?\s*", texto)
    assert m and (m.group(1) or m.group(2)), f"tiempo ilegible: {texto!r}"
    return int(m.group(1) or 0) * 60 + int(m.group(2) or 0)


def minutos_en_prosa(texto):
    """'8 horas', '7 horas y 20 minutos', '3 horas más' -> minutos."""
    h = re.search(r"(\d+)\s+horas?", texto)
    m = re.search(r"(\d+)\s+minutos?", texto)
    assert h or m, f"tiempo ilegible: {texto!r}"
    return (int(h.group(1)) * 60 if h else 0) + (int(m.group(1)) if m else 0)


def estimado(pagina):
    m = re.search(r"^estimated_time:\s*(\S+)\s*$", pagina.read_text(encoding="utf-8"), re.M)
    assert m, f"{pagina.name} no declara estimated_time"
    return minutos(m.group(1))


def filas(pagina, id_tabla):
    """Las filas de datos de una tabla `::: table {#id_tabla …}`."""
    texto = pagina.read_text(encoding="utf-8")
    m = re.search(r"^::: table \{#" + re.escape(id_tabla) + r"\b.*?\n(.*?)^:::", texto, re.M | re.S)
    assert m, f"{pagina.name} no tiene la tabla {id_tabla}"
    renglones = [r for r in m.group(1).splitlines() if r.startswith("|")]
    celdas = [[c.strip() for c in r.strip("|").split("|")] for r in renglones[2:]]
    return celdas


def paginas_de(clase):
    return sorted(p for p in clase.glob("*.md") if p.name != "0_index.md")


def numero(clase):
    return int(clase.name.split("_")[0])


@pytest.mark.parametrize("clase", CLASES, ids=lambda c: c.name)
def test_cada_pagina_lleva_en_la_tabla_de_su_clase_los_minutos_de_su_frontmatter(clase):
    tabla = filas(clase / "0_index.md", f"jue-ruta-{numero(clase)}")
    paginas = paginas_de(clase)
    assert [int(f[0]) for f in tabla] == list(range(1, len(paginas) + 1))
    for fila, pagina in zip(tabla, paginas):
        assert minutos(fila[-1]) == estimado(pagina), (
            f"{pagina.name}: la tabla dice {fila[-1]}, el frontmatter otra cosa")


@pytest.mark.parametrize("clase", CLASES, ids=lambda c: c.name)
def test_la_clase_dura_la_suma_de_sus_paginas_sin_la_tarea(clase):
    tabla = filas(clase / "0_index.md", f"jue-ruta-{numero(clase)}")
    suma = sum(minutos(f[-1]) for f in tabla if "aparte" not in f[-1])
    assert estimado(clase / "0_index.md") == suma


def test_la_tabla_de_la_unidad_repite_lo_que_declara_cada_clase():
    tabla = filas(UNIDAD / "0_index.md", "jue-clases")
    assert [int(f[0]) for f in tabla] == [numero(c) for c in CLASES]
    for fila, clase in zip(tabla, CLASES):
        assert minutos(fila[-1]) == estimado(clase / "0_index.md"), clase.name


def test_la_unidad_dura_la_suma_de_sus_clases_en_el_frontmatter_y_en_la_prosa():
    suma = sum(estimado(c / "0_index.md") for c in CLASES)
    assert estimado(UNIDAD / "0_index.md") == suma
    texto = (UNIDAD / "0_index.md").read_text(encoding="utf-8")
    m = re.search(r"El recorrido de lectura suma \*\*(.+?)\*\*", texto)
    assert m, "la prosa de la unidad ya no declara el total con la frase de siempre"
    assert minutos_en_prosa(m.group(1)) == suma


def test_las_tareas_suman_lo_que_dice_la_unidad_redondeado_a_horas():
    aparte = 0
    for clase in CLASES:
        tabla = filas(clase / "0_index.md", f"jue-ruta-{numero(clase)}")
        aparte += sum(minutos(f[-1]) for f in tabla if "aparte" in f[-1])
    texto = (UNIDAD / "0_index.md").read_text(encoding="utf-8")
    m = re.search(r"tareas suman unas \*\*(.+?)\*\*", texto)
    assert m, "la prosa de la unidad ya no declara el total de las tareas"
    assert round(aparte / 60) * 60 == minutos_en_prosa(m.group(1))
