# Tarea 4 de la unidad 9 · Tres desenlaces y uno que importa (clase 4).
# Código y orden de celdas: prog-c4 (clase_4.md §10.6). El texto de cada celda
# [texto] vive en tarea_4_desbalanceo_multiclase.texto.md (guion de Codex). Sin
# -explica ni respuestas. El proceso se escribe aquí con piezas de ml_lab
# (contrato §5.13): crédito con tres desenlaces —al corriente (0), atraso (1),
# impago (2)— en proporciones ≈ 90/8/2. Mapa único de reservas (§10.6): cal
# sale primero de datos.val, luego val_a y val_b; ninguna llamada de los
# bloques 1–5 recibe datos.val (salvo para partirlo), cal ni la prueba, y cada
# conjunto que se usa queda anotado en USADOS. Lee la prueba solo el bloque 6,
# una vez (contrato §6.6 regla 8). Ningún resultado de aquí entra a ml_cifras_c4.

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo-visible] bloque-1-juega
SEMILLA = 0          # ← o los últimos cuatro dígitos de tu clave única
CRITERIO = "mcc"     # ← tu métrica principal: decídela antes de ver nada

import warnings
import numpy as np, pandas as pd, matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

N = 10_000
datos = ml.proceso_clasificacion(
    n=N, K=3,
    x={"uso": ml.uniforme(0, 1),
       "atrasos_previos": ml.categorica([0, 1, 2, 3], [0.6, 0.25, 0.1, 0.05]),
       "ingreso": ml.lognormal(0, 0.5)},
    puntajes=[lambda d: 0 * d.uso,                                     # al corriente
              lambda d: 2.5 * d.uso + 0.6 * d.atrasos_previos,         # atraso
              lambda d: 4.0 * d.uso**2 + 1.0 * d.atrasos_previos
              - 0.8 * np.log(d.ingreso)],                              # impago
    proporcion=[0.90, 0.08, 0.02], separar="estratificado",
    fracciones=(0.5, 0.3, 0.2), semilla=SEMILLA)
# El mapa de reservas, antes de cualquier selección: cal PRIMERO
cal, resto = ml.partir(datos.val, 1 / 3, como="estratificado", semilla=SEMILLA + 1)
val_a, val_b = ml.partir(resto, 0.5, como="estratificado", semilla=SEMILLA + 2)
USADOS = {}          # cada conjunto que pasa a una llamada queda anotado aquí
RESERVAS = {"ent": datos.ent, "cal": cal, "val_a": val_a, "val_b": val_b}
cuenta = pd.DataFrame({r: d["y"].value_counts() for r, d in RESERVAS.items()})
cuenta = cuenta.reindex([0, 1, 2]).fillna(0).T
ax = cuenta.plot.barh(stacked=True, figsize=(8, 2.6), log=False)
ax.set_xlabel("casos (0 al corriente · 1 atraso · 2 impago)")
ax.set_title("Las reservas que ya existen (la prueba sigue cerrada)")
plt.show()

# %% [codigo] bloque-1-prueba
#@title Comprueba: tamaños, conteos por clase y que las reservas no se tocan
n_prueba = N - len(datos.ent) - len(datos.val)     # la prueba ni se abre aquí
print(cuenta.astype(int).assign(total=cuenta.sum(axis=1).astype(int)).to_string())
print(f"prueba: {n_prueba} casos (cerrada hasta el bloque 6)")
indices = {r: set(d.index) for r, d in RESERVAS.items()}
cruces = sum(len(indices[a] & indices[b]) for a in indices for b in indices if a < b)
print(f"índices compartidos entre ent, cal, val_a y val_b: {cruces}")
assert cruces == 0
assert indices["cal"] | indices["val_a"] | indices["val_b"] == set(datos.val.index)

# %% [texto] bloque-1-mira

# %% [texto] entrega-1

# %% [texto] bloque-2-predice

# %% [codigo-visible] bloque-2-juega
# La moda y la proporción se ajustan en datos.ent y se evalúan en val_b
bm = ml.benchmarks(datos, val_b, criterios=("mcc", "aciertos_balanceados",
                                             "aciertos", "logaritmica"))
USADOS["benchmarks"] = val_b
print("benchmark en val_b:")
print(bm.round(3).to_string())

# %% [texto] bloque-2-mira

# %% [texto] entrega-2

# %% [texto] bloque-3-predice

# %% [codigo-visible] bloque-3-juega
FORMA = "lineal"     # ← corre el bloque con "lineal" y luego con "cuadrática"
LINEAL = ["uso", "atrasos_previos", "ingreso"]
FORMAS = {"lineal": LINEAL,
          "cuadrática": LINEAL + ["uso**2", "atrasos_previos**2",
                                  "uso*atrasos_previos", "log(ingreso)"]}
PHI = ml.estandarizar(ml.columnas(*FORMAS[FORMA]))   # se ajusta en cada pliegue
MUS = [1.0, 0.1, 0.01, 1e-3, 1e-4]                   # de simple a complejo
candidatos = {(pesos, mu): (lambda df, p=pesos, mu=mu: ml.ajustar(
                  df, phi=PHI, mu=mu, penalizacion="l2", pesos=p))
              for pesos in (None, "balanceado") for mu in MUS}
# Sobre datos.ent, no sobre datos: con un Datos, la CV se comería val y cal
sel = ml.elegir(datos.ent, candidatos, con="cv", k=5, particion="estratificado",
                criterio=CRITERIO, orden_complejidad=list(candidatos))
USADOS["elegir"] = datos.ent
tabla = sel.tabla.assign(candidato=sel.tabla["candidato"].map(str))
print(f"φ {FORMA} · CV estratificada con k = 5 en ent · criterio: {CRITERIO}")
print(tabla.round(3).to_string(index=False))   # ee: dispersión entre pliegues
PESOS, MU = sel.elegido
modelo = sel.modelo
print(f"elegido: pesos = {PESOS} · μ = {MU:g}")

# %% [texto] bloque-3-mira

# %% [texto] entrega-3

# %% [texto] bloque-4-predice

# %% [codigo-visible] bloque-4-juega
CLASES = [0, 1, 2]
NOMBRES = {0: "al corriente", 1: "atraso", 2: "impago"}
y = val_b["y"]
soporte = y.value_counts().reindex(CLASES, fill_value=0)
fig, ejes = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
for ax, pesos in zip(ejes, (None, "balanceado")):     # el mismo φ y el mismo μ
    m = ml.ajustar(datos.ent, phi=PHI, mu=MU, penalizacion="l2", pesos=pesos)
    y_gorro = m.predecir(val_b)
    serie = ml.por_clase("aciertos", y, y_gorro, clases=CLASES)
    ml.dibujar_promedios(serie, soporte, ax=ax)
    ax.set_title(f"pesos = {pesos} · aciertos por clase en val_b")
    macro = ml.promediar("aciertos", y, y_gorro, como="macro", clases=CLASES)
    pond = ml.promediar("aciertos", y, y_gorro, como="ponderado", clases=CLASES)
    print(f"pesos = {pesos}: " + " · ".join(
        f"{NOMBRES[k]} {v:.3f}" for k, v in serie.items())
        + f" · macro {macro:.3f} · ponderado {pond:.3f}"
        + f" · MCC {ml.mcc(y, y_gorro, clases=CLASES):.3f}")
plt.show()
for f in ("por_clase", "promediar", "mcc"):
    USADOS[f] = val_b

# %% [texto] bloque-4-mira

# %% [texto] entrega-4

# %% [texto] bloque-5-predice

# %% [codigo-visible] bloque-5-juega
recal = ml.recalibrar(modelo, val_a)          # se ajusta en val_a…
USADOS["recalibrar"] = val_a
P, Q = modelo.predecir_prob(val_b), recal.predecir_prob(val_b)   # …y se mira en val_b
fig, ejes = plt.subplots(1, 3, figsize=(13, 4))
for k, ax in zip(CLASES, ejes):               # cada clase contra el resto
    yk = (val_b["y"] == k).astype(int)
    ml.dibujar_calibracion({"antes": ml.calibracion(P[:, k], yk, bins=5),
                            "recalibrado": ml.calibracion(Q[:, k], yk, bins=5)}, ax=ax)
    ax.set_title(f"{NOMBRES[k]} contra el resto (val_b)")
plt.show()
USADOS["calibracion"] = val_b
# El precio, simplificado: prestar 1 un periodo; impago → 0, si no → 1 + tasa
tipico = pd.DataFrame({"uso": [0.5], "atrasos_previos": [0],
                       "ingreso": [datos.ent["ingreso"].median()]})
for nombre, m in (("antes", modelo), ("recalibrado", recal)):
    p2 = m.predecir_prob(tipico)[0, 2]
    print(f"{nombre}: p̂ de impago del cliente típico = {p2:.3f}"
          f" → tasa de equilibrio p̂/(1 − p̂) = {p2 / (1 - p2):.3f}")

# %% [codigo] bloque-5-prueba
#@title Comprueba: cal y prueba intactas
dentro = set(datos.ent.index) | set(datos.val.index)
cerrados = set(cal.index) | (set(range(N)) - dentro)    # cal y la prueba
compartidos = sum(len(cerrados & set(d.index)) for d in USADOS.values())
for f, d in USADOS.items():
    print(f"{f:>12}: {len(d)} casos")
print(f"cal y prueba intactas: {compartidos} índices compartidos")
assert compartidos == 0

# %% [texto] bloque-5-mira

# %% [texto] entrega-5

# %% [texto] bloque-6-predice

# %% [codigo-visible] bloque-6-juega
# Congela todo antes de abrir la prueba: después de esta celda no se cambia nada
ETIQUETAS = modelo            # la regla que decide la clase (con o sin pesos)
PROBABILIDADES = recal        # ← o `modelo`, si en el bloque 5 decidiste no recalibrar
DELTA = 0.1                   # para el conformal por clase (opcional)
print(f"congelado: φ {FORMA} · pesos = {PESOS} · μ = {MU:g} · "
      f"probabilidades {'recalibradas' if PROBABILIDADES is recal else 'crudas'}")

# %% [codigo] bloque-6-prueba
# abre-prueba: la tarea abre la prueba una sola vez con todo congelado
#@title Abre la prueba, una vez
prueba = datos.prueba
y = prueba["y"].to_numpy()
acierto = (np.asarray(ETIQUETAS.predecir(prueba)) == y).astype(float)
P = PROBABILIDADES.predecir_prob(prueba)
l_log = -np.log(np.clip(P[np.arange(len(y)), y], 1e-15, 1))   # pérdida por caso
for nombre, l in (("pérdida logarítmica", l_log), ("aciertos A", acierto)):
    print(f"{nombre}: {l.mean():.3f} ± {2 * ml.error_estandar(l):.3f} (2 EE)")
for crit in ("mcc", "aciertos_balanceados"):
    inc = ml.incertidumbre(ETIQUETAS, prueba, crit, estratificar=False)
    a, b = inc.intervalo
    print(f"{crit}: {inc.valor:.3f}, intervalo 2.5–97.5 [{a:.3f}, {b:.3f}]"
          f" (bootstrap {inc.esquema}, {inc.repeticiones} réplicas)")
conf = ml.conformal(PROBABILIDADES, cal, delta=DELTA, por_clase=True)
print("conformal por clase (con el modelo congelado, intercambiables dentro de"
      " cada clase):")
print(conf.cobertura_por_clase(prueba).round(3).to_string())

# %% [texto] bloque-6-mira

# %% [texto] entrega-6

# %% [texto] cierre
