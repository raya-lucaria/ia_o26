# Tarea 3 de la unidad 9 · Cincuenta variables y una decisión defendible
# (clase 3). Código y orden de celdas: prog-c3 (clase_3.md §10.6.1). El texto
# de cada celda [texto] vive en tarea_3_cincuenta_variables.texto.md (guion de
# Codex). Sin -explica ni respuestas. El proceso se escribe aquí con piezas de
# ml_lab (contrato §5.13): 50 variables normales, 5 útiles con coeficientes
# (3, −2, 1.5, 1, 0.5) en unidades estándar, x6 gemela de x1 (corr 0.95), ruido
# N(0, 1), n = 300 (180 de entrenamiento), escalas de 1e-4 a 1e5. Cada alumno
# pone su semilla (últimos cuatro dígitos de su clave única). Lee la prueba
# solo el bloque 6, una vez (contrato §6.6 regla 8).

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo-visible] bloque-1-juega
SEMILLA = 0   # ← escribe aquí los últimos cuatro dígitos de tu clave única

import warnings
import numpy as np, pandas as pd, matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

J = 50
x = {f"x{j}": ml.normal() for j in range(1, J + 1)}
ESCALAS = {f"x{j}": 10.0 ** ((j % 10) - 4) for j in range(1, J + 1)}  # 1e-4 … 1e5
COEF = {"x1": 3.0, "x2": -2.0, "x3": 1.5, "x4": 1.0, "x5": 0.5}  # en unidades estándar
f = lambda d: sum(c * d[v] for v, c in COEF.items())
datos = ml.proceso(n=300, x=x, f=f, ruido=ml.normal(0, 1),
                   correlacion={("x1", "x6"): 0.95},   # x6: gemela de x1, no está en f
                   escala=ESCALAS, semilla=SEMILLA)
COLUMNAS = ml.columnas(*[f"x{j}" for j in range(1, J + 1)])
n_prueba = 300 - len(datos.ent) - len(datos.val)    # la prueba ni se toca aquí
print(f"ent: {len(datos.ent)} · val: {len(datos.val)} · prueba: {n_prueba}"
      " (cerrada hasta el bloque 6)")
cinco = ml.ajustar(datos, phi=ml.columnas("x1", "x2", "x3", "x4", "x5"))
ml.imprimir_Phi(cinco, datos.ent, filas=5)
print("desviación de cada columna en ent (sus unidades):")
print(datos.ent[[f"x{j}" for j in range(1, 11)]].std().map("{:.3g}".format).to_string())

# %% [texto] bloque-1-mira

# %% [texto] entrega-1

# %% [texto] bloque-2-predice

# %% [codigo-visible] bloque-2-juega
mc = ml.ajustar(datos, phi=COLUMNAS)          # mínimos cuadrados con las 50, en ent
print(f"mínimos cuadrados: L_ent = {ml.L(mc, datos.ent):.3f}"
      f" · L_val = {ml.L(mc, datos.val):.3f}")
ml.dibujar_tres_paneles(mc, datos.val)        # las tres vistas, en validación
plt.show()
ml.dibujar_benchmarks(mc, datos)              # contra la media y la mediana de ent
plt.show()
print(ml.benchmarks(datos, datos.val).round(3).to_string())
y = datos.val["y"].to_numpy()
l_mc = (y - mc.predecir(datos.val)) ** 2
l_media = (y - datos.ent["y"].mean()) ** 2
d, ee = ml.diferencia_pareada(l_mc, l_media)
print(f"diferencia pareada «mínimos cuadrados − media» en val: {d:.3f} (EE {ee:.3f});"
      f" le gana por más de 2 EE: {'sí' if d + 2 * ee < 0 else 'no'}")

# %% [texto] bloque-2-mira

# %% [texto] entrega-2

# %% [texto] bloque-3-predice

# %% [codigo-visible] bloque-3-juega
MUS = [float(m) for m in np.logspace(-2, 1, 16)]   # la rejilla de μ
PHI = ml.estandarizar(COLUMNAS)   # se estandariza dentro de cada pliegue
candidatos = {mu: (lambda df, mu=mu: ml.ajustar(df, phi=PHI, mu=mu, penalizacion="l1"))
              for mu in MUS}
REGLA = "un_ee"                       # o "minimo": decide antes de ver la curva
# logspace va de μ chica a grande; sin esta línea la regla de un EE leería al revés
sel = ml.elegir(datos, candidatos, con="cv", k=5, regla=REGLA,
                orden_complejidad=sorted(MUS, reverse=True))   # simple → complejo
mu_hat = sel.elegido if REGLA == "minimo" else sel.elegido_un_ee
print(f"CV_5: el mínimo elige μ = {sel.elegido:.3g};"
      f" la de un EE, μ = {sel.elegido_un_ee:.3g}")
print(f"uso la regla «{REGLA}»: μ̂ = {mu_hat:.3g}")
ml.dibujar_cv(sel, log=True)
plt.show()

# %% [texto] bloque-3-mira

# %% [texto] entrega-3

# %% [texto] bloque-4-predice

# %% [codigo-visible] bloque-4-juega
PENALIZACION = "l1"   # prueba también "elastica" (con rho=0.5 en las dos llamadas)
UTILES = ["x1", "x2", "x3", "x4", "x5", "x6"]
tabla = ml.trayectorias(datos, PHI, PENALIZACION, np.logspace(-2, 1, 40))
ml.dibujar_trayectorias(tabla, utiles=UTILES, marcar_mu=mu_hat)
plt.show()
m = ml.ajustar(datos, phi=PHI, mu=mu_hat, penalizacion=PENALIZACION)
verdadero = ml.beta_verdadero(datos, PHI)
comparar = pd.DataFrame({"β̂": m.beta_gorro, "verdadero": verdadero})
print(comparar.loc[UTILES + ["x7", "x8"]].round(3).to_string())
print(f"coeficientes ≠ 0 (ajuste con entrenamiento, {len(datos.ent)} filas):"
      f" {int((m.beta_gorro.drop('1') != 0).sum())} de {J}")


def otra_muestra(s):                  # el mismo proceso, otra semilla
    return ml.proceso(n=300, x=x, f=f, ruido=ml.normal(0, 1), escala=ESCALAS,
                      correlacion={("x1", "x6"): 0.95}, semilla=s, con_realidad=False)


veces = ml.beta_repetido(otra_muestra, PHI, 100, semilla=SEMILLA + 1, mu=mu_hat,
                         penalizacion=PENALIZACION)          # unos segundos
dos = ((veces["x1"] != 0) & (veces["x6"] != 0)).mean()
print(f"de 100 muestras: conserva x1 {100 * (veces['x1'] != 0).mean():.0f} veces,"
      f" x6 {100 * (veces['x6'] != 0).mean():.0f} y las dos {100 * dos:.0f}")

# %% [texto] bloque-4-mira

# %% [texto] entrega-4

# %% [texto] bloque-5-predice

# %% [codigo-visible] bloque-5-juega
# El mismo procedimiento, sin estandarizar: Ω suma |β_j| en las unidades de cada x
crudos = {mu: (lambda df, mu=mu: ml.ajustar(df, phi=COLUMNAS, mu=mu, penalizacion="l1"))
          for mu in MUS}
sel_crudo = ml.elegir(datos, crudos, con="cv", k=5, regla=REGLA,
                      orden_complejidad=sorted(MUS, reverse=True))
mu_crudo = sel_crudo.elegido if REGLA == "minimo" else sel_crudo.elegido_un_ee
b = ml.ajustar(datos, phi=COLUMNAS, mu=mu_crudo, penalizacion="l1").beta_gorro
desv = datos.ent[list(COEF)].std()
print(f"sin estandarizar, CV_5 elige μ = {mu_crudo:.3g}")
print(pd.DataFrame({"desviación de x": desv, "β̂ en sus unidades": b[list(COEF)],
                    "¿viva?": b[list(COEF)] != 0}).to_string())

# %% [texto] bloque-5-mira

# %% [texto] entrega-5

# %% [texto] bloque-6-predice

# %% [codigo-visible] bloque-6-juega
# abre-prueba: la prueba se abre una vez, con el procedimiento congelado
final = sel.modelo_final          # el de tu regla, reajustado con ent ∪ val
prueba = datos.prueba
y = prueba["y"].to_numpy()
l_mod = (y - final.predecir(prueba)) ** 2
media = pd.concat([datos.ent, datos.val])["y"].mean()   # el benchmark, fijado igual
l_med = (y - media) ** 2
ee_l = ml.error_estandar(l_mod)
print(f"prueba ({len(y)}): L_prueba = {l_mod.mean():.3f} ± {2 * ee_l:.3f}"
      f" (2 EE) · la media: {l_med.mean():.3f}")
d, ee = ml.diferencia_pareada(l_mod, l_med)
print(f"diferencia pareada «modelo − media» en prueba: {d:.3f} (EE {ee:.3f});"
      f" le gana por más de 2 EE: {'sí' if d + 2 * ee < 0 else 'no'}")
print(f"R (despliegue, 100 000 obs.) = {ml.riesgo(final, datos):.3f}")
print(f"coeficientes ≠ 0 del modelo final (reajuste con ent ∪ val,"
      f" {len(datos.ent) + len(datos.val)} filas): "
      f"{int((final.beta_gorro.drop('1') != 0).sum())} de {J}")

# %% [texto] bloque-6-mira

# %% [texto] entrega-6

# %% [texto] ejercicio-nueva-regularizacion

# %% [texto] cierre
