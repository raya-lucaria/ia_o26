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
    """Dos convenciones con nombre: sin inicial (P + B; bigramas W²) y con
    inicial (mu0 o la primera palabra). Mezclarlas daba 45 frente a 144
    celdas pero 41 (con mu0) frente a 132 (sin) libres."""
    assert m.parametros_lenguaje() == {
        "estados": 3, "palabras": 12,
        "celdas_hmm": 45, "libres_hmm": 39,
        "celdas_hmm_con_inicial": 48, "libres_hmm_con_inicial": 41,
        "celdas_bigramas": 144, "libres_bigramas": 132,
        "celdas_bigramas_con_inicial": 156, "libres_bigramas_con_inicial": 143,
        "libres_hmm_con_ceros": 35, "libres_hmm_con_ceros_en_P_y_B": 12,
    }


def test_los_ceros_de_P_reducen_los_libres():
    """Con los 4 ceros estructurales de P, sus filas tienen 1, 2 y 2 celdas
    posibles: 0 + 1 + 1 = 2 libres en P en lugar de 3·2 = 6. Con B completa
    (3·11 = 33) el modelo tiene 35 libres, no 39; si tambien se cuentan los
    ceros de B (4, 5 y 4 palabras por estado: 3 + 4 + 3 = 10), 12."""
    h = m.lenguaje_pequeno()
    posibles = [sum(1 for p in h["P"][s].values() if p > 0) for s in h["estados"]]
    assert posibles == [1, 2, 2]
    assert sum(k - 1 for k in posibles) == 2
    q = m.parametros_lenguaje()
    assert q["libres_hmm"] - q["libres_hmm_con_ceros"] == 4


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


# ------------------------------------------------ evidencia imposible ---

def _degenerado():
    """mu0 = (1, 0), P y B identidad: la señal (x, y) es imposible."""
    return m._hmm(["a", "b"], ["x", "y"], [1, 0], [[1, 0], [0, 1]], [[1, 0], [0, 1]])


def test_evidencia_imposible():
    h, s = _degenerado(), ["x", "y"]
    assert m.verosimilitud_hmm(h, s) == 0                  # legitimo: vale 0
    assert all(p == 0 for p in m.fuerza_bruta(h, s).values())
    for f in (m.filtrar, m.suavizar, m.viterbi, m.mejor_por_dia):
        with pytest.raises(ValueError, match="señal imposible"):
            f(h, s)
    with pytest.raises(ValueError, match="señal imposible"):
        m.posterior_trayectoria(h, ["a", "b"], s)
    with pytest.raises(ValueError, match="señal imposible"):
        m.corregir(h, h["mu0"], "y")
    # lo posible del mismo modelo si funciona
    assert m.viterbi(h, ["x", "x"]) == (["a", "a"], 1)


def test_predecir_pide_una_creencia():
    h = m.paraguas()
    for f in (m.predecir_estado, m.predecir_señal):
        with pytest.raises(ValueError, match="creencia"):
            f(h, {LL: F(0), SOL: F(0)})


# ---------------------------------------------- empates de los umbrales ---

def test_empates_de_los_umbrales():
    """Orden de ACCIONES_DIA: llevar, no llevar, mirar."""
    assert m.ACCIONES_DIA == ("llevar", "no llevar", "mirar")
    c = m.costos_dia(F(1, 4))                  # llevar = no llevar = 1
    assert c == {"llevar": 1, "no llevar": 1, "mirar": F(3, 4)}
    assert m.decidir(F(1, 4)) == "mirar"       # mirar es mas barato aun
    c = m.costos_dia(F(1, 6))                  # mirar = actuar = 2/3
    assert c["mirar"] == m.costo_actuar(F(1, 6)) == c["no llevar"] == F(2, 3)
    assert m.decidir(F(1, 6)) == "no llevar"   # empate: no llevar va antes que mirar
    c = m.costos_dia(F(1, 2))                  # mirar = llevar = 1
    assert c["mirar"] == c["llevar"] == m.costo_actuar(F(1, 2)) == 1
    assert c["no llevar"] == 2
    assert m.decidir(F(1, 2)) == "llevar"      # empate: llevar va primero
    # sin la accion mirar, en b = 1/4 actuar cuesta 1 de las dos formas
    assert m.costo_actuar(F(1, 4)) == 1 and m.umbral_paraguas() == F(1, 4)


# ------------------------------------------- anclaje del par (camino, p) ---
# Cada caso fija en UNA comparacion la trayectoria con su probabilidad
# posterior: cambiar una sin la otra rompe la prueba.

def par_trayectoria_probabilidad(hmm, señales, metodo):
    tray = m.viterbi(hmm, señales)[0] if metodo == "viterbi" else m.mejor_por_dia(hmm, señales)
    return (tuple(tray), m.posterior_trayectoria(hmm, tray, señales))


PARES = [
    ("viterbi", "viterbi", ((SOL, SOL, SOL), F(6272, 15611))),
    ("viterbi", "por_dia", ((SOL, LL, SOL), F(5184, 15611))),
    ("viterbi-4", "viterbi", ((SOL, SOL, SOL, LL), F(169344, 704647))),
    ("viterbi-4", "por_dia", ((SOL, LL, SOL, LL), F(139968, 704647))),
    ("coinciden", "viterbi", ((LL, LL, SOL, LL, LL), F(23147208, 68607401))),
    ("coinciden", "por_dia", ((LL, LL, SOL, LL, LL), F(23147208, 68607401))),
]


@pytest.mark.parametrize("clave,metodo,par", PARES)
def test_par_trayectoria_probabilidad(clave, metodo, par):
    assert par_trayectoria_probabilidad(m.paraguas(), m.SEÑALES_EJ[clave], metodo) == par


def _mutaciones(par):
    tray, p = par
    otra = tuple(SOL if e == LL else LL for e in tray)
    return [
        (otra, p),                 # camino cambiado, misma probabilidad
        (tray, p + F(1, 10**6)),   # mismo camino, probabilidad cambiada
        (tray[::-1], p) if tray[::-1] != tray else (otra, p / 2),   # el error del plan: al reves
    ]


@pytest.mark.parametrize("clave,metodo,par", PARES)
def test_la_guarda_del_par_atrapa_tres_mutaciones(clave, metodo, par):
    real = par_trayectoria_probabilidad(m.paraguas(), m.SEÑALES_EJ[clave], metodo)
    for mutado in _mutaciones(par):
        assert mutado != real


# =================================== pagina 7: decidir, parametrizado ===
# Toda cifra de 7_decidir_sin_ver.md, escrita a mano, y cada funcion
# parametrizada verificada contra la ENUMERACION de los planes del dia (no
# contra su propia formula) y por barrido de Fractions.

ACC = ("llevar", "no llevar")


def _costo_estado(s, a, llevar, mojarse):
    """costo(s, a) de la tabla del dia: la unica fuente de las pruebas."""
    if a == "llevar":
        return F(llevar)
    return F(mojarse) if s == LL else F(0)


def _planes(b, llevar=1, mojarse=4, precio=F(1, 2)):
    """Los seis planes del dia, con su costo esperado sumando sobre el clima:
    llevar, no llevar, y mirar con cada una de las 2 x 2 reglas."""
    pr = {LL: F(b), SOL: 1 - F(b)}
    planes = {a: sum(pr[s] * _costo_estado(s, a, llevar, mojarse) for s in pr) for a in ACC}
    for regla in product(ACC, repeat=2):
        r = dict(zip((LL, SOL), regla))
        planes[("mirar",) + regla] = precio + sum(
            pr[s] * _costo_estado(s, r[s], llevar, mojarse) for s in pr)
    return planes


def _enumerado(b, llevar=1, mojarse=4, precio=F(1, 2)):
    """(actuar, mirar, info) por enumeracion de planes."""
    pl = _planes(b, llevar, mojarse, precio)
    actuar = min(pl[a] for a in ACC)
    mirar = min(v for k, v in pl.items() if k[0] == "mirar")
    gratis = min(v for k, v in _planes(b, llevar, mojarse, 0).items() if k[0] == "mirar")
    return actuar, mirar, actuar - gratis


COSTOS_PRUEBA = [(1, 4, F(1, 2)), (1, 3, F(1, 2)), (2, 5, F(1, 3)), (1, 4, F(3, 4)),
                 (1, 3, F(2, 3)), (1, 3, F(7, 10)), (1, 4, 0), (3, 7, F(1, 10))]
BARRIDO_FINO = sorted({F(k, n) for n in (60, 397, 420) for k in range(n + 1)})


def test_c7_parametrizadas_coinciden_con_el_juguete():
    for b in BARRIDO[::5] + [F(1, 6), F(1, 4), F(1, 2), F(9, 11), F(69, 397)]:
        assert m.costos_dia_con(b) == m.costos_dia(b)
        assert m.costo_actuar_con(b) == m.costo_actuar(b)
        assert m.costo_mirar_con(b) == m.costo_mirar(b)
        assert m.valor_informacion_con(b) == m.valor_informacion(b)
        assert m.decidir_con(b) == m.decidir(b)
    assert m.umbral_con() == m.umbral_paraguas() == F(1, 4)
    assert m.rango_mirar_con() == m.rango_mirar() == (F(1, 6), F(1, 2))


@pytest.mark.parametrize("llevar,mojarse,precio", COSTOS_PRUEBA)
def test_c7_parametrizadas_contra_la_enumeracion_de_planes(llevar, mojarse, precio):
    for b in BARRIDO_FINO:
        actuar, mirar, info = _enumerado(b, llevar, mojarse, precio)
        assert m.costo_actuar_con(b, llevar, mojarse) == actuar
        assert m.costo_mirar_con(b, llevar, precio) == mirar
        assert m.valor_informacion_con(b, llevar, mojarse) == info >= 0
        c = m.costos_dia_con(b, llevar, mojarse, precio)
        assert c["mirar"] == mirar and min(c["llevar"], c["no llevar"]) == actuar
        assert c[m.decidir_con(b, llevar, mojarse, precio)] == min(actuar, mirar)


@pytest.mark.parametrize("llevar,mojarse,precio", COSTOS_PRUEBA)
def test_c7_umbral_y_rango_por_barrido(llevar, mojarse, precio):
    u = m.umbral_con(llevar, mojarse)
    rango = m.rango_mirar_con(llevar, mojarse, precio)
    puntos = BARRIDO_FINO + [u] + (list(rango) if rango else [])
    for b in puntos:
        pl = _planes(b, llevar, mojarse, precio)
        assert (pl["llevar"] < pl["no llevar"]) == (b > u), b
        actuar, mirar, info = _enumerado(b, llevar, mojarse, precio)
        conviene = mirar < actuar
        assert conviene == (rango is not None and rango[0] < b < rango[1]), b
        assert conviene == (info > precio), b          # el teorema
    if rango:
        for borde in rango:                            # empate exacto en los bordes
            actuar, mirar, _ = _enumerado(borde, llevar, mojarse, precio)
            assert mirar == actuar
    # vacio justo cuando el precio alcanza el maximo de info
    _, vmax = m.maximo_informacion_con(llevar, mojarse)
    assert (rango is None) == (precio >= vmax)


@pytest.mark.parametrize("llevar,mojarse", [(1, 4), (1, 3), (2, 5), (3, 7)])
def test_c7_maximo_de_info_por_barrido(llevar, mojarse):
    bmax, vmax = m.maximo_informacion_con(llevar, mojarse)
    puntos = sorted(set(BARRIDO_FINO) | {bmax})
    mejor = max(_enumerado(b, llevar, mojarse)[2] for b in puntos)
    assert mejor == vmax == _enumerado(bmax, llevar, mojarse)[2]
    assert [b for b in puntos if _enumerado(b, llevar, mojarse)[2] == vmax] == [bmax]


def test_c7_costos_invalidos():
    for args in ((4, 1), (1, 1), (0, 4)):
        with pytest.raises(ValueError):
            m.umbral_con(*args)
    with pytest.raises(ValueError):
        m.rango_mirar_con(1, 4, -1)


def test_c7_cifras_del_juguete():
    """Secciones 1, 3 y 4 de la pagina 7, con los numeros escritos a mano."""
    # 1 · con el clima a la vista: b = 1/2 sin ver cuesta 1, viendo gratis 1/2
    assert m.costo_actuar_con(F(1, 2)) == 1 and m.valor_informacion_con(F(1, 2)) == F(1, 2)
    assert _planes(F(1, 2))["no llevar"] == 2
    # ejercicio «ver gratis»: b = 1/3 -> 1, 4/3, 1/3, ahorras 2/3
    assert _planes(F(1, 3))["no llevar"] == F(4, 3)
    assert m.costo_actuar_con(F(1, 3)) == 1 and m.valor_informacion_con(F(1, 3)) == F(2, 3)
    assert m.costo_mirar_con(F(1, 3), precio=0) == F(1, 3)
    # seis planes; la regla «llevar si llueve» gana en los dos climas
    assert len(_planes(F(1, 2))) == 6
    assert min((k for k in _planes(F(1, 2)) if k[0] == "mirar"),
               key=_planes(F(1, 2)).get) == ("mirar", "llevar", "no llevar")
    # 3 · umbral 1/4, empate en 1/4, b0 = 9/11 y 1/9
    assert m.umbral_con() == F(1, 4)
    assert m.costos_dia_con(F(1, 4))["llevar"] == m.costos_dia_con(F(1, 4))["no llevar"] == 1
    assert m.costos_dia_con(F(9, 11))["no llevar"] == F(36, 11)
    assert f"{float(F(36, 11)):.2f}" == "3.27"
    assert m.costo_actuar_con(F(1, 9)) == F(4, 9)
    # ejercicio: b1 = 69/397 -> no llevar, 276/397 ≈ 0.695
    assert F(69, 397) < F(1, 4) and m.costo_actuar_con(F(69, 397)) == F(276, 397)
    assert f"{float(F(276, 397)):.3f}" == "0.695" and f"{float(F(69, 397)):.3f}" == "0.174"
    # 4 · rango, empates, mirar en 1/4 y en 9/11
    assert m.rango_mirar_con() == (F(1, 6), F(1, 2))
    assert m.costos_dia_con(F(1, 6))["mirar"] == m.costos_dia_con(F(1, 6))["no llevar"] == F(2, 3)
    assert m.costos_dia_con(F(1, 2))["mirar"] == m.costos_dia_con(F(1, 2))["llevar"] == 1
    assert m.costos_dia_con(F(1, 4)) == {"llevar": 1, "no llevar": 1, "mirar": F(3, 4)}
    assert m.costo_mirar_con(F(9, 11)) == F(29, 22) and f"{float(F(29, 22)):.2f}" == "1.32"
    # info: 3/4 en 1/4, 1/2 en 1/6 y 1/2, 2/11 en 9/11; maximo 3/4 en 1/4
    assert [m.valor_informacion_con(b) for b in (F(1, 4), F(1, 6), F(1, 2), F(9, 11))] == \
        [F(3, 4), F(1, 2), F(1, 2), F(2, 11)]
    assert m.maximo_informacion_con() == (F(1, 4), F(3, 4))
    # ejemplo que cumple: b = 1/3, mirar 5/6 < 1, info 2/3 > 1/2
    assert m.costo_mirar_con(F(1, 3)) == F(5, 6) and m.valor_informacion_con(F(1, 3)) == F(2, 3)
    # ejercicio b = 1/5: 1, 4/5, 7/10 -> mirar; info 3/5 > 1/2
    assert m.costos_dia_con(F(1, 5)) == {"llevar": 1, "no llevar": F(4, 5), "mirar": F(7, 10)}
    assert m.decidir_con(F(1, 5)) == "mirar" and m.valor_informacion_con(F(1, 5)) == F(3, 5)


def test_c7_tabla_del_python():
    """La salida del bloque de Python de la seccion 4, fila por fila."""
    filas = {
        F(1, 9): (1, F(4, 9), F(11, 18), "no llevar"),
        F(1, 6): (1, F(2, 3), F(2, 3), "no llevar"),
        F(69, 397): (1, F(276, 397), F(535, 794), "mirar"),
        F(1, 4): (1, 1, F(3, 4), "mirar"),
        F(1, 2): (1, 2, 1, "llevar"),
        F(9, 11): (1, F(36, 11), F(29, 22), "llevar"),
    }
    for b, (ll, nl, mi, a) in filas.items():
        c = m.costos_dia_con(b)
        assert (c["llevar"], c["no llevar"], c["mirar"], m.decidir_con(b)) == (ll, nl, mi, a)
        pl = _planes(b)
        assert (pl["llevar"], pl["no llevar"]) == (ll, nl)
        assert min(v for k, v in pl.items() if k[0] == "mirar") == mi
    assert f"{float(F(535, 794)):.3f}" == "0.674"
    # 69/397 «apenas arriba de 1/6»
    assert F(1, 6) < F(69, 397) < F(1, 4)


def test_c7_el_filtro_da_las_creencias_que_usa_la_pagina():
    h = m.paraguas()
    assert m.filtrar(h, [C])[0][LL] == F(9, 11)
    assert m.filtrar(h, [N])[0][LL] == F(1, 9)
    assert m.filtrar(h, [C, N])[1][LL] == F(69, 397)
    # ejercicio «cuenta las creencias»: b0 toma 2 valores, b1 cuatro
    assert {m.filtrar(h, list(s))[-1][LL] for s in product([C, N], repeat=1)} == {F(9, 11), F(1, 9)}
    b1 = {m.filtrar(h, list(s))[-1][LL] for s in product([C, N], repeat=2)}
    assert b1 == {F(621, 703), F(69, 397), F(279, 397), F(31, 503)}
    for t in range(4):
        assert len({m.filtrar(h, list(s))[-1][LL] for s in product([C, N], repeat=t + 1)}) <= 2 ** (t + 1)


def test_c7_ventana_empañada():
    """El contraejemplo del teorema: b = 1/3, la ventana muestra la señal del
    paraguas con la B del juguete. Bayes y el total por enumeracion directa
    de las reglas «accion segun la señal», sin Bayes."""
    Bv = m.ventana_empañada()
    assert Bv == {LL: {C: F(9, 10), N: F(1, 10)}, SOL: {C: F(2, 10), N: F(8, 10)}}
    assert Bv == m.paraguas()["B"]
    total, d = m.costo_mirar_con_señal(F(1, 3), Bv)
    assert total == F(16, 15) > 1
    assert d == {
        C: {"prob": F(13, 30), "creencia": F(9, 13), "accion": "llevar", "costo": 1},
        N: {"prob": F(17, 30), "creencia": F(1, 17), "accion": "no llevar", "costo": F(4, 17)},
    }
    assert F(1, 2) + F(13, 30) + F(4, 30) == F(16, 15)
    # el teorema diria «mira» (info 2/3 > 1/2), pero aqui mirar pierde
    assert m.valor_informacion_con(F(1, 3)) == F(2, 3) > F(1, 2)
    assert total > m.costo_actuar_con(F(1, 3)) == 1
    # Bayes contra la conjunta
    pr = {LL: F(1, 3), SOL: F(2, 3)}
    for o in (C, N):
        conj = {s: pr[s] * Bv[s][o] for s in pr}
        assert d[o]["prob"] == sum(conj.values())
        assert d[o]["creencia"] == conj[LL] / sum(conj.values())


def _mirar_señal_enumerado(b, Bv, llevar, mojarse, precio):
    """precio + min sobre las 4 reglas (señal -> accion) del costo esperado,
    sumando sobre clima y señal: no usa Bayes."""
    pr = {LL: F(b), SOL: 1 - F(b)}
    señales = list(Bv[LL])
    mejor = None
    for regla in product(ACC, repeat=len(señales)):
        r = dict(zip(señales, regla))
        c = sum(pr[s] * Bv[s][o] * _costo_estado(s, r[o], llevar, mojarse)
                for s in pr for o in señales)
        mejor = c if mejor is None else min(mejor, c)
    return precio + mejor


VENTANAS = [
    m.ventana_empañada(),
    {LL: {C: F(1), N: F(0)}, SOL: {C: F(0), N: F(1)}},           # revela el clima
    {LL: {C: F(1, 2), N: F(1, 2)}, SOL: {C: F(1, 2), N: F(1, 2)}},   # no informa
    {LL: {C: F(3, 5), N: F(2, 5)}, SOL: {C: F(0), N: F(1)}},
]


@pytest.mark.parametrize("Bv", VENTANAS)
@pytest.mark.parametrize("llevar,mojarse,precio", [(1, 4, F(1, 2)), (1, 3, F(1, 2)), (2, 5, F(1, 10))])
def test_c7_mirar_con_señal_contra_las_reglas(Bv, llevar, mojarse, precio):
    for b in BARRIDO[::11] + [F(1, 3), F(1, 4), F(1, 6)]:
        total, d = m.costo_mirar_con_señal(b, Bv, llevar, mojarse, precio)
        assert total == _mirar_señal_enumerado(b, Bv, llevar, mojarse, precio)
        assert sum(x["prob"] for x in d.values()) == 1
        # ver solo una señal nunca vale mas que ver el clima
        assert total >= m.costo_mirar_con(b, llevar, precio)


def test_c7_ventana_que_revela_es_mirar_y_la_que_no_informa_es_actuar():
    revela, nada = VENTANAS[1], VENTANAS[2]
    for b in BARRIDO[::13]:
        assert m.costo_mirar_con_señal(b, revela)[0] == m.costo_mirar_con(b)
        assert m.costo_mirar_con_señal(b, nada)[0] == F(1, 2) + m.costo_actuar_con(b)


def test_c7_ejercicio_mojarse_cuesta_3():
    """Respuesta del ejercicio final, punto por punto."""
    # 1 · costos
    for b in BARRIDO[::9]:
        assert m.costos_dia_con(b, 1, 3) == {"llevar": 1, "no llevar": 3 * b, "mirar": F(1, 2) + b}
    # 2 · umbral 1/3; ahi llevar = no llevar = 1, mirar 5/6 y gana
    assert m.umbral_con(1, 3) == F(1, 3)
    assert m.costos_dia_con(F(1, 3), 1, 3) == {"llevar": 1, "no llevar": 1, "mirar": F(5, 6)}
    assert m.decidir_con(F(1, 3), 1, 3) == "mirar"
    # 3 · rango (1/4, 1/2); empates 3/4 en 1/4 y 1 en 1/2
    assert m.rango_mirar_con(1, 3) == (F(1, 4), F(1, 2))
    c = m.costos_dia_con(F(1, 4), 1, 3)
    assert c["mirar"] == c["no llevar"] == F(3, 4)
    c = m.costos_dia_con(F(1, 2), 1, 3)
    assert c["mirar"] == c["llevar"] == 1
    # 4 · las formulas generales recuperan 1/4 y (1/6, 1/2)
    assert (m.umbral_con(1, 4), m.rango_mirar_con(1, 4, F(1, 2))) == (F(1, 4), (F(1, 6), F(1, 2)))
    # 5 · info = min(1, 3b) - b: 2b hasta 1/3, 1 - b despues; maximo 2/3 en 1/3
    for b in BARRIDO:
        assert m.valor_informacion_con(b, 1, 3) == (2 * b if b <= F(1, 3) else 1 - b)
    assert m.maximo_informacion_con(1, 3) == (F(1, 3), F(2, 3))
    # desde precio 2/3 mirar nunca gana estrictamente
    assert m.rango_mirar_con(1, 3, F(2, 3)) is None
    assert m.rango_mirar_con(1, 3, F(2, 3) - F(1, 1000)) is not None
    # la salida del bloque de Python: b, 1, 3b, 1/2 + b, info
    salida = [(F(1, 4), 1, F(3, 4), F(3, 4), F(1, 2)),
              (F(1, 3), 1, 1, F(5, 6), F(2, 3)),
              (F(1, 2), 1, F(3, 2), 1, F(1, 2))]
    for b, ll, nl, mi, inf in salida:
        c = m.costos_dia_con(b, 1, 3)
        assert (c["llevar"], c["no llevar"], c["mirar"], m.valor_informacion_con(b, 1, 3)) == (ll, nl, mi, inf)


# =========================== paginas 3 a 6: cifras que faltaban fijar ===

def test_c3_evidencias():
    h = m.paraguas()
    ev = m.evidencias(h, [C, C, N])
    assert ev == [F(11, 20), F(703, 1100), F(24089, 70300)]
    assert ev[0] * ev[1] * ev[2] == F(24089, 200000) == m.verosimilitud_hmm(h, [C, C, N])
    assert m.evidencias(h, [N, C]) == [F(9, 20), F(397, 900)]
    assert F(9, 20) * F(397, 900) == F(397, 2000) == m.verosimilitud_hmm(h, [N, C])
    # predecir desde b0 = 1/9: lluvia 31/90; señal de mañana 703/1100 y 397/1100
    assert m.predecir_estado(h, m.filtrar(h, [N])[0])[LL] == F(31, 90)
    assert m.predecir_estado(h, m.filtrar(h, [C, C])[1])[LL] == F(4593, 7030)
    assert m.filtrar(h, [C, C, N])[2][LL] == F(4593, 24089)


@pytest.mark.parametrize("nombre,señales", CASOS)
def test_c3_evidencias_son_cocientes_de_verosimilitudes(nombre, señales):
    h, s = MODELOS[nombre](), list(señales)
    ev = m.evidencias(h, s)
    for t in range(len(s)):
        previa = m.verosimilitud_hmm(h, s[:t]) if t else 1
        assert ev[t] == sum(m.fuerza_bruta(h, s[:t + 1]).values()) / previa


def test_c3_evidencia_imposible():
    with pytest.raises(ValueError, match="señal imposible"):
        m.evidencias(_degenerado(), ["x", "y"])


def test_c3_semana_simulada_dia_6():
    h = m.paraguas()
    tray, obs = m.simular_hmm(h, 6, m.SEMILLAS["c4-simular-semana"])
    assert tray[6] == LL
    b6 = m.filtrar(h, obs)[6][LL]
    assert f"{float(b6):.3f}" == "0.194" and f"{float(1 - b6):.3f}" == "0.806"


def test_c3_dos_inicios_opuestos():
    s = [C, C, N, C, C]

    def desde(mu):
        h = m.paraguas()
        h["mu0"] = {LL: F(mu[0]), SOL: F(mu[1])}
        return [b[LL] for b in m.filtrar(h, s)]
    lluvia, sol, medio = desde((1, 0)), desde((0, 1)), desde((F(1, 2), F(1, 2)))
    assert lluvia[:2] == [1, F(21, 23)] and sol[:2] == [0, F(27, 41)]
    assert [f"{float(x):.3f}" for x in lluvia] == ["1.000", "0.913", "0.199", "0.734", "0.868"]
    assert [f"{float(x):.3f}" for x in sol] == ["0.000", "0.659", "0.139", "0.713", "0.864"]
    assert f"{float(lluvia[4] - sol[4]):.3f}" == "0.004"
    assert sol[4] < medio[4] < lluvia[4] and f"{float(medio[4]):.3f}" == "0.867"


def test_c3_identidad_con_filas_iguales_no_olvida():
    h = m._hmm([LL, SOL], [C, N], [F(1, 3), F(2, 3)], [[1, 0], [0, 1]],
               [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]])
    for b in m.filtrar(h, [C, N, C, C]):
        assert b == h["mu0"]


def test_c3_tres_climas():
    t3 = m.hmm_tres_estados()
    NU = "nublado"
    b0 = m.filtrar(t3, [C, C])[0]
    assert b0 == {SOL: F(1, 15), NU: F(1, 3), LL: F(3, 5)}
    assert m.predecir_estado(t3, b0) == {SOL: F(11, 60), NU: F(11, 30), LL: F(9, 20)}
    b1 = m.filtrar(t3, [C, C])[1]
    assert b1 == {SOL: F(11, 364), NU: F(55, 182), LL: F(243, 364)}
    assert [f"{float(b1[s]):.3f}" for s in (SOL, NU, LL)] == ["0.030", "0.302", "0.668"]
    assert m.evidencias(t3, [C, C]) == [F(1, 2), F(91, 150)]
    assert m.verosimilitud_hmm(t3, [C, C]) == F(91, 300)


def test_c4_suavizado_tabla():
    """Tabla «adelante, atras y el suavizado de lluvia»: adelante y atras
    son, por definicion, sumas de conjuntas de trayectorias; se comprueban
    asi, sin las recurrencias."""
    h, s = m.paraguas(), [N, C, N]
    todas = m.fuerza_bruta(h, s)
    adelante = [{LL: F(1, 20), SOL: F(2, 5)}, {LL: F(279, 2000), SOL: F(59, 1000)},
                {LL: F(2307, 200000), SOL: F(1663, 25000)}]
    atras = [{LL: F(2307, 10000), SOL: F(1663, 10000)}, {LL: F(31, 100), SOL: F(59, 100)},
             {LL: F(1), SOL: F(1)}]
    for t in range(3):
        for e in (LL, SOL):
            pref = sum(p for tr, p in m.fuerza_bruta(h, s[:t + 1]).items() if tr[t] == e)
            assert pref == adelante[t][e]
            conj = sum(p for tr, p in todas.items() if tr[t] == e)
            assert conj == adelante[t][e] * atras[t][e]
    assert F(279, 2000) * F(31, 100) + F(59, 1000) * F(59, 100) == F(15611, 200000)
    assert m.filtrar(h, s)[1][LL] == F(279, 397) and f"{float(F(279, 397)):.3f}" == "0.703"
    assert [f"{float(g[e]):.3f}" for g, e in zip(m.suavizar(h, s), (SOL, LL, SOL))] == \
        ["0.852", "0.554", "0.852"]


def test_c4_fuerza_bruta_y_marginal():
    h, s = m.paraguas(), [N, C, N]
    todas = m.fuerza_bruta(h, s)
    top = sorted(todas.items(), key=lambda kv: kv[1], reverse=True)[:3]
    assert top == [((SOL, SOL, SOL), F(98, 3125)), ((SOL, LL, SOL), F(81, 3125)),
                   ((LL, LL, SOL), F(189, 25000))]
    assert F(98, 3125) == F(392, 12500)
    assert todas[(SOL, LL, LL)] == F(189, 25000) and todas[(LL, LL, LL)] == F(441, 200000)
    marg = sum(p for tr, p in todas.items() if tr[1] == LL)
    assert marg == F(8649, 200000) and marg / F(15611, 200000) == F(8649, 15611)


def test_c4_reticula_de_viterbi():
    h = m.paraguas()
    col = m.columnas_viterbi(h, [N, C, N])
    assert col == [{LL: (F(1, 20), None), SOL: (F(2, 5), None)},
                   {LL: (F(27, 250), SOL), SOL: (F(7, 125), SOL)},
                   {LL: (F(189, 25000), LL), SOL: (F(98, 3125), SOL)}]
    # ejercicio «dos paraguas»: 9/20 y 1/10; 567/2000 y 27/1000, ambos desde lluvia
    assert m.columnas_viterbi(h, [C, C]) == [
        {LL: (F(9, 20), None), SOL: (F(1, 10), None)},
        {LL: (F(567, 2000), LL), SOL: (F(27, 1000), LL)}]
    assert m.viterbi(h, [C, C]) == ([LL, LL], F(567, 2000))
    # helado (tres, uno, tres)
    e = m.helado_eisner()
    col = m.columnas_viterbi(e, ["tres helados", "un helado", "tres helados"])
    assert col == [{"calor": (F(8, 25), None), "frío": (F(1, 50), None)},
                   {"calor": (F(24, 625), "calor"), "frío": (F(8, 125), "calor")},
                   {"calor": (F(8, 625), "frío"), "frío": (F(2, 625), "frío")}]


@pytest.mark.parametrize("nombre,señales", CASOS)
def test_c4_reticula_contra_fuerza_bruta(nombre, señales):
    """mejor_t(s) = max de la conjunta de los prefijos que acaban en s."""
    h, s = MODELOS[nombre](), list(señales)
    col = m.columnas_viterbi(h, s)
    for t in range(len(s)):
        pref = m.fuerza_bruta(h, s[:t + 1])
        for e in h["estados"]:
            assert col[t][e][0] == max([p for tr, p in pref.items() if tr[t] == e], default=0)
    assert max(v for v, _ in col[-1].values()) == m.viterbi(h, s)[1]


def test_c4_helado_suavizado():
    e = m.helado_eisner()
    s = ["tres helados", "un helado", "tres helados"]
    assert [g["frío"] for g in m.suavizar(e, s)] == [F(905, 14281), F(8625, 14281), F(2533, 14281)]
    assert m.mejor_por_dia(e, s) == ["calor", "frío", "calor"] == m.viterbi(e, s)[0]


def test_c5_semana_anotada():
    tray, obs = m.simular_hmm(m.paraguas(), 6, m.SEMILLAS["c4-simular-semana"])
    P, B = m.contar_con_etiquetas([LL, SOL], [C, N], tray, obs)
    assert P == {LL: {LL: 1, SOL: 0}, SOL: {LL: F(1, 2), SOL: F(1, 2)}}
    assert B == {LL: {C: F(4, 5), N: F(1, 5)}, SOL: {C: 0, N: 1}}
    # contraejemplo: los dias 2 a 6, la fila de sol queda en ceros
    P, B = m.contar_con_etiquetas([LL, SOL], [C, N], tray[2:], obs[2:])
    assert P == {LL: {LL: 1, SOL: 0}, SOL: {LL: 0, SOL: 0}}
    assert B[SOL] == {C: 0, N: 0}


def test_c5_paso_a_mano():
    h, s = m.paraguas(), [C, N]
    todas = m.fuerza_bruta(h, s)
    assert todas == {(LL, LL): F(63, 2000), (LL, SOL): F(216, 2000),
                     (SOL, LL): F(6, 2000), (SOL, SOL): F(112, 2000)}
    L = sum(todas.values())
    assert L == F(397, 2000)
    assert [todas[k] / L for k in todas] == [F(63, 397), F(216, 397), F(6, 397), F(112, 397)]
    g = m.suavizar(h, s)
    assert g[0][LL] == F(279, 397) and g[1] == {LL: F(69, 397), SOL: F(328, 397)}
    nuevo, logL = m.paso_em(h, [s])
    assert nuevo["P"] == {LL: {LL: F(7, 31), SOL: F(24, 31)}, SOL: {LL: F(3, 59), SOL: F(56, 59)}}
    assert nuevo["B"] == {LL: {C: F(93, 116), N: F(23, 116)}, SOL: {C: F(59, 223), N: F(164, 223)}}
    assert nuevo["mu0"] == {LL: F(279, 397), SOL: F(118, 397)}
    assert f"{logL:.3f}" == "-1.617"


def test_c5_iteraciones():
    Ls = m.iterar_em(m.paraguas(), [[C, N]], 4)
    assert Ls[:2] == [F(397, 2000), F(268802881, 669153424)]
    assert [f"{float(x):.3f}" for x in Ls] == ["0.199", "0.402", "0.666", "0.943", "0.999"]
    import math
    assert [f"{math.log(x):.3f}" for x in Ls[:2]] == ["-1.617", "-0.912"]
    assert all(a <= b for a, b in zip(Ls, Ls[1:]))


def test_c5_filas_iguales_y_nombres_intercambiados():
    h = m.paraguas()
    h["B"] = {LL: {C: F(1, 2), N: F(1, 2)}, SOL: {C: F(1, 2), N: F(1, 2)}}
    todas = m.fuerza_bruta(h, [C, N])
    L = m.verosimilitud_hmm(h, [C, N])
    assert L == F(1, 4)
    assert [todas[k] / L for k in todas] == [F(7, 20), F(3, 20), F(3, 20), F(7, 20)]
    assert m.paso_em(h, [[C, N]])[0] == h
    # intercambiar las filas de B intercambia lluvia y sol en el resultado
    j = m.paraguas()
    j["B"] = {LL: dict(m.paraguas()["B"][SOL]), SOL: dict(m.paraguas()["B"][LL])}
    a, b = m.paso_em(m.paraguas(), [[C, N]])[0], m.paso_em(j, [[C, N]])[0]
    otro = {LL: SOL, SOL: LL}
    assert all(b["B"][otro[s]] == a["B"][s] and b["mu0"][otro[s]] == a["mu0"][s] for s in (LL, SOL))
    assert all(b["P"][otro[s]][otro[t]] == a["P"][s][t] for s in (LL, SOL) for t in (LL, SOL))


def test_c5_helado_con_etiquetas():
    H, FR = "calor", "frío"
    U, D, T = "un helado", "dos helados", "tres helados"
    P, B = m.contar_con_etiquetas([H, FR], [U, D, T], [H, H, FR, FR, H, H], [T, D, U, D, T, T])
    assert P == {H: {H: F(2, 3), FR: F(1, 3)}, FR: {H: F(1, 2), FR: F(1, 2)}}
    assert B == {H: {U: 0, D: F(1, 4), T: F(3, 4)}, FR: {U: F(1, 2), D: F(1, 2), T: 0}}
    P, B = m.contar_con_etiquetas([H, FR], [U, D, T], [H, H, H, FR], [D, T, T, U])
    assert P == {H: {H: F(2, 3), FR: F(1, 3)}, FR: {H: 0, FR: 0}}
    assert B[FR] == {U: 1, D: 0, T: 0}


def test_c6_lenguaje_predicciones():
    h = m.lenguaje_pequeno()
    sig = m.predecir_señal(h, m.filtrar(h, ["la", "gata"])[-1])
    assert {o: p for o, p in sig.items() if p} == {
        "come": F(3, 16), "ve": F(3, 16), "duerme": F(3, 16), "casa": F(3, 16),
        "la": F(1, 8), "una": F(1, 16), "esta": F(1, 32), "mi": F(1, 32)}
    tabla = {"casa": (F(1, 2), F(1, 2)), "la casa": (1, 0), "la gata casa": (0, 1),
             "casa casa": (F(2, 5), F(3, 5))}
    for frase, (su, ve) in tabla.items():
        b = m.filtrar(h, frase.split())[-1]
        assert (b[SUS], b[VER], b[DET]) == (su, ve, 0)
    # tras «la gata casa»: la 1/4, una 1/8, esta y mi 1/16; niña, gata, casa 1/8; sopa, luna 1/16
    sig = m.predecir_señal(h, m.filtrar(h, ["la", "gata", "casa"])[-1])
    assert {o: p for o, p in sig.items() if p} == {
        "la": F(1, 4), "una": F(1, 8), "esta": F(1, 16), "mi": F(1, 16),
        "niña": F(1, 8), "gata": F(1, 8), "casa": F(1, 8), "sopa": F(1, 16), "luna": F(1, 16)}
    # «la» tras «casa» 3/16
    assert m.predecir_señal(h, m.filtrar(h, ["casa"])[-1])["la"] == F(3, 16)
    # tras «mi»: niña, gata, casa 1/4; sopa, luna 1/8
    sig = m.predecir_señal(h, m.filtrar(h, ["mi"])[-1])
    assert {o: p for o, p in sig.items() if p} == {
        "niña": F(1, 4), "gata": F(1, 4), "casa": F(1, 4), "sopa": F(1, 8), "luna": F(1, 8)}


def test_c6_lenguaje_frases_y_ceros():
    h = m.lenguaje_pequeno()
    assert m.simular_hmm(h, 7, 2046)[1] == "casa casa la gata come niña duerme esta".split()
    assert m.simular_hmm(h, 7, 2046)[0] == [SUS, VER, DET, SUS, VER, SUS, VER, DET]
    assert m.probabilidad_conjunta(h, [DET, SUS, VER, DET, SUS], "mi luna come la casa".split()) == F(3, 32768)
    assert m.probabilidad_conjunta(h, [VER, DET, SUS], ["casa", "la", "sopa"]) == F(1, 512)
    assert m.probabilidad_conjunta(h, [SUS, DET, SUS], ["casa", "la", "sopa"]) == F(1, 1024)
    ccc = ["casa"] * 3
    assert all(g == {DET: 0, SUS: F(1, 2), VER: F(1, 2)} for g in m.suavizar(h, ccc))
    assert m.filtrar(h, ccc)[1][SUS] == F(2, 5)
    assert m.probabilidad_conjunta(h, [VER, SUS, VER], ccc) == F(3, 2048)
    for frase in (["la", "la"], ["la", "come"]):
        assert m.verosimilitud_hmm(h, frase) == 0
        with pytest.raises(ValueError, match="señal imposible"):
            m.filtrar(h, frase)
        assert m.filtrar(h, frase[:1])[0][DET] == 1


def test_c6_verbo_tras_verbo():
    g = m.lenguaje_verbo_tras_verbo()
    assert sum(g["P"][VER].values()) == 1
    ceros = [(s, t) for s in g["estados"] for t in g["estados"] if g["P"][s][t] == 0]
    assert ceros == [(DET, DET), (DET, VER), (SUS, SUS)]
    assert m.libres_reales(m.lenguaje_pequeno()) == 35 == m.parametros_lenguaje()["libres_hmm_con_ceros"]
    assert m.libres_reales(g) == 36
    assert m.verosimilitud_hmm(m.lenguaje_pequeno(), ["come", "ve"]) == 0
    assert m.verosimilitud_hmm(g, ["come", "ve"]) == F(1, 640)
    ccc = ["casa"] * 3
    todas = m.fuerza_bruta(g, ccc)
    L = sum(todas.values())
    assert L == F(161, 51200) == m.verosimilitud_hmm(g, ccc)
    tray, p = m.viterbi(g, ccc)
    assert (tray, p) == ([SUS, VER, SUS], F(27, 20480)) and p == max(todas.values())
    assert p / L == F(135, 322) and f"{float(p / L):.3f}" == "0.419"
    dias = m.mejor_por_dia(g, ccc)
    assert dias == [SUS, VER, VER]
    assert todas[tuple(dias)] == F(3, 10240) and todas[tuple(dias)] / L == F(15, 161)
    assert f"{float(F(15, 161)):.3f}" == "0.093"


def test_c8_pasillo_q_estrella():
    j = m.pasillo()
    V = {1: F(-5), 2: F(-2)}
    assert m.cumple_bellman(j, V)
    assert m.q_valor(j, V, 1, m.CAMINAR) == V[1] == -5
    assert m.q_valor(j, V, 1, m.CORRER) < -5


def test_c4_helado_paraguas():
    """Ejercicio final de la pagina 4: mu0 y P del paraguas, B del helado,
    diario (uno, tres, uno). Todo contra fuerza bruta y a mano."""
    H, FR = "calor", "frío"
    U, D, T = "un helado", "dos helados", "tres helados"
    h = m.helado_paraguas()
    assert h["estados"] == [H, FR] and h["señales"] == [U, D, T]
    assert h["mu0"] == {H: F(1, 2), FR: F(1, 2)}
    assert h["P"] == {H: {H: F(7, 10), FR: F(3, 10)}, FR: {H: F(3, 10), FR: F(7, 10)}}
    assert h["B"] == {H: {U: F(1, 5), D: F(2, 5), T: F(2, 5)},
                      FR: {U: F(1, 2), D: F(2, 5), T: F(1, 10)}}
    assert m.helado_eisner()["mu0"] == {H: F(4, 5), FR: F(1, 5)}     # la de la pagina 2 sigue igual
    s = [U, T, U]
    todas = m.fuerza_bruta(h, s)
    L = sum(todas.values())
    # reticula: 1/10, 1/4; 3/100 (desde frio), 7/400 (desde frio); 21/5000 (desde calor), 49/8000 (desde frio)
    assert m.columnas_viterbi(h, s) == [
        {H: (F(1, 10), None), FR: (F(1, 4), None)},
        {H: (F(3, 100), FR), FR: (F(7, 400), FR)},
        {H: (F(21, 5000), H), FR: (F(49, 8000), FR)}]
    assert F(3, 100) > F(7, 400)                  # calor va adelante el dia 1
    # Viterbi: frio, frio, frio con 49/8000 > 21/5000
    assert m.viterbi(h, s) == ([FR, FR, FR], F(49, 8000))
    assert max(todas.values()) == todas[(FR, FR, FR)] == F(49, 8000) > F(21, 5000)
    # suavizado de calor 374/1009, 3364/5045, 374/1009; calor gana solo el dia 1
    g = m.suavizar(h, s)
    assert [x[H] for x in g] == [F(374, 1009), F(3364, 5045), F(374, 1009)]
    for t in range(3):
        assert g[t][H] == sum(p for tr, p in todas.items() if tr[t] == H) / L
    assert F(3364, 5045) > F(1, 2) > F(374, 1009)
    # mejor por dia: frio, calor, frio con conjunta 9/2000 < 49/8000
    assert m.mejor_por_dia(h, s) == [FR, H, FR]
    assert todas[(FR, H, FR)] == F(1, 2) * F(1, 2) * F(3, 10) * F(2, 5) * F(3, 10) * F(1, 2) == F(9, 2000)
    assert F(9, 2000) < F(49, 8000)
