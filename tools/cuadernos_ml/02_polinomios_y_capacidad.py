# Notebook 02 de la unidad 9 · Polinomios y capacidad (acompaña
# ml-polinomios-y-capacidad, clase 1). Código y orden de celdas: prog-c1
# (clase_1.md §10.3 NB02). El texto de cada celda [texto] vive en
# 02_polinomios_y_capacidad.texto.md (guion de Codex). Todo proceso se construye
# con fracciones=(1, 0, 0): en la clase 1 no hay validación ni prueba.

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo] bloque-1-juega
#@title Juega: Taylor contra mínimos cuadrados
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SEMILLA = 0
FUNCIONES = {"recíproca": ("inverso", (0.3, 3.0)), "seno": ("seno", (0.0, 2.0))}


def bloque_1(curva_f, N, centro, ruido):
    clave, (lo, hi) = FUNCIONES[curva_f]
    centro = min(max(centro, lo + 0.05), hi)   # el centro, dentro del dominio
    sin_ruido = {} if ruido else {"ruido": ml.normal(0, 0)}
    datos = ml.PROCESOS[clave](n=20, semilla=SEMILLA, fracciones=(1, 0, 0), **sin_ruido)
    f = lambda v: datos.f_visible(pd.DataFrame({"x": v}))
    taylor = ml.taylor(clave, centro=centro, N=N)
    mco = ml.ajustar(datos, phi=ml.polinomio(N))
    ax = ml.dibujar_ajuste({f"Taylor de grado {N} en x₀ = {centro:.1f}": taylor,
                            f"mínimos cuadrados, grado {N}": mco}, datos,
                           ventana=(lo, hi))
    x = np.linspace(lo, hi, 300)
    ax.plot(x, f(x), color="green", lw=3, zorder=1, label="f verdadera")
    if clave == "inverso" and centro == 1.0:
        ax.axvline(2, ls=":", color="black", label="x = 2: Taylor deja de converger")
    ax.set(xlim=(lo, hi), ylim=(min(f(x)) - 2, max(f(x)) + 2), ylabel="y")
    ax.legend(loc="upper right", fontsize=8), plt.show()
    b = np.array([hi])
    e_t = abs(taylor(b) - f(b))[0]
    e_m = abs(mco.predecir(pd.DataFrame({"x": b})) - f(b))[0]
    print(f"en el borde x = {hi}: error de Taylor = {e_t:.3f}"
          f"   ·   de mínimos cuadrados = {e_m:.3f}")


ml.laboratorio(bloque_1, curva_f=ml.selector("función", list(FUNCIONES)),
               N=ml.deslizador("grado N", 1, 9, 1, 3),
               centro=ml.deslizador("centro x₀", 0.3, 3.0, 0.1, 1.0),
               ruido=ml.interruptor("datos con ruido", True))

# %% [texto] bloque-1-mira

# %% [texto] bloque-1-explica

# %% [texto] bloque-2-predice

# %% [codigo] bloque-2-juega
#@title Juega: la curva de capacidad en vivo
SEMILLA = 0
CURVAS = {}   # (n, σ) -> (datos, tabla): se calcula una vez por combinación


def curva(n, sigma):
    if (n, sigma) not in CURVAS:
        datos = ml.PROCESOS["inverso"](n=n, semilla=SEMILLA, fracciones=(1, 0, 0),
                                       ruido=ml.normal(0, sigma))
        grados = {N: (lambda df, N=N: ml.ajustar(df, phi=ml.polinomio(N)))
                  for N in range(1, 16)}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            tabla = ml.curva_capacidad(datos, grados, conjuntos=("ent", "realidad"))
        CURVAS[(n, sigma)] = (datos, tabla)
    return CURVAS[(n, sigma)]


def bloque_2(N, n, sigma):
    datos, tabla = curva(n, sigma)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.2))
    m = ml.ajustar(datos, phi=ml.polinomio(N))
    ml.dibujar_ajuste({f"grado {N}": m}, datos, ax=a1)
    a1.set(ylim=(0, 20), ylabel="y")
    media = ml.benchmarks(datos, datos.realidad).loc["media", "cuadratica"]
    ml.dibujar_curva_capacidad(tabla, brecha=True, zonas=True, optimo=True,
                               piso=ml.piso(datos), benchmark=media, marcar=N, ax=a2)
    a2.set_yscale("log")   # R del grado 15 puede valer miles: en escala log se ve todo
    plt.show()
    L = tabla[tabla.candidato == N].set_index("conjunto")["L"]
    print(f"grado {N}: L_ent = {L['ent']:.3f}   ·   R = {L['realidad']:.3f}"
          f"   ·   brecha = {L['realidad'] - L['ent']:.3f}")
    print(f"piso = {ml.piso(datos):.3f}   ·   la media (benchmark), R = {media:.3f}")


ml.laboratorio(bloque_2, N=ml.deslizador("grado N", 1, 15, 1, 4),
               n=ml.deslizador("datos n", 20, 200, 10, 20),
               sigma=ml.deslizador("ruido σ_ε", 0.1, 1.5, 0.1, 0.5))

# %% [texto] bloque-2-mira

# %% [texto] bloque-2-explica

# %% [texto] bloque-3-predice

# %% [codigo] bloque-3-juega
#@title Juega: ¿quién elige N?
SEMILLA, REPETICIONES = 0, 200
MALLA = np.linspace(0.3, 3, 1000)   # R = E_x[(f − f̂)²] + σ², con x uniforme
grande = ml.PROCESOS["inverso"](n=20 * REPETICIONES, semilla=SEMILLA,
                                fracciones=(1, 0, 0), con_realidad=False).ent


def ajuste(x, y, N):
    """El ajuste de ml.ajustar(phi=ml.polinomio(N)), en forma cerrada (más rápido)."""
    z = lambda v: 2 * (v - x.min()) / (x.max() - x.min()) - 1
    beta = np.linalg.lstsq(np.vander(z(x), N + 1, increasing=True), y, rcond=None)[0]
    return lambda v: np.vander(z(v), N + 1, increasing=True) @ beta


def experimento(s):   # la muestra s (20 datos): L_ent y R de cada grado 1..15
    trozo = grande.iloc[20 * (s - SEMILLA):20 * (s - SEMILLA + 1)]
    x, y, filas = trozo["x"].to_numpy(), trozo["y"].to_numpy(), {}
    for N in range(1, 16):
        g = ajuste(x, y, N)
        filas[f"L{N}"] = np.mean((y - g(x)) ** 2)
        filas[f"R{N}"] = np.mean((2 + 5 / MALLA - g(MALLA)) ** 2) + 0.25
    return filas


TODAS = ml.repetir(experimento, repeticiones=REPETICIONES, semilla=SEMILLA)


def bloque_3(N_max):
    elegido = lambda c: TODAS[[f"{c}{N}" for N in range(1, N_max + 1)]].to_numpy()
    tabla = pd.DataFrame({"N_ent": elegido("L").argmin(axis=1) + 1,
                          "N_R": elegido("R").argmin(axis=1) + 1})
    ml.dibujar_elecciones(tabla)
    plt.show()
    print(f"de {REPETICIONES} muestras, L_ent eligió N = {N_max} (el máximo) "
          f"{(tabla.N_ent == N_max).sum()} veces")
    print("el N de menor R:", tabla.N_R.value_counts().sort_index().to_dict())


ml.laboratorio(bloque_3, N_max=ml.deslizador("N_max", 5, 15, 1, 15))

# %% [texto] bloque-3-mira

# %% [texto] bloque-3-explica

# %% [texto] bloque-4-predice

# %% [codigo] bloque-4-juega
#@title Juega: elegir φ contra fuerza bruta
SEMILLA = 0
CASO_3 = ml.caso(3, n=60, semilla=SEMILLA)


def bloque_4(phi, N, escalar):
    datos = CASO_3
    with warnings.catch_warnings():
        warnings.simplefilter("always")   # el aviso de mal condicionamiento se muestra
        if phi == "polinomio":
            m = ml.ajustar(datos, phi=ml.polinomio(N, escalar=escalar))
        else:
            m = ml.ajustar(datos, phi=ml.columnas("1/x"))
    nombre = f"polinomio de grado {N}" if phi == "polinomio" else "φ = (1, 1/x)"
    ml.dibujar_ajuste({nombre: m}, datos).set(ylim=(0, 40), ylabel="y")
    plt.show()
    ml.imprimir_Phi(m, datos.ent, filas=4)
    media = ml.benchmarks(datos, datos.despliegue).loc["media", "cuadratica"]
    print(f"columnas de Φ: {len(m.beta_gorro)}   ·   L_ent = {ml.L(m, datos.ent):.3f}"
          f"   ·   R (despliegue) = {ml.riesgo(m, datos):.3f}")
    print(f"piso = {ml.piso(datos):.3f}   ·   la media (benchmark), R = {media:.3f}")
    print(f"el mayor coeficiente en valor absoluto: {m.beta_gorro.abs().max():.3g}")


ml.laboratorio(bloque_4, phi=ml.selector("φ", ["polinomio", "(1, 1/x)"]),
               N=ml.deslizador("grado N", 1, 40, 1, 10),
               escalar=ml.interruptor("escalar x", True))

# %% [texto] bloque-4-mira

# %% [texto] bloque-4-explica

# %% [texto] bloque-5-predice

# %% [codigo] bloque-5-juega
#@title Juega: extrapolar
SEMILLA = 0
RANGOS = {"entregas": ("entregas", 0, 6), "seno": ("seno", 0, 2), "recursivo": (
    "recursivo", 0, 0), "mezcla de logaritmos": ("mezcla_logs", 1, 5)}


def bloque_5(proceso, N, zona, anterior):
    clave, lo, hi = RANGOS[proceso]
    if clave == "recursivo":   # la x crece con el tiempo: «fuera» es el futuro
        datos = ml.PROCESOS["recursivo"](semilla=SEMILLA)
        phi = ml.polinomio(N, "x")   # y, si lo pides, el tiempo anterior observado
        phi = ml.combinar(phi, ml.columnas("y_anterior")) if anterior else phi
        m = ml.ajustar(datos, phi=phi)
        todo = pd.concat([datos.ent, datos.prueba], ignore_index=True)
        ax = plt.subplots(figsize=(8, 3.8))[1]
        ax.scatter(datos.ent.t, datos.ent.y, s=16, label="entrenamiento: 60 pasos")
        ax.scatter(datos.prueba.t, datos.prueba.y, s=16, ec="gray", label="después")
        ax.plot(todo.t, m.predecir(todo), color="C1", label="predicción a un paso")
        ax.set(xlabel="paso (la x crece con el tiempo)", ylabel="y")
        ax.legend(), plt.show()
        print(f"dentro: L = {ml.L(m, datos.realidad):.3f}  ·  a un paso en el futuro: "
              f"R = {ml.riesgo(m, datos):.3f}  ·  piso = {ml.piso(datos):.3f}")
        return
    datos = ml.PROCESOS[clave](semilla=SEMILLA, fracciones=(1, 0, 0))
    hasta, m = lo + zona * (hi - lo), ml.ajustar(datos, phi=ml.polinomio(N))
    f = lambda v: datos.f_visible(pd.DataFrame({"x": v}))
    x = np.linspace(lo, hasta, 400)
    ax = ml.dibujar_ajuste({f"grado {N}": m}, datos, ventana=(lo, hasta))
    ax.plot(x, f(x), color="green", lw=3, zorder=1, label="f verdadera")
    ax.set(ylim=(min(f(x)) - 3, max(f(x)) + 3), ylabel="y"), ax.legend(), plt.show()
    if hasta > hi:
        tabla = ml.error_por_zona(m, datos, {"dentro": (lo, hi), "fuera": (hi, hasta)})
        tabla = tabla[["zona", "desde", "hasta", "R_zona"]].round(3)
        print(tabla.to_string(index=False))


ml.laboratorio(bloque_5, proceso=ml.selector("proceso", list(RANGOS)),
               N=ml.deslizador("grado N", 1, 10, 1, 7),
               zona=ml.deslizador("zona de uso (× el rango)", 1.0, 2.0, 0.1, 1.5),
               anterior=ml.interruptor("agregar la columna del tiempo anterior", False))

# %% [texto] bloque-5-mira

# %% [texto] bloque-5-explica

# %% [texto] bloque-6-predice

# %% [codigo] bloque-6-juega
#@title Juega: no free lunch
from fractions import Fraction

REGLAS = {"vecino más cercano": "vecino", "mayoría (empate → 1)": "mayoria",
          "siempre 1": "siempre_1"}
TABLA_NFL = ml.no_free_lunch(entrenamiento=(0, 3, 5, 6))   # 000, 011, 101, 110


def bloque_6(regla):
    trozo = TABLA_NFL[TABLA_NFL.regla == REGLAS[regla]]
    ml.dibujar_no_free_lunch(trozo)
    plt.show()
    promedio = sum(trozo.aciertos_fuera, Fraction(0)) / len(trozo)
    print(f"{regla}: promedio exacto sobre las {len(trozo)} funciones = {promedio}")
    medias = trozo.aciertos_fuera.astype(float).groupby(trozo.rugosidad).mean()
    print("aciertos medios por rugosidad:", medias.round(3).to_dict())


ml.laboratorio(bloque_6, regla=ml.selector("regla", list(REGLAS)))

# %% [codigo] bloque-6-prueba
#@title Mira: cada modelo gana en su proceso
SEMILLA = 0
CURVAS_B = {"suave": lambda d: 10 + 4 * d.x - 0.3 * d.x ** 2,
            "periódico": lambda d: 4 + 2 * np.sin(5 * d.x)}
RUIDOS = {"suave": 1.0, "periódico": 0.3}
filas = []
for nombre, f in CURVAS_B.items():
    datos = ml.proceso(n=60, x={"x": ml.uniforme(0, 6)}, f=f, semilla=SEMILLA,
                       ruido=ml.normal(0, RUIDOS[nombre]), fracciones=(1, 0, 0))
    polinomio = ml.ajustar(datos, phi=ml.polinomio(3))
    vecinos = ml.ajustar_otro(datos, familia="vecinos", n_vecinos=3)
    filas.append({"proceso": nombre, "polinomio N = 3": ml.riesgo(polinomio, datos),
                  "vecinos (3)": ml.riesgo(vecinos, datos)})
print("R (despliegue) de cada modelo en cada proceso:")
print(pd.DataFrame(filas).round(3).to_string(index=False))


# %% [texto] bloque-6-mira

# %% [texto] bloque-6-explica

# %% [texto] taller-intro

# %% [codigo-visible] taller
datos = ml.proceso(n=20, x={"x": ml.uniforme(0.3, 3)}, f=lambda d: 2 + 5 / d.x,
                   ruido=ml.normal(0, 0.5), fracciones=(1, 0, 0))
ml.taller(datos, clase=1, phi=ml.polinomio(4), N_max=15)
# ml.taller(datos, clase=1, phi=ml.columnas("1/x"), N_max=15)   # la columna correcta
# datos = ml.proceso(n=50, x={"x": ml.uniforme(0, 2)},
#                    f=lambda d: 4 + 2 * np.sin(5 * d.x),
#                    ruido=ml.normal(0, 0.3), fracciones=(1, 0, 0))
# ml.taller(datos, clase=1, phi=ml.periodicas("x", periodo=2 * np.pi / 5), N_max=15)
# datos = ml.proceso(n=40, x={"x": ml.uniforme(-2, 2)}, f=lambda d: d.x ** 3 - d.x,
#                    ruido=ml.normal(0, 0.5), fracciones=(1, 0, 0))   # tu f

# %% [texto] galeria-intro

# %% [codigo] galeria
#@title Galería: casos que se rompen a la vista
ml.galeria(clase=1, casos=[3, 4, 5, 23])

# %% [texto] ejercicio-fuerza-bruta

# %% [texto] ejercicio-fuerza-bruta-respuesta

# %% [texto] ejercicio-grado-con-entrenamiento

# %% [texto] ejercicio-grado-con-entrenamiento-respuesta

# %% [texto] cierre
