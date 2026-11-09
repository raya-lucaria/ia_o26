# Tarea 1 de la unidad 9 · Propón la representación (clase 1). Código y orden
# de celdas: prog-c1 (clase_1.md §10.6). El texto de cada celda [texto] vive en
# tarea_1_proponer_phi.texto.md. Sin -explica ni respuestas. Instrumento de la
# clase 1: la muestra enorme (riesgo y desempeno contra el despliegue), que en
# la vida real no existe. Todos los procesos con fracciones=(1, 0, 0): no hay
# validación ni prueba. Secuencia de los bloques 2 y 3: propón con la nube y
# L_ent (juega), registra y revela (prueba, colapsada). Los procesos de los
# bloques 2 a 5 viven en bloque-1-prueba, colapsada: la portada pide no abrirla
# hasta el bloque 6. Sus números son los de cifras_c1_tarea (ml_cifras_c1.py),
# y test_ml_cifras_c1.py comprueba que este archivo los trae literales. La
# solución docente del bloque 3 no está aquí ni en el repo.

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo-visible] bloque-1-juega
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")


def medir(sigma, n, N, repeticiones=30):
    """Medianas de L_ent y de R en 30 muestras del mismo proceso, y su piso."""
    L_ent, R = [], []
    for s in range(repeticiones):
        datos = ml.proceso(n=n, x={"x": ml.uniforme(0, 2)},
                           f=lambda d: 4 + 2 * np.sin(3 * d["x"]),
                           ruido=ml.normal(0, sigma), fracciones=(1, 0, 0),
                           semilla=s, n_realidad=20_000)
        m = ml.ajustar(datos, phi=ml.polinomio(N))
        L_ent.append(ml.L(m, datos.ent))
        R.append(ml.riesgo(m, datos))    # la muestra enorme: no existe en la vida real
    return np.median(L_ent), np.median(R), ml.piso(datos)


CAMBIOS = {"base: σ_ε = 0.5, n = 20, N = 3": (0.5, 20, 3),
           "sube σ_ε a 1": (1.0, 20, 3),
           "sube n a 200": (0.5, 200, 3),
           "sube N a 8": (0.5, 20, 8)}
tabla = pd.DataFrame([medir(*v) for v in CAMBIOS.values()], index=list(CAMBIOS),
                     columns=["L_ent (mediana)", "R (mediana)", "piso"])
print(tabla.round(3).to_string())

# %% [codigo] bloque-1-prueba
#@title Prepara los procesos de los bloques 2 a 5 (no abras el código hasta el bloque 6)
SEMILLA = 0
_PERIODO, _N_2, _SIGMA_2, _X_2 = 2.5, 40, 0.5, (0, 6)


def proceso_periodico():
    return ml.proceso(n=40, x={"x": ml.uniforme(0, 6)},
                      f=lambda d: 3 + 2 * np.sin(2 * np.pi * d["x"] / 2.5),
                      ruido=ml.normal(0, 0.5), fracciones=(1, 0, 0), semilla=SEMILLA)


def proceso_nube():
    return ml.proceso_clasificacion(
        n=400, x={"x1": ml.uniforme(-1.5, 1.5), "x2": ml.uniforme(-1, 2.5)},
        puntaje=lambda d: 10 * (0.36 - (d["x2"] - d["x1"] ** 2) ** 2),
        fracciones=(1, 0, 0), semilla=SEMILLA)


def techo_de_bayes(datos):
    """Aciertos del oráculo que conoce Pr(y = 1 | x): el máximo posible."""
    d = datos.despliegue
    return float(np.mean((d["prob"] >= 0.5).astype(int) == d["y"]))


print("listo: proceso_periodico() y proceso_nube() esperan en los bloques 2 y 3")

# %% [texto] bloque-1-mira

# %% [texto] entrega-1

# %% [texto] bloque-2-predice

# %% [codigo-visible] bloque-2-juega
datos2 = proceso_periodico()   # el periodo no lo sabes: propónlo mirando la nube
N_FIJO = 5                     # el grado del polinomio lo fija el notebook
PERIODO = None                 # ← tu propuesta exploratoria, un número positivo
POR_QUE = ""                   # ← en una línea: con qué la propones
PERIODOS_A_PROBAR = []         # opcional: otros periodos, para comparar su L_ent

poli = ml.ajustar(datos2, phi=ml.polinomio(N_FIJO))
modelos = {f"polinomio de grado {N_FIJO}": poli}
if PERIODO is not None:
    peri = ml.ajustar(datos2, phi=ml.periodicas("x", periodo=PERIODO))
    modelos[f"periódica, periodo {PERIODO}"] = peri
ax = ml.dibujar_proceso(datos2, mostrar_f=False)
ml.dibujar_ajuste(modelos, ventana=ax.get_xlim(), ax=ax)
ax.set_ylabel("y")
plt.show()
for nombre, m in modelos.items():
    print(f"{nombre}: L_ent = {ml.L(m, datos2.ent):.3f}")
for p in PERIODOS_A_PROBAR:
    m = ml.ajustar(datos2, phi=ml.periodicas("x", periodo=p))
    print(f"   periodo {p}: L_ent = {ml.L(m, datos2.ent):.3f}")
if PERIODO is None:
    print("Escribe tu PERIODO y tu POR_QUE, y vuelve a correr esta celda.")

# %% [codigo] bloque-2-prueba
#@title Revela: R con la muestra enorme (solo tras llenar `entrega-2`)
if PERIODO is None or not POR_QUE.strip():
    print("Primero registra PERIODO y POR_QUE en el bloque 2 y en `entrega-2`.")
else:
    REGISTRO_2 = globals().get("REGISTRO_2") or (PERIODO, POR_QUE)
    print(f"propuesta registrada: periodo {REGISTRO_2[0]} · {REGISTRO_2[1]}")
    if (PERIODO, POR_QUE) != REGISTRO_2:
        print(f"⚠ cambiaste la propuesta a {PERIODO} después de ver R:"
              " decláralo como experimento en el veredicto.")
    for nombre, m in modelos.items():
        print(f"{nombre}: L_ent = {ml.L(m, datos2.ent):.3f}"
              f"   ·   R (muestra enorme) = {ml.riesgo(m, datos2):.3f}")
    print("En la vida real esta revisión no existe; la clase 2 usa validación.")

# %% [texto] bloque-2-mira

# %% [texto] entrega-2

# %% [texto] bloque-3-predice

# %% [codigo-visible] bloque-3-juega
datos3 = proceso_nube()
MI_PHI = None   # ← tu φ con ml.columnas(...); no polar ni el producto x1·x2
POR_QUE_3 = ""  # ← en una línea: qué viste en la nube

cart = ml.ajustar(datos3, tarea="clasificacion")    # cartesianas (1, x1, x2)
modelos3 = {"cartesianas (1, x1, x2)": cart}
if MI_PHI is not None:
    mio = ml.ajustar(datos3, phi=MI_PHI, tarea="clasificacion")
    modelos3["tu φ"] = mio
for nombre, m in modelos3.items():
    ml.dibujar_frontera(m, datos3.ent)
    plt.title(f"{nombre}: frontera, en entrenamiento")
    plt.show()
moda_ent = ml.benchmarks(datos3, datos3.ent).loc["moda", "aciertos"]
print(f"la moda (benchmark): aciertos en ent = {moda_ent:.3f}")
for nombre, m in modelos3.items():
    print(f"{nombre}: aciertos en ent = {ml.evaluar(m, datos3.ent, 'aciertos'):.3f}")
if MI_PHI is None:
    print("Escribe tu MI_PHI y tu POR_QUE_3, y vuelve a correr esta celda.")

# %% [codigo] bloque-3-prueba
#@title Revela: aciertos en la muestra enorme (solo tras llenar `entrega-3`)
if MI_PHI is None or not POR_QUE_3.strip():
    print("Primero registra MI_PHI y POR_QUE_3 en el bloque 3 y en `entrega-3`.")
else:
    columnas_3 = list(mio.Phi(datos3.ent).columns)
    REGISTRO_3 = globals().get("REGISTRO_3") or (columnas_3, POR_QUE_3)
    print(f"φ registrada: {REGISTRO_3[0]} · {REGISTRO_3[1]}")
    if (columnas_3, POR_QUE_3) != REGISTRO_3:
        print(f"⚠ cambiaste tu φ a {columnas_3} después de ver los aciertos:"
              " decláralo como experimento en el veredicto.")
    moda = ml.benchmarks(datos3, datos3.despliegue).loc["moda", "aciertos"]
    print(f"la moda (benchmark): aciertos en el despliegue = {moda:.3f}")
    for nombre, m in modelos3.items():
        ent = ml.evaluar(m, datos3.ent, "aciertos")
        desp = ml.desempeno(m, datos3, "aciertos")
        print(f"{nombre}: aciertos en ent = {ent:.3f}   ·   en el despliegue ="
              f" {desp:.3f}   ·   ent − despliegue = {ent - desp:+.3f}")
    print(f"techo de Bayes (el oráculo): {techo_de_bayes(datos3):.3f}")
    print("En la vida real esta revisión no existe; la clase 2 usa validación.")

# %% [texto] bloque-3-mira

# %% [texto] entrega-3

# %% [texto] bloque-4-predice

# %% [codigo-visible] bloque-4-juega
if MI_PHI is None:
    print("Primero propón tu φ en el bloque 3.")
else:
    ml.imprimir_Phi(mio, datos3.ent, filas=4)
    print("coeficientes β̂:", mio.beta_gorro.round(3).to_dict())

# %% [texto] bloque-4-mira

# %% [texto] entrega-4

# %% [texto] bloque-5-predice

# %% [codigo-visible] bloque-5-juega
ZONAS = {"dentro: x en [0, 6]": (0, 6), "fuera: x en [6, 9]": (6, 9)}
ax = ml.dibujar_proceso(datos2, mostrar_f=False)
ml.dibujar_ajuste(modelos, ventana=(0, 9), ax=ax)
ax.axvline(6, ls=":", color="gray")
ax.set_xlim(0, 9)
ax.set_ylim(-4, 8)
ax.set_ylabel("y")
ax.legend(loc="lower left")
plt.show()
for nombre, m in modelos.items():
    print(nombre)
    t = ml.error_por_zona(m, datos2, ZONAS)
    print(t[["zona", "dif2", "var_y_dado_x", "R_zona"]].round(3).to_string(index=False))
print("Qué datos usar para evaluar cada uso es tema de la clase 2.")

# %% [texto] bloque-5-mira

# %% [texto] entrega-5

# %% [texto] bloque-6-predice

# %% [codigo] bloque-6-juega
#@title Abre el proceso (córrela al llegar aquí, con tus propuestas ya registradas)
print("Bloques 2 y 5: y = 3 + 2·sen(2πx / periodo) + ε,"
      f" periodo = {_PERIODO}, x ~ U{_X_2}, ε ~ N(0, {_SIGMA_2}²), n = {_N_2}")
print(f"   tu propuesta: periodo {PERIODO} · piso R_Bayes = σ_ε² ="
      f" {ml.piso(datos2):.3f}")
print("Bloques 3 y 4: Pr(y = 1 | x) = σ(10·(0.36 − (x2 − x1²)²)),"
      " x1 ~ U(−1.5, 1.5), x2 ~ U(−1, 2.5), n = 400")
print(f"   la frontera de Bayes: la banda |x2 − x1²| < 0.6 · techo de aciertos ="
      f" {techo_de_bayes(datos3):.3f}")

# %% [texto] bloque-6-mira

# %% [texto] entrega-6

# %% [texto] cierre
