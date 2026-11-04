# Tarea 2 de la unidad 9 · Separar, elegir y reportar (clase 2). Código y
# orden de celdas: prog-c2 (clase_2.md §10.6). El texto de cada celda
# [texto] vive en tarea_2_separar_y_elegir.texto.md (guion de Codex).
# Sin -explica ni respuestas. El proceso se escribe aquí con piezas de ml_lab
# (contrato §5.13): f(x) = 10 + 12/x, x ~ U(1, 5), ruido N(0, 2²), n = 150, con
# un contrato iid explícito. Cada alumno pone su semilla (últimos cuatro
# dígitos de su clave única). Leen la prueba el bloque 4 (el reporte, una vez)
# y el bloque 6 (el engaño, a propósito); el 4 está pedido a coord para la
# lista cerrada de §6.6 regla 8 (SOLICITUD prog-c2-4).

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo-visible] bloque-1-juega
SEMILLA = 0   # ← escribe aquí los últimos cuatro dígitos de tu clave única

import warnings
import numpy as np, pandas as pd, matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

# Contrato: «se usará con entregas nuevas de esta misma ciudad, sacadas igual
# que la muestra». Por eso la separación es al azar: 80 % desarrollo, 20 % prueba.
datos = ml.proceso(n=150, x={"x": ml.uniforme(1, 5)}, f=lambda d: 10 + 12 / d.x,
                   ruido=ml.normal(0, 2), fracciones=(0.8, 0, 0.2), semilla=SEMILLA)
print(f"desarrollo: {len(datos.ent)} entregas · prueba: {len(datos.prueba)} (cerrada)")
ml.dibujar_proceso(datos, mostrar_f=False)
plt.show()

# %% [texto] bloque-1-mira

# %% [texto] entrega-1

# %% [texto] bloque-2-predice

# %% [codigo-visible] bloque-2-juega
# Antes de correr nada más, escribe tus tres apuestas (números).
MIS_APUESTAS = {
    "grado que elegirá la CV": None,
    "L_prueba del modelo final (min²)": None,
    "L_prueba del benchmark (min²)": None,
}
for que, valor in MIS_APUESTAS.items():
    print(f"{que}: {'¡falta tu apuesta!' if valor is None else valor}")

# %% [texto] bloque-2-mira

# %% [texto] entrega-2

# %% [texto] bloque-3-predice

# %% [codigo-visible] bloque-3-juega
ORDEN = list(range(13))     # declarado ANTES de medir: de simple (0) a complejo (12)
REGLA = "un_ee"             # o "minimo": decide antes de ver la tabla
candidatos = {N: (lambda df, N=N: ml.ajustar(df, phi=ml.polinomio(N))) for N in ORDEN}
sel = ml.elegir(datos, candidatos, con="cv", k=5, regla=REGLA, orden_complejidad=ORDEN)
print(sel.tabla.round(3).to_string(index=False))
N_hat = sel.elegido if REGLA == "minimo" else sel.elegido_un_ee
print(f"CV_5: el mínimo elige N = {sel.elegido}; la de un EE, N = {sel.elegido_un_ee}")
print(f"uso la regla «{REGLA}»: N̂ = {N_hat}")
ml.dibujar_cv(sel)
plt.show()

# %% [texto] bloque-3-mira

# %% [texto] entrega-3

# %% [texto] bloque-4-predice

# %% [codigo-visible] bloque-4-juega
# abre-prueba: el reporte final, una sola vez y con el modelo ya fijado
final = sel.modelo_final                       # reajustado con todo el desarrollo
media_ent = datos.ent["y"].mean()              # el benchmark: la media de entrenamiento
y = datos.prueba["y"].to_numpy()
l_mod = np.asarray(ml.perdida(y, final.predecir(datos.prueba)), float)
l_ben = (y - media_ent) ** 2
for nombre, l in (("modelo final", l_mod), ("benchmark", l_ben)):
    print(f"prueba ({len(y)}): {nombre}: L_prueba = {l.mean():.2f}"
          f" ± {2 * ml.error_estandar(l):.2f} (2 EE)")
d, ee = ml.diferencia_pareada(l_mod, l_ben)
print(f"diferencia pareada «modelo − benchmark» en prueba: {d:.2f} (EE {ee:.2f});"
      f" le gana por más de 2 EE: {'sí' if d + 2 * ee < 0 else 'no'}")

# %% [texto] bloque-4-mira

# %% [texto] entrega-4

# %% [texto] bloque-5-predice

# %% [codigo-visible] bloque-5-juega
# Una celda siembra un pliegue anómalo: dos entregas lejanas, a 9 y 10 km.
rng = np.random.default_rng(SEMILLA)
lejanas = pd.DataFrame({"x": [9.0, 10.0]})
lejanas["y"] = 10 + 12 / lejanas["x"] + rng.normal(0, 2, 2)
auditar = pd.concat([datos.ent, lejanas], ignore_index=True)
auditar.attrs = datos.ent.attrs
for k in (3, 5, 20):
    res = {N: ml.validacion_cruzada(auditar, candidatos[N], k=k) for N in (1, 4, 8)}
    ml.dibujar_cajas_pliegues(res)
    plt.yscale("log"); plt.title(f"k = {k}: {13 * k + 1} ajustes para 13 grados")
    plt.show()

# %% [texto] bloque-5-mira

# %% [texto] entrega-5

# %% [texto] bloque-6-predice

# %% [codigo] bloque-6-juega
# abre-prueba: el engaño, medido a propósito
#@title Elige con la prueba para medir cuánto te habrías engañado
def fabrica(s):
    return ml.proceso(n=150, x={"x": ml.uniforme(1, 5)}, f=lambda d: 10 + 12 / d.x,
                      ruido=ml.normal(0, 2), fracciones=(0.6, 0.2, 0.2), semilla=s,
                      n_realidad=2000)


largo = ml.optimismo_por_seleccion(fabrica, candidatos, repeticiones=200,
                                   semilla=SEMILLA, detalle=True)   # ~25 s
t = largo.sort_values(["repeticion", "candidato"])
elegidos = t.loc[t.groupby("repeticion")["L_prueba"].idxmin()]
engano = (elegidos["L_prueba"] - elegidos["R"]).to_numpy()
ml.dibujar_histograma_estimaciones(engano, verdadero=0, etiqueta="anunciado − real")
plt.show()
print(f"sesgo medio eligiendo con la prueba: {engano.mean():.2f}"
      f" ± {engano.std(ddof=1) / np.sqrt(len(engano)):.2f} (EE de Monte Carlo)")
print("tu reporte del bloque 4 no cambió: esta celda no lo toca")

# %% [texto] bloque-6-mira

# %% [texto] entrega-6

# %% [texto] cierre
