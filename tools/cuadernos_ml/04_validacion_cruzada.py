# Notebook 04 de la unidad 9 · Validación cruzada (acompaña
# ml-validacion-cruzada, clase 2). Código y orden de celdas: prog-c2
# (clase_2.md §10.3 NB04). El texto de cada celda [texto] vive en
# 04_validacion_cruzada.texto.md (guion de Codex). Las cifras que el guion
# cita salen de tools/ml_cifras_c2.py con estas mismas constantes.
# Ninguna celda lee la prueba: la CV rota dentro del desarrollo (ent ∪ val).

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo] bloque-1-juega
#@title Juega: los pliegues, dibujados
import warnings
import numpy as np, pandas as pd, matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
SEMILLA = 0
construir = lambda N: (lambda df, N=N: ml.ajustar(df, phi=ml.polinomio(N)))
CANDIDATOS = {N: construir(N) for N in range(13)}
DATOS = ml.PROCESOS["entregas_curvas"](n=60, semilla=SEMILLA)
DESARROLLO = pd.concat([DATOS.ent, DATOS.val])          # 48 entregas; la prueba no rota
DESARROLLO.attrs = DATOS.ent.attrs


def bloque_1(k, m):
    m = min(m, k)
    part = ml.pliegues(DESARROLLO, k=k, semilla=SEMILLA)
    ajuste, valida = part[m - 1]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4))
    ml.dibujar_pliegues(len(DESARROLLO), k, m_activo=m, prueba=True, particion=part,
                        ax=a1)
    df_aj, df_va = DESARROLLO.iloc[ajuste], DESARROLLO.iloc[valida]
    a2.scatter(df_aj["x"], df_aj["y"], marker="o", label=f"ajusta ({len(ajuste)})")
    a2.scatter(df_va["x"], df_va["y"], marker="^", s=60,
               label=f"valida ({len(valida)})")
    modelo = construir(4)(df_aj)
    malla = pd.DataFrame({"x": np.linspace(0, 6, 300)})
    a2.plot(malla["x"], modelo.predecir(malla), label=f"grado 4 sin el pliegue {m}")
    a2.set_xlabel("x (km)"); a2.set_ylabel("y (min)"); a2.legend()
    plt.show()
    print(f"vuelta {m} de {k}: ajusta con {len(ajuste)} entregas y valida con"
          f" {len(valida)}; L del pliegue = {ml.L(modelo, df_va):.2f}")


ml.laboratorio(bloque_1, k=ml.deslizador("pliegues k", 2, 10, 1, 5),
               m=ml.deslizador("vuelta m", 1, 10, 1, 1))

# %% [texto] bloque-1-mira

# %% [texto] bloque-1-explica

# %% [texto] bloque-2-predice

# %% [codigo] bloque-2-juega
#@title Juega: CV contra el grado, con barras
def bloque_2(k, regla, semilla, ver_R):
    datos = ml.PROCESOS["entregas_curvas"](n=60, semilla=semilla)
    s = ml.elegir(datos, CANDIDATOS, con="cv", k=k, regla=regla,
                  orden_complejidad=list(range(13)))
    des = pd.concat([datos.ent, datos.val]); des.attrs = datos.ent.attrs
    bench = (s.cv[0].media, s.cv[0].ee)                  # N = 0: la media de ent
    R = {N: ml.riesgo(c(des), datos) for N, c in CANDIDATOS.items()} if ver_R else None
    L_ent = {N: ml.L(c(des), des) for N, c in CANDIDATOS.items()}   # como R
    ml.dibujar_cv(s, R=R, L_ent=L_ent, piso=ml.piso(datos) if ver_R else None,
                  benchmark=bench)
    plt.yscale("log")
    plt.show()
    t = s.tabla.set_index("candidato")
    N_min, N_ee = s.elegido, s.elegido_un_ee
    print(f"CV_{k}: mínimo en N = {N_min} ({t.loc[N_min, 'valor']:.2f} ±"
          f" {t.loc[N_min, 'ee']:.2f}); la regla de un EE elige N = {N_ee}")
    print(f"benchmark (N = 0, la media de entrenamiento): CV {bench[0]:.2f} ±"
          f" {bench[1]:.2f}")
    print(f"ajustes: {s.costo_ajustes} (= 13·{k} + 1)")
    if ver_R:
        mejor = min(R, key=R.get)
        print(f"con esta semilla, el mejor R es el del grado {mejor} ({R[mejor]:.2f});"
              f" el elegido tiene R = {R[s.elegido if regla == 'minimo' else N_ee]:.2f}"
              )


ml.laboratorio(bloque_2, k=ml.selector("k", [3, 5, 10], 5),
               regla=ml.selector("regla", {"mínimo": "minimo", "un EE": "un_ee"}),
               semilla=ml.deslizador("semilla", 0, 20, 1, SEMILLA),
               ver_R=ml.interruptor("mostrar la realidad R", False))

# %% [texto] bloque-2-mira

# %% [texto] bloque-2-explica

# %% [texto] bloque-3-predice

# %% [codigo] bloque-3-juega
#@title Juega: CV contra una sola validación
def una_muestra(s):
    d = ml.PROCESOS["entregas_curvas"](n=60, semilla=s, n_realidad=2000)
    m = construir(4)(d)
    lv = np.asarray(ml.perdida(d.val["y"], m.predecir(d.val)), float)
    cv = ml.validacion_cruzada(d, construir(4), k=5)
    return {"L_val": lv.mean(), "ee_val": ml.error_estandar(lv), "cv": cv.media,
            "ee_cv": cv.ee, "R": ml.riesgo(m, d)}


T_B3 = ml.repetir(una_muestra, repeticiones=200, semilla=SEMILLA)


def bloque_3(estimador):
    series = {"una validación (12)": T_B3["L_val"], "CV_5 (48)": T_B3["cv"]}
    if estimador != "ambos":
        series = {k: v for k, v in series.items() if k.startswith(estimador)}
    ml.dibujar_histograma_estimaciones({k: v.to_numpy() for k, v in series.items()},
                                       verdadero=T_B3["R"].mean(),
                                       etiqueta="estimación")
    plt.show()
    print(f"E_D[R] ≈ {T_B3['R'].mean():.2f} (200 muestras)")
    print(f"una validación: desviación real {T_B3['L_val'].std():.2f}, EE medio"
          f" reportado {T_B3['ee_val'].mean():.2f}; 1 ajuste")
    print(f"CV_5: desviación real {T_B3['cv'].std():.2f}, EE medio reportado"
          f" {T_B3['ee_cv'].mean():.2f}; 5 ajustes")


ml.laboratorio(bloque_3, estimador=ml.selector(
    "estimador", ["una validación", "CV_5", "ambos"]))

# %% [texto] bloque-3-mira

# %% [texto] bloque-3-explica

# %% [texto] bloque-4-predice

# %% [codigo] bloque-4-juega
#@title Juega: mirar dentro de los pliegues
UMBRAL_MIN = 5.0                     # minutos: «error grande»


def var_residual(y, y_gorro):        # dentro del pliegue, divisor tamaño − 1
    return float(np.var(np.asarray(y) - np.asarray(y_gorro), ddof=1))


def prop_grandes(y, y_gorro):
    return float(np.mean(np.abs(np.asarray(y) - np.asarray(y_gorro)) > UMBRAL_MIN))


ESTADISTICOS = {"pérdida cuadrática": None, "varianza del residual": var_residual,
                f"proporción de errores > {UMBRAL_MIN:g} min": prop_grandes}
DATOS_B4 = {"entregas": DATOS, "caso 16": ml.caso(16)}


def bloque_4(estadistico, cual):
    f = ESTADISTICOS[estadistico]
    res = {N: ml.validacion_cruzada(DATOS_B4[cual], construir(N), k=5, estadistico=f)
           for N in (0, 1, 4, 8)}                    # N = 0: el benchmark
    ml.dibujar_cajas_pliegues(res, estadistico=f is not None)
    plt.yscale("log" if f is None else "linear")
    plt.show()
    for N, r in res.items():
        v = r.por_pliegue if f is None else r.por_pliegue_estadistico
        print(f"grado {N}: " + ", ".join(f"{x:.2f}" for x in v)
              + f"   (media {np.mean(v):.2f})")


ml.laboratorio(bloque_4, estadistico=ml.selector("estadístico", list(ESTADISTICOS)),
               cual=ml.selector("datos", list(DATOS_B4), "caso 16"))

# %% [texto] bloque-4-mira

# %% [texto] bloque-4-explica

# %% [texto] bloque-5-predice

# %% [codigo] bloque-5-juega
#@title Juega: estratificar
def vacios(df, k, como, particiones=1000):
    y = df["y"].to_numpy()
    parts = (ml.pliegues(df, k=k, como=como, semilla=s) for s in range(particiones))
    return np.mean([any(y[v].sum() == 0 for _, v in p) for p in parts])


def bloque_5(positivos, k, como):
    y = np.r_[np.ones(positivos, int), np.zeros(60 - positivos, int)]
    df = pd.DataFrame({"y": y})
    part = ml.pliegues(df, k=k, como=como, semilla=SEMILLA)
    ml.dibujar_pliegues(60, k, prueba=False, y=df["y"], particion=part)
    plt.show()
    print("positivos por pliegue: " + ", ".join(str(int(y[v].sum())) for _, v in part))
    print(f"en 1000 particiones: al azar {vacios(df, k, 'azar'):.1%}, estratificada"
          f" {vacios(df, k, 'estratificado'):.1%} con algún pliegue sin positivos")


ml.laboratorio(bloque_5, positivos=ml.deslizador("positivos", 1, 12, 1, 6),
               k=ml.selector("k", [3, 5, 10], 5),
               como=ml.selector("pliegues", {"al azar": "azar",
                                             "estratificados": "estratificado"}))

# %% [texto] bloque-5-mira

# %% [texto] bloque-5-explica

# %% [texto] bloque-6-predice

# %% [codigo] bloque-6-juega
#@title Juega: CV anidada, en corto
CANDS_B6 = {N: construir(N) for N in range(9)}


def una_anidada(s):
    d = ml.PROCESOS["entregas_curvas"](n=60, semilla=s, n_realidad=2000)
    sel = ml.elegir(d, CANDS_B6, con="cv", k=5)
    an = ml.cv_anidada(d, CANDS_B6, k_externo=5, k_interno=5)
    des = pd.concat([d.ent, d.val]); des.attrs = d.ent.attrs
    rng = np.random.default_rng(s)
    sub = des.iloc[np.sort(rng.choice(len(des), size=len(des) * 4 // 5, replace=False))]
    sub.attrs = des.attrs
    proc = ml.elegir(sub, CANDS_B6, con="cv", k=5)
    cv_ganador = sel.tabla.set_index("candidato").loc[sel.elegido, "valor"]
    return {"CV del ganador": cv_ganador, "anidada": an.media,
            "R del procedimiento (4/5)": ml.riesgo(proc.modelo_final, d),
            "R del modelo final": ml.riesgo(sel.modelo_final, d),
            "R del benchmark": ml.riesgo(CANDS_B6[0](des), d)}


T_B6 = ml.repetir(una_anidada, repeticiones=30, semilla=SEMILLA)   # ~30 s, una vez


def bloque_6(repeticiones):
    t = T_B6.iloc[:repeticiones].drop(columns=["repeticion", "semilla"])
    medias, ee = t.mean(), t.std(ddof=1) / np.sqrt(len(t))
    plt.errorbar(range(len(medias)), medias, yerr=2 * ee, fmt="o", capsize=4)
    plt.xticks(range(len(medias)), [c.replace(" (", "\n(").replace("del ", "del\n")
                                    for c in t.columns], fontsize=8)
    plt.axvline(2.5, ls=":", color="gray")
    plt.ylabel("pérdida promedio"); plt.show()
    for c in t.columns:
        print(f"{c}: {medias[c]:.2f} ± {2 * ee[c]:.2f} (2 EE de Monte Carlo)")


ml.laboratorio(bloque_6, repeticiones=ml.selector("repeticiones", [10, 20, 30], 30))

# %% [texto] bloque-6-mira

# %% [texto] bloque-6-explica

# %% [texto] taller-intro

# %% [codigo-visible] taller
datos = ml.PROCESOS["entregas_curvas"](n=60, semilla=0)
# 1) otra f:   datos = ml.proceso(n=60, x={"x": ml.uniforme(0, 6)},
#                                 f=lambda d: 10 + 12 / (1 + d.x))
# 2) caso 16:  datos = ml.caso(16)
# 3) k chico contra k grande: cambia k=10 por k=3
ml.taller(datos, clase=2, que="elegir", k=10, regla="un_ee")

# %% [texto] galeria-intro

# %% [codigo] galeria
#@title Galería: casos que se rompen a la vista
ml.galeria(clase=2)

# %% [texto] ejercicio-cinco-pliegues

# %% [texto] ejercicio-cinco-pliegues-respuesta

# %% [texto] cierre
