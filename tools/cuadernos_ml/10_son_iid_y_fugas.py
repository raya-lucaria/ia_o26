# Notebook 10 de la unidad 9 · ¿Son iid? Fugas (acompaña ml-son-iid-y-fugas,
# clase 5). Código y orden de celdas: prog-c5 (clase_5.md §10.3). El texto de
# cada celda [texto] vive en 10_son_iid_y_fugas.texto.md (guion de Codex).
# Ninguna celda lee la prueba: B3–B5 comparan la CV (sobre ent ∪ val) con el
# despliegue, y medir_fugas no toca la prueba (contrato §6.6 regla 8). Lo caro se
# calcula una vez al correr la celda de cada bloque; los controles solo leen.
# Los procesos son los de tools/ml_cifras_c5.py, escritos aquí con piezas de ml_lab.

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo] bloque-1-juega
#@title Juega: bolsas, puñados y una bolsa que cambia
import warnings, numpy as np, pandas as pd, matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
SEMILLA, N_BOLAS, MUESTRAS = 0, 200, 200
rng = np.random.default_rng(SEMILLA)


def sacar(como, punado):
    """La proporción de rojas en MUESTRAS muestras de N_BOLAS bolas."""
    props = []
    for _ in range(MUESTRAS):
        if como == "una por una (iid)":
            bolas = rng.random(N_BOLAS) < 0.4
        elif como == "a puñados":             # un puñado comparte su mezcla
            k = N_BOLAS // punado
            p = np.clip(rng.normal(0.4, 0.2, k), 0, 1)
            bolas = rng.random((k, punado)) < p[:, None]
        elif como == "de una bolsa que se tiñe":   # la mezcla camina
            p = np.clip(0.4 + np.cumsum(rng.normal(0, 0.03, N_BOLAS)), 0, 1)
            bolas = rng.random(N_BOLAS) < p
        else:                                  # otra bolsa: iid, otra mezcla
            bolas = rng.random(N_BOLAS) < 0.55
        props.append(np.mean(bolas))
    return np.array(props)


def bloque_1(como, punado):
    props = sacar(como, punado)
    ml.dibujar_histograma_estimaciones({como: props}, verdadero=0.4,
                                       etiqueta="proporción de rojas")
    ee = np.sqrt(0.4 * 0.6 / N_BOLAS)
    plt.axvspan(props.mean() - 2 * ee, props.mean() + 2 * ee, color="gold", alpha=0.15)
    plt.show()
    print(f"desviación real de las {MUESTRAS} proporciones: {props.std():.3f} · "
          f"la que promete la fórmula iid: {ee:.3f} · bolsa del uso: 0.40")


COMO = ["una por una (iid)", "a puñados", "de una bolsa que se tiñe", "de otra bolsa"]
ml.laboratorio(bloque_1, como=ml.selector("Cómo se saca", COMO, COMO[0]),
               punado=ml.deslizador("Tamaño del puñado", 1, 50, 1, 10))

# %% [texto] bloque-1-mira

# %% [texto] bloque-1-explica

# %% [texto] bloque-2-predice

# %% [codigo] bloque-2-juega
#@title Juega: tres detectores
X = {"distancia": ml.uniforme(0, 6), "hora": ml.uniforme(8, 22),
     "lluvia": ml.categorica([0, 1], [0.8, 0.2])}
f = lambda d: (10 + 12 * np.log1p(d.distancia) + 6.0 * d.lluvia + 0.4 * (d.hora - 15)
               + 4 * np.exp(-(d.distancia - 3) ** 2 / 0.5))   # entregas de la clase 2
PHI = ml.combinar(ml.polinomio(6, variable="distancia"), ml.columnas("lluvia", "hora"))
base = dict(n=400, x=X, f=f, semilla=SEMILLA, n_realidad=3000)
otra = dict(base, despliegue="otra_poblacion")
ESC = {"nada": (base, None), "el mes que viene (deriva en distancia)": (
           otra, lambda t: {"distancia": ml.uniforme(1.5, 7.5)}),
       "ruido con memoria": (base, None),
       "mismas marginales, otra correlación": (base, None),
       "el tráfico (caso 28)": (otra, lambda t: {"f": lambda d: f(d) + 6 * np.log1p(
           d.distancia)})}
DET = {}
for nombre, (kw, deriva) in ESC.items():
    memoria = ml.ar1(0.9 if nombre == "ruido con memoria" else 0.0, 3.0)
    d = ml.PROCESOS["entregas_curvas"](**kw, **({"deriva": deriva} if deriva else {}),
                                       ruido=memoria, separar="tiempo")
    uso = d.despliegue.sample(100, random_state=SEMILLA)
    if nombre.startswith("mismas"):   # mismas marginales, otra correlación
        u, v = rng.random(100), rng.random(100)
        uso = uso.assign(distancia=6 * u, hora=8 + 14 * np.mod(u + 0.15 * v, 1))
    adv = {c: ml.validacion_adversarial(d.ent, uso, columnas=list(X), familia=c)
           for c in ("bosque", "logistica")}
    DET[nombre] = (adv, ml.ks_por_variable(d.ent, uso, columnas=["distancia", "hora"]),
                   ml.ajustar(d.ent, phi=PHI), d)

def bloque_2(que, clasificador, valores_p):
    adv, ks, m, d = DET[que]
    fig, ejes = plt.subplots(1, 3, figsize=(15, 4))
    ml.dibujar_adversarial(adv[clasificador], ax=ejes[0])
    ml.dibujar_ks(ks, ax=ejes[1])
    ml.dibujar_residual_tiempo(m, d.val, ax=ejes[2])
    plt.show()
    if valores_p: print(ks.round(3).to_string(index=False))   # supone filas iid

ml.laboratorio(bloque_2, que=ml.selector("Qué cambió", list(ESC), "nada"),
               clasificador=ml.selector("Clasificador", ["bosque", "logistica"]),
               valores_p=ml.interruptor("Mostrar valores p", False))

# %% [codigo] bloque-2-prueba
#@title Comprueba: la señal principal de cada escenario (sin umbral)
for nombre, (adv, ks, m, d) in DET.items():
    a = adv["bosque"]
    print(f"{nombre}: pérdida log {a.log_loss:.3f} contra su benchmark "
          f"{a.log_loss_benchmark:.3f} → {a.senal}; "
          f"MCC (τ = ō = {a.o_bar:.2f}) {a.mcc:.2f}")

# %% [texto] bloque-2-mira

# %% [texto] bloque-2-explica

# %% [texto] bloque-3-predice

# %% [codigo] bloque-3-juega
#@title Juega: la validación cruzada que miente
CLASE2 = {13: lambda df: ml.ajustar_otro(df, familia="vecinos", columnas_x=["x", "t"],
                                         n_vecinos=5),       # los modelos de la clase 2
          14: lambda df: ml.ajustar(df, phi=ml.combinar(
              ml.polinomio(3), ml.dummies("grupo", codificacion="efectos")))}
FUERZA = {13: lambda a: {"persistencia": 0.9 * a}, 14: lambda a: {"desv_grupo": 5 * a}}
TABLAS = {}
for caso, rot, sep in ((14, "clientes que repiten", "grupo"),
                       (13, "días seguidos", "temporal")):
    for fuerza in (0.25, 0.5, 0.75, 1.0):
        d = ml.caso(caso, n=300, semilla=SEMILLA, **FUERZA[caso](fuerza))
        dev = pd.concat([d.ent, d.val])
        dev.attrs = d.ent.attrs
        filas = []
        for modelo, construir in (("lineal en x", lambda df: ml.ajustar(df)),
                                  ("el de la clase 2", CLASE2[caso])):
            R = ml.riesgo(construir(dev), d)
            for nombre, part in (("al azar", "azar"), (sep, sep)):
                cv = ml.validacion_cruzada(d, construir, particion=part).media
                filas.append(dict(modelo=modelo, contrato=rot, separacion=nombre,
                                  estimado=cv, R=R, benchmark=np.nan))
        TABLAS[(rot, fuerza)] = pd.DataFrame(filas)


def bloque_3(datos_caso, fuerza, modelo):
    t = TABLAS[(datos_caso, fuerza)]
    t = t[t["modelo"] == modelo]
    ml.dibujar_contratos(t.drop(columns="modelo"))
    plt.show()
    print(t[["separacion", "estimado", "R"]].round(1).to_string(index=False))


DATOS = ["clientes que repiten", "días seguidos"]
ml.laboratorio(bloque_3, datos_caso=ml.selector("Datos", DATOS, DATOS[0]),
               fuerza=ml.selector("Fuerza", [0.25, 0.5, 0.75, 1.0], 0.75),
               modelo=ml.selector("Modelo", ["lineal en x", "el de la clase 2"],
                                  "el de la clase 2"))

# %% [texto] bloque-3-mira

# %% [texto] bloque-3-explica

# %% [texto] bloque-4-predice

# %% [codigo] bloque-4-juega
#@title Juega: fugas, el número demasiado bueno
llego_tarde = ml.proceso_clasificacion(
    n=600, x={"distancia": ml.uniforme(0.5, 8.0), "hora": ml.uniforme(8.0, 22.0),
              "lluvia": ml.categorica([0, 1], [0.8, 0.2])},
    puntaje=lambda d: (0.6 * (d["distancia"] - 4.0) + 1.5 * d["lluvia"]
                       + 0.04 * (d["hora"] - 15.0) ** 2),
    proporcion=0.25, faltantes={"distancia": (0.3, "depende_x")},
    semilla=SEMILLA, n_realidad=2000)


def construir(df):   # vecinos (1) dentro de una tubería: imputa y escala en el pliegue
    cols = list(df.attrs["ml"]["columnas_x"])
    falta = [f"{c}_falta" for c in cols if df[c].isna().any()]
    phi = ml.estandarizar(ml.columnas(*(cols + falta)))
    return ml.tuberia(ml.imputador(), phi,
                      modelo={"familia": "vecinos", "n_vecinos": 1})(df)


RUTA = {"ninguna": "ninguna", "calificación posterior": "posterior",
        "escalar e imputar antes de separar": "preprocesar_antes",
        "pedidos duplicados": "duplicados"}
FUGAS = ml.medir_fugas(llego_tarde, construir, tipos=list(RUTA.values()),
                       intensidades=(0.5, 1.0), criterio="mcc")


def bloque_4(fuga, intensidad):
    t = FUGAS[FUGAS["intensidad"] == intensidad]
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4))
    ml.dibujar_fugas(t, ax=a)
    d = llego_tarde if RUTA[fuga] == "ninguna" else ml.sembrar_fuga(
        llego_tarde, RUTA[fuga], intensidad)
    m = construir(pd.concat([d.ent]))
    ml.dibujar_importancia(ml.importancia(m, d.val, "mcc"), ax=b)
    plt.show()
    print(t.round(2).to_string(index=False))


ml.laboratorio(bloque_4, fuga=ml.selector("Fuga", list(RUTA), "ninguna"),
               intensidad=ml.selector("Intensidad", [0.5, 1.0], 1.0))

# %% [texto] bloque-4-mira

# %% [texto] bloque-4-explica

# %% [texto] bloque-5-predice

# %% [codigo] bloque-5-juega
#@title Juega: la tubería, todo lo que se ajusta adentro
nada = ml.proceso_clasificacion(        # el caso 26: y no depende de ninguna columna
    n=100, x={"distancia": ml.uniforme(0.5, 8.0), "hora": ml.uniforme(8.0, 22.0),
              "lluvia": ml.categorica([0, 1], [0.8, 0.2])},
    puntaje=lambda d: 0.0 * d["distancia"], proporcion=0.25, semilla=SEMILLA,
    n_realidad=2000)
elegidas = ml.sembrar_fuga(nada, "seleccion_previa")   # 10 de 503, con todas las filas
SIN = {"escalar e imputar antes": (ml.sembrar_fuga(llego_tarde, "preprocesar_antes"),
                                   construir),
       "elegir variables antes": (elegidas, lambda df: ml.ajustar(df))}
CON = {"escalar e imputar antes": (llego_tarde, construir),
       "elegir variables antes": (elegidas, ml.tuberia(
           ml.seleccionar(k=10), modelo={"familia": "logistica"}))}
filas = []
for ruta in SIN:
    for etiqueta, (d, c) in (("sin tubería", SIN[ruta]), ("con tubería", CON[ruta])):
        t = ml.medir_fugas(d, c, tipos=("ninguna",), criterio="mcc")
        filas.append(t.assign(tipo=f"{ruta} · {etiqueta}"))
B5 = pd.concat(filas, ignore_index=True)
B5.attrs["criterio"] = "mcc"


def bloque_5(fuga, dentro):
    etiqueta = "con tubería" if dentro else "sin tubería"
    ml.dibujar_fugas(B5[B5["tipo"].str.startswith(fuga)])
    plt.show()
    print(B5.round(2).to_string(index=False))
    if fuga.startswith("escalar") and dentro:
        ml.imprimir_Phi(construir(llego_tarde.ent), llego_tarde.ent, filas=5)
    print(f"Ahora ves: {fuga} · {etiqueta}")


ml.laboratorio(bloque_5, fuga=ml.selector("Fuga", list(SIN), "elegir variables antes"),
               dentro=ml.interruptor("Ajustar dentro de cada pliegue (tubería)",
                                     False))

# %% [texto] bloque-5-mira

# %% [texto] bloque-5-explica

# %% [texto] taller-intro

# %% [codigo-visible] taller
# Tu proceso: cambia una línea y vuelve a correr la celda
datos = ml.proceso(n=300, x={"distancia": ml.uniforme(0.5, 8)},
                   f=lambda d: 5 + 4 * d.distancia,
                   ruido=ml.efecto_grupo(n_grupos=30, desv_grupo=2.0),
                   separar="azar", despliegue="grupos_nuevos")
# 1) Tiempo: ruido=ml.ar1(persistencia=0.9), despliegue="futuro"
# 2) Otra ciudad: despliegue="otra_poblacion",
#    deriva=lambda t: {"distancia": ml.uniforme(4, 12)}
# 3) Una fuga: datos = ml.sembrar_fuga(datos, tipo="duplicados")
ml.taller(datos, clase=5)

# %% [texto] galeria-intro

# %% [codigo] galeria
#@title Galería: casos que se rompen a la vista
ml.galeria(clase=5, casos=[13, 14, 15, 16, 19, 20, 21, 26, 27, 28])

# %% [texto] ejercicio-pliegue-raro

# %% [texto] ejercicio-pliegue-raro-respuesta

# %% [texto] ejercicio-submuestra

# %% [texto] ejercicio-submuestra-respuesta

# %% [texto] ejercicio-residuos-alternos

# %% [texto] ejercicio-residuos-alternos-respuesta

# %% [texto] cierre
