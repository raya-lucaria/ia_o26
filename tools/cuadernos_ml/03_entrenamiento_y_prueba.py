# Notebook 03 de la unidad 9 · Entrenamiento y prueba (acompaña
# ml-entrenamiento-y-prueba, clase 2). Código y orden de celdas: prog-c2
# (clase_2.md §10.3 NB03). El texto de cada celda [texto] vive en
# 03_entrenamiento_y_prueba.texto.md (guion de Codex). Las cifras que el guion
# cita salen de tools/ml_cifras_c2.py con estas mismas constantes (semilla 0,
# 60 entregas, muestra enorme de 2000 en las fábricas repetidas).
# Solo los bloques 3 y 4 leen la prueba (contrato §6.6, regla 8).

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo] bloque-1-juega
#@title Juega: deja que el entrenamiento elija
import functools, warnings
import numpy as np, pandas as pd, matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
SEMILLA = 0
construir = lambda N: (lambda df, N=N: ml.ajustar(df, phi=ml.polinomio(N)))
CANDIDATOS = {N: construir(N) for N in range(13)}


@functools.lru_cache(maxsize=None)
def curva_b1(n, semilla):
    datos = ml.PROCESOS["entregas_curvas"](n=n, semilla=semilla)
    tabla = ml.curva_capacidad(datos, CANDIDATOS, conjuntos=("ent", "realidad"))
    bench = ml.benchmarks(datos, datos.realidad).loc["media"].iloc[0]
    return datos, tabla, bench


def bloque_1(N, n, semilla, ver_R):
    datos, tabla, bench = curva_b1(n, semilla)
    if not ver_R:
        tabla = tabla[tabla["conjunto"] == "ent"]
    modelo = CANDIDATOS[N](datos)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
    ml.dibujar_ajuste([modelo], datos, ax=a1)
    ml.dibujar_curva_capacidad(tabla, marcar=N, benchmark=bench if ver_R else None,
                               ax=a2)
    plt.show()
    ent = tabla[tabla["conjunto"] == "ent"].set_index("candidato")["L"]
    print(f"entrenamiento: el grado de menor L_ent es {int(ent.idxmin())}")
    ml.imprimir_Phi(modelo, datos.ent, filas=3)


ml.laboratorio(bloque_1, N=ml.deslizador("grado N", 0, 12, 1, 3),
               n=ml.deslizador("entregas n", 20, 200, 10, 60),
               semilla=ml.deslizador("semilla", 0, 20, 1, SEMILLA),
               ver_R=ml.interruptor("mostrar la realidad R", False))

# %% [texto] bloque-1-mira

# %% [texto] bloque-1-explica

# %% [texto] bloque-2-predice

# %% [codigo] bloque-2-juega
#@title Juega: una prueba honesta también baila
DATOS_B2 = ml.PROCESOS["entregas_curvas"](n=60, semilla=SEMILLA)
MODELO_B2 = construir(4)(DATOS_B2)                     # congelado: ya no se ajusta
D = DATOS_B2.despliegue                                 # el visor de la realidad
PERDIDAS_B2 = np.asarray(ml.perdida(D["y"], MODELO_B2.predecir(D)), float)
R_B2 = PERDIDAS_B2.mean()
BENCH_B2 = ml.benchmarks(DATOS_B2, D).loc["media"].iloc[0]   # la media de ent
TAMANOS = [5, 10, 20, 50, 100, 200, 400]


def bloque_2(n_prueba, intervalos):
    rng = np.random.default_rng(SEMILLA)
    L, cubre = [], 0
    for _ in range(500):
        l = PERDIDAS_B2[rng.choice(len(PERDIDAS_B2), size=n_prueba, replace=False)]
        ee = ml.error_estandar(l)
        L.append(l.mean())
        cubre += abs(l.mean() - R_B2) <= 2 * ee
    ml.dibujar_histograma_estimaciones(np.array(L), verdadero=R_B2, etiqueta="L_prueba")
    plt.show()
    print(f"R (despliegue, 100 000) = {R_B2:.2f}; desviación de las 500 L_prueba:"
          f" {np.std(L, ddof=1):.2f}")
    print(f"benchmark (la media de entrenamiento) en el despliegue = {BENCH_B2:.2f}")
    if intervalos:
        print(f"L_prueba ± 2 EE cubre R en {cubre / 5:.0f} % de las 500 pruebas")


ml.laboratorio(bloque_2, n_prueba=ml.selector("n_prueba", TAMANOS, 20),
               intervalos=ml.interruptor("mostrar intervalos ±2 EE", False))

# %% [texto] bloque-2-mira

# %% [texto] bloque-2-explica

# %% [texto] bloque-3-predice

# %% [codigo] bloque-3-juega
# abre-prueba: el engaño de elegir con la prueba
#@title Juega: el engaño de elegir con la prueba
REPETICIONES_B3 = 300                   # las de la página (tarda ~30 s, una vez)


def fabrica(s):
    return ml.PROCESOS["entregas_curvas"](n=60, semilla=s, n_realidad=2000)


LARGO_B3 = ml.optimismo_por_seleccion(fabrica, CANDIDATOS, REPETICIONES_B3,
                                      semilla=SEMILLA, detalle=True)
MODOS = {"elegir con la prueba": "L_prueba", "elegir con validación": "L_val"}


def bloque_3(modo, M):
    t = LARGO_B3[LARGO_B3["candidato"] < M].sort_values(["repeticion", "candidato"])
    elegidos = t.loc[t.groupby("repeticion")[MODOS[modo]].idxmin()]
    d = (elegidos["L_prueba"] - elegidos["R"]).to_numpy()
    ml.dibujar_histograma_estimaciones(
        {modo: d}, verdadero=0,
        etiqueta="anunciado − real del elegido (sin reajuste)")
    plt.title("sin reajuste: el mismo entrenamiento en los dos modos")
    plt.show()
    ee = d.std(ddof=1) / np.sqrt(len(d))
    print(f"{modo}, grados 0..{M - 1}: media {d.mean():.2f} ± {ee:.2f} (EE de Monte"
          f" Carlo); mediana {np.median(d):.2f};"
          f" anuncian de menos {np.mean(d < 0):.0%}")


ml.laboratorio(bloque_3, modo=ml.selector("elegir con", list(MODOS)),
               M=ml.deslizador("candidatos M", 1, 13, 1, 13))

# %% [texto] bloque-3-mira

# %% [texto] bloque-3-explica

# %% [texto] bloque-4-predice

# %% [codigo] bloque-4-juega
# abre-prueba: lo que promete la prueba según cómo se separó
#@title Juega: ¿qué imita tu prueba?
VECINOS = lambda d: ml.ajustar_otro(d, familia="vecinos", columnas_x=["x", "t"],
                                    n_vecinos=5)
EFECTOS = ml.dummies("grupo", codificacion="efectos")
PACIENTE = lambda d: ml.ajustar(d, phi=ml.combinar(ml.polinomio(3), EFECTOS))
POR_CV = lambda d: ml.elegir(d, {N: construir(N) for N in range(9)}, con="cv").modelo
OTRA = lambda t: {"x": ml.uniforme(4, 10)}
CONTRATOS = {   # (datos al azar, datos que imitan o None, el modelo del contrato)
    "más de lo mismo": (ml.PROCESOS["entregas_curvas"](n=240), None, POR_CV),
    "el mes que viene": (ml.caso(13), ml.caso(13, separar="tiempo"), VECINOS),
    "pacientes nuevos": (ml.caso(14, n_grupos=48),
                         ml.caso(14, n_grupos=48, separar="grupo"), PACIENTE),
    "otra ciudad": (ml.caso(15, deriva=OTRA), None, POR_CV)}

def medir(c, d, construir_m, sep):
    m, bench = construir_m(d), ml.benchmarks(d, d.despliegue).loc["media"].iloc[0]
    return {"contrato": c, "separacion": sep, "L_prueba": ml.L(m, d.prueba),
            "R": ml.riesgo(m, d), "benchmark": bench}

FILAS_B4 = {}
for c, (a, i, cm) in CONTRATOS.items():
    FILAS_B4[c, "al azar"] = medir(c, a, cm, "al azar")
    if i is not None:
        FILAS_B4[c, "como el contrato"] = medir(c, i, cm, "como el contrato")

def bloque_4(contrato, separar):
    fila = FILAS_B4.get((contrato, separar))
    if fila is None and contrato == "más de lo mismo":
        print("«más de lo mismo»: separar al azar ya imita este contrato.")
        fila = FILAS_B4[contrato, "al azar"]
    elif fila is None:
        print(f"«{contrato}»: ninguna separación de tu muestra lo imita;"
              " declara el alcance.")
        fila = FILAS_B4[contrato, "al azar"]
    ml.dibujar_contratos(pd.DataFrame(list(FILAS_B4.values())), resaltar=contrato)
    plt.yscale("log")
    plt.show()
    print(f"{contrato}, {fila['separacion']}: L_prueba = {fila['L_prueba']:.1f}   R en"
          f" el despliegue = {fila['R']:.1f}   benchmark = {fila['benchmark']:.1f}")

ml.laboratorio(bloque_4, contrato=ml.selector("contrato", list(CONTRATOS)),
               separar=ml.selector("cómo separar", ["al azar", "como el contrato"]))

# %% [texto] bloque-4-mira

# %% [texto] bloque-4-explica

# %% [texto] bloque-5-predice

# %% [codigo] bloque-5-juega
#@title Juega: cuánto dejar en cada conjunto
def fabrica_n(n):
    return lambda s: ml.PROCESOS["entregas_curvas"](n=n, semilla=s, n_realidad=2000)


TABLAS_B5 = {n: ml.reparto(fabrica_n(n), construir(4), repeticiones=100,
                           semilla=SEMILLA) for n in (60, 240, 960)}
BENCH_B5 = {n: ml.benchmarks(d, d.despliegue).loc["media"].iloc[0]
            for n, d in ((n, fabrica_n(n)(SEMILLA)) for n in (60, 240, 960))}


def bloque_5(fraccion, n_total):
    t = TABLAS_B5[n_total]
    ml.dibujar_reparto(t, marca=fraccion)
    plt.show()
    g = t[np.isclose(t["fraccion"], fraccion)]
    print(f"n = {n_total}, {fraccion:.0%} a prueba: R medio del modelo ="
          f" {g['R'].mean():.2f}; desviación de L_prueba − R ="
          f" {g['error'].std(ddof=1):.2f}")
    print("benchmark (la media de entrenamiento, una muestra) ="
          f" {BENCH_B5[n_total]:.2f}")


ml.laboratorio(bloque_5,
               fraccion=ml.deslizador("fracción de prueba", 0.05, 0.5, 0.05, 0.2),
               n_total=ml.selector("n total", [60, 240, 960], 60))

# %% [texto] bloque-5-mira

# %% [texto] bloque-5-explica

# %% [texto] taller-intro

# %% [codigo-visible] taller
datos = ml.PROCESOS["entregas_curvas"](n=60, semilla=0)
# 1) otra f:      datos = ml.proceso(n=60, x={"x": ml.uniforme(0, 6)},
#                                    f=lambda d: 10 + 12 / (1 + d.x))
# 2) el futuro:   datos = ml.caso(13, separar="azar")
# 3) pocos datos: datos = ml.PROCESOS["entregas_curvas"](n=25)
ml.taller(datos, clase=2, que="elegir")

# %% [texto] galeria-intro

# %% [codigo] galeria
#@title Galería: casos que se rompen a la vista
ml.galeria(clase=2)

# %% [texto] ejercicio-optimismo-m

# %% [texto] ejercicio-optimismo-m-respuesta

# %% [texto] cierre
