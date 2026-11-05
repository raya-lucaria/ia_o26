# Notebook 09 de la unidad 9 · Calibración y conformal (acompaña
# ml-calibracion-y-conformal, clase 4). Código y orden de celdas: prog-c4
# (clase_4.md §10.3). El texto de cada celda [texto] vive en
# 09_calibracion_y_conformal.texto.md (guion de Codex). Procesos de ml.PROCESOS.
# Mapa único de reservas: cal se aparta primero; val_a recalibra; val_b diagnostica;
# la prueba no se toca en clase. Ninguna celda mezcla variables de los dos procesos.

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo] bloque-1-juega
#@title Juega: ¿significa 0.8 lo que dice?
import warnings, numpy as np, pandas as pd, matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
SEMILLA = 0
fraude, mensajes3 = ml.PROCESOS["fraude"], ml.PROCESOS["mensajes3"]
datos = fraude(n=2000, semilla=SEMILLA, proporcion=0.05, fracciones=(0.5, 0.3, 0.2))
val_a, val_b = ml.partir(datos.val, 0.5, como="estratificado", semilla=SEMILLA)
PHI = ml.estandarizar(ml.columnas("x1", "x2"))
cands = {mu: (lambda df, mu=mu: ml.ajustar(df, phi=PHI, mu=mu, penalizacion="l2"))
         for mu in [1.0, 0.1, 0.01, 1e-3, 1e-4]}
MU = ml.elegir(datos.ent, cands, con="cv", particion="estratificado",
               criterio="logaritmica").elegido          # μ por CV, solo en ent
M = {nombre: ml.ajustar(datos.ent, phi=PHI, mu=MU, penalizacion="l2", pesos=p)
     for nombre, p in (("sin pesos", None), ("con pesos balanceados", "balanceado"))}
YBAR = datos.ent["y"].mean()                             # la proporción de ent
REAL = datos.realidad
VERDADERA = ml.calibracion(REAL["prob"], REAL["y"])
BM = ml.benchmarks(datos, val_b, criterios=("brier", "logaritmica")).loc["proporcion"]


def prob(modelo, df):               # la proporción de ent es el benchmark
    return (np.full(len(df), YBAR) if modelo == "proporción (benchmark)"
            else M[modelo].predecir_p(df))

def bloque_1(modelo, muestra, grupos):
    df = REAL if muestra is None else val_b.sample(muestra, random_state=SEMILLA)
    ml.dibujar_calibracion({modelo: ml.calibracion(prob(modelo, df), df["y"],
                            bins=grupos)}, verdadera=VERDADERA)
    plt.show()
    pb, yb = prob(modelo, val_b), val_b["y"]
    print(f"en val_b ({len(val_b)} casos): Brier {ml.brier(yb, pb):.3f} "
          f"(benchmark {BM['brier']:.3f}) · pérdida logarítmica "
          f"{ml.log_loss(yb, pb):.3f} (benchmark {BM['logaritmica']:.3f})")

MUESTRAS = {"100 casos de val_b": 100, f"toda val_b ({len(val_b)})": len(val_b),
            "realidad (100 000)": None}
ml.laboratorio(bloque_1, modelo=ml.selector(
    "modelo", list(M) + ["proporción (benchmark)"], "con pesos balanceados"),
    muestra=ml.selector("con qué se dibuja", MUESTRAS, len(val_b)),
    grupos=ml.deslizador("grupos", 5, 20, 5, 10))

# %% [texto] bloque-1-mira

# %% [texto] bloque-1-explica

# %% [texto] bloque-2-predice

# %% [codigo] bloque-2-juega
#@title Juega: recalibrar
m_pesos = M["con pesos balanceados"]
REC = {"ninguno": m_pesos,                               # Platt e isotónica: en val_a
       "platt": ml.recalibrar(m_pesos, val_a, "platt"),
       "isotonica": ml.recalibrar(m_pesos, val_a, "isotonica")}


def bloque_2(metodo, mismos):
    m = REC[metodo]
    donde, df = ("val_a (los mismos datos que recalibraron)", val_a) if mismos else \
        ("val_b (datos que la recalibración no vio)", val_b)
    ml.dibujar_calibracion({donde: ml.calibracion(m.predecir_p(df), df["y"]),
                            "realidad": ml.calibracion(m.predecir_p(REAL), REAL["y"])},
                           verdadera=VERDADERA)
    plt.show()
    for nombre, mm in (("antes", m_pesos), ("después", m)):
        p = mm.predecir_p(val_b)
        print(f"{nombre}: en val_b, Brier {ml.brier(val_b['y'], p):.3f} · "
              f"pérdida logarítmica {ml.log_loss(val_b['y'], p):.3f}")
    if metodo == "platt":
        print("β̂ de la recalibración (son parámetros):", m.hiperparametros["beta_cal"])


ml.laboratorio(
    bloque_2,
    metodo=ml.selector("método", ["ninguno", "platt", "isotonica"], "platt"),
    mismos=ml.interruptor("evaluar con los mismos datos que recalibraron", False),
)

# %% [texto] bloque-2-mira

# %% [texto] bloque-2-explica

# %% [texto] bloque-3-predice

# %% [codigo] bloque-3-juega
#@title Juega: un conjunto en vez de una etiqueta
datos3 = mensajes3(n=10_000, semilla=SEMILLA, proporcion=[1 / 3] * 3)
cal3, resto3 = ml.partir(datos3.val, 1 / 3, como="azar", semilla=SEMILLA)  # primero
PHI3 = ml.estandarizar(ml.columnas("x1", "x2"))
cands3 = {mu: (lambda df, mu=mu: ml.ajustar(df, phi=PHI3, mu=mu, penalizacion="l2"))
          for mu in [1.0, 0.1, 0.01, 1e-3]}
modelo3 = ml.elegir(datos3.ent, cands3, con="cv", particion="estratificado",
                    criterio="logaritmica").modelo        # softmax, solo con datos3.ent
MENSAJES = pd.DataFrame({"x1": [-2.0, 0.6, 0.3], "x2": [-1.5, 0.8, 0.3]},
                        index=["claro", "ambiguo", "difícil"])


def bloque_3(delta, caso):
    conf = ml.conformal(modelo3, cal3, delta)
    ml.dibujar_conformal(conf, datos3.despliegue)
    plt.show()
    x = MENSAJES.loc[[caso]]
    print(f"ĉ = {conf.c_gorro:.3f} · mensaje {caso}: p̂ = "
          f"{np.round(modelo3.predecir_prob(x)[0], 3)} → "
          f"C(x) = {conf.predecir_conjunto(x)[0]}")
    print(f"en el despliegue: cobertura {conf.cobertura(datos3.despliegue):.3f} "
          f"(1 − δ = {1 - delta:.2f}) · "
          f"tamaño medio {conf.tamano_medio(datos3.despliegue):.2f}")


ml.laboratorio(
    bloque_3,
    delta=ml.deslizador("δ (1 − cobertura)", 0.01, 0.30, 0.01, 0.10),
    caso=ml.selector("mensaje", list(MENSAJES.index), "ambiguo"),
)

# %% [texto] bloque-3-mira

# %% [texto] bloque-3-explica

# %% [texto] bloque-4-predice

# %% [codigo] bloque-4-juega
#@title Juega: la garantía es marginal
D4 = {}
for n in (2000, 10_000):
    d4 = mensajes3(n=n, semilla=SEMILLA, proporcion=[0.9, 0.08, 0.02])
    cal, _ = ml.partir(d4.val, 1 / 3, como="azar", semilla=SEMILLA)    # primero
    m4 = ml.elegir(d4.ent, cands3, con="cv", particion="estratificado",
                   criterio="logaritmica").modelo                     # sin pesos
    D4[n] = (d4, cal, m4)


def bloque_4(por_clase, delta, n):
    d4, cal, m4 = D4[n]
    conf = ml.conformal(m4, cal, delta, por_clase=por_clase)
    ml.dibujar_cobertura_por_clase(conf, d4.despliegue)
    plt.show()
    print(f"fraudes en cal: {int((cal['y'] == 2).sum())} · ĉ = {conf.c_gorro}")


ml.laboratorio(
    bloque_4,
    por_clase=ml.interruptor("conformal por clase", False),
    delta=ml.deslizador("δ", 0.05, 0.30, 0.05, 0.10),
    n=ml.selector("casos en la muestra", [2000, 10_000], 10_000),
)

# %% [texto] bloque-4-mira

# %% [texto] bloque-4-explica

# %% [texto] taller-intro

# %% [codigo-visible] taller
# Tu proceso: cambia una línea y vuelve a correr.
datos = fraude(n=3000, semilla=0, proporcion=0.05)
ml.taller(datos, clase=4, delta=0.1)
# a) fraude(n=3000, semilla=0, proporcion=0.02)
# b) ml.taller(datos, clase=4, delta=0.1, pesos=(None,))  contra pesos=("balanceado",)
# c) datos = mensajes3(n=10_000, semilla=0, separar="estratificado")
#    ml.taller(datos, clase=4, delta=0.1, por_clase=True)
# d) datos = fraude(n=3000, semilla=0, proporcion=0.05, separar="azar")

# %% [texto] galeria-intro

# %% [codigo] galeria
#@title Galería: casos que se rompen a la vista
ml.galeria(clase=4)

# %% [texto] ejercicio-cinco-puntajes

# %% [texto] ejercicio-cinco-puntajes-respuesta

# %% [texto] ejercicio-tasa

# %% [texto] ejercicio-tasa-respuesta

# %% [texto] cierre
