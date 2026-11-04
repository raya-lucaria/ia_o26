# Notebook 07 de la unidad 9 · El lagrangeano en acción (acompaña
# ml-lagrangeano-en-accion, clase 3). Código y orden de celdas: prog-c3
# (clase_3.md §10.3.2). El texto de cada celda [texto] vive en
# 07_el_lagrangeano_en_accion.texto.md (guion de Codex). Los procesos son los
# de tools/ml_cifras_c3.py (datos_regiones, datos_entregas_curvas,
# datos_muchas): las cifras que cita la página salen de ahí. Solo la celda
# bloque-5-prueba lee la prueba (contrato §6.6 regla 8).

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo] bloque-1-juega
#@title Juega: restringir es penalizar
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SEMILLA = 0
DATOS_B1 = ml.proceso(n=334, x={"x1": ml.normal(), "x2": ml.normal()},
                      f=lambda d: 0.3 * d.x1 + 1.5 * d.x2,
                      correlacion={("x1", "x2"): 0.5}, semilla=SEMILLA)  # 200 de ent
PHI_B1 = ml.estandarizar(ml.columnas("x1", "x2"))
MC_B1 = ml.ajustar(DATOS_B1, phi=PHI_B1).beta_gorro[["x1", "x2"]]
OMEGA = {"l2": (MC_B1 ** 2).sum(), "l1": MC_B1.abs().sum(),
         "elastica": 0.5 * MC_B1.abs().sum() + 0.5 * (MC_B1 ** 2).sum()}


def bloque_1(region, fraccion, mostrar_mu, curva):
    d = fraccion * OMEGA[region]                # el presupuesto, siempre > 0
    fig, ejes = plt.subplots(1, 2 if curva else 1, figsize=(11 if curva else 5.5, 5))
    a1 = ejes[0] if curva else ejes
    ml.dibujar_regiones(DATOS_B1, PHI_B1, region, d, mostrar_mu=mostrar_mu, ax=a1)
    if curva:                                   # 40 presupuestos > 0, sin el 0
        ds = np.linspace(0.05, 1.2, 40) * OMEGA[region]
        ml.dibujar_presupuesto(DATOS_B1, PHI_B1, region, ds, d_marcado=d, ax=ejes[1])
    plt.show()
    beta, mu = ml.optimo_restringido(DATOS_B1, PHI_B1, region, d)
    print(f"d = {d:.3f} · β̂ = ({beta['x1']:.3f}, {beta['x2']:.3f}) · μ = {mu:.3f}")


ml.laboratorio(
    bloque_1,
    region=ml.selector("región Ω ≤ d", {"disco (ridge)": "l2",
                                        "diamante (lasso)": "l1",
                                        "red elástica, ρ = 0.5": "elastica"}, "l1"),
    fraccion=ml.deslizador("presupuesto d, como fracción de Ω sin penalizar",
                           0.05, 1.2, 0.05, 0.5),
    mostrar_mu=ml.interruptor("mostrar μ", True),
    curva=ml.interruptor("ver la curva del presupuesto: mejor L_ent contra d", False),
)

# %% [texto] bloque-1-mira

# %% [texto] bloque-1-explica

# %% [texto] bloque-2-predice

# %% [codigo] bloque-2-juega
#@title Juega: encoger o anular
rng = np.random.default_rng(0)
X_B2 = rng.normal(size=200)
X_B2 = (X_B2 - X_B2.mean()) / np.sqrt(np.mean((X_B2 - X_B2.mean()) ** 2))
U_B2 = rng.normal(size=200)
U_B2 = U_B2 - U_B2.mean() - np.mean(U_B2 * X_B2) * X_B2   # ⟂ a la constante y a x


def bloque_2(b, mu, penalizacion):
    ml.dibujar_encoger_1d(vista="solucion", mu=mu)
    beta = ml.encoger_1d(b, mu, penalizacion)
    plt.plot([b], [beta], "o", ms=10, color="black", label="tu b")
    plt.legend(); plt.show()
    df = pd.DataFrame({"x": X_B2, "y": b * X_B2 + U_B2})   # (1/n)Σx² = 1, b exacta
    m = ml.ajustar(df, phi=ml.columnas("x"), mu=mu, penalizacion=penalizacion,
                   columnas_x=["x"], tarea="regresion")
    print(f"encoger_1d({b:.1f}, μ = {mu:.1f}) = {beta:.6f}")
    print(f"ajustar con datos de esa b    = {m.beta_gorro['x']:.6f}")


ml.laboratorio(
    bloque_2,
    b=ml.deslizador("b: pendiente sin penalizar", -3.0, 3.0, 0.1, 0.4),
    mu=ml.deslizador("μ", 0.0, 3.0, 0.1, 1.0),
    penalizacion=ml.selector("penalización",
                             {"ridge": "l2", "lasso": "l1",
                              "red elástica, ρ = 0.5": "elastica"}, "l1"),
)

# %% [texto] bloque-2-mira

# %% [texto] bloque-2-explica

# %% [texto] bloque-3-predice

# %% [codigo] bloque-3-juega
#@title Juega: grado 12 con μ, las entregas de la clase 2
PHI_B3 = ml.estandarizar(ml.polinomio(12, escalar=True))
MUS_B3 = [float(m) for m in np.logspace(-6, 2, 17)]
CAND_B3 = {m: (lambda df, m=m: ml.ajustar(df, phi=PHI_B3, mu=m, penalizacion="l2"))
           for m in MUS_B3}
_DATOS_B3, _U_B3 = {}, {}


def bloque_3(log_mu, semilla, que):
    if semilla not in _DATOS_B3:                # n = 60: 36 de entrenamiento
        _DATOS_B3[semilla] = ml.PROCESOS["entregas_curvas"](n=60, semilla=semilla)
    datos, mu = _DATOS_B3[semilla], float(10 ** log_mu)
    m = ml.ajustar(datos, phi=PHI_B3, mu=mu, penalizacion="l2")
    if que == "ajuste":
        ax = ml.dibujar_proceso(datos)
        ml.dibujar_ajuste({f"μ = {mu:.2g}": m}, ventana=ax.get_xlim(), ax=ax)
    elif que == "vistas":
        ml.dibujar_tres_paneles(m, datos.val)
    else:                                       # la U contra μ, como en la clase 2
        if semilla not in _U_B3:                # orden: μ de mayor a menor
            _U_B3[semilla] = (ml.elegir(datos, CAND_B3, con="cv", k=5,
                                        orden_complejidad=sorted(MUS_B3, reverse=True)),
                              ml.curva_capacidad(datos, CAND_B3))
        sel, curva = _U_B3[semilla]
        tu = min(MUS_B3, key=lambda c: abs(np.log10(c) - log_mu))
        ml.dibujar_cv(sel, R=curva, L_ent=curva, log=True, anotar={tu: "tú"})
        print(f"μ del mínimo de CV₅ = {sel.elegido:.2g}")
    plt.show()
    e = datos.val["y"] - m.predecir(datos.val)
    media = ml.benchmarks(datos, datos.val).loc["media", "cuadratica"]
    print(f"L_ent = {ml.L(m, datos.ent):.2f} · L_val = {ml.L(m, datos.val):.2f} · "
          f"R = {ml.riesgo(m, datos):.2f} · la media en val (benchmark) = {media:.2f}")
    print(f"residuales de validación: centro = {e.mean():.2f}, ancho = {e.std():.2f}")


ml.laboratorio(bloque_3, log_mu=ml.deslizador("log₁₀ μ", -6.0, 2.0, 0.5, -2.0),
               semilla=ml.deslizador("semilla", 0, 9, 1, 0),
               que=ml.selector("qué ver", {"el ajuste": "ajuste",
                                           "las tres vistas en validación": "vistas",
                                           "la U contra μ": "u"}, "ajuste"))

# %% [texto] bloque-3-mira

# %% [texto] bloque-3-explica

# %% [texto] bloque-4-predice

# %% [codigo] bloque-4-juega
#@title Juega: trayectorias con 50 variables
PHI_50 = ml.estandarizar(ml.columnas(*[f"x{j}" for j in range(1, 51)]))
MUS_B4 = np.logspace(-3, 1, 60)
UTILES = ["x1", "x2", "x3", "x4", "x5"]
_TRAY_B4, _PAREJA_B4 = {}, {}


def _datos_b4(semilla, gemela, realidad=True):
    return ml.muchas_variables(n=300, J=50, utiles=5, semilla=semilla,
                               gemelas={"x1": 0.95} if gemela else None,
                               con_realidad=realidad)


def bloque_4(penalizacion, rho, gemela, semilla):
    clave = (penalizacion, rho if penalizacion == "elastica" else None, gemela, semilla)
    if clave not in _TRAY_B4:
        _TRAY_B4[clave] = ml.trayectorias(_datos_b4(semilla, gemela, False), PHI_50,
                                          penalizacion, MUS_B4, rho=rho)
    ml.dibujar_trayectorias(_TRAY_B4[clave], utiles=UTILES + (["x6"] if gemela else []))
    plt.show()
    if gemela and penalizacion != "l2":         # 100 réplicas con μ = 0.3, una vez
        if clave[:2] not in _PAREJA_B4:
            fab = lambda s: _datos_b4(s, True, False)
            t = ml.beta_repetido(fab, PHI_50, 100, mu=0.3, penalizacion=penalizacion,
                                 rho=rho)
            _PAREJA_B4[clave[:2]] = (t[["x1", "x6"]] != 0).mean()
        f = _PAREJA_B4[clave[:2]]
        print(f"de 100 muestras, con μ = 0.3: conserva x1 {100 * f['x1']:.0f} veces"
              f" y su gemela x6 {100 * f['x6']:.0f}")


ml.laboratorio(
    bloque_4,
    penalizacion=ml.selector("penalización", {"ridge": "l2", "lasso": "l1",
                                              "red elástica": "elastica"}, "l1"),
    rho=ml.selector("ρ (solo red elástica)", [0.2, 0.5, 0.8], 0.5),
    gemela=ml.interruptor("una útil con una gemela casi idéntica", False),
    semilla=ml.deslizador("semilla", 0, 9, 1, 0),
)

# %% [texto] bloque-4-mira

# %% [texto] bloque-4-explica

# %% [texto] bloque-5-predice

# %% [codigo] bloque-5-juega
#@title Juega: ¿quién elige μ?
DATOS_B5 = ml.muchas_variables(n=300, J=50, utiles=5, semilla=0)   # los del bloque 4
MUS_B5 = [float(m) for m in np.logspace(-4, 3, 30)]
BENCH_B5 = ml.benchmarks(DATOS_B5, DATOS_B5.despliegue).loc["media", "cuadratica"]
_AJ, _SEL_B5 = {}, {}

def _candidatos(p):           # estandariza dentro de cada pliegue; un ajuste, una vez
    def c(df, mu):
        k = (p, mu, tuple(df.index))
        if k not in _AJ:
            _AJ[k] = ml.ajustar(df, phi=PHI_50, mu=mu, penalizacion=p)
        return _AJ[k]
    return {mu: (lambda df, mu=mu: c(df, mu)) for mu in MUS_B5}

def seleccion_b5(con, regla, p):              # simple → complejo: μ de mayor a menor
    k = (con, regla if con == "cv" else "minimo", p)
    if k not in _SEL_B5:
        _SEL_B5[k] = ml.elegir(DATOS_B5, _candidatos(p), con=con, k=5, regla=k[1],
                               orden_complejidad=sorted(MUS_B5, reverse=True))
    return _SEL_B5[k]

def bloque_5(con, regla, p):
    sel = seleccion_b5(con, regla, p)
    mods = {mu: c(DATOS_B5.ent) for mu, c in _candidatos(p).items()}
    nz = {mu: str(int((m.beta_gorro.drop("1") != 0).sum())) for mu, m in mods.items()}
    R = {mu: ml.riesgo(m, DATOS_B5) for mu, m in mods.items()}
    Le = None if con == "ent" else {mu: ml.L(m, DATOS_B5.ent) for mu, m in mods.items()}
    ml.dibujar_cv(sel, R=R, L_ent=Le, benchmark=BENCH_B5, log=True,
                  anotar={mu: nz[mu] for mu in MUS_B5[::4]})
    plt.show()
    mu = sel.elegido_un_ee if (con, regla) == ("cv", "un_ee") else sel.elegido
    v, ee = sel.tabla.set_index("candidato").loc[mu, ["valor", "ee"]]
    valor = f"CV₅ = {v:.3f} ± {ee:.3f}" if con == "cv" else f"L_{con} = {v:.3f}"
    print(f"μ elegida = {mu:.3g} · {valor} · {nz[mu]} coeficientes ≠ 0 · "
          f"R = {R[mu]:.3f} · la media (benchmark): R = {BENCH_B5:.3f}")

ml.laboratorio(bloque_5, con=ml.selector("elige con", {"L_ent": "ent", "L_val": "val",
                                                      "CV con k = 5": "cv"}, "ent"),
               regla=ml.selector("regla", {"el mínimo": "minimo", "un EE": "un_ee"}),
               p=ml.selector("penalización", {"lasso": "l1", "ridge": "l2"}, "l1"))

# %% [codigo] bloque-5-prueba
# abre-prueba: procedimiento fijado (lasso, CV5, un EE); se mira una vez
#@title La prueba, una sola vez
sel = seleccion_b5("cv", "un_ee", "l1")   # fijado antes; no cambia con los controles
final, prueba = sel.modelo_final, DATOS_B5.prueba
l_mod = (prueba["y"] - final.predecir(prueba)) ** 2
media = pd.concat([DATOS_B5.ent, DATOS_B5.val])["y"].mean()   # benchmark fijado igual
l_med = (prueba["y"] - media) ** 2
dif, ee = ml.diferencia_pareada(l_mod.to_numpy(), l_med.to_numpy())
ee_l = l_mod.std() / np.sqrt(len(l_mod))
print(f"L_prueba del procedimiento = {l_mod.mean():.3f} ± {2 * ee_l:.3f} (2 EE)")
print(f"la media en prueba (benchmark) = {l_med.mean():.3f}")
print(f"diferencia pareada modelo − media en prueba = {dif:.3f} ± {ee:.3f} (1 EE)")
print(f"R del procedimiento (muestra enorme) = {ml.riesgo(final, DATOS_B5):.3f}")

# %% [texto] bloque-5-mira

# %% [texto] bloque-5-explica

# %% [texto] bloque-6-predice

# %% [codigo] bloque-6-juega
#@title Juega: estandarizar
MUS_B6 = np.logspace(-3, 1, 40)


def bloque_6(factor_x2, estandarizar, factor_y, log_mu):
    escala = {"x2": factor_x2, "y": factor_y}
    datos = ml.proceso(n=300, x={"x1": ml.normal(), "x2": ml.normal()},
                       f=lambda d: 1 + d.x1 + d.x2, ruido=ml.normal(0, 1),
                       escala=escala, semilla=0)
    phi = ml.columnas("x1", "x2")
    phi = ml.estandarizar(phi) if estandarizar else phi
    mu = float(10 ** log_mu)
    tabla = ml.trayectorias(datos, phi, "l1", MUS_B6)
    ml.dibujar_trayectorias(tabla, utiles=["x1", "x2"], marcar_mu=mu)
    plt.show()
    m = ml.ajustar(datos, phi=phi, mu=mu, penalizacion="l1")
    print(f"con μ = {mu:.3g}: β̂ = {m.beta_gorro.drop('1').round(6).to_dict()}")
    ml.imprimir_Phi(m, datos.val, filas=3)


ml.laboratorio(
    bloque_6,
    factor_x2=ml.selector("x2 multiplicada por", {"× 0.001": 0.001, "× 1": 1.0,
                                                  "× 1000": 1000.0}, 1000.0),
    estandarizar=ml.interruptor("estandarizar con entrenamiento", False),
    factor_y=ml.selector("y multiplicada por (caso 24)", {"× 1": 1.0, "× 1000": 1000.0},
                         1.0),
    log_mu=ml.deslizador("log₁₀ μ", -3.0, 1.0, 0.25, -1.0),
)

# %% [texto] bloque-6-mira

# %% [texto] bloque-6-explica

# %% [texto] taller-intro

# %% [codigo-visible] taller
datos = ml.muchas_variables(n=300, J=20, utiles=3, semilla=0)
ml.taller(datos, clase=3, que="lagrangeano", penalizacion="l1")
# 1) penalizacion="l2"   o   penalizacion="elastica", rho=0.5
# 2) datos = ml.proceso(n=300, x={"x1": ml.normal(), "x2": ml.normal()},
#        f=lambda d: d.x1 + d.x2, correlacion={("x1", "x2"): 0.95})
# 3) datos = ml.muchas_variables(n=300, J=20, utiles=3,
#        escala={"x1": 1000}, semilla=0)

# %% [texto] galeria-intro

# %% [codigo] galeria
#@title Galería: casos que se rompen a la vista
ml.galeria(clase=3, casos=[9, 10, 23, 24], que="lagrangeano")

# %% [texto] ejercicio-cero-a-mano

# %% [texto] ejercicio-cero-a-mano-respuesta

# %% [texto] ejercicio-grupo

# %% [texto] ejercicio-grupo-respuesta

# %% [texto] cierre
