# Notebook 08 de la unidad 9 · Pérdida, métrica y desbalanceo (acompaña
# ml-perdida-metrica-desbalanceo, clase 4). Código y orden de celdas: prog-c4
# (clase_4.md §10.3). El texto de cada celda [texto] vive en
# 08_perdida_metrica_y_desbalanceo.texto.md (guion de Codex). Los procesos hilo
# salen de ml.PROCESOS («fraude», «mensajes3») y de ml.caso: aquí no se redefinen.
# Ninguna celda de este notebook lee la prueba ni evalúa con pesos.

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo] bloque-1-juega
#@title Juega: la logística como lagrangeano
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
SEMILLA = 0
fraude = ml.PROCESOS["fraude"]
mensajes3 = ml.PROCESOS["mensajes3"]
PHI_X = ml.estandarizar(ml.columnas("x"))   # media y desviación de cada ent
MUS = 10 ** np.arange(-6, 0.5, 0.5)         # la rejilla del deslizador
d_sep = ml.caso(17)                          # separable
d_ruido = ml.caso(17, ruido_etiquetas=0.2)   # el mismo, con etiquetas reasignadas
AJ = {"separable": ml.ajustes_por_mu(d_sep, PHI_X, "l2", MUS, tarea="clasificacion"),
      "con ruido": ml.ajustes_por_mu(d_ruido, PHI_X, "l2", MUS, tarea="clasificacion")}
DD = {"separable": d_sep, "con ruido": d_ruido}


def bloque_1(log10_mu, separable):
    orden = ["separable", "con ruido"] if separable else ["con ruido", "separable"]
    mu = 10 ** log10_mu
    ml.dibujar_separable({k: AJ[k] for k in orden}, mu=mu,
                         datos={k: DD[k] for k in orden})
    plt.show()
    d, m = DD[orden[0]], AJ[orden[0]].modelo(mu)   # el modelo guardado: no se reajusta
    for nombre, df in (("ent", d.ent), ("val", d.val)):
        base = ml.benchmarks(d, df).loc["proporcion", "logaritmica"]
        print(f"{nombre}: aciertos A = {ml.aciertos(df['y'], m.predecir(df)):.3f} · "
              f"L = {m.L(df):.3f} (benchmark, la proporción: {base:.3f})")


ml.laboratorio(
    bloque_1,
    log10_mu=ml.deslizador("log₁₀ μ", -6, 0, 0.5, -2),
    separable=ml.interruptor("datos separables (caso 17)", True),
)

# %% [texto] bloque-1-mira

# %% [texto] bloque-1-explica

# %% [texto] bloque-2-predice

# %% [codigo] bloque-2-juega
#@title Juega: la pérdida no es la métrica
SEMILLA = 0
datos2 = fraude(n=600, semilla=SEMILLA, proporcion=0.1)
MUS_CV = [1.0, 0.1, 0.01, 1e-3, 1e-4]       # de simple a complejo
cands = {mu: (lambda df, mu=mu: ml.ajustar(
    df, phi=ml.estandarizar(ml.columnas("x1", "x2")), mu=mu, penalizacion="l2"))
    for mu in MUS_CV}
sel = ml.elegir(datos2.ent, cands, con="cv", particion="estratificado",
                criterio="logaritmica")       # μ por CV estratificada, solo en ent
modelo = sel.modelo
TAU_VAL = ml.elegir_umbral(modelo, datos2.val, "mcc")   # en validación, nunca en prueba


def bloque_2(tau, elegido):
    ml.dibujar_umbral(modelo, datos2.val, tau=tau,
                      tau_elegido=TAU_VAL if elegido else None)
    plt.show()
    y_gorro = (modelo.predecir_p(datos2.despliegue) >= tau).astype(int)
    print(f"μ elegido por CV = {sel.elegido:g} · "
          f"τ que elige validación = {TAU_VAL:.2f}")
    print(f"MCC en el despliegue con τ = {tau:.2f}: "
          f"{ml.mcc(datos2.despliegue['y'], y_gorro):.3f}")


ml.laboratorio(
    bloque_2,
    tau=ml.deslizador("umbral τ", 0.05, 0.95, 0.05, 0.5),
    elegido=ml.interruptor("marcar el τ que elige validación", False),
)

# %% [texto] bloque-2-mira

# %% [texto] bloque-2-explica

# %% [texto] bloque-3-predice

# %% [codigo] bloque-3-juega
#@title Juega: el 99 % que no detecta nada
SEMILLA = 0
PROPS = [0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
# 20 reentrenamientos por proporción (plan §10.3: 20–50): con 2, el ±2 EE de las
# barras sería ruido. Se calcula una vez, aquí, fuera de bloque_3 (~30 s).
TABLA_DES = ml.metricas_vs_proporcion(PROPS, pesos=(None, "balanceado"), n=600,
                                      repeticiones=20, semilla=SEMILLA)
TABLA_VAL, CONTRIB = {}, {}                    # la banda de validación, al pedirla
for p in (0.5, 0.01):
    d = fraude(n=2000, semilla=SEMILLA, proporcion=p)
    m = ml.ajustar(d, phi=ml.estandarizar(ml.columnas("x1", "x2")), mu=1e-3,
                   penalizacion="l2")
    CONTRIB[p] = ml.contribucion_por_clase(m, d.ent)


def bloque_3(proporcion, pesos, medir):
    t = TABLA_DES if pesos else TABLA_DES[TABLA_DES["modelo"] != "balanceado"]
    if medir:
        if not TABLA_VAL:
            TABLA_VAL["t"] = ml.metricas_vs_proporcion(
                PROPS, pesos=("balanceado",), n=600, repeticiones=1, contra=("val",),
                repeticiones_val=50, semilla=SEMILLA)
        t = pd.concat([t, TABLA_VAL["t"]])
    fig = ml.dibujar_metricas_vs_proporcion(t)
    for ax in fig.axes:
        ax.axvline(proporcion, color="0.5", lw=1)
    plt.show()
    ax = ml.dibujar_contribucion_por_clase(
        {f"{int(100 * p)} %": CONTRIB[p]["fraccion_peso"] for p in CONTRIB})
    ax.set_ylabel("fracción del peso total")
    plt.show()
    print(CONTRIB[0.01].round(3).to_string())


ml.laboratorio(
    bloque_3,
    proporcion=ml.selector("proporción de fraude Pr(y=1)",
                           {"50 %": 0.5, "20 %": 0.2, "10 %": 0.1, "5 %": 0.05,
                            "2 %": 0.02, "1 %": 0.01}, 0.1),
    pesos=ml.interruptor("con pesos balanceados (los explica el bloque 4)", False),
    medir=ml.interruptor("medir en validación", False),
)

# %% [texto] bloque-3-mira

# %% [texto] bloque-3-explica

# %% [texto] bloque-4-predice

# %% [codigo] bloque-4-juega
#@title Juega: pesos, cambiar el problema y no los datos
SEMILLA = 0
datos4 = fraude(n=3000, semilla=SEMILLA, proporcion=0.05)
RAZONES = list(10 ** np.linspace(0, 2, 21))
TABLA_PESOS = ml.efecto_de_pesos(datos4, RAZONES)   # ajusta una vez por razón
BALANCEADA = (datos4.ent["y"] == 0).sum() / (datos4.ent["y"] == 1).sum()


def bloque_4(log10_razon, umbral):
    razon = RAZONES[int(round(10 * log10_razon))]
    ml.dibujar_efecto_de_pesos(TABLA_PESOS, razon=razon,
                               datos=datos4 if umbral else None)
    plt.show()
    fila = TABLA_PESOS.iloc[(TABLA_PESOS["razon"] - razon).abs().argmin()]
    print(f"razón w₁/w₀ = {razon:.1f} (la balanceada es {BALANCEADA:.1f}) · "
          f"p̂ promedio en la realidad = {fila['p_promedio']:.3f} "
          f"contra Pr(y=1) = {fila['prob_real']:.3f}")
    print(f"en el despliegue, τ = 0.5: MCC {fila['mcc_tau05']:.3f} · "
          f"A_bal {fila['aciertos_balanceados_tau05']:.3f} · "
          f"A {fila['aciertos_tau05']:.3f}")


ml.laboratorio(
    bloque_4,
    log10_razon=ml.deslizador("log₁₀(w₁/w₀)", 0, 2, 0.1, 0),
    umbral=ml.interruptor("comparar con mover τ en el modelo sin pesos", True),
)

# %% [texto] bloque-4-mira

# %% [texto] bloque-4-explica

# %% [texto] bloque-5-predice

# %% [codigo] bloque-5-juega
#@title Juega: tres clases
SEMILLA = 0
MEZCLAS = {"iguales": (1 / 3, 1 / 3, 1 / 3), "90/8/2": (0.9, 0.08, 0.02),
           "98/1.5/0.5": (0.98, 0.015, 0.005)}
PHI_3 = ml.estandarizar(ml.columnas("x1", "x2"))
D5 = {nombre: mensajes3(n=10_000, semilla=SEMILLA, proporcion=mezcla)
      for nombre, mezcla in MEZCLAS.items()}
M5 = {(n5, p): ml.ajustar(D5[n5], phi=PHI_3, mu=1e-3, penalizacion="l2", pesos=p)
      for n5 in MEZCLAS for p in (None, "balanceado")}
ml.imprimir_Phi(M5["90/8/2", None], D5["90/8/2"].val, filas=3)
COLORES = ["0.9", "#fde3a7", "#f8b4c8"]


def regiones(m, df, ax):            # ml.dibujar_frontera es binaria en esta versión
    u, v = np.meshgrid(np.linspace(-3, 3, 121), np.linspace(-3, 3, 121))
    malla = pd.DataFrame({"x1": u.ravel(), "x2": v.ravel()})
    z = m.predecir_prob(malla).argmax(axis=1).reshape(u.shape)
    ax.contourf(u, v, z, levels=[-0.5, 0.5, 1.5, 2.5], colors=COLORES)
    s = df.sample(min(len(df), 600), random_state=0)   # al azar: proporciones reales
    for k, mk in zip(range(3), "o^s"):
        ax.scatter(s.x1[s.y == k], s.x2[s.y == k], s=10, marker=mk, label=f"clase {k}")
    ax.legend(); ax.set_xlabel("x1 (enlaces)"); ax.set_ylabel("x2 (urgencia)")


def bloque_5(mezcla, pesos):
    d, m = D5[mezcla], M5[mezcla, "balanceado" if pesos else None]
    val, y, y_gorro = d.val, d.val["y"], m.predecir(d.val)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
    regiones(m, val, a1)                       # regiones de las tres clases
    soporte = y.value_counts().reindex([0, 1, 2], fill_value=0)
    ml.dibujar_promedios(ml.por_clase("aciertos", y, y_gorro, clases=[0, 1, 2]),
                         soporte, ax=a2)
    plt.show()
    moda = ml.benchmarks(d, val, criterios=("mcc",)).loc["moda", "mcc"]
    print(f"MCC multiclase en validación: modelo {ml.mcc(y, y_gorro):.3f}"
          f" · moda {moda:.3f}")


ml.laboratorio(bloque_5, mezcla=ml.selector("proporciones", list(MEZCLAS), "90/8/2"),
               pesos=ml.interruptor("pesos balanceados", False))

# %% [texto] bloque-5-mira

# %% [texto] bloque-5-explica

# %% [texto] bloque-6-predice

# %% [codigo] bloque-6-juega
#@title Juega: una métrica por pliegue
SEMILLA = 0
PHI_6 = ml.estandarizar(ml.columnas("x1", "x2"))
construir = lambda df: ml.ajustar(df, phi=PHI_6, mu=1e-2, penalizacion="l2",
                                  pesos="balanceado")
def _con_raros(r, n=500):                       # exactamente r fraudes de n
    df = fraude(n=4 * n, semilla=SEMILLA, proporcion=r / n, fracciones=(1, 0, 0)).ent
    df = pd.concat([df[df["y"] == 1].head(r), df[df["y"] == 0].head(n - r)])
    return df.sample(frac=1, random_state=SEMILLA).reset_index(drop=True)
DF6 = {r: _con_raros(r) for r in (3, 10, 30)}
TABLAS6 = {}                                    # cada (raros, k), una vez


def _tabla6(raros, k):
    if (raros, k) not in TABLAS6:
        df = DF6[raros]
        clases = df.attrs["ml"]["clases"]
        filas = []
        for nombre, met in (("mcc", ml.mcc),
                            ("aciertos_balanceados", ml.aciertos_balanceados)):
            cv = ml.validacion_cruzada(df, construir, k, particion="estratificado",
                                       estadistico=ml.con_clases(met, clases))
            pares = zip(cv.por_pliegue_estadistico, cv.pliegues)
            for i, (v, (_, idx)) in enumerate(pares, 1):
                filas.append({"k": k, "pliegue": i, "metrica": nombre, "valor": v,
                              "raros": int(df["y"].iloc[idx].sum())})
        TABLAS6[raros, k] = pd.DataFrame(filas)
    return TABLAS6[raros, k]

def bloque_6(k, raros):
    print(f"fraudes en la muestra: {int(DF6[raros]['y'].sum())} de {len(DF6[raros])}")
    ml.dibujar_metrica_por_pliegue(_tabla6(raros, k), k=k)
    plt.show()


ml.laboratorio(
    bloque_6,
    k=ml.deslizador("pliegues k", 2, 10, 1, 5),
    raros=ml.selector("fraudes en la muestra", [3, 10, 30], 10),
)

# %% [texto] bloque-6-mira

# %% [texto] bloque-6-explica

# %% [texto] taller-intro

# %% [codigo-visible] taller
# Tu proceso: cambia una línea y vuelve a correr.
datos = fraude(n=3000, semilla=0, proporcion=0.05)
ml.taller(datos, clase=4)
# a) datos = ml.proceso_clasificacion(n=3000, proporcion=0.005,
#        puntaje=lambda d: 2.0 * d.x1 - 1.0 * d.x2, semilla=0)
# b) datos = ml.anillos(n=600, semilla=1)   y en ml.taller: phi=ml.polares()
# c) datos = ml.proceso_clasificacion(n=3000, K=3, puntajes=[lambda d: 0 * d.x1,
#        lambda d: d.x1, lambda d: d.x2], proporcion=[0.9, 0.08, 0.02], semilla=0)

# %% [texto] galeria-intro

# %% [codigo] galeria
#@title Galería: casos que se rompen a la vista
ml.galeria(clase=4)

# %% [texto] ejercicio-moda

# %% [texto] ejercicio-moda-respuesta

# %% [texto] ejercicio-regresion-y-sigmoide

# %% [texto] ejercicio-regresion-y-sigmoide-respuesta

# %% [texto] cierre
