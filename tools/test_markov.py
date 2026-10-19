"""Las cifras de la clase 1 de cadenas de Markov salen de markov.py y estan
en su pagina.

Tres capas, como pide el plan de unidad §7:

1. Cada cifra con su assert: lo que calcula markov.py contra el valor escrito
   a mano aqui (cambiar una regla sin tocar la prosa rompe la suite).
2. CIFRAS_EN_PAGINAS {texto literal: [(archivo de pagina, ancla)]}: la cifra
   se busca en el bloque de la pagina que empieza en el encabezado `##` que
   contiene el ancla y termina en el siguiente `##` (cambiar la prosa sin tocar
   la regla tambien la rompe; defecto 39). Si la pagina no existe, FALLA.
   FUENTE_DE_CADA_CIFRA ata cada texto a la funcion de markov.py que lo da.
3. El Python de cada pagina corre, define lo que promete y da lo mismo que
   markov.py.

Formato que se busca en las paginas (tras _limpio): decimales con punto
(0.181); miles con espacio («20 000»: el espacio puede ser normal, fino
U+202F/U+2009, duro U+00A0 o «\\,» de LaTeX); fracciones como 2/11 o
\\frac{2}{11} (tambien \\tfrac y \\dfrac); porcentajes pegados o no al «%».
"""
import hashlib
import math
import random
import re
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

import pytest

import markov as m

RAIZ = Path(__file__).resolve().parent.parent
CLASE = RAIZ / "course/8_markov/1_que_es_una_cadena"
P1 = "1_lo_que_necesitas.md"
P2 = "2_el_problema_de_markov.md"
P3 = "3_ajustar_contando.md"
P4 = "4_predecir.md"
P5 = "5_generar_texto.md"
PAGINAS = (P1, P2, P3, P4, P5)

SHA_ORIGINAL = "534f41d59f7142163fa0964076ac6351845c006ea6433778be637fac6d5b04d7"
SHA_CORTE = "7e40231809f16318113cbefbf58a8c271857c2e84b95260c6ff083927c657e92"
TOPE_POR_ARCHIVO = 12 * 1024 * 1024


def fr(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def dec(x, cifras=3):
    return f"{float(x):.{cifras}f}"


def miles(n):
    return f"{int(n):,}".replace(",", " ")


def P_frase():
    return m.matriz_estimada(m.frase_vc())


# ====================================================== el corpus ===

def test_el_corpus_es_el_corte_declarado():
    datos = m.CORPUS.read_bytes()
    assert hashlib.sha256(datos).hexdigest() == SHA_CORTE
    assert len(datos) < TOPE_POR_ARCHIVO
    texto = datos.decode("utf-8")
    assert "\r" not in texto
    assert texto.startswith("Capítulo primero. Que trata de la condición y ejercicio")
    assert "gutenberg" not in texto.lower()
    assert "En un lugar de la Mancha, de cuyo nombre no quiero acordarme" in texto
    readme = (m.CORPUS.parent / "README.md").read_text(encoding="utf-8")
    for dato in (SHA_ORIGINAL, SHA_CORTE, "https://www.gutenberg.org/cache/epub/2000/pg2000.txt",
                 "2026-10-18", "Capítulo primero. Que trata de la condición y ejercicio del "
                 "famoso hidalgo", "*** END OF THE PROJECT GUTENBERG EBOOK DON QUIJOTE ***"):
        assert dato in readme, dato


def test_las_frases_de_las_paginas_estan_en_el_corte():
    texto = m.cargar_corpus()
    assert m.FRASE_EN_EL_CORPUS in texto
    assert m.capitulo_de(m.FRASE) == (2, "IX")
    assert m.FRASE_E in texto and m.capitulo_de(m.FRASE_E) == (2, "XXVI")
    assert m.FRASE_ESPACIOS in texto and m.capitulo_de(m.FRASE_ESPACIOS) == (1, "primero")


def test_tamano_del_corpus():
    assert len(m.letras_corpus()) == 1_620_532
    assert len(m.caracteres_corpus()) == 1_997_128
    assert len(m.palabras_corpus()) == 376_597
    assert len(m.vocabulario()) == 22_164


# ==================================================== normalizar ===

def test_normalizar_vc_funde_acentos_y_conserva_la_ene():
    assert m.normalizar_vc("¡Qué pingüino, Ñandú y año!") == "quepinguinoñanduyaño"
    assert m.normalizar_vc("à ù ï Í") == "auii"
    assert m.normalizar_vc("1605 — ¿Sí?") == "si"


def test_la_y_es_consonante_y_clase_vc_rechaza_lo_que_no_es_letra():
    assert m.clase_vc("y") == "C" and m.clase_vc("ñ") == "C" and m.clase_vc("u") == "V"
    for malo in (" ", "á", "A", ",", "ab", ""):
        with pytest.raises(ValueError):
            m.clase_vc(malo)


def test_normalizar_caracteres_deja_28_simbolos_y_un_solo_espacio():
    assert m.normalizar_caracteres("  Hola,\n—dijo  él; ¿qué?  ") == "hola dijo el que"
    assert len(m.ALFABETO) == 28 and m.ALFABETO.endswith(" ")
    texto = m.caracteres_corpus()
    # La «k» no aparece en todo el corte: su fila de memoria 1 es un contexto
    # sin observaciones (N(k) = 0), el caso que la pagina 3 distingue.
    assert set(m.ALFABETO) - set(texto) == {"k"}
    assert "  " not in texto and texto == texto.strip()


def test_normalizar_palabras():
    assert m.normalizar_palabras("Don Quijote—dijo Sancho—, ¡vuestra merced!") == [
        "don", "quijote", "dijo", "sancho", "vuestra", "merced"]
    assert m.normalizar_palabras("año 1605: d'él") == ["año", "d", "el"]


# =============================================== la frase congelada ===

def test_la_frase_a_mano_es_la_del_plan():
    assert m.FRASE == "Con la iglesia hemos dado, Sancho"
    assert m.FRASE_EN_EL_CORPUS == "— Con la iglesia hemos dado, Sancho."
    assert m.frase_a_mano() == "conlaiglesiahemosdadosancho"
    assert len(m.frase_a_mano()) == 27
    assert m.frase_vc() == "CVCCVVCCVCVVCVCVCCVCVCVCCCV"
    N = m.matriz_conteos(m.frase_vc(), m.ESTADOS_VC)
    assert N == [[2, 9], [10, 5]]                       # orden V, C
    assert m.salidas(N) == [11, 15]
    assert sum(m.salidas(N)) == 26
    assert P_frase() == [[F(2, 11), F(9, 11)], [F(2, 3), F(1, 3)]]
    assert m.frase_vc()[0] == "C" and m.MU0_C == (0, 1)


def test_la_frase_cumple_los_requisitos_de_cualquier_sustituta():
    seq = m.frase_vc()
    N = m.matriz_conteos(seq, m.ESTADOS_VC)
    assert seq[0] == "C" and all(n > 0 for f in N for n in f)
    assert len(m.frase_a_mano()) <= 30 and "y" not in m.frase_a_mano()


# ================================== pagina 1 · lo que necesitas ===

def test_p1_el_experimento_de_las_26_posiciones():
    e = m.experimento_posiciones()
    assert e["posiciones"] == 26
    assert e["A"] == F(12, 26) and e["B"] == F(11, 26) and e["AyB"] == F(2, 26)
    assert e["A|B"] == F(2, 11) == e["AyB"] / e["B"]
    # no hay independencia: Pr(A ∩ B) = 2/26 ≈ 0.077 contra Pr(A)Pr(B) ≈ 0.195
    assert e["A*B"] == F(33, 169) and dec(e["A*B"]) == "0.195" and dec(e["AyB"]) == "0.077"
    assert e["AyB"] != e["A*B"] and e["A|B"] != e["A"]
    # probabilidad total con la particion {actual V, actual C}
    assert e["A|noB"] == F(10, 15) and e["noB"] == F(15, 26)
    assert e["total"] == e["A"] == F(2, 11) * F(11, 26) + F(10, 15) * F(15, 26)


def test_p1_la_regla_del_producto_en_un_tramo():
    r = m.regla_del_producto("CVC")
    assert (r["ventanas"], r["x"], r["xy"], r["xyz"]) == (25, 14, 9, 7)
    assert (r["Pr(x)"], r["Pr(y|x)"], r["Pr(z|x,y)"]) == (F(14, 25), F(9, 14), F(7, 9))
    assert r["conjunta"] == F(7, 25) == r["Pr(x)"] * r["Pr(y|x)"] * r["Pr(z|x,y)"]


def test_p1_la_independencia_condicional_es_un_supuesto():
    c = m.condicionales_memoria_2()
    assert (dec(c["C"]), dec(c["VC"]), dec(c["CC"])) == ("0.710", "0.624", "0.922")
    assert (dec(c["V"]), dec(c["VV"]), dec(c["CV"])) == ("0.181", "0.100", "0.198")


def test_p1_ejercicio_tres_valores_en_otra_frase():
    seq, N, P = m.matriz_vce(m.FRASE_ESPACIOS)
    assert m.normalizar_caracteres(m.FRASE_ESPACIOS) == "en un lugar de la mancha"
    assert seq == "VC_VC_CVCVC_CV_CV_CVCCCV" and len(seq) - 1 == 23
    assert N == [[0, 5, 2], [6, 2, 3], [1, 4, 0]]       # orden V, C, _
    assert m.salidas(N) == [7, 11, 5]
    assert P == [[0, F(5, 7), F(2, 7)], [F(6, 11), F(2, 11), F(3, 11)], [F(1, 5), F(4, 5), 0]]


# ============================== pagina 2 · el problema de Markov ===

def test_p2_aritmetica_de_markov_1913():
    a = m.aritmetica_markov_1913()
    assert a["consonantes"] == 11_362
    assert dec(a["Pr(V|V)"]) == "0.128" and dec(a["Pr(V|C)"]) == "0.663"
    assert a["Pr(V|V)"] == F(1104, 8638) and a["Pr(V|C)"] == F(7534, 11362)


def test_p2_lo_mismo_en_el_corpus():
    assert m.vocales_corpus() == 752_551
    assert dec(m.pr_vocal_corpus()) == "0.464"
    assert m.conteos_vc_corpus() == [[135_916, 616_635], [616_635, 251_345]]
    assert [[dec(x) for x in f] for f in m.matriz_corpus()] == [
        ["0.181", "0.819"], ["0.710", "0.290"]]


def test_p2_probabilidad_de_un_tramo_de_la_frase():
    tramo = m.frase_vc()[:5]
    assert tramo == "CVCCV"
    assert m.probabilidad_trayectoria(P_frase(), m.MU0_C, tramo) == F(4, 33)
    assert F(1) * F(2, 3) * F(9, 11) * F(1, 3) * F(2, 3) == F(4, 33)


def test_p2_el_ejemplo_de_tres_estados():
    seq, N, P = m.matriz_vce(m.FRASE)
    assert seq == "CVC_CV_VCCVCVV_CVCVC_CVCV_CVCCCV" and len(seq) - 1 == 31
    assert N == [[1, 7, 3], [10, 3, 2], [1, 4, 0]]
    assert m.salidas(N) == [11, 15, 5]
    assert P == [[F(1, 11), F(7, 11), F(3, 11)], [F(2, 3), F(1, 5), F(2, 15)],
                 [F(1, 5), F(4, 5), 0]]
    assert all(sum(f) == 1 for f in P)
    assert [sum(f[j] for f in P) for j in range(3)] != [1, 1, 1]   # columnas no
    assert P[2][2] == 0      # tras un espacio nunca otro espacio: cero estructural


def test_p2_muestrear_fila_a_mano():
    P = P_frase()
    assert m.fila_acumulada(P[0]) == [F(2, 11), 1] and m.fila_acumulada(P[1]) == [F(2, 3), 1]
    pasos, visitados = m.trayectoria_a_mano(P, "C", m.U_A_MANO)
    assert m.U_A_MANO == (0.40, 0.75, 0.90, 0.25, 0.10)
    assert visitados == "CVCCVV"
    assert pasos == [("C", 0.40, "V"), ("V", 0.75, "C"), ("C", 0.90, "C"),
                     ("C", 0.25, "V"), ("V", 0.10, "V")]


def test_p2_rachas():
    r = m.rachas_resumen()
    assert dec(r["q_markov"]) == "0.290" and dec(r["q_independiente"]) == "0.536"
    assert r["reales"] == Counter({1: 384_971, 2: 212_310, 3: 19_027, 4: 323, 5: 3})
    assert r["total"] == 616_634
    assert [dec(r["pr_markov"][l]) for l in range(1, 6)] == [
        "0.710", "0.206", "0.060", "0.017", "0.005"]
    assert [dec(r["pr_independiente"][l]) for l in range(1, 6)] == [
        "0.464", "0.249", "0.133", "0.071", "0.038"]
    assert [dec(F(r["reales"][l], r["total"])) for l in range(1, 4)] == [
        "0.624", "0.344", "0.031"]


def test_p2_rachas_simuladas():
    """10 replicas del largo del corpus por modelo (semillas 2026 y 2027)."""
    assert m.N_RACHAS == 10
    assert m.SEMILLAS["rachas-markov"] == 2026 and m.SEMILLAS["rachas-independiente"] == 2027
    sim = m.rachas_simuladas("markov")
    assert {l: v[0] for l, v in sim.items()} == {
        1: 438_112.5, 2: 126_722.5, 3: 36_729.0, 4: 10_684.0, 5: 3_072.5, 6: 892.5}
    ind = m.rachas_simuladas("independiente")
    assert {l: v[0] for l, v in ind.items()} == {
        1: 187_124.5, 2: 100_176.0, 3: 53_611.5, 4: 28_819.5, 5: 15_360.5, 6: 8_303.5}
    # la franja del 5 % al 95 % es angosta: menos del 7 % de la mediana en ℓ ≤ 5
    for s in (sim, ind):
        for l in range(1, 6):
            med, p5, p95 = s[l]
            assert p5 <= med <= p95 and (p95 - p5) / med < 0.07


def test_p2_ejercicio_a_cadena_dada_como_grafo():
    assert all(sum(f) == 1 for f in m.EJ_P2_P)
    assert m.probabilidad_trayectoria(m.EJ_P2_P, m.EJ_P2_MU0, m.EJ_P2_TRAYECTORIA,
                                      m.EJ_P2_ESTADOS) == F(1, 8)


def test_p2_ejercicio_b_e_contra_no_e():
    e = m.ejercicio_p2_e()
    assert e["letras"] == "llanezamuchachonoteencumbres" and len(e["letras"]) == 28
    assert e["N"] == [[1, 3], [3, 20]]                     # orden E, N
    assert e["P"] == [[F(1, 4), F(3, 4)], [F(3, 23), F(20, 23)]]
    assert e["Pr(e)"] == F(1, 7)
    assert dec(e["corpus_Pr(e)"]) == "0.140"
    assert dec(e["corpus_P"][0][0]) == "0.034" and dec(e["corpus_P"][1][0]) == "0.157"


# ==================================== pagina 3 · ajustar contando ===

TRAZA = [  # (j, s, s', N(V,V), N(V,C), N(C,V), N(C,C)) tras sumar el paso j, desde 0
    (0, "C", "V", 0, 0, 1, 0), (1, "V", "C", 0, 1, 1, 0), (2, "C", "C", 0, 1, 1, 1),
    (3, "C", "V", 0, 1, 2, 1), (4, "V", "V", 1, 1, 2, 1), (5, "V", "C", 1, 2, 2, 1),
    (6, "C", "C", 1, 2, 2, 2), (7, "C", "V", 1, 2, 3, 2), (8, "V", "C", 1, 3, 3, 2),
    (9, "C", "V", 1, 3, 4, 2), (10, "V", "V", 2, 3, 4, 2), (11, "V", "C", 2, 4, 4, 2),
    (12, "C", "V", 2, 4, 5, 2), (13, "V", "C", 2, 5, 5, 2), (14, "C", "V", 2, 5, 6, 2),
    (15, "V", "C", 2, 6, 6, 2), (16, "C", "C", 2, 6, 6, 3), (17, "C", "V", 2, 6, 7, 3),
    (18, "V", "C", 2, 7, 7, 3), (19, "C", "V", 2, 7, 8, 3), (20, "V", "C", 2, 8, 8, 3),
    (21, "C", "V", 2, 8, 9, 3), (22, "V", "C", 2, 9, 9, 3), (23, "C", "C", 2, 9, 9, 4),
    (24, "C", "C", 2, 9, 9, 5), (25, "C", "V", 2, 9, 10, 5)]


def test_p3_la_traza_de_contar_fila_por_fila():
    assert [(j, s, s2) + n for j, s, s2, n in m.traza_contar(m.frase_vc())] == TRAZA
    N, sal, Pg = m.contar_transiciones(m.frase_vc(), ("V", "C"))
    assert N == {("V", "V"): 2, ("V", "C"): 9, ("C", "V"): 10, ("C", "C"): 5}
    assert sal == {"V": 11, "C": 15}
    assert Pg[("V", "V")] == F(2, 11) and Pg[("C", "C")] == F(1, 3)
    # un estado que no aparece conserva su columna y no tiene fila
    N, sal, Pg = m.contar_transiciones("CCCC", ("V", "C"))
    assert N[("C", "V")] == 0 and sal["V"] == 0
    assert ("V", "C") not in Pg and Pg[("C", "V")] == 0


def test_p3_el_error_de_una_replica_trazada():
    """La réplica CVCCVV (la muestreada a mano en la página 2) da filas
    (1/2, 1/2) y (2/3, 1/3): su error contra la matriz generadora es 0.319."""
    P = m.redondear_matriz(m.matriz_corpus())
    N = m.matriz_conteos("CVCCVV", m.ESTADOS_VC)
    Phat = m.estimar(N)
    assert Phat == [[F(1, 2), F(1, 2)], [F(2, 3), F(1, 3)]]
    assert f"{m.error_recuperacion(P, Phat):.3f}" == "0.319"


def test_p3_la_verosimilitud_condicionada_a_s0():
    seq = m.frase_vc()
    L = m.verosimilitud(P_frase(), seq)
    assert L == F(2, 11) ** 2 * F(9, 11) ** 9 * F(2, 3) ** 10 * F(1, 3) ** 5
    assert L == F(110592, 285311670611)
    assert f"{float(L):.2e}" == "3.88e-07"
    L_mitad = m.verosimilitud(m.P_MITADES, seq)
    assert L_mitad == F(1, 2 ** 26) and f"{float(L_mitad):.2e}" == "1.49e-08"
    L_corpus = m.verosimilitud(m.redondear_matriz(m.matriz_corpus()), seq)
    assert f"{float(L_corpus):.2e}" == "3.63e-07"
    assert L > L_corpus > L_mitad
    assert round(L / L_mitad) == 26


def test_p3_la_estimacion_maximiza_la_verosimilitud_fila_por_fila():
    """Cualquier otra fila (en una rejilla de centesimas) da menos."""
    seq = m.frase_vc()
    L = m.verosimilitud(P_frase(), seq)
    for a in range(1, 100):
        for b in range(1, 100):
            P = [[F(a, 100), 1 - F(a, 100)], [F(b, 100), 1 - F(b, 100)]]
            assert m.verosimilitud(P, seq) < L


def test_p3_una_fila_sin_salidas_queda_sin_estimar():
    assert m.estimar([[0, 0], [3, 1]]) == [None, [F(3, 4), F(1, 4)]]


def test_p3_recuperar_una_matriz_conocida():
    assert m.SEMILLAS["recuperar-p"] == 2028
    assert m.LONGITUDES_T == (10, 30, 100, 300, 1000, 3000, 10000)
    assert m.REPLICAS_RECUPERAR == 200
    assert m.redondear_matriz(m.matriz_corpus()) == [[F(181, 1000), F(819, 1000)],
                                                     [F(710, 1000), F(290, 1000)]]
    d = m.recuperar_p()
    assert {T: (dec(v["mediana"]), dec(v["p5"]), dec(v["p95"])) for T, v in d.items()} == {
        10: ("0.210", "0.069", "0.319"), 30: ("0.105", "0.033", "0.219"),
        100: ("0.067", "0.025", "0.130"), 300: ("0.035", "0.009", "0.071"),
        1000: ("0.020", "0.006", "0.042"), 3000: ("0.011", "0.003", "0.022"),
        10000: ("0.006", "0.002", "0.013")}
    assert all(v["sin_salidas"] == 0 for v in d.values())
    assert all(len(v["errores"]) == 200 for v in d.values())


def test_p3_lo_general_784_entradas():
    e = m.entradas_memoria_1()
    assert e == {"entradas": 784, "ceros": 393, "menos_de_5": 433, "entre_1_y_4": 40,
                 "contextos_sin_salidas": ["k"]}
    assert len(m.ALFABETO) ** 2 == 784


def test_p3_laplace_en_la_frase_y_en_el_corpus():
    N = m.matriz_conteos(m.frase_vc(), m.ESTADOS_VC)
    assert m.estimar(N, suavizado=1) == [[F(3, 13), F(10, 13)], [F(11, 17), F(6, 17)]]
    sin, total = m.fila_caracteres("q", "ua", 0)
    con, _ = m.fila_caracteres("q", "ua", 1)
    assert total == 32_155
    assert sin == {"u": 1, "a": 0}
    assert con == {"u": F(32_156, 32_183), "a": F(1, 32_183)}
    assert dec(con["u"], 4) == "0.9992"


def test_p3_tabla_de_ceros_por_memoria():
    filas = [m.fraccion_no_vista(h) for h in range(4)]
    assert [(f["no_vistas"], f["total"]) for f in filas] == [
        (0, 998_564), (29, 998_563), (718, 998_562), (5_694, 998_561)]
    assert [f"{float(f['fraccion']) * 100:.3f}" for f in filas] == [
        "0.000", "0.003", "0.072", "0.570"]
    assert [(f["contextos_vistos"], f["contextos_posibles"]) for f in filas] == [
        (1, 1), (27, 28), (379, 784), (3_328, 21_952)]


def test_p3_ejercicio_mini_texto_de_tres_simbolos():
    e = m.ejercicio_p3()
    assert m.EJ_P3_TEXTO == "abacabbcabac"
    assert e["N"] == [[0, 3, 2], [2, 1, 1], [2, 0, 0]]
    assert e["salidas"] == [5, 4, 2]
    assert e["P"] == [[0, F(3, 5), F(2, 5)], [F(1, 2), F(1, 4), F(1, 4)], [1, 0, 0]]
    assert e["laplace"] == [[F(1, 8), F(1, 2), F(3, 8)], [F(3, 7), F(2, 7), F(2, 7)],
                            [F(3, 5), F(1, 5), F(1, 5)]]


# ============================================ pagina 4 · predecir ===

def test_p4_el_arbol_de_dos_pasos():
    hojas = m.arbol_dos_pasos(P_frase(), "C")
    assert hojas == {("V", "V"): F(4, 33), ("V", "C"): F(6, 11),
                     ("C", "V"): F(2, 9), ("C", "C"): F(1, 9)}
    assert sum(hojas.values()) == 1
    assert hojas[("V", "V")] + hojas[("C", "V")] == F(34, 99)


def test_p4_mu_t_a_mano_desde_c():
    mus = m.mu_t(P_frase(), m.MU0_C, 3)
    assert mus == [[0, 1], [F(2, 3), F(1, 3)], [F(34, 99), F(65, 99)],
                   [F(1634, 3267), F(1633, 3267)]]


def test_p4_mu_t_del_corpus_y_su_simulacion():
    assert m.SEMILLAS["mu-t-desde-V"] == 2029 and m.SEMILLAS["mu-t-desde-C"] == 2030
    d = m.mu_t_corpus()
    assert [dec(p) for p in d["V"]["cuenta"]] == [
        "1.000", "0.181", "0.615", "0.385", "0.507", "0.442", "0.476", "0.458", "0.468"]
    assert [dec(p) for p in d["C"]["cuenta"]] == [
        "0.000", "0.710", "0.334", "0.533", "0.428", "0.484", "0.454", "0.470", "0.462"]
    assert [dec(p) for p in d["V"]["simulada"]] == [
        "1.000", "0.180", "0.611", "0.392", "0.498", "0.438", "0.476", "0.460", "0.464"]
    assert [dec(p) for p in d["C"]["simulada"]] == [
        "0.000", "0.712", "0.326", "0.543", "0.424", "0.485", "0.452", "0.467", "0.470"]
    peor, peor_z = m.diferencia_maxima_mu_t()
    assert dec(peor) == "0.010" and f"{peor_z:.1f}" == "2.0" and peor_z < 3
    assert max(m.error_estandar(p, 10_000) for v in d.values() for p in v["cuenta"]) <= 0.005


def test_p4_ejercicio_a_mu2_en_tres_estados():
    assert all(sum(f) == 1 for f in m.EJ_P4_P)
    assert m.predecir(m.EJ_P4_P, m.EJ_P4_MU0, 1) == [F(5, 12), F(1, 8), F(11, 24)]
    assert m.predecir(m.EJ_P4_P, m.EJ_P4_MU0, 2) == [F(1, 4), F(1, 3), F(5, 12)]


def test_p4_ejercicio_b_leer_una_simulacion():
    assert m.SEMILLAS["ejercicio-simulacion"] == 2031 and m.N_EJ_SIMULACION == 400
    e = m.ejercicio_p4_simulacion()
    assert [dec(x) for x in e["simulada"]] == ["0.000", "0.693", "0.352", "0.512"]
    assert [dec(x) for x in e["cuenta"]] == ["0.000", "0.710", "0.334", "0.533"]
    assert [dec(x) for x in e["ee"]] == ["0.000", "0.023", "0.024", "0.025"]
    for t in (1, 2, 3):
        assert abs(e["simulada"][t] - e["cuenta"][t]) < 2 * e["ee"][t]


# ========================================= pagina 5 · generar texto ===

GENERADOS = {
    0: " pusnve dprate duuutesrsacee insi qlsao iamsopaa ceecae do vnoov  oausu q i etg anls "
       "oalilanosll y  grcgiiypeo ldes eees eebdessatoes uoed nn enlea aa oehtbo mehs n "
       "naoeesiaya ysitrn laa  muercltsoi n",
    1: "er gonos sesel usiava lera cuecive de lo ta ques pera a lodasijeralgosper ene l y y "
       "mabera y tidelerla tia quenoncalerela tre dandaue cr s quede en ve sin suieo e a "
       "cuestadui des que pa fe y mbesctrta",
    2: "enchombolaso aquisia veasagionallegar que parespel er arovicino pro es quecienes do "
       "la dos mues y fue el minto acaba queño as dejote noco a y dechacescuanajabese lle "
       "nos hano de encera quesar y pue ma",
    3: "en su amosura en el dijote espero otrastilla paremostan de señor como acomo el "
       "cuerte lo en cuandoliconvies sustra y un gran vizcaidad del fio hacenca que pros de "
       "burrespondios en loco de tendicen otr",
}
GENERADO_PALABRAS = ("en tanto artificio que sus aguelos ahora la ventana que venian del pie "
                     "llano a don quijote de sirgo pon el famoso caballero en las desdichas "
                     "del a pasar habiendole")


def test_p5_generar_a_mano_con_la_tabla_de_tres_simbolos():
    _, _, P = m.matriz_vce(m.FRASE)
    assert m.U_GENERAR_A_MANO == (0.90, 0.55, 0.30)
    assert m.generar_a_mano(P, m.ESTADOS_VCE, "C", m.U_GENERAR_A_MANO) == [
        ("C", 0.90, "_"), ("_", 0.55, "C"), ("C", 0.30, "V")]


def test_p5_ejercicio_cuatro_simbolos():
    assert all(sum(f) == 1 for f in m.EJ_P5_TABLA)
    pasos = m.generar_a_mano(m.EJ_P5_TABLA, m.EJ_P5_SIMBOLOS, m.EJ_P5_INICIO, m.EJ_P5_U)
    assert "".join(s for _, _, s in pasos) == "nan "
    assert pasos == [(" ", 0.62, "n"), ("n", 0.15, "a"), ("a", 0.40, "n"), ("n", 0.90, " ")]


def test_p5_las_salidas_con_semilla():
    assert [m.SEMILLAS[f"generar-{h}"] for h in range(4)] == [2032, 2033, 2034, 2035]
    for h, esperado in GENERADOS.items():
        g = m.generar(h)
        assert g == esperado, h
        assert len(g) == 200 and g.startswith(m.CONTEXTO_INICIAL[:h])
    assert m.SEMILLAS["generar-palabras"] == 2036
    assert m.generar(1, "palabras") == GENERADO_PALABRAS
    assert len(GENERADO_PALABRAS.split()) == 30


def test_p5_repetir_fragmentos_del_corpus():
    largos = [m.subcadena_mas_larga_en_corpus(m.generar(h)) for h in range(4)]
    assert largos == [6, 10, 11, 13]
    fracciones = [m.fraccion_ngramas_en_corpus(m.generar(h), 8) for h in range(4)]
    assert fracciones == [0, F(18, 193), F(39, 193), F(82, 193)]
    assert [f"{float(x) * 100:.0f}" for x in fracciones] == ["0", "9", "20", "42"]


def test_p5_un_contexto_nunca_visto_usa_la_fila_uniforme():
    tabla = {"a": [0.0, 1.0]}
    rng = random.Random(1)
    salida = m.generar_desde(tabla, "ab", "b", 1, rng)
    u = random.Random(1).random()
    assert salida == "b" + "ab"[m.muestrear_fila([0.5, 0.5], u)]


# ========================================= muestrear y simular ===

def test_muestrear_fila_casos_borde():
    assert m.muestrear_fila([F(2, 3), F(1, 3)], 0) == 0
    assert m.muestrear_fila([F(2, 3), F(1, 3)], F(2, 3)) == 1      # u = suma: sigue
    assert m.muestrear_fila([0, 1, 0], 0.5) == 1
    assert m.muestrear_fila([0.1] * 10, 0.9999999999999999) == 9   # redondeo


def test_simular_es_reproducible_y_gasta_un_u_por_paso():
    P = P_frase()
    a = m.simular(P, m.MU0_C, 5, 4, 7)
    assert a == m.simular(P, m.MU0_C, 5, 4, 7)
    rng = random.Random(7)
    us = [rng.random() for _ in range(5)]
    s = m.muestrear_fila([0.0, 1.0], us[0])
    tray = [s]
    for u in us[1:]:
        s = m.muestrear_fila([float(x) for x in P[s]], u)
        tray.append(s)
    assert a[0] == tray


def test_nunca_usa_random_choices():
    fuente = Path(m.__file__).read_text(encoding="utf-8")
    assert "choices(" not in fuente and "random.choice(" not in fuente


# ================================== cifras en su pagina y su bloque ===

def _exp():
    return m.experimento_posiciones()


def _cuenta(fraccion, n):
    return f"{int(fraccion * n)}/{n}"


def _rp(T, campo):
    return dec(m.recuperar_p()[T][campo])


def _ceros(h):
    return f"{float(m.fraccion_no_vista(h)['fraccion']) * 100:.3f}%"


def _ngramas(h):
    return f"{float(m.fraccion_ngramas_en_corpus(m.generar(h))) * 100:.0f}%"


def _mantisa(P):
    """3.88 de L(P) ≈ 3.88 × 10⁻⁷ sobre la frase."""
    return f"{float(m.verosimilitud(P, m.frase_vc())):.2e}"[:4]


def _gen40(h):
    return m.generar(h)[:40].strip()


def _cifras():
    """(texto, pagina, ancla, fuente): la fuente devuelve el texto desde
    markov.py. Las anclas son tentativas (el orquestador las ajusta al
    encabezado final)."""
    P = P_frase()
    Pc = m.matriz_corpus()
    e = _exp
    r = m.rachas_resumen
    sim4 = m.ejercicio_p4_simulacion
    vce = m.matriz_vce
    lst = [
        # --- p1
        ("26", P1, "experimento", lambda: str(e()["posiciones"])),
        ("12/26", P1, "experimento", lambda: _cuenta(e()["A"], 26)),
        ("11/26", P1, "experimento", lambda: _cuenta(e()["B"], 26)),
        ("2/26", P1, "condicional", lambda: _cuenta(e()["AyB"], 26)),
        ("2/11", P1, "condicional", lambda: fr(e()["A|B"])),
        ("12/26", P1, "Independencia", lambda: _cuenta(e()["A"], 26)),
        ("2/11", P1, "Independencia", lambda: fr(e()["A|B"])),
        ("0.195", P1, "Independencia", lambda: dec(e()["A*B"])),
        ("0.077", P1, "Independencia", lambda: dec(e()["AyB"])),
        ("14/25", P1, "producto", lambda: fr(m.regla_del_producto()["Pr(x)"])),
        ("9/14", P1, "producto", lambda: fr(m.regla_del_producto()["Pr(y|x)"])),
        ("7/9", P1, "producto", lambda: fr(m.regla_del_producto()["Pr(z|x,y)"])),
        ("7/25", P1, "producto", lambda: fr(m.regla_del_producto()["conjunta"])),
        ("10/15", P1, "total", lambda: _cuenta(e()["A|noB"], 15)),
        ("15/26", P1, "total", lambda: _cuenta(e()["noB"], 26)),
        ("12/26", P1, "total", lambda: _cuenta(e()["total"], 26)),
        ("0.710", P1, "Independencia condicional",
         lambda: dec(m.condicionales_memoria_2()["C"])),
        ("0.624", P1, "Independencia condicional",
         lambda: dec(m.condicionales_memoria_2()["VC"])),
        ("0.922", P1, "Independencia condicional",
         lambda: dec(m.condicionales_memoria_2()["CC"])),
        ("23", P1, "Ejercicios", lambda: str(len(vce(m.FRASE_ESPACIOS)[0]) - 1)),
        ("5/7", P1, "Ejercicios", lambda: fr(vce(m.FRASE_ESPACIOS)[2][0][1])),
        ("2/7", P1, "Ejercicios", lambda: fr(vce(m.FRASE_ESPACIOS)[2][0][2])),
        ("6/11", P1, "Ejercicios", lambda: fr(vce(m.FRASE_ESPACIOS)[2][1][0])),
        ("3/11", P1, "Ejercicios", lambda: fr(vce(m.FRASE_ESPACIOS)[2][1][2])),
        ("4/5", P1, "Ejercicios", lambda: fr(vce(m.FRASE_ESPACIOS)[2][2][1])),
        # --- p2
        ("2/11", P2, "Contar", lambda: fr(P[0][0])),
        ("2/3", P2, "Contar", lambda: fr(P[1][0])),
        ("20 000", P2, "problema", lambda: miles(m.MARKOV_1913["letras"])),
        ("8 638", P2, "problema", lambda: miles(m.MARKOV_1913["vocales"])),
        ("0.128", P2, "problema", lambda: dec(m.aritmetica_markov_1913()["Pr(V|V)"])),
        ("0.663", P2, "problema", lambda: dec(m.aritmetica_markov_1913()["Pr(V|C)"])),
        ("1 620 532", P2, "problema", lambda: miles(len(m.letras_corpus()))),
        ("752 551", P2, "problema", lambda: miles(m.vocales_corpus())),
        ("0.464", P2, "problema", lambda: dec(m.pr_vocal_corpus())),
        ("0.181", P2, "problema", lambda: dec(Pc[0][0])),
        ("0.710", P2, "problema", lambda: dec(Pc[1][0])),
        ("4/33", P2, "trayectoria",
         lambda: fr(m.probabilidad_trayectoria(P, m.MU0_C, m.frase_vc()[:5]))),
        ("1/11", P2, "matriz", lambda: fr(vce()[2][0][0])),
        ("7/11", P2, "matriz", lambda: fr(vce()[2][0][1])),
        ("3/11", P2, "matriz", lambda: fr(vce()[2][0][2])),
        ("2/15", P2, "matriz", lambda: fr(vce()[2][1][2])),
        ("4/5", P2, "matriz", lambda: fr(vce()[2][2][1])),
        ("31", P2, "matriz", lambda: str(len(vce()[0]) - 1)),
        ("0.40", P2, "Muestrear", lambda: f"{m.U_A_MANO[0]:.2f}"),
        ("0.75", P2, "Muestrear", lambda: f"{m.U_A_MANO[1]:.2f}"),
        ("0.90", P2, "Muestrear", lambda: f"{m.U_A_MANO[2]:.2f}"),
        ("0.25", P2, "Muestrear", lambda: f"{m.U_A_MANO[3]:.2f}"),
        ("0.10", P2, "Muestrear", lambda: f"{m.U_A_MANO[4]:.2f}"),
        ("CVCCVV", P2, "Muestrear", lambda: m.trayectoria_a_mano(P, "C", m.U_A_MANO)[1]),
        ("0.290", P2, "Rachas", lambda: dec(r()["q_markov"])),
        ("0.536", P2, "Rachas", lambda: dec(r()["q_independiente"])),
        ("616 634", P2, "Rachas", lambda: miles(r()["total"])),
        ("384 971", P2, "Rachas", lambda: miles(r()["reales"][1])),
        ("212 310", P2, "Rachas", lambda: miles(r()["reales"][2])),
        ("19 027", P2, "Rachas", lambda: miles(r()["reales"][3])),
        ("323", P2, "Rachas", lambda: miles(r()["reales"][4])),
        ("0.624", P2, "Rachas", lambda: dec(F(r()["reales"][1], r()["total"]))),
        ("0.464", P2, "Rachas", lambda: dec(r()["pr_independiente"][1])),
        ("1/8", P2, "Ejercicios", lambda: fr(m.probabilidad_trayectoria(
            m.EJ_P2_P, m.EJ_P2_MU0, m.EJ_P2_TRAYECTORIA, m.EJ_P2_ESTADOS))),
        ("1/4", P2, "Ejercicios", lambda: fr(m.ejercicio_p2_e()["P"][0][0])),
        ("3/4", P2, "Ejercicios", lambda: fr(m.ejercicio_p2_e()["P"][0][1])),
        ("3/23", P2, "Ejercicios", lambda: fr(m.ejercicio_p2_e()["P"][1][0])),
        ("20/23", P2, "Ejercicios", lambda: fr(m.ejercicio_p2_e()["P"][1][1])),
        ("1/7", P2, "Ejercicios", lambda: fr(m.ejercicio_p2_e()["Pr(e)"])),
        ("0.140", P2, "Ejercicios", lambda: dec(m.ejercicio_p2_e()["corpus_Pr(e)"])),
        ("0.034", P2, "Ejercicios", lambda: dec(m.ejercicio_p2_e()["corpus_P"][0][0])),
        ("0.157", P2, "Ejercicios", lambda: dec(m.ejercicio_p2_e()["corpus_P"][1][0])),
        # --- p3
        ("2/11", P3, "Por qué contar", lambda: fr(P[0][0])),
        ("9/11", P3, "Por qué contar", lambda: fr(P[0][1])),
        ("2/3", P3, "Por qué contar", lambda: fr(P[1][0])),
        ("1/3", P3, "Por qué contar", lambda: fr(P[1][1])),
        ("3.88", P3, "Por qué contar", lambda: _mantisa(P)),
        ("1.49", P3, "Por qué contar", lambda: _mantisa(m.P_MITADES)),
        ("3.63", P3, "Por qué contar", lambda: _mantisa(m.redondear_matriz(Pc))),
        ("26", P3, "Algoritmo", lambda: str(len(m.traza_contar(m.frase_vc())))),
        ("200", P3, "Simul", lambda: str(m.REPLICAS_RECUPERAR)),
        ("0.210", P3, "Simul", lambda: _rp(10, "mediana")),
        ("0.069", P3, "Simul", lambda: _rp(10, "p5")),
        ("0.319", P3, "Simul", lambda: _rp(10, "p95")),
        ("0.006", P3, "Simul", lambda: _rp(10000, "mediana")),
        ("0.002", P3, "Simul", lambda: _rp(10000, "p5")),
        ("0.013", P3, "Simul", lambda: _rp(10000, "p95")),
        ("0.290", P3, "Simul", lambda: dec(m.redondear_matriz(Pc)[1][1])),
        ("784", P3, "general", lambda: str(m.entradas_memoria_1()["entradas"])),
        ("393", P3, "general", lambda: str(m.entradas_memoria_1()["ceros"])),
        ("433", P3, "general", lambda: str(m.entradas_memoria_1()["menos_de_5"])),
        ("3/13", P3, "nunca se vio", lambda: fr(m.estimar(
            m.matriz_conteos(m.frase_vc(), m.ESTADOS_VC), 1)[0][0])),
        ("10/13", P3, "nunca se vio", lambda: fr(m.estimar(
            m.matriz_conteos(m.frase_vc(), m.ESTADOS_VC), 1)[0][1])),
        ("32 155", P3, "nunca se vio", lambda: miles(m.fila_caracteres("q", "u")[1])),
        ("32 183", P3, "nunca se vio", lambda: miles(
            m.fila_caracteres("q", "a", 1)[0]["a"].denominator)),
        ("0.003%", P3, "memoria", lambda: _ceros(1)),
        ("0.072%", P3, "memoria", lambda: _ceros(2)),
        ("0.570%", P3, "memoria", lambda: _ceros(3)),
        ("379", P3, "memoria", lambda: str(m.fraccion_no_vista(2)["contextos_vistos"])),
        ("3 328", P3, "memoria", lambda: miles(m.fraccion_no_vista(3)["contextos_vistos"])),
        ("21 952", P3, "memoria", lambda: miles(m.fraccion_no_vista(3)["contextos_posibles"])),
        ("3/5", P3, "Ejercicios", lambda: fr(m.ejercicio_p3()["P"][0][1])),
        ("2/5", P3, "Ejercicios", lambda: fr(m.ejercicio_p3()["P"][0][2])),
        ("1/4", P3, "Ejercicios", lambda: fr(m.ejercicio_p3()["P"][1][1])),
        ("1/5", P3, "Ejercicios", lambda: fr(m.ejercicio_p3()["laplace"][2][1])),
        ("3/8", P3, "Ejercicios", lambda: fr(m.ejercicio_p3()["laplace"][0][2])),
        # --- p4
        ("4/33", P4, "mano", lambda: fr(m.arbol_dos_pasos(P)[("V", "V")])),
        ("6/11", P4, "mano", lambda: fr(m.arbol_dos_pasos(P)[("V", "C")])),
        ("2/9", P4, "mano", lambda: fr(m.arbol_dos_pasos(P)[("C", "V")])),
        ("1/9", P4, "mano", lambda: fr(m.arbol_dos_pasos(P)[("C", "C")])),
        ("34/99", P4, "mano", lambda: fr(m.mu_t(P, m.MU0_C, 2)[2][0])),
        ("65/99", P4, "mano", lambda: fr(m.mu_t(P, m.MU0_C, 2)[2][1])),
        ("1634/3267", P4, "mano", lambda: fr(m.mu_t(P, m.MU0_C, 3)[3][0])),
        ("1633/3267", P4, "mano", lambda: fr(m.mu_t(P, m.MU0_C, 3)[3][1])),
        ("10 000", P4, "Simul", lambda: miles(10_000)),
        ("0.710", P4, "Simul", lambda: dec(m.mu_t_corpus()["C"]["cuenta"][1])),
        ("0.334", P4, "Simul", lambda: dec(m.mu_t_corpus()["C"]["cuenta"][2])),
        ("0.533", P4, "Simul", lambda: dec(m.mu_t_corpus()["C"]["cuenta"][3])),
        ("0.005", P4, "Simul", lambda: dec(max(m.error_estandar(p, 10_000) for v in
                                               m.mu_t_corpus().values() for p in v["cuenta"]))),
        ("0.010", P4, "Simul", lambda: dec(m.diferencia_maxima_mu_t()[0])),
        ("5/12", P4, "Ejercicios", lambda: fr(m.predecir(m.EJ_P4_P, m.EJ_P4_MU0, 1)[0])),
        ("11/24", P4, "Ejercicios", lambda: fr(m.predecir(m.EJ_P4_P, m.EJ_P4_MU0, 1)[2])),
        ("1/4", P4, "Ejercicios", lambda: fr(m.predecir(m.EJ_P4_P, m.EJ_P4_MU0, 2)[0])),
        ("1/3", P4, "Ejercicios", lambda: fr(m.predecir(m.EJ_P4_P, m.EJ_P4_MU0, 2)[1])),
        ("400", P4, "Ejercicios", lambda: str(m.N_EJ_SIMULACION)),
        ("0.352", P4, "Ejercicios", lambda: dec(sim4()["simulada"][2])),
        ("0.334", P4, "Ejercicios", lambda: dec(sim4()["cuenta"][2])),
        ("0.024", P4, "Ejercicios", lambda: dec(sim4()["ee"][2])),
        # --- p5
        ("0.90", P5, "mano", lambda: f"{m.U_GENERAR_A_MANO[0]:.2f}"),
        ("0.55", P5, "mano", lambda: f"{m.U_GENERAR_A_MANO[1]:.2f}"),
        ("0.30", P5, "mano", lambda: f"{m.U_GENERAR_A_MANO[2]:.2f}"),
        ("2/15", P5, "mano", lambda: fr(vce()[2][1][2])),
        ("2032", P5, "Ejemplos", lambda: str(m.SEMILLAS["generar-0"])),
        ("2035", P5, "Ejemplos", lambda: str(m.SEMILLAS["generar-3"])),
        (_gen40(0), P5, "Ejemplos", lambda: _gen40(0)),
        (_gen40(1), P5, "Ejemplos", lambda: _gen40(1)),
        (_gen40(2), P5, "Ejemplos", lambda: _gen40(2)),
        (_gen40(3), P5, "Ejemplos", lambda: _gen40(3)),
        ("9%", P5, "arriesga", lambda: _ngramas(1)),
        ("20%", P5, "arriesga", lambda: _ngramas(2)),
        ("42%", P5, "arriesga", lambda: _ngramas(3)),
        ("0.62", P5, "Ejercicios", lambda: f"{m.EJ_P5_U[0]:.2f}"),
        ("0.15", P5, "Ejercicios", lambda: f"{m.EJ_P5_U[1]:.2f}"),
        ("0.40", P5, "Ejercicios", lambda: f"{m.EJ_P5_U[2]:.2f}"),
        ("0.90", P5, "Ejercicios", lambda: f"{m.EJ_P5_U[3]:.2f}"),
        ("3/4", P5, "Ejercicios", lambda: fr(m.EJ_P5_TABLA[1][0])),
    ]
    return lst


CIFRAS = _cifras()
CIFRAS_EN_PAGINAS = {}
for _t, _p, _a, _ in CIFRAS:
    CIFRAS_EN_PAGINAS.setdefault(_t, []).append((_p, _a))
FUENTE_DE_CADA_CIFRA = [(_t, _f) for _t, _, _, _f in CIFRAS]


@pytest.mark.parametrize("texto,fuente", FUENTE_DE_CADA_CIFRA,
                         ids=[f"{k}-{t}" for k, (t, _) in enumerate(FUENTE_DE_CADA_CIFRA)])
def test_cada_cifra_de_las_paginas_sale_de_markov(texto, fuente):
    assert fuente() == texto


def _limpio(s):
    """El texto de la pagina sin lo que no es la cifra."""
    s = s.replace("\u2212", "-").replace("\u2060", "")
    s = re.sub(r"\\[td]?frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2", s)
    for fino in ("\u202f", "\u2009", "\u00a0", "\\,", "\\;", "\\ ", "~"):
        s = s.replace(fino, " ")
    s = re.sub(r"\\(?:text|textbf|mathrm|mathbf)\{([^{}]*)\}", r"\1", s)
    s = s.replace("\\%", "%").replace("\\approx", "≈").replace("\\cdot", "·")
    s = s.replace("\\times", "×")
    s = s.replace("**", "").replace("$", "").replace("`", "")
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r" %", "%", s)
    return s


def _pagina(nombre):
    ruta = CLASE / nombre
    assert ruta.is_file(), f"no existe la pagina {ruta}"
    return ruta.read_text(encoding="utf-8")


def _bloque(texto, ancla):
    """Del encabezado `##` (nivel 2 exacto) que contiene el ancla hasta el
    siguiente `##`. El primero que la contenga, sin distinguir mayusculas."""
    lineas = texto.splitlines()
    inicio = next((i for i, l in enumerate(lineas)
                   if l.startswith("## ") and ancla.lower() in l.lower()), None)
    assert inicio is not None, f"no hay encabezado ## con «{ancla}»"
    fin = next((i for i in range(inicio + 1, len(lineas)) if lineas[i].startswith("## ")),
               len(lineas))
    return "\n".join(lineas[inicio:fin])


def _esta(cifra, texto):
    patron = r"(?<![\d./])" + re.escape(cifra) + r"(?![\d/])"
    return re.search(patron, texto) is not None


@pytest.mark.parametrize("pagina", PAGINAS)
def test_cifras_de_la_pagina_en_su_bloque(pagina):
    texto = _pagina(pagina)
    faltan = []
    for cifra, p, ancla, _ in CIFRAS:
        if p != pagina:
            continue
        try:
            bloque = _limpio(_bloque(texto, ancla))
        except AssertionError as e:
            faltan.append(f"{cifra!r}: {e}")
            continue
        if not _esta(cifra, bloque):
            faltan.append(f"{cifra!r} no esta en el bloque «{ancla}»")
    assert not faltan, f"{pagina}: " + "; ".join(faltan)


def test_el_limpiador_lee_los_formatos_permitidos():
    assert _esta("2/11", _limpio(r"$\widehat P(V\mid V)=\frac{2}{11}$"))
    assert _esta("2/11", _limpio(r"$\tfrac{2}{11}$ y $\dfrac{9}{11}$"))
    assert _esta("20 000", _limpio("20\u202f000 letras")) and _esta("20 000", _limpio(r"$20\,000$"))
    assert _esta("0.570%", _limpio(r"0.570 \%")) and _esta("0.570%", _limpio("0.570%"))
    assert not _esta("2/3", _limpio("2/33")) and not _esta("1/3", _limpio("11/3"))
    assert not _esta("0.71", _limpio("0.710"))


# ================================== el Python de cada pagina corre ===

FUNCIONES_POR_PAGINA = {
    P2: ["muestrear_fila"],
    P3: ["contar_transiciones"],
    P4: ["predecir"],
    P5: ["generar"],
}


def _bloques_python(pagina):
    return re.findall(r"^```python\n(.*?)^```$", _pagina(pagina), re.S | re.M)


def _cargar(pagina):
    """Ejecuta en orden los bloques ```python de la pagina en un espacio
    propio. La pagina 5 recibe muestrear_fila de la pagina 2 (lo que trae)."""
    ns = {"__name__": "pagina", "random": random, "Fraction": F}
    if pagina == P5:
        ns["muestrear_fila"] = m.muestrear_fila
    for codigo in _bloques_python(pagina):
        exec(compile(codigo, pagina, "exec"), ns)
    return ns


@pytest.mark.parametrize("pagina", sorted(FUNCIONES_POR_PAGINA))
def test_el_python_de_la_pagina_define_y_calcula_lo_mismo(pagina):
    assert _bloques_python(pagina), f"{pagina} no trae ningun bloque ```python"
    ns = _cargar(pagina)
    for nombre in FUNCIONES_POR_PAGINA[pagina]:
        assert callable(ns.get(nombre)), (pagina, nombre)
    P = P_frase()
    if pagina == P2:
        f = ns["muestrear_fila"]
        s, visitados = "C", "C"
        for u in m.U_A_MANO:
            s = m.ESTADOS_VC[f(P[m.ESTADOS_VC.index(s)], u)]
            visitados += s
        assert visitados == "CVCCVV"
        rng = random.Random(0)
        for _ in range(300):
            fila = [rng.random() for _ in range(4)]
            fila = [x / sum(fila) for x in fila]
            u = rng.random()
            assert f(fila, u) == m.muestrear_fila(fila, u)
    elif pagina == P3:
        f = ns["contar_transiciones"]
        for secuencia, estados in ((m.frase_vc(), ("V", "C")),
                                   (m.EJ_P3_TEXTO, ("a", "b", "c")),
                                   ("CCCC", ("V", "C"))):
            assert tuple(f(secuencia, estados)) == m.contar_transiciones(secuencia, estados)
    elif pagina == P4:
        f = ns["predecir"]
        assert list(f(P, [F(0), F(1)], 3)) == [F(1634, 3267), F(1633, 3267)]
        assert list(f(m.EJ_P4_P, list(m.EJ_P4_MU0), 2)) == [F(1, 4), F(1, 3), F(5, 12)]
    elif pagina == P5:
        texto = m.normalizar_caracteres(m.FRASE)
        tabla = m.tabla_desde_conteos(m.contar(texto, 1), m.ALFABETO)
        for semilla in (2033, 7):
            esperado = m.generar_desde(tabla, m.ALFABETO, "c", 50, random.Random(semilla))
            obtenido = ns["generar"](tabla, m.ALFABETO, "c", 50, random.Random(semilla))
            assert obtenido == esperado, semilla


@pytest.mark.parametrize("pagina", PAGINAS)
def test_los_bloques_python_caben_en_64_columnas(pagina):
    for codigo in _bloques_python(pagina):
        for linea in codigo.splitlines():
            assert len(linea) <= 64, (pagina, linea)
