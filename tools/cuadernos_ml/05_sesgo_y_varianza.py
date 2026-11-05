# Notebook 05 de la unidad 9 · Sesgo y varianza (acompaña
# ml-sesgo-y-varianza, clase 2). Código y orden de celdas: prog-c2
# (clase_2.md §10.3 NB05). El texto de cada celda [texto] vive en
# 05_sesgo_y_varianza.texto.md (guion de Codex). Las cifras que el guion
# cita salen de tools/ml_cifras_c2.py con estas mismas constantes y fábricas.
# Ninguna celda lee la prueba: todo se mide en el simulador o con CV.

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo] bloque-1-juega
#@title Juega: el abanico y la diana
import functools, warnings
import numpy as np, pandas as pd, matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
SEMILLA = 0
construir = lambda N: (lambda df, N=N: ml.ajustar(df, phi=ml.polinomio(N)))
CANDIDATOS = {N: construir(N) for N in range(13)}


def fabrica(s, n=60, sigma=3.0):
    return ml.PROCESOS["entregas_curvas"](n=n, semilla=int(s), sigma_e=sigma,
                                         n_realidad=2000)


SV = ml.sesgo_varianza(fabrica, CANDIDATOS, repeticiones=100, semilla=SEMILLA)
X_MALLA = SV.malla["x"].to_numpy()


def bloque_1(N, x0, diana):
    i = int(np.argmin(np.abs(X_MALLA - x0)))      # el punto de la malla más cercano
    p = SV.predicciones[N][:, i]
    if diana:
        ml.dibujar_diana(SV, x0, candidatos=[N])
        # el eje cubre todas las marcas: ninguna predicción queda escondida
        margen = 0.05 * (p.max() - p.min()) + 2
        plt.xlim(min(15, p.min() - margen), max(55, p.max() + margen))
    else:
        ml.dibujar_abanico(SV, N)
        plt.ylim(0, 50)
        P = SV.predicciones[N]
        fuera = int(((P < 0) | (P > 50)).any(axis=1).sum())
        if fuera:
            print(f"{fuera} de {len(p)} curvas salen del eje de 0 a 50 en algún punto")
    plt.show()
    print(f"grado {N}, x0 = {X_MALLA[i]:.2f} km: E[y|x0] = {SV.verdad[i]:.1f};"
          f" sesgo = {p.mean() - SV.verdad[i]:.2f}; varianza = {p.var():.2f}"
          f" (desviación {p.std():.2f})")


ml.laboratorio(bloque_1, N=ml.deslizador("grado N", 0, 12, 1, 4),
               x0=ml.deslizador("x0 (km)", 0.5, 5.5, 0.25, 5.0),
               diana=ml.interruptor("ver la diana", False))

# %% [texto] bloque-1-mira

# %% [texto] bloque-1-explica

# %% [texto] bloque-2-predice

# %% [codigo] bloque-2-juega
#@title Juega: la descomposición, numérica
SIGMAS, NS = (1.5, 3.0, 6.0), (30, 60, 120)
@functools.lru_cache(maxsize=None)                     # cada combinación, la primera vez
def sv_b2(s, n):
    return ml.sesgo_varianza(lambda r: fabrica(r, n=n, sigma=s), CANDIDATOS,
                             repeticiones=50, semilla=SEMILLA)


def bloque_2(sigma, n):
    sv = sv_b2(sigma, n)
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4))
    ml.dibujar_sesgo_varianza(sv, ax=a)
    datos = fabrica(SEMILLA, n=n, sigma=sigma)
    s = ml.elegir(datos, CANDIDATOS, con="cv", k=5)
    ml.dibujar_cv(s, ax=b)
    b.set_yscale("log")
    plt.show()
    t = sv.tabla.set_index("candidato")
    N0 = int(t["total"].idxmin())
    bench = t.loc[0, "total"]                 # N = 0: error esperado de la media de ent
    print(f"σ = {sigma:g}, n = {n}: menor total en N⋆ = {N0}"
          f" (ruido {t.loc[N0, 'ruido']:.2f},"
          f" sesgo² {t.loc[N0, 'sesgo2']:.2f}, varianza {t.loc[N0, 'varianza']:.2f})")
    print(f"benchmark (N = 0, la media de entrenamiento): error esperado {bench:.2f};"
          f" la CV_5 de una muestra elige N̂ = {s.elegido}")


ml.laboratorio(bloque_2, sigma=ml.selector("ruido σ", list(SIGMAS), 3.0),
               n=ml.selector("entregas n", list(NS), 60))

# %% [texto] bloque-2-mira

# %% [texto] bloque-2-explica

# %% [texto] bloque-3-predice

# %% [codigo] bloque-3-juega
#@title Juega: más datos
NS_B3 = [30, 60, 120, 240, 480, 960]
fabrica_960 = lambda s: ml.PROCESOS["entregas_curvas"](
    n=960, semilla=int(s), n_realidad=2000, fracciones=(1, 0, 0))
CURVA = ml.curva_aprendizaje(fabrica_960, {N: construir(N) for N in (1, 4, 10)},
                             ns=NS_B3, repeticiones=50, semilla=SEMILLA)
ELEGIDO = ml.capacidad_elegida(fabrica_960, CANDIDATOS, ns=NS_B3, k=5, repeticiones=20,
                               semilla=SEMILLA)
PISO = ml.piso(fabrica_960(SEMILLA))
_D960 = fabrica_960(SEMILLA)
BENCH_B3 = ml.benchmarks(_D960, _D960.despliegue).loc["media"].iloc[0]  # media de ent


def bloque_3(modelos, abajo):
    grados = [1, 10] if modelos == "1 y 10" else [1, 4, 10]
    t = CURVA[CURVA["candidato"].isin(grados)]
    ml.dibujar_curva_aprendizaje(t, piso=PISO, elegido=ELEGIDO if abajo else None,
                                 resumen="mediana")
    plt.show()
    med = t.groupby(["candidato", "n"])["R"].median()
    for N in grados:
        print(f"grado {N}: R (mediana de 50) con 30 = {med[N, 30]:.1f}, con 960 ="
              f" {med[N, 960]:.1f}; piso {PISO:.1f}")
    e = ELEGIDO.groupby("n")["elegido"].median()
    print(f"grado que elige la CV_5 (mediana de 20): {e[30]:g} con 30,"
          f" {e[960]:g} con 960")
    print(f"benchmark (la media de entrenamiento, 960 entregas) en el despliegue ="
          f" {BENCH_B3:.1f}")


ml.laboratorio(bloque_3, modelos=ml.selector("modelos", ["1 y 10", "1, 4 y 10"]),
               abajo=ml.interruptor("panel del grado elegido", True))

# %% [texto] bloque-3-mira

# %% [texto] bloque-3-explica

# %% [texto] bloque-4-predice

# %% [codigo] bloque-4-juega
#@title Juega: cuatro procesos misteriosos
PROCESOS_B4 = {   # (datos, grado del modelo actual); los de ml_cifras_c2
    "A": (ml.PROCESOS["entregas_curvas"](n=400, semilla=SEMILLA, n_realidad=2000), 1),
    "B": (ml.PROCESOS["entregas_curvas"](n=40, semilla=SEMILLA, n_realidad=2000), 12),
    "C": (ml.proceso(n=400, x={"x": ml.uniforme(0, 6)}, f=lambda d: 30 + 0.2 * d["x"],
                     ruido=ml.normal(0, 8), semilla=SEMILLA, n_realidad=2000), 1),
    "D": (ml.PROCESOS["entregas_curvas"](n=400, semilla=SEMILLA, n_realidad=2000), 4)}


def bloque_4(proceso, revelar):
    datos, N = PROCESOS_B4[proceso]
    grados = range(max(8, N) + 1)
    tabla = ml.curva_capacidad(datos, {g: construir(g) for g in grados},
                               conjuntos=("ent", "cv"))
    cv = {g: ml.validacion_cruzada(datos, construir(g), k=5) for g in (0, N)}
    ml.dibujar_curva_capacidad(tabla, marcar=N, benchmark=(cv[0].media, cv[0].ee),
                               piso=ml.piso(datos) if revelar else None)
    plt.yscale("log"); plt.show()
    modelo, bench = construir(N)(datos.ent), construir(0)(datos.ent)   # solo con ent
    y = datos.val["y"].to_numpy()
    d, ee = ml.diferencia_pareada(ml.perdida(y, modelo.predecir(datos.val)),
                                  ml.perdida(y, bench.predecir(datos.val)))
    gana = "sí" if d < -2 * ee else "no"
    print("(a) en validación (la validación no eligió este modelo):"
          f" modelo − benchmark = {d:.2f} (EE {ee:.2f});"
          f" le gana por más de dos EE: {gana}")
    dp = ml.diferencia_por_pliegue(cv[N], cv[0])
    por, media = dp["diferencia"].to_numpy(float)[:5], float(dp["diferencia"].iloc[5])
    senal = "señal" if abs(media) > por.std(ddof=1) else "falta evidencia"
    print(f"(b) con CV (descriptivo): diferencia media {media:.2f}; por pliegue "
          + ", ".join(f"{v:.2f}" for v in por) + f" → {senal}")
    print(f"    {dp.attrs['nota']}")
    if revelar:   # con la media condicional conocida: R − piso no puede ser negativo
        D = datos.despliegue
        p = ml.piso(datos)
        exceso = np.mean((np.asarray(modelo.predecir(D), float)
                          - np.asarray(datos.f_visible(D), float)) ** 2)
        print(f"solo en el simulador: R = {p + exceso:.2f}, piso {p:.2f},"
              f" por ganar {exceso:.2f}")


ml.laboratorio(bloque_4, proceso=ml.selector("proceso", list(PROCESOS_B4)),
               revelar=ml.interruptor("revelar el piso y R (solo en el simulador)"))

# %% [texto] bloque-4-mira

# %% [texto] bloque-4-explica

# %% [texto] taller-intro

# %% [codigo-visible] taller
datos = ml.PROCESOS["entregas_curvas"](n=60, semilla=0)
# 1) otra f:      datos = ml.proceso(n=60, x={"x": ml.uniforme(0, 6)},
#                                    f=lambda d: 10 + 12 / (1 + d.x))
# 2) más ruido:   datos = ml.PROCESOS["entregas_curvas"](n=60, semilla=0, sigma_e=6)
# 3) n = 200:     datos = ml.PROCESOS["entregas_curvas"](n=200, semilla=0)
ml.taller(datos, clase=2, que="descomponer")

# %% [texto] galeria-intro

# %% [codigo] galeria
#@title Galería: casos que se rompen a la vista
ml.galeria(clase=2)

# %% [texto] ejercicio-tres-predicciones

# %% [texto] ejercicio-tres-predicciones-respuesta

# %% [texto] cierre
