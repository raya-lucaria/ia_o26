"""Pruebas de prosa de la clase 0 de la unidad 9 (D-003; corren en S2).

Atan cada cifra de `1_que_es_aprender/1_repaso.md` a **su frase o su
bloque**, no a la pagina entera (patron de test_juegos.py), y vigilan lo que
el brief prohibe y raya validate no ve. Los valores salen de
tools/ml_cifras_c0.py; ninguno se escribe aqui. Las trece pruebas son las de
clase_0.md §10.7, en su orden; la 14 (ronda 1 de revision) ata ademas toda
cifra de la pagina a su oracion, y la prueba 1 exige que la primera cifra de
error tras el nombre de una regla sea la suya.

Se escriben en C0.T4, antes de despachar la redaccion: mientras la pagina y
el indice no existan, las que los leen fallan (rojo esperado, se anota). Con
ML_CLASES puesta y sin el 0, el archivo entero se salta.

Mutacion obligatoria (prueba 8): la propia suite copia la pagina con el 7
de memorizar y el 12 del promedio intercambiados en lo nuevo y exige que el
comprobador de la prueba 1 lo note; ademas se corre a mano en C0.T7 y se
anota en el commit.
"""
import os
import re
from pathlib import Path

import pytest

import figuras_ml_c0 as fig
import ml_cifras_c0 as cifras

_clases = os.environ.get("ML_CLASES", "").strip()
if _clases and "0" not in [c.strip() for c in _clases.split(",")]:
    pytest.skip("ML_CLASES sin la clase 0", allow_module_level=True)

RAIZ = Path(__file__).resolve().parent.parent
CLASE = RAIZ / "course/9_aprendizaje_maquina/1_que_es_aprender"
PAGINA = CLASE / "1_repaso.md"
INDICE = CLASE / "0_index.md"
UNIDAD_6 = RAIZ / "course/6_optimizacion/5_practica_de_modelado/4_regresion_practica.md"

C = cifras.cifras_c0_memorizar()
f = cifras.redondeo
REGLAS = ("memorizar", "recta", "promedio")
# «en promedio» y «promedio al cuadrado» no nombran la regla del promedio.
NOMBRE_REGLA = {
    "memorizar": r"memoriza\w*",
    "recta": r"recta",
    "promedio": r"(?<!\ben )promedio(?! al cuadrado)",
}
CONJUNTOS = {
    "mae_vistas": r"\bvio\b|\bvistas?\b|lo visto",
    "mae_nuevas": r"\bnuevas?\b|lo nuevo",
}
# Solo las oraciones que hablan de error atan cifras de error.
DE_ERROR = re.compile(r"error|falla|\bMAE\b|se equivoca", re.I)


# ----------------------------------------------------------- lectura ---

def _leer(ruta):
    assert ruta.exists(), f"{ruta.relative_to(RAIZ)} no existe todavía (rojo esperado antes de C0.T5/C0.T6)"
    return ruta.read_text(encoding="utf-8")


def _cuerpo(texto):
    """Sin frontmatter."""
    if texto.startswith("---"):
        return texto.split("\n---", 1)[1]
    return texto


def _seccion(texto, inicio):
    """Desde el encabezado `## <inicio>` hasta el siguiente `## `."""
    m = re.search(rf"^## {re.escape(inicio)}.*$", texto, re.M)
    assert m, f"no hay encabezado «## {inicio}…»"
    fin = re.search(r"^## ", texto[m.end():], re.M)
    return texto[m.end(): m.end() + fin.start() if fin else len(texto)]


_DIRECTIVA = re.compile(r"^:::\s*(\w+)\s*\{#([\w-]+)[^}]*\}\s*$")


def _bloque(texto, ident):
    """Contenido de la directiva `::: tipo {#ident …}` hasta su `:::`."""
    lineas = texto.split("\n")
    for k, linea in enumerate(lineas):
        m = _DIRECTIVA.match(linea.strip())
        if m and m.group(2) == ident:
            for j in range(k + 1, len(lineas)):
                if lineas[j].strip() == ":::":
                    return "\n".join(lineas[k + 1: j])
    raise AssertionError(f"no hay bloque {{#{ident}}}")


def _sin_figuras(texto):
    return re.sub(r"^:::\s*figure\b.*?^:::\s*$", "", texto, flags=re.M | re.S)


def _oraciones(texto):
    """Oraciones: corta en fin de oracion, renglon en blanco y viñeta."""
    texto = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "\n\n", texto, flags=re.M)
    piezas = []
    for parrafo in re.split(r"\n\s*\n", texto):
        parrafo = " ".join(parrafo.split())
        piezas += [o for o in re.split(r"(?<=[.!?])\s+", parrafo) if o]
    return piezas


def _numero(valor):
    """Regex de un numero suelto: 1.2 no casa dentro de 11.2 ni de 1.25."""
    return re.compile(rf"(?<![\d.,]){re.escape(valor)}(?![\d]|[.,]\d)")


def _tramos_por_regla(oracion):
    """{regla: [texto desde su nombre hasta el nombre de la siguiente regla]}."""
    marcas = sorted((m.start(), m.end(), regla) for regla in REGLAS
                    for m in re.finditer(NOMBRE_REGLA[regla], oracion, re.I))
    tramos = {}
    for k, (ini, fin, regla) in enumerate(marcas):
        hasta = marcas[k + 1][0] if k + 1 < len(marcas) else len(oracion)
        tramos.setdefault(regla, []).append(oracion[fin:hasta])
    return tramos


_PRIMERA_CIFRA = re.compile(r"(?<![\w.,])\d+(?:\.\d+)?(?![\w]|[.,]\d)")


def comprobar_cifras_por_regla(texto):
    """Prueba 1 sobre un texto: lista de errores (vacia si todo cuadra).

    Para cada regla y conjunto: (a) alguna oracion que nombra el conjunto y
    habla de error tiene, en el tramo de esa regla, su valor; (b) ninguna
    oracion asi tiene, en el tramo de esa regla, el valor de otra regla en
    ese conjunto (y que no sea tambien el suyo)."""
    errores = []
    texto = re.sub(r"(?<![\w@])@[\w-]+", " ", texto)   # ids: «@ml-c0-memorizar-…»
    oraciones = [o for o in _oraciones(texto) if DE_ERROR.search(o)]
    for clave, conjunto in CONJUNTOS.items():
        del_conjunto = [o for o in oraciones if re.search(conjunto, o, re.I)]
        for regla in REGLAS:
            propio = f(C[regla][clave])
            ajenos = {f(C[r][clave]) for r in REGLAS if r != regla} - {propio}
            vista = False
            for o in del_conjunto:
                # en una oracion de un solo conjunto, la primera cifra que
                # sigue al nombre de la regla es la suya (r1: un 8 por el 7
                # pasaba porque otra oracion si traia el 7)
                solo_uno = sum(bool(re.search(c, o, re.I)) for c in CONJUNTOS.values()) == 1
                for tramo in _tramos_por_regla(o).get(regla, []):
                    if _numero(propio).search(tramo):
                        vista = True
                    # la cifra de error es la primera tras la ultima palabra
                    # de error del tramo («anuncia 25 y falla por 7» → 7)
                    desde = [m.end() for m in DE_ERROR.finditer(tramo)]
                    primera = _PRIMERA_CIFRA.search(tramo, desde[-1] if desde else 0)
                    if solo_uno and primera and primera.group() != propio:
                        errores.append(f"{regla}/{clave}: «{o}» le pone {primera.group()}")
                    for ajeno in ajenos:
                        if _numero(ajeno).search(tramo) and not _numero(propio).search(tramo):
                            errores.append(f"{regla}/{clave}: «{o}» le pone {ajeno}")
            if not vista:
                errores.append(f"{regla}/{clave}: ninguna oración da {propio}")
    return errores


# -------------------------------------------- 1 · cifras por regla ---

def test_1_cifras_por_regla_y_por_conjunto_en_la_seccion_1():
    s1 = _sin_figuras(_seccion(_cuerpo(_leer(PAGINA)), "1 ·"))
    assert comprobar_cifras_por_regla(s1) == []


def test_1b_la_vineta_de_aprender_trae_los_seis_numeros_en_orden():
    llevar = _seccion(_cuerpo(_leer(PAGINA)), "Lo que hay que llevarse")
    vinetas = [v for v in re.split(r"^\s*[-*]\s+", llevar, flags=re.M)[1:]]
    assert len(vinetas) == 4, "«Lo que hay que llevarse» lleva 4 viñetas"
    primera = " ".join(vinetas[0].split())
    orden = [f(C[r][k]) for r in REGLAS for k in ("mae_vistas", "mae_nuevas")]
    pos = 0
    for valor in orden:
        m = _numero(valor).search(primera, pos)
        assert m, f"la viñeta de aprender no trae {valor} en el orden memorizar, recta, promedio"
        pos = m.end()
    assert comprobar_cifras_por_regla(primera) == []


# ------------------------------------------- 2 · frase ancla unidad 6 ---

def test_2_frase_ancla_de_la_unidad_6_y_frase_de_perdida_y_metrica():
    oraciones = _oraciones(_cuerpo(_leer(PAGINA)))
    b0, b1 = C["beta_seis_exacta"]
    recta6 = f"{float(b0):g}+({b1.numerator}/{b1.denominator})x"
    ancla = [o for o in oraciones if "solo con las cuatro primeras" in o]
    assert ancla, "falta «solo con las cuatro primeras»"
    assert any(recta6 in re.sub(r"\s", "", o) for o in ancla), recta6
    assert any(all(p in o for p in ("cuadrados", "MAE", "clase 4")) for o in oraciones)


# ----------------------------------------- 3 · los seis pares de la 6 ---

def test_3_los_seis_pares_coinciden_con_la_unidad_6():
    seccion = UNIDAD_6.read_text(encoding="utf-8").split("Ver el error en seis entregas", 1)[1]
    filas = re.findall(r"^\|\s*(\d)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", seccion, re.M)[:6]
    assert tuple((int(km), int(m)) for _, km, m in filas) == cifras.ENTREGAS
    texto = _cuerpo(_leer(PAGINA))
    for i in cifras.VISTAS:
        km, minutos = cifras.ENTREGAS[i]
        assert f"({km}, {minutos})" in texto, (km, minutos)


# ------------------------------------------ 4 · datos de ejercicios ---

def test_4_datos_dentro_de_los_ejercicios():
    texto = _cuerpo(_leer(PAGINA))
    d = cifras.datos_c0_ejercicios()
    micro = _bloque(texto, "ml-c0-ej-aprende-o-recuerda")
    for v in (d["por_semana"], *d["mae_visto"], d["semanas"], d["mae_nuevo"]):
        assert _numero(str(v)).search(micro), v
    final = _bloque(texto, "ml-c0-ej-final-repaso-que-es-aprender")
    assert _numero(str(d["entregas_zona"])).search(final)


# --------------------------------------------------- 5 · figuras ---

def _figuras_de_la_clase():
    ids = {}
    for md in sorted(CLASE.glob("*.md")):
        for m in re.finditer(r"^:::\s*figure\s*\{#([\w-]+)[^}]*\}\s*$(.*?)^:::\s*$",
                             md.read_text(encoding="utf-8"), re.M | re.S):
            ids[m.group(1)] = m.group(2)
    return ids


def test_5_cada_figura_del_tramo_esta_en_un_figure_de_la_clase():
    _leer(PAGINA)
    ids = _figuras_de_la_clase()
    for ident in fig.FIGURAS_C0:
        assert ident in ids, ident
        assert f"_assets/{ident}.svg)" in ids[ident], ident


def test_5b_el_alt_de_f1b_pone_cada_regla_junto_a_su_valor():
    _leer(PAGINA)
    cuerpo = _figuras_de_la_clase()["ml-c0-memorizar-contra-ajustar"]
    alt = re.search(r"!\[(.*?)\]\(", cuerpo, re.S).group(1)
    assert comprobar_cifras_por_regla(alt.replace("Abajo:", ". Abajo: las nuevas,")) == []


ALT_DE = {
    "ml-c0-tres-reglas-en-lo-visto": fig.ALT_F1A,
    "ml-c0-memorizar-contra-ajustar": fig.ALT_F1B,
    "ml-c0-con-y-sin-y": fig.ALT_F2,
    "ml-c0-jerarquia": fig.ALT_F3,
    "ml-c0-quien-elige-phi": fig.ALT_F4,
}


def test_5c_cada_alt_es_el_aria_label_de_su_figura():
    """El alt de la pagina es literal el del generador: asi las cifras del alt
    (las de F2 incluidas: 3.5 km, 2 a 3 y 9 a 11 paquetes) salen de
    ml_cifras_c0 y ninguna se copia a mano."""
    _leer(PAGINA)
    ids = _figuras_de_la_clase()
    assert set(ALT_DE) == set(fig.FIGURAS_C0)
    for ident, alt in ALT_DE.items():
        cuerpo = ids[ident]
        hallado = re.search(r"!\[(.*?)\]\(", cuerpo, re.S).group(1)
        assert " ".join(hallado.split()) == alt, ident
        assert re.search(r'aria-label="([^"]*)"', fig.FIGURAS_C0[ident]()).group(1) == \
            alt.replace('"', "&quot;")


# --------------------------------------- 6 · sin ids de otras clases ---

@pytest.mark.parametrize("ruta", (PAGINA, INDICE), ids=("pagina", "indice"))
def test_6_no_cita_ids_ni_paginas_de_otras_clases(ruta):
    texto = _leer(ruta)
    assert not re.search(r"@ml-c[1-5]-", texto)
    propios = {"ml-clase-1-el-problema", "ml-clase-0-que-es-aprender",
               "ml-repaso-que-es-aprender"}
    for destino in re.findall(r"\[\[(ml-[\w-]+)\|", texto):
        assert destino in propios, destino


# ---------------------------------------- 7 · T, E, P solo en Mitchell ---

def test_7_t_e_p_sueltas_solo_en_la_definicion_de_mitchell():
    texto = _cuerpo(_leer(PAGINA))
    definicion = _bloque(texto, "ml-c0-def-aprender")
    assert re.search(r"\$T\$", definicion) and re.search(r"\$E\$", definicion)
    fuera = texto.replace(definicion, "")
    assert not re.findall(r"\$[TEP]\$", fuera)


# --------------------------------------------------- 8 · mutacion ---

def test_8_mutacion_intercambiar_7_y_12_la_atrapa_la_prueba_1(tmp_path):
    s1 = _sin_figuras(_seccion(_cuerpo(_leer(PAGINA)), "1 ·"))
    siete = f(C["memorizar"]["mae_nuevas"])
    doce = f(C["promedio"]["mae_nuevas"])
    mutada = _numero(siete).sub("\0", s1)
    mutada = _numero(doce).sub(siete, mutada).replace("\0", doce)
    copia = tmp_path / "1_repaso.md"
    copia.write_text(mutada, encoding="utf-8")
    assert siete in mutada and doce in mutada
    assert comprobar_cifras_por_regla(copia.read_text(encoding="utf-8")) != []


# -------------------------------------------- 9 · subindices de x ---

@pytest.mark.parametrize("ruta", (PAGINA, INDICE), ids=("pagina", "indice"))
def test_9_sin_x_con_subindice_numerico(ruta):
    assert not re.search(r"x_\{?\s*\d", _leer(ruta))


# ------------------------------------------- 10 · sin sesion ni fecha ---

MESES = ("enero febrero marzo abril mayo junio julio agosto septiembre octubre "
         "noviembre diciembre lunes martes miércoles jueves viernes sábado domingo").split()


@pytest.mark.parametrize("ruta", (PAGINA, INDICE), ids=("pagina", "indice"))
def test_10_sin_sesion_ni_fecha(ruta):
    texto = _cuerpo(_leer(ruta)).lower()
    for prohibida in ("pizarrón", "pizarron", "lo que vimos", "en clase vimos"):
        assert prohibida not in texto, prohibida
    for palabra in MESES:
        assert not re.search(rf"\b{palabra}\b", texto), palabra


# ------------------------------------------- 11 · argmin conjunto ---

def test_11_argmin_como_conjunto_y_unicidad_en_la_misma_oracion():
    texto = _cuerpo(_leer(PAGINA))
    plano = re.sub(r"\s", "", texto)
    assert r"\beta^\star\in\operatorname*{arg\,min}" in plano
    assert r"\beta^\star=\operatorname*{arg\,min}" not in plano
    con_valor = [o for o in _oraciones(texto) if r"\beta^\star=(11," in re.sub(r"\s", "", o)]
    assert con_valor and all("único" in o for o in con_valor)


# --------------------------------------------- 12 · enfoque unidad ---

def test_12_enfoque_de_la_unidad_sin_prometer_clasificacion_tardia():
    texto = _cuerpo(_leer(PAGINA))
    parrafos = re.split(r"\n\s*\n", texto)
    hallado = False
    for p in parrafos:
        oraciones = _oraciones(p)
        for k, o in enumerate(oraciones):
            if "no supervisado" in o and "queda fuera" in o:
                antes = oraciones[:k]
                assert any("clase 1" in a and "clasificación" in a for a in antes), o
                hallado = True
    assert hallado, "falta la oración «… no supervisado queda fuera»"
    for ruta in (PAGINA, INDICE):
        t = _leer(ruta)
        assert "regresión primero" not in t and "clasificación en la clase 4" not in t


# ------------------------------------------- 13 · phi sin subindice ---

@pytest.mark.parametrize("ruta", (PAGINA, INDICE), ids=("pagina", "indice"))
def test_13_sin_phi_con_subindice_numerico(ruta):
    texto = _leer(ruta)
    assert not re.search(r"\\phi\s*_\{?\s*\d", texto)
    assert not re.search(r"[φϕ]\s*_\{?\s*\d|[φϕ][₀-₉]", texto)


# --------------------------------------- comprobador (sin pagina) ---

def test_el_comprobador_de_la_prueba_1_acepta_y_rechaza():
    """Corre siempre (S1 incluido): el comprobador sobre frases de muestra."""
    buena = ("En las cuatro que vio, el error medio de memorizar es 0, el de la recta 0.8 "
             "y el del promedio 4. En las dos nuevas, la recta falla por 1.2, memorizar "
             "falla en promedio por 7 y el promedio por 12.")
    assert comprobar_cifras_por_regla(buena) == []
    mala = buena.replace("por 7", "por X").replace("por 12", "por 7").replace("por X", "por 12")
    assert comprobar_cifras_por_regla(mala) != []


# ------------------------------- 14 · toda cifra atada a su oracion (r1) ---
#
# La prueba 1 ata los MAE por regla; esta ata **toda** cifra de la pagina a
# la oracion que la dice. Cada oracion con una cifra tiene que casar con una
# entrada de ATADAS (un ancla y la lista exacta de cifras, en orden, sacadas
# de ml_cifras_c0); una oracion con cifras y sin ancla falla como «sin
# atar». Lo que no es cifra del ejemplo se quita antes de leer: referencias
# (unidad 6, clase 1, sección 3, §5.1, figuras 1.4 y 1.5, años), subíndices
# y exponentes, ids y wikilinks, y la notación (1,x,x^2).

_CIFRA = re.compile(r"(?<![\d.])\d+(?:\.\d+)?(?![\d]|\.\d)")
_NO_ES_CIFRA = [
    r"\(1,\s*x,\s*x\^2\)", r"\bi=1\b", r"\[\[[^\]]*\]\]", r"(?<![\w@])@[\w-]+", r"\(\.\./[^)]*\)",
    r"\*\*\d+\.\*\*",
    r"\b(?:unidad|unidades|clase|clases|sección|capítulo|figuras?|Pista)\s+\d+(?:\.\d+)*"
    r"(?:\s*y\s*\d+(?:\.\d+)*)?",
    r"§\s?\d+(?:\.\d+)*", r"\b(?:19|20)\d\d\b",
    r"[_^]\{[^}]*\}", r"[_^]\w", r"\\frac\d\w", r"\\ge\s*0",
]


def _cifras(oracion):
    t = oracion
    for patron in _NO_ES_CIFRA:
        t = re.sub(patron, " ", t)
    return _CIFRA.findall(t)


def _atadas():
    v = {r: [f(a) for a in C[r]["anuncios_nuevas"]] for r in REGLAS}
    mae = {(r, k): f(C[r][k]) for r in REGLAS for k in ("mae_vistas", "mae_nuevas")}
    b0, b1 = (f(b) for b in C["beta_estrella"])
    km = {i: str(cifras.ENTREGAS[i][0]) for i in range(len(cifras.ENTREGAS))}
    kn = [km[i] for i in cifras.NUEVAS]
    vecino = km[max(cifras.VISTAS)]
    b06, b16 = C["beta_seis_exacta"]
    d = cifras.datos_c0_ejercicios()
    phi = cifras.phi_cuadratica(cifras.PHI_EJEMPLO_KM)
    pares = [str(x) for i in cifras.VISTAS for x in cifras.ENTREGAS[i]]
    prom = f(C["promedio_vistas"])
    return [
        # entrada
        ("min de lectura", [str(cifras_minutos())]),
        # §1
        ("el programa vio (", pares),
        ("llegarán después", kn),
        ("Para 5 y 6 km, es la de", kn + [vecino, v["memorizar"][0]]),
        ("El promedio fijo de lo visto", [prom]),
        ("con $n=", [str(len(cifras.VISTAS))]),
        ("el mínimo es único", [b0, b1, b0, b1]),
        ("Para 5 km anuncia", [kn[0], b0, b1, kn[0], v["recta"][0]]),
        ("con las seis salía", [f(b06), str(b16.numerator), str(b16.denominator)]),
        ("En las vistas, memorizar gana",
         [mae["memorizar", "mae_vistas"], mae["recta", "mae_vistas"],
          mae["promedio", "mae_vistas"]]),
        ("Piensa: en las entregas de", kn),
        ("En las nuevas, el MAE es",
         [mae["recta", "mae_nuevas"], mae["memorizar", "mae_nuevas"],
          mae["promedio", "mae_nuevas"]]),
        ("lo lleva a cero y falla por", [mae["memorizar", "mae_nuevas"]]),
        ("Cada semana llegan", [str(d["por_semana"])]),
        ("semanas, el error medio en lo visto baja",
         [str(d["semanas"])] + [str(x) for x in d["mae_visto"]]),
        ("aún no vistas, permanece en", [str(d["mae_nuevo"])]),
        ("en entregas que no vio: sigue en", [str(d["mae_nuevo"])]),
        ("Bajar de", [str(x) for x in d["mae_visto"]]),
        # §2 (0 y 1: la convención de guardar dos categorías, no una cifra del ejemplo)
        ("por ejemplo 0 y 1", ["0", "1"]),
        ("ajustamos $", [b0, b1]),
        # §3
        ("para 3 km", [str(cifras.PHI_EJEMPLO_KM), str(cifras.PHI_EJEMPLO_KM)]
         + [str(x) for x in phi]),
        # ejercicio final y su respuesta
        ("Tiene ", [str(d["entregas_zona"])]),
        ("la experiencia son las", [str(d["entregas_zona"])]),
        ("El error en las", [str(d["entregas_zona"])]),
        ("basta el error en las", [str(d["entregas_zona"])]),
        ("al azar parte de las", [str(d["entregas_zona"])]),
        # lo que hay que llevarse
        ("El error de memorizar es",
         [mae[r, k] for r in REGLAS for k in ("mae_vistas", "mae_nuevas")]),
    ]


def cifras_minutos():
    from contrato_unidad import minutos
    fm = _leer(PAGINA).split("\n---", 1)[0]
    return minutos(re.search(r"^estimated_time:\s*(\S+)", fm, re.M).group(1))


def comprobar_toda_cifra_atada(texto):
    errores = []
    atadas = _atadas()
    usadas = set()
    plano = re.sub(r"^\s*(?::::|#+ ).*$", "", _sin_figuras(texto), flags=re.M)
    for o in _oraciones(plano):
        cifras_o = _cifras(o)
        if not cifras_o:
            continue
        anclas = [(a, esp) for a, esp in atadas if a in o]
        if not anclas:
            errores.append(f"sin atar: «{o}» dice {cifras_o}")
            continue
        ancla, esperadas = anclas[0]
        usadas.add(ancla)
        if cifras_o != esperadas:
            errores.append(f"«{o}»: dice {cifras_o}, ml_cifras_c0 da {esperadas}")
    for ancla, _ in atadas:
        if ancla not in usadas:
            errores.append(f"ninguna oración con cifras trae el ancla «{ancla}»")
    return errores


def test_14_toda_cifra_de_la_pagina_esta_atada_a_su_oracion():
    assert comprobar_toda_cifra_atada(_cuerpo(_leer(PAGINA))) == []


@pytest.mark.parametrize("de, a", [
    ("memorizar 7, promedio", "memorizar 8, promedio"),   # la mutacion de r1
    ("anuncia 25.", "anuncia 26."),
    ("obtienes $\\phi(3)=(1,3,9)$", "obtienes $\\phi(3)=(1,3,8)$"),
    ("Tiene 200 entregas", "Tiene 300 entregas"),
])
def test_14b_la_prueba_14_atrapa_una_cifra_cambiada(de, a):
    texto = _cuerpo(_leer(PAGINA))
    assert de in texto, de
    assert comprobar_toda_cifra_atada(texto.replace(de, a, 1)) != []
