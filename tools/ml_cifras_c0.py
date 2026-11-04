"""Cifras de la clase 0 de la unidad de aprendizaje de maquina (unidad 9).

Unica fuente de cada numero que citan la pagina `1_que_es_aprender/1_repaso.md`
y las figuras de tools/figuras_ml_c0.py (D-009.5). Solo numpy y fracciones
exactas: no importa ml_lab (la guarda de origen de contrato §5.2 no obliga a
importarlo; si algun dia lo importa, sera de tools/aprendizaje_maquina.py y
nunca de _assets/).

Los datos son las seis entregas de la unidad 6
(course/6_optimizacion/5_practica_de_modelado/4_regresion_practica.md, §3,
«Ver el error en seis entregas»): distancia en km, tiempo en minutos. El
programa «ve» las cuatro primeras y las dos ultimas «llegan despues».

Tres reglas ajustadas solo con las cuatro vistas:
- memorizar: anuncia el tiempo de la entrega vista con la distancia mas
  cercana (vecino mas cercano); en lo visto acierta por construccion;
- el promedio fijo de lo visto (el punto de comparacion, benchmark);
- la recta de minimos cuadrados sobre las cuatro vistas.

Pruebas: tools/test_ml_cifras_c0.py (puras) y tools/test_ml_prosa_c0.py (las
ata a su frase en la pagina).
"""
from fractions import Fraction

import numpy as np

# (km, min) de las seis entregas de la unidad 6, en orden de distancia.
ENTREGAS = ((1, 15), (2, 17), (3, 23), (4, 25), (5, 31), (6, 33))
VISTAS = (0, 1, 2, 3)
NUEVAS = (4, 5)

# DECISIÓN prog-c0 (clase_0.md §10.12): paquetes y zona de cada entrega, para
# la figura con y sin respuesta (ml-c0-con-y-sin-y). Enteros 1-12 y tres
# zonas. En el plano (distancia, paquetes) se ven dos agrupaciones razonables
# y distintas, cada una con su criterio, y ninguna es vistas/nuevas:
# por distancia (cerca: 1-3 km / lejos: 4-6 km) y por paquetes (pocos: 2-3 /
# muchos: 9-11). Ningun texto depende de estos valores.
PAQUETES = (2, 10, 3, 9, 2, 11)
ZONAS = ("centro", "centro", "norte", "sur", "norte", "sur")
CORTE_DISTANCIA_KM = 3.5
CORTE_PAQUETES = 6


def entregas_c0():
    """Los seis pares (km, min) y el corte vistas / nuevas."""
    return {
        "pares": ENTREGAS,
        "vistas": list(VISTAS),
        "nuevas": list(NUEVAS),
    }


def _xy(indices):
    x = np.array([ENTREGAS[i][0] for i in indices], dtype=float)
    y = np.array([ENTREGAS[i][1] for i in indices], dtype=float)
    return x, y


def recta_minimos_cuadrados(indices):
    """(b0, b1) de minimos cuadrados cerrados sobre las entregas `indices`."""
    x, y = _xy(indices)
    xm, ym = x.mean(), y.mean()
    b1 = float(((x - xm) * (y - ym)).sum() / ((x - xm) ** 2).sum())
    b0 = float(ym - b1 * xm)
    return b0, b1


def recta_exacta(indices):
    """La misma recta en fracciones exactas: (b0, b1) como Fraction."""
    xs = [Fraction(ENTREGAS[i][0]) for i in indices]
    ys = [Fraction(ENTREGAS[i][1]) for i in indices]
    n = len(xs)
    xm, ym = sum(xs) / n, sum(ys) / n
    b1 = sum((a - xm) * (b - ym) for a, b in zip(xs, ys)) / sum((a - xm) ** 2 for a in xs)
    return ym - b1 * xm, b1


def anuncio_memorizar(km, vistas=VISTAS):
    """Tiempo de la entrega vista con la distancia mas cercana."""
    i = min(vistas, key=lambda j: (abs(ENTREGAS[j][0] - km), ENTREGAS[j][0]))
    return float(ENTREGAS[i][1])


def _mae(anuncios, indices):
    _, y = _xy(indices)
    return float(np.abs(np.asarray(anuncios, dtype=float) - y).mean())


def cifras_c0_memorizar():
    """Anuncios y MAE de las tres reglas en las vistas y en las nuevas."""
    xv, _ = _xy(VISTAS)
    xn, _ = _xy(NUEVAS)
    _, yv = _xy(VISTAS)
    promedio = float(yv.mean())
    b0, b1 = recta_minimos_cuadrados(VISTAS)
    reglas = {
        "memorizar": (
            [anuncio_memorizar(k) for k in xv],
            [anuncio_memorizar(k) for k in xn]),
        "promedio": ([promedio] * len(xv), [promedio] * len(xn)),
        "recta": ([b0 + b1 * k for k in xv], [b0 + b1 * k for k in xn]),
    }
    salida = {}
    for nombre, (en_vistas, en_nuevas) in reglas.items():
        salida[nombre] = {
            "anuncios_vistas": en_vistas,
            "anuncios_nuevas": en_nuevas,
            "mae_vistas": _mae(en_vistas, VISTAS),
            "mae_nuevas": _mae(en_nuevas, NUEVAS),
        }
    salida["beta_estrella"] = (b0, b1)
    salida["beta_seis"] = recta_minimos_cuadrados(VISTAS + NUEVAS)
    salida["beta_seis_exacta"] = recta_exacta(VISTAS + NUEVAS)
    salida["promedio_vistas"] = promedio
    return salida


def cifras_c0_curva():
    """(Tramo completo, F6.) MAE en las dos nuevas de la recta ajustada con
    las primeras 2, 3 y 4 vistas: {n: (b0, b1, mae)}. No es monotona."""
    curva = {}
    for n in (2, 3, 4):
        indices = VISTAS[:n]
        b0, b1 = recta_minimos_cuadrados(indices)
        xn, _ = _xy(NUEVAS)
        curva[n] = (b0, b1, _mae([b0 + b1 * k for k in xn], NUEVAS))
    return curva


def cifras_c0_paquetes():
    """Paquetes y zona de las seis entregas y las dos agrupaciones de F2,
    cada una con su criterio (listas de indices de ENTREGAS)."""
    todos = range(len(ENTREGAS))
    return {
        "paquetes": PAQUETES,
        "zonas": ZONAS,
        "agrupaciones": {
            "por distancia": {
                "criterio": f"cerca: hasta {CORTE_DISTANCIA_KM:g} km / lejos: mas",
                "corte": CORTE_DISTANCIA_KM,
                "grupos": (
                    [i for i in todos if ENTREGAS[i][0] < CORTE_DISTANCIA_KM],
                    [i for i in todos if ENTREGAS[i][0] > CORTE_DISTANCIA_KM]),
            },
            "por paquetes": {
                "criterio": f"pocos: menos de {CORTE_PAQUETES} / muchos: mas",
                "corte": CORTE_PAQUETES,
                "grupos": (
                    [i for i in todos if PAQUETES[i] < CORTE_PAQUETES],
                    [i for i in todos if PAQUETES[i] > CORTE_PAQUETES]),
            },
        },
    }


def datos_c0_ejercicios():
    """Constantes de los enunciados (las ata la prueba de prosa)."""
    return {
        "por_semana": 10,
        "mae_visto": (3, 1),
        "semanas": 4,
        "mae_nuevo": 6,
        "entregas_zona": 200,
    }


# El ejemplo de representacion de §3: phi(x) = (1, x, x^2) en 3 km.
PHI_EJEMPLO_KM = 3


def phi_cuadratica(x):
    """La representacion elegida a mano de §3: (1, x, x^2)."""
    return (1, x, x ** 2)


def redondeo(x):
    """Como se escribe una cifra en la pagina: una cifra decimal, sin .0."""
    r = round(float(x), 1)
    return str(int(r)) if r == int(r) else str(r)


if __name__ == "__main__":
    c = cifras_c0_memorizar()
    for regla in ("memorizar", "recta", "promedio"):
        print(f"{regla:10s} vistas {redondeo(c[regla]['mae_vistas']):>4s}  "
              f"nuevas {redondeo(c[regla]['mae_nuevas']):>4s}  "
              f"anuncios nuevas {[redondeo(a) for a in c[regla]['anuncios_nuevas']]}")
    print("beta* =", tuple(redondeo(b) for b in c["beta_estrella"]),
          " seis =", c["beta_seis_exacta"])
    print("curva =", {n: redondeo(v[2]) for n, v in cifras_c0_curva().items()})
