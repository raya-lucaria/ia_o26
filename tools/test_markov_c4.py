"""Fija cada cifra de la clase 4 de Markov (course/8_markov/4_lo_que_no_se_ve/,
«Lo que no se ve»: modelo oculto y decidir sin ver) contra su funcion de
tools/markov.py, con el valor escrito a mano, y verifica cada algoritmo del
modelo oculto contra la enumeracion de todas las trayectorias (fuerza_bruta)
en los cuatro modelos: paraguas, helado, tres estados y lenguaje pequeño.

Ninguna prueba pide internet ni scipy.

Una correccion al plan (§3): con las señales (sin, con, sin, con) Viterbi da
sol, sol, sol, lluvia (169344/704647 ≈ 0.2403) y el mejor por dia del
suavizado sol, lluvia, sol, lluvia (139968/704647 ≈ 0.1986). El plan las
escribio al reves (lluvia-sol-sol-sol y lluvia-sol-lluvia-sol); las
probabilidades si coinciden. El dia 0 sin paraguas deja Pr(lluvia) en 0.15.
"""
from fractions import Fraction as F
from itertools import product

import pytest

import markov as m

LL, SOL = "lluvia", "sol"
C, N = "paraguas", "sin paraguas"
DET, SUS, VER = "determinante", "sustantivo", "verbo"

MODELOS = {
    "paraguas": m.paraguas,
    "helado": m.helado_eisner,
    "tres": m.hmm_tres_estados,
    "lenguaje": m.lenguaje_pequeno,
}

SECUENCIAS = {
    "paraguas": [[C], [N], [C, C], [N, C, N], [N, C, N, C], [C, C, N, C, C], [N, N, N, C]],
    "helado": [["tres helados"], ["tres helados", "un helado", "tres helados"],
               ["un helado", "dos helados", "tres helados", "dos helados"]],
    "tres": [[C], [C, N, C], [N, N, C, C], [C, C, C, N, N]],
    "lenguaje": [["casa"], ["casa", "la", "sopa"], ["la", "gata", "casa", "casa"],
                 ["casa", "casa", "casa"], ["la", "niña", "ve", "la", "casa"],
                 ["mi", "luna", "come"]],
}

CASOS = [(nombre, tuple(s)) for nombre, lista in SECUENCIAS.items() for s in lista]


def _norm(d):
    total = sum(d.values())
    return {k: v / total for k, v in d.items()}


# ---------------------------------------------------------- los modelos ---

@pytest.mark.parametrize("nombre", MODELOS)
def test_filas_suman_1(nombre):
    h = MODELOS[nombre]()
    assert sum(h["mu0"].values()) == 1
    for s in h["estados"]:
        assert list(h["P"][s]) == h["estados"]
        assert list(h["B"][s]) == h["señales"]
        assert sum(h["P"][s].values()) == 1
        assert sum(h["B"][s].values()) == 1
        assert all(isinstance(p, F) and p >= 0 for p in h["P"][s].values())
        assert all(isinstance(p, F) and p >= 0 for p in h["B"][s].values())


def test_paraguas_numeros():
    h = m.paraguas()
    assert h["estados"] == [LL, SOL] and h["señales"] == [C, N]
    assert h["mu0"] == {LL: F(1, 2), SOL: F(1, 2)}
    assert h["P"] == {LL: {LL: F(7, 10), SOL: F(3, 10)}, SOL: {LL: F(3, 10), SOL: F(7, 10)}}
    assert h["B"] == {LL: {C: F(9, 10), N: F(1, 10)}, SOL: {C: F(1, 5), N: F(4, 5)}}


def test_paraguas_todo_positivo_ninguna_secuencia_imposible():
    h = m.paraguas()
    assert all(p > 0 for s in h["estados"] for p in h["P"][s].values())
    assert all(p > 0 for s in h["estados"] for p in h["B"][s].values())
    for T in range(1, 6):
        for señales in product(h["señales"], repeat=T):
            assert all(p > 0 for p in m.fuerza_bruta(h, list(señales)).values())


def test_helado_es_2_por_3():
    h = m.helado_eisner()
    assert h["estados"] == ["calor", "frío"]
    assert h["señales"] == ["un helado", "dos helados", "tres helados"]
    assert h["mu0"] == {"calor": F(4, 5), "frío": F(1, 5)}
    assert h["P"]["calor"] == {"calor": F(3, 5), "frío": F(2, 5)}
    assert h["B"]["frío"] == {"un helado": F(1, 2), "dos helados": F(2, 5), "tres helados": F(1, 10)}


def test_tres_estados():
    h = m.hmm_tres_estados()
    assert h["estados"] == [SOL, "nublado", LL] and h["señales"] == [C, N]
    assert all(p > 0 for s in h["estados"] for p in h["P"][s].values())


# ----------------------------------------------------- lenguaje pequeño ---

def test_lenguaje_diseño():
    h = m.lenguaje_pequeno()
    assert h["estados"] == [DET, SUS, VER]
    assert len(h["señales"]) == len(set(h["señales"])) == 12
    assert h["mu0"] == {DET: F(1, 2), SUS: F(1, 4), VER: F(1, 4)}
    # «casa» la emiten el sustantivo y el verbo
    assert h["B"][SUS]["casa"] > 0 and h["B"][VER]["casa"] > 0 and h["B"][DET]["casa"] == 0
    # cada palabra la emite algun estado
    assert all(any(h["B"][s][o] > 0 for s in h["estados"]) for o in h["señales"])
    # los ceros estructurales de P
    ceros = [(s, t) for s in h["estados"] for t in h["estados"] if h["P"][s][t] == 0]
    assert ceros == [(DET, DET), (DET, VER), (SUS, SUS), (VER, VER)]


def test_parametros_lenguaje():
    assert m.parametros_lenguaje() == {
        "estados": 3, "palabras": 12,
        "celdas_hmm": 45, "celdas_bigramas": 144,
        "libres_hmm": 41, "libres_bigramas": 132,
    }


def test_lenguaje_tiene_trayectorias_imposibles_y_viterbi_las_evita():
    h = m.lenguaje_pequeno()
    vistas = 0
    for T in range(1, 5):
        for señales in product(h["señales"], repeat=T):
            señales = list(señales)
            if m.verosimilitud_hmm(h, señales) == 0:
                continue
            todas = m.fuerza_bruta(h, señales)
            vistas += sum(1 for p in todas.values() if p == 0)
            tray, p = m.viterbi(h, señales)
            assert p > 0 and m.probabilidad_conjunta(h, tray, señales) == p
    assert vistas > 0


def test_lenguaje_frases():
    h = m.lenguaje_pequeno()
    s = m.FRASES_EJ["casa-ambigua"]
    assert m.verosimilitud_hmm(h, s) == F(3, 1024)
    assert m.viterbi(h, s) == ([VER, DET, SUS], F(1, 512))
    assert m.posterior_trayectoria(h, [VER, DET, SUS], s) == F(2, 3)
    assert m.posterior_trayectoria(h, [SUS, DET, SUS], s) == F(1, 3)
    s = m.FRASES_EJ["sin-ambiguedad"]
    assert m.viterbi(h, s) == ([DET, SUS, VER, SUS], F(3, 2048))
    assert m.posterior_trayectoria(h, [DET, SUS, VER, SUS], s) == 1
    # el mejor por dia (empate 1/2-1/2 cada dia) arma una frase imposible
    s = m.FRASES_EJ["por-dia-imposible"]
    assert m.mejor_por_dia(h, s) == [SUS, SUS, SUS]
    assert m.probabilidad_conjunta(h, [SUS, SUS, SUS], s) == 0
    assert m.viterbi(h, s) == ([SUS, VER, SUS], F(3, 2048))


# ------------------------------------ algoritmos contra fuerza bruta ---

@pytest.mark.parametrize("nombre,señales", CASOS)
def test_verosimilitud_es_la_suma_de_todas(nombre, señales):
    h, s = MODELOS[nombre](), list(señales)
    assert m.verosimilitud_hmm(h, s) == sum(m.fuerza_bruta(h, s).values())


@pytest.mark.parametrize("nombre,señales", CASOS)
def test_conjunta_a_mano(nombre, señales):
    h, s = MODELOS[nombre](), list(señales)
    for tr, p in m.fuerza_bruta(h, s).items():
        esperado = h["mu0"][tr[0]] * h["B"][tr[0]][s[0]]
        for t in range(1, len(s)):
            esperado *= h["P"][tr[t - 1]][tr[t]] * h["B"][tr[t]][s[t]]
        assert p == esperado == m.probabilidad_conjunta(h, list(tr), s)


@pytest.mark.parametrize("nombre,señales", CASOS)
def test_filtrar_contra_enumeracion(nombre, señales):
    h, s = MODELOS[nombre](), list(señales)
    creencias = m.filtrar(h, s)
    assert len(creencias) == len(s)
    for t, b in enumerate(creencias):
        assert sum(b.values()) == 1
        marg = {e: F(0) for e in h["estados"]}
        for tr, p in m.fuerza_bruta(h, s[:t + 1]).items():
            marg[tr[t]] += p
        assert b == _norm(marg)


@pytest.mark.parametrize("nombre,señales", CASOS)
def test_suavizar_contra_enumeracion(nombre, señales):
    h, s = MODELOS[nombre](), list(señales)
    todas = m.fuerza_bruta(h, s)
    for t, g in enumerate(m.suavizar(h, s)):
        assert sum(g.values()) == 1
        marg = {e: F(0) for e in h["estados"]}
        for tr, p in todas.items():
            marg[tr[t]] += p
        assert g == _norm(marg)
    # el ultimo dia suavizado es el filtro
    assert m.suavizar(h, s)[-1] == m.filtrar(h, s)[-1]


@pytest.mark.parametrize("nombre,señales", CASOS)
def test_viterbi_es_el_argmax_de_la_conjunta(nombre, señales):
    h, s = MODELOS[nombre](), list(señales)
    todas = m.fuerza_bruta(h, s)
    tray, p = m.viterbi(h, s)
    assert p == max(todas.values())
    assert todas[tuple(tray)] == p
    assert m.posterior_trayectoria(h, tray, s) == p / sum(todas.values())


@pytest.mark.parametrize("nombre,señales", CASOS)
def test_posteriores_suman_1(nombre, señales):
    h, s = MODELOS[nombre](), list(señales)
    total = sum(m.posterior_trayectoria(h, list(tr), s) for tr in m.fuerza_bruta(h, s))
    assert total == 1


@pytest.mark.parametrize("nombre,señales", CASOS)
def test_mejor_por_dia_es_el_argmax_del_suavizado(nombre, señales):
    h, s = MODELOS[nombre](), list(señales)
    dias = m.mejor_por_dia(h, s)
    for e, g in zip(dias, m.suavizar(h, s)):
        assert g[e] == max(g.values())


@pytest.mark.parametrize("nombre,señales", CASOS)
def test_predecir_estado_y_señal_suman_1(nombre, señales):
    h, s = MODELOS[nombre](), list(señales)
    b = m.filtrar(h, s)[-1]
    pred = m.predecir_estado(h, b)
    assert sum(pred.values()) == 1
    sen = m.predecir_señal(h, b)
    assert list(sen) == h["señales"] and sum(sen.values()) == 1
    # predecir la señal es la verosimilitud de una señal mas, entre la de hoy
    for o, p in sen.items():
        assert p == m.verosimilitud_hmm(h, s + [o]) / m.verosimilitud_hmm(h, s)


def test_viterbi_empate_gana_el_primer_estado():
    h = m.paraguas()
    h["mu0"] = {LL: F(1, 2), SOL: F(1, 2)}
    h["B"] = {LL: {C: F(1, 2), N: F(1, 2)}, SOL: {C: F(1, 2), N: F(1, 2)}}
    assert m.viterbi(h, [C, C, C])[0] == [LL, LL, LL]


# --------------------------------------------------- cifras del paraguas ---

def test_filtrar_paraguas():
    b = m.filtrar(m.paraguas(), m.SEÑALES_EJ["filtrar"])
    assert b[0] == {LL: F(9, 11), SOL: F(2, 11)}
    assert b[1] == {LL: F(621, 703), SOL: F(82, 703)}
    assert f"{float(b[0][LL]):.3f}" == "0.818" and f"{float(b[1][LL]):.3f}" == "0.883"


def test_filtrar_paso_a_paso():
    h = m.paraguas()
    b0 = m.corregir(h, h["mu0"], C)
    assert b0 == {LL: F(9, 11), SOL: F(2, 11)}
    pred = m.predecir_estado(h, b0)
    assert pred == {LL: F(69, 110), SOL: F(41, 110)}
    assert m.corregir(h, pred, C) == {LL: F(621, 703), SOL: F(82, 703)}
    assert m.predecir_señal(h, b0) == {C: F(703, 1100), N: F(397, 1100)}


def test_verosimilitudes_paraguas():
    h = m.paraguas()
    assert m.verosimilitud_hmm(h, [C, C]) == F(703, 2000)
    assert m.verosimilitud_hmm(h, [N, C, N]) == F(15611, 200000)
    assert m.verosimilitud_hmm(h, [N, C, N, C]) == F(704647, 20000000)
    assert m.verosimilitud_hmm(h, [C, C, N, C, C]) == F(68607401, 2000000000)


def test_no_markov_paraguas():
    a, b = m.no_markov_paraguas()
    assert (a, b) == (F(46211, 70300), F(24089, 39700))
    assert f"{float(a):.3f}" == "0.657" and f"{float(b):.3f}" == "0.607"
    assert a != b


def test_viterbi_frente_a_mejor_por_dia_tres_dias():
    h, s = m.paraguas(), m.SEÑALES_EJ["viterbi"]
    assert s == [N, C, N]
    tray, p = m.viterbi(h, s)
    assert tray == [SOL, SOL, SOL] and p == F(392, 12500)
    assert m.posterior_trayectoria(h, tray, s) == F(6272, 15611)
    dias = m.mejor_por_dia(h, s)
    assert dias == [SOL, LL, SOL]
    assert m.posterior_trayectoria(h, dias, s) == F(5184, 15611)
    assert m.suavizar(h, s) == [
        {LL: F(2307, 15611), SOL: F(13304, 15611)},
        {LL: F(8649, 15611), SOL: F(6962, 15611)},
        {LL: F(2307, 15611), SOL: F(13304, 15611)}]
    assert [f"{float(m.posterior_trayectoria(h, x, s)):.4f}" for x in (tray, dias)] == ["0.4018", "0.3321"]


def test_viterbi_frente_a_mejor_por_dia_cuatro_dias():
    h, s = m.paraguas(), m.SEÑALES_EJ["viterbi-4"]
    assert s == [N, C, N, C]
    tray, p = m.viterbi(h, s)
    assert tray == [SOL, SOL, SOL, LL]
    assert m.posterior_trayectoria(h, tray, s) == F(169344, 704647)
    dias = m.mejor_por_dia(h, s)
    assert dias == [SOL, LL, SOL, LL]
    assert m.posterior_trayectoria(h, dias, s) == F(139968, 704647)
    assert [f"{float(m.posterior_trayectoria(h, x, s)):.4f}" for x in (tray, dias)] == ["0.2403", "0.1986"]


def test_viterbi_y_mejor_por_dia_coinciden():
    h, s = m.paraguas(), m.SEÑALES_EJ["coinciden"]
    assert s == [C, C, N, C, C]
    tray, _ = m.viterbi(h, s)
    assert tray == m.mejor_por_dia(h, s) == [LL, LL, SOL, LL, LL]
    assert m.posterior_trayectoria(h, tray, s) == F(23147208, 68607401)


def test_helado_y_tres_estados_cifras():
    e = m.helado_eisner()
    s = ["tres helados", "un helado", "tres helados"]
    assert m.viterbi(e, s) == (["calor", "frío", "calor"], F(8, 625))
    assert m.verosimilitud_hmm(e, s) == F(14281, 500000)
    t3 = m.hmm_tres_estados()
    s = [C, N, C]
    assert m.filtrar(t3, s)[0] == {SOL: F(1, 15), "nublado": F(1, 3), LL: F(3, 5)}
    assert m.viterbi(t3, s) == ([LL, "nublado", "nublado"], F(9, 800))
    assert m.mejor_por_dia(t3, s) == [LL, "nublado", LL]


# ------------------------------------------------------------- aprender ---

def test_contar_con_etiquetas():
    tray = [LL, LL, SOL, SOL, SOL, LL]
    obs = [C, C, N, C, N, C]
    P, B = m.contar_con_etiquetas([LL, SOL], [C, N], tray, obs)
    assert P == {LL: {LL: F(1, 2), SOL: F(1, 2)}, SOL: {LL: F(1, 3), SOL: F(2, 3)}}
    assert B == {LL: {C: F(1), N: F(0)}, SOL: {C: F(1, 3), N: F(2, 3)}}


def test_contar_fila_sin_datos_queda_en_ceros():
    P, _ = m.contar_con_etiquetas([LL, SOL], [C, N], [LL, LL], [C, C])
    assert P[SOL] == {LL: 0, SOL: 0}


@pytest.mark.parametrize("nombre", MODELOS)
def test_paso_em_no_baja_la_verosimilitud(nombre):
    h = MODELOS[nombre]()
    secuencias = [list(s) for s in SECUENCIAS[nombre]]
    nuevo, log_L = m.paso_em(h, secuencias)
    for s in nuevo["estados"]:
        assert sum(nuevo["P"][s].values()) == 1 and sum(nuevo["B"][s].values()) == 1
    assert sum(nuevo["mu0"].values()) == 1
    antes = 1
    despues = 1
    for s in secuencias:
        antes *= m.verosimilitud_hmm(h, s)
        despues *= m.verosimilitud_hmm(nuevo, s)
    assert despues >= antes
    _, log_L2 = m.paso_em(nuevo, secuencias)
    assert log_L2 >= log_L - 1e-12


# -------------------------------------------------------------- simular ---

def test_simular_semana():
    assert m.SEMILLAS["c4-simular-semana"] == 2045
    tray, obs = m.simular_hmm(m.paraguas(), 6, m.SEMILLAS["c4-simular-semana"])
    assert tray == [SOL, SOL, LL, LL, LL, LL, LL]
    assert obs == [N, N, C, C, C, C, N]
    assert (tray, obs) == m.simular_hmm(m.paraguas(), 6, 2045)


def test_generar_frase():
    assert m.SEMILLAS["c4-generar-frase"] == 2046
    h = m.lenguaje_pequeno()
    tray, obs = m.simular_hmm(h, 7, 2046)
    assert len(tray) == len(obs) == 8
    assert m.probabilidad_conjunta(h, tray, obs) > 0


def test_semillas_no_chocan():
    assert len(set(m.SEMILLAS.values())) == len(m.SEMILLAS)
    assert sum(1 for k in m.SEMILLAS if k.startswith("c4-")) == 2


# ------------------------------------------------------ decidir sin ver ---

def test_costos_del_juguete():
    assert (m.COSTO_PARAGUAS, m.COSTO_MOJARSE, m.COSTO_MIRAR) == (1, 4, F(1, 2))
    assert m.umbral_paraguas() == F(1, 4)
    assert m.rango_mirar() == (F(1, 6), F(1, 2))
    assert m.valor_informacion(F(1, 2)) == F(1, 2)
    assert m.costo_actuar(F(1, 2)) == 1 and m.costo_mirar(F(1, 2)) == 1


BARRIDO = [F(k, 600) for k in range(601)]


@pytest.mark.parametrize("b", BARRIDO[::7] + [F(1, 6), F(1, 4), F(1, 2)])
def test_formulas_de_costo(b):
    assert m.costo_actuar(b) == min(F(1), 4 * b)
    assert m.costo_mirar(b) == F(1, 2) + b
    assert m.valor_informacion(b) == min(F(1), 4 * b) - b
    assert m.valor_informacion(b) >= 0


def test_mirar_conviene_solo_entre_un_sexto_y_un_medio():
    lo, hi = m.rango_mirar()
    for b in BARRIDO:
        conviene = m.costo_mirar(b) < m.costo_actuar(b)
        assert conviene == (lo < b < hi), b
    # en las fronteras empata
    assert m.costo_mirar(lo) == m.costo_actuar(lo)
    assert m.costo_mirar(hi) == m.costo_actuar(hi)


def test_umbral_de_llevar():
    for b in BARRIDO:
        assert (4 * b > 1) == (b > m.umbral_paraguas())


def test_decidir():
    assert m.decidir(0) == "no llevar"
    assert m.decidir(F(1, 10)) == "no llevar"
    assert m.decidir(F(1, 6)) == "no llevar"          # empata con mirar: gana el primero
    assert m.decidir(F(1, 4)) == "mirar"
    assert m.decidir(F(1, 2)) == "llevar"             # empata con mirar
    assert m.decidir(F(9, 10)) == "llevar"
    for b in BARRIDO:
        c = {"llevar": 1, "no llevar": 4 * b, "mirar": F(1, 2) + b}
        assert c[m.decidir(b)] == min(c.values())
