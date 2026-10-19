"""Los minutos de la unidad de cadenas de Markov suman lo que dicen.

Copia de `test_tiempos_juegos.py`, que está fija a juegos. Cada página
declara su `estimated_time`, la tabla de su clase (`mkv-ruta-N`) lo repite,
el índice de la clase declara la suma, la tabla de la unidad (`mkv-clases`)
la repite, y el índice de la unidad declara el total en el frontmatter y en
la prosa («El recorrido de lectura suma **…**»). Las filas «aparte» (tareas
de refuerzo, cuando existan) no cuentan en la suma. El contrato de unidad
solo avisa de la suma de minutos; esta prueba la hace obligatoria.
"""
import re
from pathlib import Path

import pytest

UNIDAD = Path(__file__).resolve().parent.parent / "course/8_markov"
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


def encabezado(pagina, id_tabla):
    """Las celdas del encabezado de una tabla `::: table {#id_tabla …}`."""
    texto = pagina.read_text(encoding="utf-8")
    m = re.search(r"^::: table \{#" + re.escape(id_tabla) + r"\b.*?\n(\|.*?)$", texto, re.M)
    assert m, f"{pagina.name} no tiene la tabla {id_tabla}"
    return [c.strip() for c in m.group(1).strip("|").split("|")]


def ruta(clase):
    """Las filas de `mkv-ruta-N` como (número de página, minutos en texto).

    La columna de minutos se busca por su encabezado «Minutos», no por
    posición: va segunda, con la página y lo que resuelve juntos en la
    tercera, para que a 390 px la tabla quepa sin desplazamiento lateral y
    los minutos no queden escondidos."""
    id_tabla = f"mkv-ruta-{numero(clase)}"
    cabeza = encabezado(clase / "0_index.md", id_tabla)
    assert "Minutos" in cabeza, f"{clase.name}: {id_tabla} no tiene columna «Minutos»"
    col = cabeza.index("Minutos")
    return [(f[0], f[col]) for f in filas(clase / "0_index.md", id_tabla)]


def paginas_de(clase):
    # Por el prefijo numérico, no por el nombre: «10_tarea» va después de «9_…».
    return sorted((p for p in clase.glob("*.md") if p.name != "0_index.md"),
                  key=lambda p: int(p.name.split("_", 1)[0]))


def numero(clase):
    return int(clase.name.split("_")[0])


@pytest.mark.parametrize("clase", CLASES, ids=lambda c: c.name)
def test_cada_pagina_lleva_en_la_tabla_de_su_clase_los_minutos_de_su_frontmatter(clase):
    tabla = ruta(clase)
    paginas = paginas_de(clase)
    assert [int(n) for n, _ in tabla] == list(range(1, len(paginas) + 1))
    for (_, tiempo), pagina in zip(tabla, paginas):
        assert minutos(tiempo) == estimado(pagina), (
            f"{pagina.name}: la tabla dice {tiempo}, el frontmatter otra cosa")


@pytest.mark.parametrize("clase", CLASES, ids=lambda c: c.name)
def test_la_clase_dura_la_suma_de_sus_paginas_sin_la_tarea(clase):
    suma = sum(minutos(t) for _, t in ruta(clase) if "aparte" not in t)
    assert estimado(clase / "0_index.md") == suma


def test_la_tabla_de_la_unidad_repite_lo_que_declara_cada_clase():
    tabla = filas(UNIDAD / "0_index.md", "mkv-clases")
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
