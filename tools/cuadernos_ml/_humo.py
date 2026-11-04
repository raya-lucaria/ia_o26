# Notebook de humo de la unidad 9 (contrato §8.3 U.T4). No se publica: existe
# para probar el generador y el cargador de ml_lab de punta a punta. Solo usa
# lo mínimo de ml_lab (VERSION, requiere, tema), para no depender de 1.0.

# %% [texto] portada

# %% [texto] idea

# %% [texto] bloque-1-predice

# %% [codigo] bloque-1-juega
#@title Juega: ¿qué versión cargó la celda de arranque?
SEMILLA = 0
x, y = ml.VERSION.split(".")
print(f"ml_lab cargado: versión {ml.VERSION} (X = {x}, Y = {y})")
ml.requiere(ml.VERSION)

# %% [texto] bloque-1-mira

# %% [texto] bloque-1-explica

# %% [texto] taller-intro

# %% [codigo-visible] taller
# Cambia el número y corre la celda: ¿la acepta requiere?
version_pedida = ml.VERSION
ml.requiere(version_pedida)
print("requiere aceptó", version_pedida)

# %% [texto] cierre
