# Notebook 06 de la unidad 9 · Leer el error (acompaña ml-leer-el-error, clase 3).
# Código y orden de celdas: prog-c3 (clase_3.md §10.3.1). El texto de cada
# celda [texto] vive en 06_leer_el_error.texto.md (guion de Codex). Los
# procesos son los de tools/ml_cifras_c3.py (datos_b1, datos_senal, piezas_colas,
# datos_cola_en_x, datos_abanico): las cifras que cita la página salen de ahí.
# Nada de este notebook lee la prueba.

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo] bloque-1-juega
#@title Juega: las tres vistas
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SEMILLA = 0
F_B1 = {"correcto": lambda d: 1 + 2 * d.x1,
        "curva": lambda d: 1 + 2 * d.x1 + d.x1 ** 2,
        "omitida": lambda d: 1 + 2 * d.x1 + 1.5 * d.x2}
X_B1 = {"x1": ml.uniforme(-2, 2), "x2": ml.uniforme(-2, 2)}


def bloque_1(modelo, sigma, donde, semilla):
    datos = ml.proceso(n=300, x=X_B1, f=F_B1[modelo], ruido=ml.normal(0, sigma),
                       omitir=["x2"], semilla=semilla)
    m = ml.ajustar(datos, phi=ml.columnas("x1"))
    df = datos.val if donde == "validación" else datos.ent
    e = df["y"] - m.predecir(df)
    vista, hist = ml.dibujar_tres_paneles(m, df).axes[:2]
    lim = (min(*vista.get_xlim(), *vista.get_ylim()), max(*vista.get_xlim(), *vista.get_ylim()))
    vista.set_xlim(lim); vista.set_ylim(lim)        # ŷ y y con los mismos límites
    hist.axvspan(e.mean() - e.std(), e.mean() + e.std(), color="0.6", alpha=0.3)
    hist.axvline(0, ls="--", color="0.3"); hist.axvline(e.mean(), color="0.1")
    plt.show()
    media = ml.benchmarks(datos, df).loc["media", "cuadratica"]
    nombre = "val" if donde == "validación" else "ent"
    print(f"L_{nombre} = {ml.L(m, df):.3f}   ·   centro ē_{nombre} = {e.mean():.3f}"
          f"   ·   la media de entrenamiento (benchmark): {media:.3f}")
    print(f"R (despliegue, 100 000 obs.) = {ml.riesgo(m, datos):.3f}")


ml.laboratorio(
    bloque_1,
    modelo=ml.selector("modelo", {"recta (el correcto)": "correcto",
                                  "recta a una curva": "curva",
                                  "sin ver x2": "omitida"}, "correcto"),
    sigma=ml.deslizador("ruido σ_ε", 0.0, 3.0, 0.25, 1.0),
    donde=ml.selector("dónde se leen", ["validación", "entrenamiento"], "validación"),
    semilla=ml.deslizador("semilla", 0, 9, 1, SEMILLA),
)

# %% [texto] bloque-1-mira

# %% [texto] bloque-1-explica

# %% [texto] bloque-2-predice

# %% [codigo] bloque-2-juega
#@title Juega: ¿bueno o malo?
SEMILLA = 0


def bloque_2(nivel, senal, entre_nivel):
    datos = ml.proceso(n=1000, x={"x": ml.uniforme(-1, 1)},
                       f=lambda d: nivel + senal * 2 * d.x, ruido=ml.normal(0, 1),
                       semilla=SEMILLA)
    m = ml.ajustar(datos)                       # se ajusta solo con entrenamiento
    ml.dibujar_benchmarks(m, datos)             # en validación
    plt.show()
    val, media = datos.val, datos.ent["y"].mean()
    l_mod = (val["y"] - m.predecir(val)) ** 2
    l_med = (val["y"] - media) ** 2
    rmse = np.sqrt(l_mod.mean())
    if entre_nivel:
        print(f"RMSE / ȳ = {rmse / media:.4f}   (dividir entre el nivel)")
    else:
        print(f"RMSE / desviación de y en ent = {rmse / datos.ent['y'].std():.3f}")
    print(f"mejora sobre la media (val) = {1 - l_mod.mean() / l_med.mean():.3f}")
    dif, ee = ml.diferencia_pareada(l_mod.to_numpy(), l_med.to_numpy())
    gana = "sí" if dif < -2 * ee else "no"
    print(f"diferencia pareada modelo − media en val = {dif:.3f} ± {ee:.3f} (1 EE)")
    print(f"¿le gana por más de 2 EE en validación, que aquí no eligió nada? {gana}")


ml.laboratorio(
    bloque_2,
    nivel=ml.deslizador("nivel: se suma a y", 0, 1000, 100, 0),
    senal=ml.deslizador("fuerza de la señal", 0.0, 2.0, 0.125, 1.0),
    entre_nivel=ml.interruptor("dividir el RMSE entre el nivel ȳ "
                               "(y no entre la dispersión de y)", False),
)

# %% [texto] bloque-2-mira

# %% [texto] bloque-2-explica

# %% [texto] bloque-3-predice

# %% [codigo] bloque-3-juega
#@title Juega: colas largas
SEMILLA = 0
RUIDOS_B3 = {"normal": ml.normal(), "t3": ml.t_student(3),
             "pareto": ml.pareto(1.5), "cauchy": ml.cauchy()}


def _datos_b3(ruido, donde, semilla):
    if donde == "x":     # la cola vive en x: x lognormal, f curva, ruido normal
        return ml.proceso(n=1000, x={"x": ml.lognormal(0, 1)}, semilla=semilla,
                          f=lambda d: 2 + np.exp(d.x / 3), ruido=ml.normal(0, 0.5))
    return ml.proceso(n=1000, x={"x": ml.uniforme(0, 1)}, f=lambda d: 2 + 3 * d.x,
                      ruido=RUIDOS_B3[ruido], semilla=semilla)


def bloque_3(ruido, que, donde, semilla):
    datos = _datos_b3(ruido, donde, semilla)
    m, val = ml.ajustar(datos), datos.val       # una recta en los dos casos
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 3.8))
    if donde == "x":                            # la vista 3: e contra x
        a1.scatter(val["x"], val["y"] - m.predecir(val), s=12)
        a1.set_xlabel("x (validación)"); a1.set_ylabel("residual e")
    else:
        ml.dibujar_media_acumulada({ruido: RUIDOS_B3[ruido]}, estadistico=que, ax=a1)
    ml.dibujar_peso_de_filas(m, val, ax=a2)
    plt.show()
    print("Los 5 peores errores en validación:")
    print(ml.peores_errores(m, val, k=5).round(2).to_string())


ml.laboratorio(
    bloque_3,
    ruido=ml.selector("ruido", {"normal": "normal", "t de Student, 3 g.l.": "t3",
                                "Pareto, exponente 1.5": "pareto", "Cauchy": "cauchy"},
                      "pareto"),
    que=ml.selector("qué se promedia", {"cuadrados (MSE)": "cuadrado",
                                        "valores absolutos (MAE)": "absoluto"}),
    donde=ml.selector("dónde vive la cola", {"en el ruido": "ruido",
                                             "en x (ruido normal)": "x"}),
    semilla=ml.deslizador("semilla", 0, 9, 1, SEMILLA),
)

# %% [texto] bloque-3-mira

# %% [texto] bloque-3-explica

# %% [texto] bloque-4-predice

# %% [codigo] bloque-4-juega
#@title Juega: lo que el modelo no ve
SEMILLA, _CACHE_B4 = 0, {}

def _datos_b4(que, corr, endog, agregar, semilla, realidad=True):
    prod = 2 if que == "producto" else 0        # f = 1 + 2·x1 + 3·x2 (+ 2·x1·x2)
    return ml.proceso(n=200, x={"x1": ml.normal(), "x2": ml.normal()},
                      f=lambda d: 1 + 2 * d.x1 + 3 * d.x2 + prod * d.x1 * d.x2,
                      ruido=ml.normal(0, 1), endogeno=endog,
                      correlacion={("x1", "x2"): corr} if corr else None,
                      omitir=["x2"] if que == "x2" and not agregar else None,
                      semilla=semilla, con_realidad=realidad)

def bloque_4(que, corr, endog, agregar):
    phi = (ml.combinar(ml.columnas("x1", "x2"), ml.interacciones(("x1", "x2")))
           if que == "producto" and agregar else None)   # None: todo lo visible
    clave = (que, corr, endog, agregar)
    if clave not in _CACHE_B4:                  # 200 entrenamientos, una vez
        fab = lambda s: _datos_b4(que, corr, endog, agregar, s, realidad=False)
        _CACHE_B4[clave] = ml.beta_repetido(fab, phi, 200)
    cuenta = 2 + (3 * corr if que == "x2" and not agregar else 0) + endog
    ml.dibujar_beta_repetido(_CACHE_B4[clave], verdadero={"x1": 2.0}, columnas=("x1",))
    plt.axvline(cuenta, color="gray", ls="--", label="la cuenta")
    plt.legend(); plt.show()
    datos = _datos_b4(que, corr, endog, agregar, SEMILLA)
    m = ml.ajustar(datos, phi=phi)
    print(f"media de 200 β̂₁ = {_CACHE_B4[clave]['x1'].mean():.3f}"
          f" · la cuenta = {cuenta:.2f}\nL_val = {ml.L(m, datos.val):.3f}"
          f" · piso con lo visible = {ml.piso(datos):.3f}")
    if que == "producto":
        ml.dibujar_residuales_plano(m, datos.val, "x1", "x2"); plt.show()
        ml.imprimir_Phi(m, datos.val, filas=3)

ml.laboratorio(
    bloque_4,
    que=ml.selector("qué no ve el modelo", {"nada": "nada", "x2": "x2",
                                            "el producto x1·x2": "producto"}, "x2"),
    corr=ml.deslizador("corr(x1, x2)", 0.0, 0.9, 0.1, 0.3),
    endog=ml.deslizador("corr(x1, ε): endogeneidad", 0.0, 0.6, 0.1, 0.0),
    agregar=ml.interruptor("agregar la columna que falta", False),
)

# %% [texto] bloque-4-mira

# %% [texto] bloque-4-explica

# %% [texto] bloque-5-predice

# %% [codigo] bloque-5-juega
#@title Juega: reaprender con colinealidad
SEMILLA = 0
CORRS_B5 = [0.0, 0.5, 0.9, 0.99, 0.999]
PUNTOS_B5 = {"dentro": (1.0, 1.0), "fuera": (1.0, -1.0)}


def _fab_b5(corr):
    return lambda s: ml.caso(9, semilla=s, correlacion={("x1", "x2"): corr},
                             con_realidad=False)


TABLAS_B5 = {}                                  # cada (correlación, semilla), una vez


def bloque_5(corr, donde, semilla):
    if (corr, semilla) not in TABLAS_B5:
        TABLAS_B5[corr, semilla] = ml.beta_repetido(_fab_b5(corr), None, 200,
                                                    semilla=semilla)
    t = TABLAS_B5[corr, semilla]
    x1, x2 = PUNTOS_B5[donde]
    y_gorro = t["1"] + t["x1"] * x1 + t["x2"] * x2
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
    ml.dibujar_beta_repetido(t, verdadero={"x1": 1.0, "x2": 1.0},
                             columnas=("x1", "x2"), ax=a1)
    a2.hist(y_gorro, bins=30)
    a2.set_xlabel(f"ŷ en x1 = {x1:g}, x2 = {x2:g}")
    plt.show()
    print(f"desviación de β̂₁ en 200 entrenamientos = {t['x1'].std():.3f}")
    print(f"desviación de ŷ en ese punto = {y_gorro.std():.3f}")


ml.laboratorio(
    bloque_5,
    corr=ml.selector("corr(x1, x2)", CORRS_B5, 0.9),
    donde=ml.selector("dónde predices",
                      {"dentro de la nube: x1 = x2 = 1": "dentro",
                       "fuera de la diagonal de los datos: x1 = 1, x2 = −1": "fuera"},
                      "dentro"),
    semilla=ml.deslizador("semilla", 0, 9, 1, SEMILLA),
)

# %% [texto] bloque-5-mira

# %% [texto] bloque-5-explica

# %% [texto] taller-intro

# %% [codigo-visible] taller
# Tu proceso: cambia una línea y vuelve a correr.
datos = ml.proceso(n=300,
                   x={"x1": ml.normal(), "x2": ml.normal()},
                   f=lambda d: 1 + 2 * d.x1 + 3 * d.x2,
                   ruido=ml.normal(0, 1),
                   correlacion={("x1", "x2"): 0.5},
                   omitir=["x2"], semilla=0)
ml.taller(datos, clase=3, que="error")
# 1) ruido=ml.heterocedastico(lambda d: 0.5 + abs(d.x1))
# 2) f=lambda d: 1 + 2 * d.x1 + 3 * d.x1 * d.x2   y quita omitir
# 3) ruido=ml.t_student(2)

# %% [texto] galeria-intro

# %% [codigo] galeria
#@title Galería: casos que se rompen a la vista
ml.galeria(clase=3, casos=[6, 7, 8, 9, 11, 12], que="error")

# %% [texto] ejercicio-endogena

# %% [texto] ejercicio-endogena-respuesta

# %% [texto] ejercicio-abanico

# %% [texto] ejercicio-abanico-respuesta

# %% [texto] cierre
