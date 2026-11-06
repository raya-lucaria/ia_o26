"""Pruebas de prosa de la clase 4 (D-003; clase_4.md §10.11, C4.T13).

Cada cifra de tools/ml_cifras_c4.py que una página cita aparece en esa página
con su forma literal («cita»); cada figura de FIGURAS_C4 vive en un
`::: figure` con su id y el title del brief; los guiones de los notebooks 08,
09 y de la tarea no tienen secciones vacías; y las guardas de frase de
§10.11 C4.T13 (v3, v4, v5): ningún $R$ junto a una métrica, el mapa único de
reservas, el supuesto condicionado de conformal, ninguna fecha, etc.

Lee páginas y guiones, así que no es parte de S1: corre en S2 y en la
validación de cada borrador de Codex (C4.T11). Mientras una página no existe,
sus pruebas fallan a propósito con «falta … (la redacta Codex)».
"""
import re
from functools import lru_cache
from pathlib import Path

import pytest

pytest.importorskip("pandas")
pytest.importorskip("sklearn")

import ml_cifras_c4 as c  # noqa: E402
from figuras_ml_c4 import FIGURAS_C4  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
CLASE = RAIZ / "course/9_aprendizaje_maquina/5_clasificacion"
ASSETS = RAIZ / "course/9_aprendizaje_maquina/_assets"
GUIONES = RAIZ / "tools/cuadernos_ml"

P1 = CLASE / "1_perdida_metrica_y_desbalanceo.md"
P2 = CLASE / "2_calibracion_y_conformal.md"
TAREA = CLASE / "3_tarea.md"
INDICE = CLASE / "0_index.md"
NB08 = GUIONES / "08_perdida_metrica_y_desbalanceo.texto.md"
NB09 = GUIONES / "09_calibracion_y_conformal.texto.md"
NBT = GUIONES / "tarea_4_desbalanceo_multiclase.texto.md"
PAGINAS = (P1, P2, TAREA, INDICE)
GUIONES_C4 = (NB08, NB09, NBT)


@lru_cache(maxsize=None)
def leer(ruta):
    assert ruta.exists(), f"falta {ruta.relative_to(RAIZ)} (la redacta Codex)"
    return ruta.read_text(encoding="utf-8")


def secciones(texto):
    """{n: texto de la sección «## n · …» hasta el siguiente «## »}."""
    salida = {}
    for p in re.split(r"(?m)^## ", texto)[1:]:
        m = re.match(r"(\d+) · ", p)
        if m:
            salida[int(m.group(1))] = p
    return salida


def celdas(texto):
    """{clave: texto} de un guion («### celda: <clave>»)."""
    partes = re.split(r"(?m)^### celda: ([a-z0-9-]+)\s*$", texto)
    return {partes[i]: partes[i + 1] for i in range(1, len(partes), 2)}


def directiva(texto, ident):
    m = re.search(r"(?ms)^:::\s*\w+\s*\{#" + re.escape(ident) + r"\b[^\n]*\n(.*?)^:::\s*$",
                  texto)
    assert m, f"no hay directiva {{#{ident}}}"
    return m.group(1)


def formas(cifra):
    """Formas equivalentes: negativo con «−» o «-»; «%» con o sin espacio."""
    s = str(cifra)
    out = {s}
    if s.startswith("-"):
        out.add("−" + s[1:])
    if s.endswith(" %"):
        out |= {s.replace(" %", " %"), s.replace(" %", "%")}
    return out


def comprobar(texto, cifras, donde):
    faltan = [x for x in cifras if not any(f in texto for f in formas(x))]
    assert not faltan, f"{donde}: no cita {faltan}"


def cita(nombre):
    return getattr(c, nombre)()["cita"]


# --------------------------------------------------------------- cifras ---

def cifras_p1():
    """Lo que clase_4.md §10.2 (página 1) y el brief 1 piden citar."""
    moda, dos = cita("cifras_c4_moda"), cita("cifras_c4_dos_reglas")
    pb, un = cita("cifras_c4_pesos_balanceados"), cita("cifras_c4_mcc_un_fraude")
    no, fin = cita("cifras_c4_noticias"), cita("cifras_c4_final_p1")
    return [moda["uno"]["aciertos"], dos["A"]["perdida"], dos["A"]["mcc"],
            dos["B"]["perdida"], pb["w0"], pb["umbral"], un["A"]["mcc"],
            un["A"]["aciertos_balanceados"], cita("cifras_c4_quien_manda")["ponderado"],
            no["macro"], no["ponderado"], no["mcc"],
            cita("cifras_c4_separable")["por_decada"], *fin["w"]]


def cifras_p2():
    """Lo que clase_4.md §10.2 (página 2) y el brief 2 piden citar."""
    cal, tasa = cita("cifras_c4_calibracion"), cita("cifras_c4_tasa")
    cinco, fin = cita("cifras_c4_cinco_puntajes"), cita("cifras_c4_final_p2")
    return [cal["brier_con"], cal["brier_benchmark"], tasa["sin"],
            cita("cifras_c4_cliente_tipico")["razon"], cinco["tercio"][1],
            cinco["sexto"][1], cita("cifras_c4_minimo_por_clase")["minimo"],
            cita("cifras_c4_noventa_global")["fraude"], fin["global"], fin["fraude"]]


def test_p1_cita_sus_cifras():
    comprobar(leer(P1), cifras_p1(), P1.name)


def test_p2_cita_sus_cifras():
    comprobar(leer(P2), cifras_p2(), P2.name)


# ------------------------------------------------- cifras con su etiqueta ---
# Revisión ronda 1 (H8): buscar cada cifra en cualquier lugar de la página
# dejaba pasar un umbral 0.18 → 0.88 (otro 0.18 seguía en la página), pérdidas
# o Brier intercambiados y un intercepto −3.08 → −30.8. Aquí cada cifra se
# busca DENTRO de su frase, tabla o celda, junto a la palabra que la nombra,
# también en las copias de los guiones. Reescribir la frase-ancla hace fallar
# la prueba aunque la cifra esté bien: es a propósito (como test_lecturas).

def _num(v):
    """Regex de una cifra citada: «-» o «−»; termina donde termina el número."""
    s = re.escape(str(v))
    if str(v).startswith("-"):
        s = "[-−]" + re.escape(str(v)[1:])
    return s + r"(?![0-9])"


def anclas():
    um, dos = cita("cifras_c4_umbral"), cita("cifras_c4_dos_reglas")
    cal, pl = cita("cifras_c4_calibracion"), cita("cifras_c4_platt")
    de = cita("cifras_c4_desbalanceo")
    A, B = dos["A"], dos["B"]
    return [
        (P1, r"el umbral que elige MCC es {}", [um["tau"]]),
        (P1, r"\| {}, elegido \| {} \| {} \|", [um["tau"], um["mcc_val_elegido"],
                                                um["mcc_des_elegido"]]),
        (P1, r"con el umbral {}\]", [um["tau"]]),
        (P1, r"A tiene menor pérdida: {} contra {}\.", [A["perdida"], B["perdida"]]),
        (P1, r"la banda va de ±{} con 50 % de fraude a ±{} con 1 %", [de["banda_50"],
                                                                     de["banda_01"]]),
        (NB08, r"la regla A tiene pérdida {}, aciertos {} y MCC {}\. La regla B tiene "
               r"pérdida {}, aciertos {} y MCC {}\.",
         [A["perdida"], A["aciertos"], A["mcc"], B["perdida"], B["aciertos"], B["mcc"]]),
        (P2, r"Allí da {}, frente a {} sin pesos y {} con pesos\.",
         [cal["brier_benchmark"], cal["brier_sin"], cal["brier_con"]]),
        (P2, r"La pérdida logarítmica da, respectivamente, {}, {} y {}\.",
         [cal["log_benchmark"], cal["log_sin"], cal["log_con"]]),
        (P2, r"\\widehat\\beta\^\{{\\text\{{cal\}}\}}_0={}\$ y "
             r"\$\\widehat\\beta\^\{{\\text\{{cal\}}\}}_1={}\$; la referencia del intercepto es {}\.",
         [pl["beta0"], pl["beta1"], pl["menos_ln_razon"]]),
        (P2, r"el Brier recalibrado es {} contra {} del constante; la pérdida logarítmica "
             r"es {} contra {}\.", [cal["brier_recalibrado"], cal["brier_benchmark"],
                                   cal["log_recalibrado"], cal["log_benchmark"]]),
        (P2, r"Brier sin pesos {}, con pesos {} y recalibrado {}; el constante da {}",
         [cal["brier_sin"], cal["brier_con"], cal["brier_recalibrado"], cal["brier_benchmark"]]),
        (P2, r"el anuncio promedio sube de {} a {} con pesos; Platt en `val_a` lo regresa a {}\.",
         [cal["p_sin"], cal["p_con"], cal["p_rec"]]),
    ]


def test_cada_cifra_ancla_va_junto_a_su_etiqueta():
    faltan = []
    for ruta, patron, valores in anclas():
        rx = patron.format(*[_num(v) for v in valores])
        if not re.search(rx, leer(ruta)):
            faltan.append(f"{ruta.name}: {patron} con {valores}")
    assert not faltan, "cifra separada de su etiqueta:\n  " + "\n  ".join(faltan)


def test_las_anclas_atrapan_las_mutaciones_de_la_revision():
    """Las cuatro mutaciones que pasaban la guarda vieja ya no pasan."""
    um, dos = cita("cifras_c4_umbral"), cita("cifras_c4_dos_reglas")
    cal, pl = cita("cifras_c4_calibracion"), cita("cifras_c4_platt")
    mutaciones = [
        (P1, f"el umbral que elige MCC es {um['tau']}", "el umbral que elige MCC es 0.88"),
        (P1, f"menor pérdida: {dos['A']['perdida']} contra {dos['B']['perdida']}",
         f"menor pérdida: {dos['B']['perdida']} contra {dos['A']['perdida']}"),
        (P2, f"frente a {cal['brier_sin']} sin pesos y {cal['brier_con']} con pesos",
         f"frente a {cal['brier_con']} sin pesos y {cal['brier_sin']} con pesos"),
        (P2, f"_0={pl['beta0']}$", f"_0={pl['beta0'][:-3]}0{pl['beta0'][-3:]}$"),
    ]
    for ruta, original, mutado in mutaciones:
        texto = leer(ruta)
        assert original in texto, f"la frase de la mutación cambió: {original}"
        mut = texto.replace(original, mutado)
        rotas = [p for r, p, v in anclas() if r == ruta
                 and not re.search(p.format(*[_num(x) for x in v]), mut)]
        assert rotas, f"la mutación «{mutado}» pasa las anclas"


# -------------------------------------------------------------- figuras ---

TITULOS = {
    P1: {"ml-c4-moda-99": "Cien mensajes y una regla que nunca detecta nada",
         "ml-c4-separable": "Sin penalización, los coeficientes no se detienen",
         "ml-c4-cadena-decision": "Del dato a la etiqueta: tres decisiones",
         "ml-c4-perdida-vs-metrica": "La pérdida cambia suave; las métricas, a saltos",
         "ml-c4-umbral": "Mover el umbral no toca la pérdida",
         "ml-c4-contribucion-clases": "Cuántos votos tiene cada clase en el ajuste",
         "ml-c4-metricas-vs-proporcion":
             "Aciertos, aciertos balanceados y MCC contra la proporción de fraude",
         "ml-c4-pesos-umbral": "Pesar es mover el intercepto",
         "ml-c4-anillos-metricas":
             "Los pesos no cambian la forma de la frontera; la representación sí",
         "ml-c4-mcc-por-pliegue": "Una métrica por pliegue, con pocos fraudes",
         "ml-c4-softmax": "Regresión softmax con tres clases",
         "ml-c4-fronteras-tres-clases": "Tres clases, sin pesos y con pesos",
         "ml-c4-macro-ponderado": "Macro contra ponderado en el ejemplo de noticias",
         "ml-c4-recuadro-confusion": "La matriz de confusión, la curva ROC y la curva PR"},
    P2: {"ml-c4-confiabilidad": "¿Ocurre lo que se anuncia?",
         "ml-c4-tasa": "Una probabilidad que se cobra",
         "ml-c4-mapa-reservas": "Qué conjunto ajusta cada pieza",
         "ml-c4-conformal-rangos": "Cinco puntajes y un corte",
         "ml-c4-conformal-conjuntos": "Conjuntos que crecen donde hay duda",
         "ml-c4-cobertura-por-clase": "La cobertura, clase por clase"},
}
FIGURA_PAGINA = [(p, i) for p, d in TITULOS.items() for i in d]


def test_los_titulos_cubren_el_catalogo():
    assert sorted(i for _, i in FIGURA_PAGINA) == sorted(FIGURAS_C4)


@pytest.mark.parametrize("ruta,ident", FIGURA_PAGINA,
                         ids=[f"{p.stem[:12]}-{i}" for p, i in FIGURA_PAGINA])
def test_cada_figura_vive_en_un_figure_con_su_id_y_su_title(ruta, ident):
    texto = leer(ruta)
    m = re.search(r"(?ms)^:::\s*figure\s*\{#" + re.escape(ident) + r"\b([^\n]*)\n(.*?)^:::\s*$",
                  texto)
    assert m, f"{ruta.name}: no hay ::: figure {{#{ident}}}"
    assert f'title="{TITULOS[ruta][ident]}"' in m.group(1), f"{ident}: title distinto del brief"
    assert f"_assets/{ident}.svg" in m.group(2), f"{ident}: el figure no enlaza su SVG"


# ------------------------------------------------- enlaces y continuidad ---

@pytest.mark.parametrize("ruta", PAGINAS, ids=lambda p: p.stem)
def test_ninguna_pagina_cita_la_clase_5_por_id(ruta):
    assert "@ml-c5-" not in leer(ruta)


def test_continua_con():
    assert re.search(r"Continúa con \[\[ml-calibracion-y-conformal\|", leer(P1))
    assert re.search(r"Continúa con \[\[ml-clase-5-supuestos-y-metodologia\|", leer(P2))


def test_p1_cita_la_estratificada_de_la_clase_2_y_no_la_redibuja():
    t = leer(P1)
    assert "@ml-c2-estratificada" in t
    assert "ml-c4-estratificar" not in t and "tres-fraudes" not in t


# ------------------------------------------------------ guardas de frase ---

def _todas():
    return [(r, leer(r)) for r in PAGINAS + GUIONES_C4]


METRICA = r"(MCC|A_\{\\text\{bal\}\}|aciertos|Brier)"


@pytest.mark.parametrize("ruta", PAGINAS + GUIONES_C4, ids=lambda p: p.name)
def test_ningun_R_junto_a_una_metrica(ruta):
    """r1-18: $R$ es la pérdida esperada; a menos de 60 caracteres de una
    métrica tiene que mediar la palabra «pérdida»."""
    t = leer(ruta)
    malos = []
    for m in re.finditer(r"\$R\$|\$R[_(\\ ]", t):
        if re.search(r"(nunca|no es|ni|llamar)\s+$", t[max(0, m.start() - 12):m.start()]):
            continue          # la prohibición misma: «…, nunca $R$» (ml-c4-def-perdida-vs-metrica)
                              # o «Penaliza: … llamar $R$ a un MCC» (rúbrica, clase_4.md §10.6)
        a, b = max(0, m.start() - 60), m.end() + 60
        ventana = t[a:b]
        for x in re.finditer(METRICA, ventana):
            entre = ventana[min(x.start(), m.start() - a):max(x.end(), m.end() - a)]
            if "pérdida" not in entre:
                malos.append(ventana.replace("\n", " "))
                break
    assert not malos, f"{ruta.name}: $R$ junto a una métrica: {malos[:2]}"


@pytest.mark.parametrize("ruta", PAGINAS + GUIONES_C4, ids=lambda p: p.name)
def test_frases_prohibidas(ruta):
    t = leer(ruta)
    plano = re.sub(r"\s+", " ", t)
    for f in ("val_eval", "val_cal", "val3_b", "val$_b$", "en unos días",
              "la próxima clase", "sacarlos independientes del mismo proceso lo implica",
              "nunca las dos", "o pesos con"):
        assert f not in plano, f"{ruta.name}: «{f}»"
    assert not re.search(r"aprende a comprobar.{0,80}intercambi|intercambi.{0,80}aprende a comprobar",
                         plano), f"{ruta.name}: la clase 5 no comprueba la intercambiabilidad"
    assert not re.search(r"(cualquier|ninguna) regla lineal.{0,80}MCC|MCC.{0,80}(cualquier|ninguna) regla lineal",
                         plano), f"{ruta.name}: caso 25 dicho como «toda regla lineal»"
    assert not re.search(r"techo.{0,60}MCC|MCC.{0,60}techo", plano), \
        f"{ruta.name}: «techo» de MCC (r3-16)"
    assert not re.search(r"\\phi_\{?[12]\b", t), f"{ruta.name}: \\phi_1 o \\phi_2 (r2-01)"
    assert not re.search(r"\b\d{1,2} de (enero|febrero|marzo|abril|mayo|junio|julio|agosto|"
                         r"septiembre|octubre|noviembre|diciembre)\b|\b20\d\d-\d\d-\d\d\b",
                         plano), f"{ruta.name}: una fecha (D-008)"


def test_ninguna_figura_dice_techo_de_mcc_ni_phi_con_indice():
    for ident in FIGURAS_C4:
        svg = (ASSETS / f"{ident}.svg").read_text(encoding="utf-8")
        for etiqueta in re.findall(r'aria-label="([^"]*)"', svg):
            assert not re.search(r"techo.{0,60}MCC|MCC.{0,60}techo", etiqueta), ident
        assert not re.search(r"φ[₁₂]|\\phi_\{?[12]\b", svg), ident


@pytest.mark.parametrize("ruta", (P1, P2), ids=lambda p: p.stem)
def test_ningun_argmin_con_igual(ruta):
    assert r"=\operatorname*{arg\,min}" not in leer(ruta).replace(" ", "")


def test_p1_frases_literales():
    t = re.sub(r"\s+", " ", leer(P1))
    assert re.search(r"aquí \$\\phi\$ no incluye la constante", t, re.I)
    assert "son dos decisiones distintas" in t
    sep = [s for s in re.split(r"(?m)^## ", leer(P1)) if "ml-c4-separable" in s]
    assert sep and not any("×10" in s or "explota" in s for s in sep)


def test_softmax_con_sus_hipotesis():
    d = re.sub(r"\s+", " ", directiva(leer(P1), "ml-c4-def-softmax"))
    assert "la de menor índice" in d
    assert r"Con $\mu>0$ y las $K$ clases presentes" in d
    assert "sí son únicas" not in d


def test_teorema_conformal_con_su_supuesto_condicionado():
    t = leer(P2)
    teo = re.sub(r"\s+", " ", directiva(t, "ml-c4-teo-cobertura-conformal"))
    for f in (r"condicionado en $\mathcal D_{\text{ajuste}}$",
              "su distribución conjunta no cambia si se permutan",
              "No basta con no usar la calibración"):
        assert f in teo, f"falta «{f}» en el teorema"
    assert "función fija" in re.sub(r"\s+", " ", directiva(t, "ml-c4-dem-cobertura-conformal"))


def test_p2_y_guion_09_usan_el_mapa_unico():
    s3 = secciones(leer(P2))[3]
    nb = leer(NB09)
    for nombre in ("val_a", "val_b", "cal"):
        assert nombre in s3, f"P2 §3 no nombra {nombre}"
        assert nombre in nb, f"guion 09 no nombra {nombre}"


def test_guion_09_bloque_1_en_val_b():
    cs = celdas(leer(NB09))
    b1 = "".join(v for k, v in cs.items() if k.startswith("bloque-1-"))
    assert "toda la validación" not in b1 and "600" not in b1


def test_tarea_fecha_y_benchmark():
    assert "la fecha la da el profesor" in leer(TAREA).lower()
    cs = celdas(leer(NBT))
    b2 = "".join(v for k, v in cs.items() if k.startswith("bloque-2-") or k == "entrega-2")
    assert "val_b" in b2, "el guion de la tarea no dice que el benchmark va en val_b"


# --------------------------------------------------------------- guiones ---

def _claves_texto(stem):
    src = (GUIONES / f"{stem}.py").read_text(encoding="utf-8")
    return re.findall(r"^# %% \[texto\] ([a-z0-9-]+)", src, re.M)


@pytest.mark.parametrize("ruta", GUIONES_C4, ids=lambda p: p.name)
def test_los_guiones_tienen_sus_claves_y_ninguna_vacia(ruta):
    cs = celdas(leer(ruta))
    stem = ruta.name.removesuffix(".texto.md")
    assert list(cs) == _claves_texto(stem)
    vacias = [k for k, v in cs.items() if not v.strip()]
    assert not vacias, f"{ruta.name}: celdas vacías {vacias}"
