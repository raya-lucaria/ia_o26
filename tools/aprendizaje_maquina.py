"""ml_lab · el laboratorio de la unidad de aprendizaje de máquina.

Un solo archivo que se lee de arriba abajo: piezas aleatorias, procesos que
generan datos con una f conocida, representaciones Φ, el ajuste, las pérdidas
y las gráficas que usan las páginas y los notebooks. Todo lo aleatorio recibe
una `semilla`; la población (la muestra enorme `realidad` y la de uso
`despliegue`) no cambia con ella.

Uso: import ml_lab as ml; datos = ml.PROCESOS["entregas"](); m = ml.ajustar(datos)
"""

# === 0 · Versión y tema ===

VERSION = "1.0"

import ast  # noqa: E402
import copy  # noqa: E402
import inspect  # noqa: E402
import math  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import warnings  # noqa: E402
from collections import OrderedDict  # noqa: E402
from dataclasses import dataclass  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import optimize, special, stats  # noqa: E402

__all__ = [
    "VERSION", "CAMBIOS", "NoAplica", "requiere",
    # 1 · piezas
    "Pieza", "Mecanismo", "normal", "uniforme", "categorica",
    # 2 · procesos
    "Datos", "proceso", "anillos", "PROCESOS", "CasoBorde", "CASOS_BORDE", "caso",
    # 4 · representaciones
    "Phi", "polinomio", "columnas", "polares", "periodicas", "dummies", "combinar", "taylor",
    # 5 · ajuste
    "Modelo", "ajustar", "ajustar_otro",
    # 6 · pérdidas y métricas
    "perdida", "Criterio", "SENTIDO", "evaluar", "L", "riesgo", "desempeno", "piso", "mse",
    "aciertos", "benchmarks",
    # 8 · capacidad
    "curva_capacidad",
    # 9 · regularización
    "beta_verdadero",
    # 12 · gráficas
    "ROLES", "tema", "dibujar_proceso", "dibujar_ajuste", "dibujar_frontera", "imprimir_Phi",
    "dibujar_curva_capacidad", "dibujar_tres_paneles", "dibujar_piso", "dibujar_perdida_1d",
    # 13 · interactividad
    "laboratorio", "deslizador", "selector", "interruptor", "galeria", "taller",
    "ANALISIS_TALLER",
]


class NoAplica(TypeError):
    """La capacidad no existe para esta familia («un árbol no tiene matriz de diseño»)."""


def _version(texto):
    x, y = str(texto).split(".")
    return int(x), int(y)


def requiere(version_minima):
    """Exige que el ml_lab cargado sea compatible con la versión pedida.

    Compatible = la misma X y una Y mayor o igual. Si no, lanza un error.
    Ejemplo: ml.requiere("1.0")
    """
    xc, yc = _version(VERSION)
    xp, yp = _version(version_minima)
    if xc != xp or yc < yp:
        raise RuntimeError(
            f"Este notebook pide ml_lab {version_minima} y se cargó la versión {VERSION}: "
            "vuelve a correr la celda de arranque."
        )


# === 1 · Piezas aleatorias ===


class Pieza:
    """Una distribución independiente: sirve para una variable x o como ruido.

    Plantilla para agregar una en el taller (tres líneas):
        class Mia(ml.Pieza):
            nombre, media, varianza = "mia", 0.0, 1.0
            def muestrear(self, n, rng): return rng.laplace(0, 1 / 2**0.5, n)
    """

    nombre = "pieza"
    media = float("nan")
    varianza = float("nan")  # inf si es infinita; nan solo si no se conoce

    def muestrear(self, n, rng):
        raise NotImplementedError("una Pieza define muestrear(n, rng)")

    def __repr__(self):
        return f"{self.nombre}()"


class Mecanismo:
    """Un ruido que depende del contexto (crea columnas como "t" o "grupo").

    Dos pasos: preparar(n, rng) crea las columnas de contexto; muestrear(df, rng)
    saca el ruido dado un DataFrame con todas las variables y el contexto.
    Ejemplo: los trae la clase 2 (ar1, efecto_grupo).
    """

    nombre = "mecanismo"
    crea = []

    def preparar(self, n, rng):
        return {}

    def muestrear(self, df, rng):
        raise NotImplementedError("un Mecanismo define muestrear(df, rng)")

    def varianza_en(self, df):
        return np.full(len(df), np.nan)

    def __repr__(self):
        return f"{self.nombre}()"


class _Normal(Pieza):
    def __init__(self, media, desv):
        if desv < 0:
            raise ValueError("la desviación de normal() no puede ser negativa")
        self.media, self.desv = float(media), float(desv)
        self.varianza = self.desv ** 2
        self.nombre = "normal"
        self._desv_abs = self.desv * math.sqrt(2 / math.pi)  # E|ε − mediana|

    def muestrear(self, n, rng):
        return rng.normal(self.media, self.desv, n)

    def _cuantil(self, u):
        return stats.norm.ppf(u, self.media, self.desv)

    def __repr__(self):
        return f"normal(media={self.media}, desv={self.desv})"


class _Uniforme(Pieza):
    def __init__(self, a, b):
        if b < a:
            raise ValueError("uniforme(a, b) pide a <= b")
        self.a, self.b = float(a), float(b)
        self.media = (self.a + self.b) / 2
        self.varianza = (self.b - self.a) ** 2 / 12
        self.nombre = "uniforme"
        self._desv_abs = (self.b - self.a) / 4

    def muestrear(self, n, rng):
        return rng.uniform(self.a, self.b, n)

    def _cuantil(self, u):
        return self.a + (self.b - self.a) * np.asarray(u)

    def __repr__(self):
        return f"uniforme(a={self.a}, b={self.b})"


class _Categorica(Pieza):
    def __init__(self, categorias, probs):
        self.categorias = list(categorias)
        k = len(self.categorias)
        if k == 0:
            raise ValueError("categorica() necesita al menos una categoría")
        p = np.full(k, 1 / k) if probs is None else np.asarray(probs, float)
        if len(p) != k or np.any(p < 0) or not np.isclose(p.sum(), 1):
            raise ValueError("probs debe tener una probabilidad por categoría y sumar 1")
        self.probs = p
        self.nombre = "categorica"
        if all(isinstance(c, (int, float, np.integer, np.floating)) and not isinstance(c, bool)
               for c in self.categorias):
            v = np.asarray(self.categorias, float)
            self.media = float(p @ v)
            self.varianza = float(p @ (v - self.media) ** 2)

    def muestrear(self, n, rng):
        idx = rng.choice(len(self.categorias), size=n, p=self.probs)
        return np.asarray(self.categorias, dtype=object)[idx].tolist() if self._texto() else \
            np.asarray(self.categorias)[idx]

    def _texto(self):
        return any(isinstance(c, str) for c in self.categorias)

    def _cuantil(self, u):
        idx = np.searchsorted(np.cumsum(self.probs), np.asarray(u), side="right")
        return np.asarray(self.categorias)[np.minimum(idx, len(self.categorias) - 1)]

    def __repr__(self):
        return f"categorica(categorias={self.categorias!r}, probs={self.probs.tolist()!r})"


def normal(media=0.0, desv=1.0):
    """Pieza normal con esa media y desviación estándar.

    Ejemplo: ruido = ml.normal(0, 2)
    """
    return _Normal(media, desv)


def uniforme(a=0.0, b=1.0):
    """Pieza uniforme en [a, b].

    Ejemplo: x = {"x": ml.uniforme(0, 6)}
    """
    return _Uniforme(a, b)


def categorica(categorias, probs=None):
    """Pieza que elige una categoría (por omisión, todas igual de probables).

    Ejemplo: x = {"lluvia": ml.categorica([0, 1])}
    """
    return _Categorica(categorias, probs)


# === 2 · Procesos y casos borde ===


@dataclass(repr=False)
class Datos:
    """Lo que devuelve un proceso: la muestra partida y la población.

    ent, val, prueba: la muestra (columnas_x, "y" y el contexto; nunca oráculos).
    realidad: muestra enorme del proceso de entrenamiento; despliegue: la de uso,
    contra la que se calcula R. Ejemplo: datos.ent.head()
    """

    ent: pd.DataFrame
    val: pd.DataFrame
    prueba: pd.DataFrame
    realidad: pd.DataFrame
    despliegue: pd.DataFrame
    f: object
    f_visible: object
    columnas_x: list
    columnas_contexto: list
    oraculos: list
    omitidas: list
    tarea: str
    K: object
    clases: object
    sigma2_e: float
    separacion: str
    despliegue_como: str
    semilla: int
    semilla_realidad: int
    descripcion: str
    columnas_universo: object = None

    def __repr__(self):
        return (f"Datos({self.descripcion!r}: ent={len(self.ent)}, val={len(self.val)}, "
                f"prueba={len(self.prueba)}, columnas_x={self.columnas_x}, tarea={self.tarea!r})")


def _f_por_omision(d):
    return 1 + 2 * d["x"]


def _meta(columnas_x, contexto, tarea, K, clases):
    return {"columnas_x": list(columnas_x), "columnas_contexto": list(contexto),
            "tarea": tarea, "K": K, "clases": None if clases is None else list(clases)}


def _con_meta(df, meta):
    df.attrs["ml"] = copy.deepcopy(meta)
    return df


class _Poblacion:
    """Lo que define una población de regresión: x, f, ruido y sus arreglos."""

    tarea = "regresion"

    def __init__(self, x, f, ruido, correlacion, endogeno, omitir, escala, f_visible_cerrada):
        self.x = dict(x)
        if not self.x:
            raise ValueError("x necesita al menos una variable")
        for nombre, pieza in self.x.items():
            if not isinstance(pieza, Pieza):
                raise ValueError(f"x[{nombre!r}] debe ser una Pieza (normal, uniforme, ...)")
        self.f = f
        self.mecanismo = ruido if isinstance(ruido, Mecanismo) else None
        if self.mecanismo is None and not isinstance(ruido, Pieza):
            raise ValueError("ruido debe ser una Pieza o un Mecanismo")
        self.ruido = ruido
        self.correlacion = dict(correlacion or {})
        for (a, b), r in self.correlacion.items():
            if a not in self.x or b not in self.x:
                raise ValueError(f"correlacion nombra una variable que no está en x: {(a, b)}")
            if not -1 < r < 1:
                raise ValueError("cada correlación debe estar en (-1, 1)")
        self.endogeno = float(endogeno)
        if not -1 < self.endogeno < 1:
            raise ValueError("endogeno es una correlación: debe estar en (-1, 1)")
        self.omitidas = list(omitir or [])
        for o in self.omitidas:
            if o not in self.x:
                raise ValueError(f"omitir nombra {o!r}, que no está en x")
        self.visibles = [k for k in self.x if k not in self.omitidas]
        if not self.visibles:
            raise ValueError("el modelo tiene que ver al menos una variable")
        self.escala = dict(escala or {})
        for k in self.escala:
            if k != "y" and k not in self.x:
                raise ValueError(f"escala nombra {k!r}, que no está en x ni es 'y'")
        self.c_y = float(self.escala.get("y", 1.0))
        self.var_endogena = "x1" if "x1" in self.x else next(iter(self.x))
        if self.endogeno and self.mecanismo is not None:
            raise ValueError("endogeno solo se combina con un ruido que sea Pieza")
        self.cerrada = f_visible_cerrada
        self.contexto = list(getattr(self.mecanismo, "crea", []) or [])
        self.tipo = self._tipo_f_visible()
        self.J = 200  # sorteos de Monte Carlo sobre las omitidas (f_visible)

    def llave(self):
        return ("reg", id(self.f), id(self.cerrada), repr(self.x), repr(self.ruido),
                repr(sorted(self.correlacion.items())), self.endogeno, tuple(self.omitidas),
                repr(sorted(self.escala.items())))

    def _tipo_f_visible(self):
        if self.cerrada is not None:
            return "cerrada"
        if not self.omitidas:
            return "directa"
        if self.endogeno and self.var_endogena in self.omitidas:
            return None
        for (a, b) in self.correlacion:
            if (a in self.omitidas) != (b in self.omitidas):
                return None
        return "mc"

    def sigma2_e(self):
        if self.mecanismo is not None:
            return float("nan")
        return float(self.ruido.varianza) * self.c_y ** 2

    def _x(self, n, rng):
        valores = {}
        grupo = []
        for (a, b) in self.correlacion:
            for v in (a, b):
                if v not in grupo:
                    grupo.append(v)
        if grupo:
            C = np.eye(len(grupo))
            for (a, b), r in self.correlacion.items():
                i, j = grupo.index(a), grupo.index(b)
                C[i, j] = C[j, i] = r
            z = rng.multivariate_normal(np.zeros(len(grupo)), C, size=n, method="cholesky")
            u = stats.norm.cdf(z)
            for i, v in enumerate(grupo):
                pieza = self.x[v]
                if not hasattr(pieza, "_cuantil"):
                    raise ValueError(f"la pieza de {v!r} no sabe su cuantil: no entra en correlacion")
                valores[v] = pieza._cuantil(u[:, i])
        for v, pieza in self.x.items():
            if v not in valores:
                valores[v] = pieza.muestrear(n, rng)
        return {v: np.asarray(valores[v]) for v in self.x}

    def _evaluar_f(self, df):
        return np.asarray(self.f(df), dtype=float).reshape(-1) * np.ones(len(df))

    def _media_ruido(self, xs):
        """E[ε | todas las x] y Var(ε | todas las x), antes de escalar y."""
        n = len(next(iter(xs.values())))
        if self.mecanismo is not None:
            return np.zeros(n), None
        mr, vr = float(self.ruido.media), float(self.ruido.varianza)
        if not np.isfinite(mr):
            mr = 0.0
        if self.endogeno:
            pieza = self.x[self.var_endogena]
            z1 = (np.asarray(xs[self.var_endogena], float) - pieza.media) / math.sqrt(pieza.varianza)
            return mr + self.endogeno * math.sqrt(vr) * z1, np.full(n, (1 - self.endogeno ** 2) * vr)
        return np.full(n, mr), np.full(n, vr)

    def completo(self, n, rng):
        xs = self._x(n, rng)
        ctx = self.mecanismo.preparar(n, rng) if self.mecanismo is not None else {}
        todo = pd.DataFrame({**xs, **ctx})
        fval = self._evaluar_f(todo)
        m, v = self._media_ruido(xs)
        if self.mecanismo is not None:
            eps = np.asarray(self.mecanismo.muestrear(todo, rng), float)
            v = np.asarray(self.mecanismo.varianza_en(todo), float)
        else:
            u = np.asarray(self.ruido.muestrear(n, rng), float)
            if self.endogeno:
                mr = float(self.ruido.media) if np.isfinite(self.ruido.media) else 0.0
                eps = m + math.sqrt(1 - self.endogeno ** 2) * (u - mr)
            else:
                eps = u
        df = pd.DataFrame(index=pd.RangeIndex(n))
        for k in self.visibles:
            df[k] = xs[k] * self.escala.get(k, 1.0) if k in self.escala else xs[k]
        for k in self.omitidas:
            df[k] = xs[k]
        for k in ctx:
            df[k] = ctx[k]
        df["y"] = (fval + eps) * self.c_y
        df["_f"] = fval * self.c_y
        df["_m"] = m * self.c_y
        df["_v"] = v * self.c_y ** 2
        return df

    def _sin_escala(self, df):
        d = df.copy()
        for k, c in self.escala.items():
            if k != "y" and k in d:
                d[k] = d[k] / c
        return d

    def f_estructural(self, df):
        return self._evaluar_f(self._sin_escala(df)) * self.c_y

    def _m_visible(self, df):
        d = self._sin_escala(df)
        xs = {self.var_endogena: d[self.var_endogena].to_numpy()} if self.endogeno else {
            next(iter(self.x)): np.zeros(len(d))}
        if not self.endogeno:
            m = 0.0 if self.mecanismo is not None else float(self.ruido.media)
            return np.full(len(d), (m if np.isfinite(m) else 0.0) * self.c_y)
        return self._media_ruido(xs)[0] * self.c_y

    def _sorteos_omitidas(self, semilla_realidad):
        """J sorteos de las omitidas, estratificados (hipercubo latino) cuando se puede,
        para que la media sobre ellos no arrastre el error de un sorteo al azar."""
        rng = np.random.default_rng([semilla_realidad, 4])
        al_azar = self._x(self.J, rng)
        enlazadas = {v for par in self.correlacion for v in par}
        sorteos = {}
        for o in self.omitidas:
            pieza = self.x[o]
            if hasattr(pieza, "_cuantil") and o not in enlazadas:
                u = (rng.permutation(self.J) + rng.uniform(size=self.J)) / self.J
                sorteos[o] = np.asarray(pieza._cuantil(u))
            else:
                sorteos[o] = al_azar[o]
        return sorteos

    def _repetir_f(self, d, sorteos, J, paso_filas=None):
        """f en cada fila de d con J valores de las omitidas; sorteos[o] es (J,) o (n, J)."""
        n = len(d)
        salida = np.empty((n, J))
        paso = paso_filas or max(1, 2_000_000 // J)
        cols = [c for c in d.columns if c not in self.omitidas]
        for i in range(0, n, paso):
            bloque = d.iloc[i:i + paso]
            k = len(bloque)
            rep = {c: np.repeat(bloque[c].to_numpy(), J) for c in cols}
            for o in self.omitidas:
                s = sorteos[o]
                rep[o] = np.tile(s, k) if s.ndim == 1 else s[i:i + k].reshape(-1)
            salida[i:i + k] = self._evaluar_f(pd.DataFrame(rep)).reshape(k, J)
        return salida

    def _mc(self, df_visible, semilla_realidad):
        """E[f | lo visible] por fila: media sobre J sorteos comunes de las omitidas."""
        d = self._sin_escala(df_visible)
        vals = self._repetir_f(d, self._sorteos_omitidas(semilla_realidad), self.J)
        return vals.mean(axis=1) * self.c_y

    def _var_omitidas(self, df_visible, semilla_realidad, K=16):
        """Var(f | lo visible) por fila, con K sorteos frescos por fila (sin sesgo:
        el error de cada fila se promedia al sacar el piso)."""
        d = self._sin_escala(df_visible)
        n = len(d)
        xs = self._x(n * K, np.random.default_rng([semilla_realidad, 5]))
        sorteos = {o: np.asarray(xs[o]).reshape(n, K) for o in self.omitidas}
        vals = self._repetir_f(d, sorteos, K)
        return vals.var(axis=1, ddof=1) * self.c_y ** 2

    def f_visible(self, df, semilla_realidad=0):
        if self.tipo == "cerrada":
            return np.asarray(self.cerrada(df), float).reshape(-1) * np.ones(len(df))
        if self.tipo == "directa":
            return self.f_estructural(df) + self._m_visible(df)
        if self.tipo == "mc":
            return self._mc(df, semilla_realidad) + self._m_visible(df)
        raise ValueError("f_visible no se puede calcular en este proceso")

    def oraculos(self, completo, semilla_realidad):
        out = {"f": completo["_f"].to_numpy()}
        vis = completo[self.visibles + self.contexto]
        if self.tipo == "directa":
            out["f_visible"] = completo["_f"].to_numpy() + completo["_m"].to_numpy()
        elif self.tipo == "cerrada":
            out["f_visible"] = self.f_visible(vis)
        elif self.tipo == "mc":
            out["f_visible"] = self._mc(vis, semilla_realidad) + completo["_m"].to_numpy()
            out["_varmc"] = self._var_omitidas(vis, semilla_realidad)
        return out

    def nombres_oraculos(self):
        return ["f"] + (["f_visible"] if self.tipo else [])

    def piso(self, desp, perdida):
        if perdida == "logaritmica":
            raise ValueError("la pérdida logarítmica es de clasificación; aquí es regresión")
        if perdida == "cuadratica":
            if self.mecanismo is None and math.isinf(self.ruido.varianza):
                return float("inf")
            if self.tipo is None or (self.endogeno and not isinstance(self.ruido, _Normal)):
                return None
            v = desp["_v"].to_numpy()
            if self.tipo == "directa":
                return float(np.mean(v))
            if self.tipo == "mc":
                return float(np.mean(desp["_varmc"]) + np.mean(v))
            dif = desp["_f"] + desp["_m"] - desp["f_visible"]
            return float(np.mean(dif ** 2) + np.mean(v))
        if perdida == "absoluta":
            if self.mecanismo is None and math.isinf(self.ruido.varianza):
                return float("inf") if getattr(self.ruido, "nombre", "") == "cauchy" else None
            if self.tipo == "directa" and not self.endogeno and hasattr(self.ruido, "_desv_abs"):
                return float(self.ruido._desv_abs * abs(self.c_y))
            return None
        raise ValueError(f"perdida debe ser 'cuadratica', 'absoluta' o 'logaritmica', no {perdida!r}")


class _PoblacionAnillos:
    """Dos anillos: y=1 el exterior. Radio ~ N(R_y, grosor²), ángulo uniforme,
    más ruido gaussiano isótropo de desviación `ruido` en cada coordenada."""

    tarea = "clasificacion"
    visibles = ["x1", "x2"]
    omitidas = []
    contexto = []
    tipo = "directa"
    c_y = 1.0

    def __init__(self, radio_interior, radio_exterior, grosor, ruido):
        if not 0 <= radio_interior < radio_exterior:
            raise ValueError("anillos pide 0 <= radio_interior < radio_exterior")
        if grosor < 0 or ruido < 0:
            raise ValueError("grosor y ruido no pueden ser negativos")
        self.R = (float(radio_interior), float(radio_exterior))
        self.g, self.s = float(grosor), float(ruido)
        self._malla = None

    def llave(self):
        return ("anillos", self.R, self.g, self.s)

    def sigma2_e(self):
        return float("nan")

    def _densidad(self, rho, R):
        g, s = self.g, self.s
        if s < max(g / 10, 1e-9):
            if g == 0:
                return np.exp(-((rho - R) / max(s, 1e-9)) ** 2 / 2)
            return stats.norm.pdf(rho, R, g) + stats.norm.pdf(-rho, R, g)
        if g > 0:
            t = np.linspace(-7, 7, 281)
            rs = np.abs(R + g * t)
            pesos = stats.norm.pdf(t)
            pesos = pesos / pesos.sum()
        else:
            rs, pesos = np.array([R]), np.array([1.0])
        K = np.exp(-(rho[:, None] - rs) ** 2 / (2 * s * s)) * special.i0e(rho[:, None] * rs / (s * s))
        return K @ pesos / (2 * math.pi * s * s)

    def prob(self, df):
        rho = np.hypot(np.asarray(df["x1"], float), np.asarray(df["x2"], float))
        if self._malla is None:
            tope = self.R[1] + 9 * (self.g + self.s) + 1e-6
            malla = np.linspace(0, tope, 3000)
            d0, d1 = self._densidad(malla, self.R[0]), self._densidad(malla, self.R[1])
            tot = d0 + d1
            p = np.where(tot > 0, d1 / np.where(tot > 0, tot, 1), (malla > np.mean(self.R)) * 1.0)
            self._malla = (malla, p)
        malla, p = self._malla
        return np.interp(rho, malla, p, right=1.0)

    def completo(self, n, rng):
        y = rng.integers(0, 2, n)
        r = np.where(y == 1, self.R[1], self.R[0]) + self.g * rng.normal(size=n)
        th = rng.uniform(0, 2 * math.pi, n)
        e = self.s * rng.normal(size=(n, 2))
        df = pd.DataFrame({"x1": r * np.cos(th) + e[:, 0], "x2": r * np.sin(th) + e[:, 1], "y": y})
        return df

    def f_estructural(self, df):
        return self.prob(df)

    def f_visible(self, df, semilla_realidad=0):
        return self.prob(df)

    def oraculos(self, completo, semilla_realidad):
        return {"prob": self.prob(completo)}

    def nombres_oraculos(self):
        return ["prob"]

    def piso(self, desp, perdida):
        if perdida != "logaritmica":
            raise ValueError("en clasificación el piso de 1.0 es con perdida='logaritmica'")
        p = np.clip(desp["prob"].to_numpy(), 1e-300, 1)
        q = np.clip(1 - desp["prob"].to_numpy(), 1e-300, 1)
        return float(np.mean(-(desp["prob"] * np.log(p) + (1 - desp["prob"]) * np.log(q))))


_CACHE = OrderedDict()
_CACHE_MAX = 12


def _poblacion_grande(pob, n_realidad, semilla_realidad):
    """Las dos muestras enormes (completas, con columnas privadas), en caché."""
    llave = (pob.llave(), n_realidad, semilla_realidad)
    if llave in _CACHE:
        _CACHE.move_to_end(llave)
        return _CACHE[llave][1]
    salida = []
    for flujo in (1, 2):
        c = pob.completo(n_realidad, np.random.default_rng([semilla_realidad, flujo]))
        for k, v in pob.oraculos(c, semilla_realidad).items():
            c[k] = v
        salida.append(c)
    _CACHE[llave] = (pob, tuple(salida))  # guarda pob para que su id no se reuse
    while len(_CACHE) > _CACHE_MAX:
        _CACHE.popitem(last=False)
    return tuple(salida)


def _publica(completo, columnas):
    return completo[[c for c in columnas if c in completo.columns]].copy()


def _partir_indices(n, fracciones, rng, estratos=None):
    fr = tuple(float(v) for v in fracciones)
    if len(fr) != 3 or min(fr) < 0 or not math.isclose(sum(fr), 1.0, abs_tol=1e-9):
        raise ValueError("fracciones son tres números no negativos que suman 1, p. ej. (0.6, 0.2, 0.2)")
    grupos = [np.arange(n)] if estratos is None else [
        np.flatnonzero(estratos == v) for v in np.unique(estratos)]
    partes = ([], [], [])
    for idx in grupos:
        perm = idx[rng.permutation(len(idx))]
        k = len(idx)
        a = min(k, int(round(k * fr[0])))
        b = min(k, a + int(round(k * fr[1])))
        if fr[2] == 0:  # lo que sobra por redondeo no cae en una parte pedida vacía
            if fr[1] == 0:
                a = b = k
            else:
                b = k
        for i, trozo in enumerate((perm[:a], perm[a:b], perm[b:])):
            partes[i].append(trozo)
    return tuple(np.sort(np.concatenate(p)) for p in partes)


_SEPARAR = ("azar", "tiempo", "grupo", "estratificado")
_DESPLIEGUE = ("igual", "futuro", "grupos_nuevos", "otra_poblacion")


def _validar_adelantos(separar, despliegue, deriva, faltantes, permitidos=("azar",)):
    if deriva is not None and despliegue == "igual":
        raise ValueError('`deriva` solo vale con despliegue="futuro" u "otra_poblacion"')
    if separar not in _SEPARAR:
        raise ValueError(f"separar debe ser uno de {_SEPARAR}, no {separar!r}")
    if despliegue not in _DESPLIEGUE:
        raise ValueError(f"despliegue debe ser uno de {_DESPLIEGUE}, no {despliegue!r}")
    if separar not in permitidos:
        raise NotImplementedError(f'separar="{separar}" llega con la versión de la clase 2')
    if despliegue != "igual":
        raise NotImplementedError(f'despliegue="{despliegue}" llega con la versión de la clase 2')
    if deriva is not None:
        raise NotImplementedError("`deriva` llega con la versión de la clase 2")
    if faltantes is not None:
        raise NotImplementedError("`faltantes` llega con la versión de la clase 4")


def _armar(pob, muestra, fracciones, rng_particion, separar, n_realidad, semilla,
           semilla_realidad, con_realidad, descripcion, rehacer, K=None, clases=None):
    cols_x = list(pob.visibles)
    ctx = list(pob.contexto)
    meta = _meta(cols_x, ctx, pob.tarea, K, clases)
    publicas = cols_x + ["y"] + ctx
    estratos = muestra["y"].to_numpy() if separar == "estratificado" else None
    i_ent, i_val, i_pru = _partir_indices(len(muestra), fracciones, rng_particion, estratos)
    partes = [_con_meta(muestra.iloc[i][publicas].copy(), meta) for i in (i_ent, i_val, i_pru)]
    columnas_grandes = cols_x + list(pob.omitidas) + ctx + ["y"] + pob.nombres_oraculos()
    if con_realidad:
        real_c, desp_c = _poblacion_grande(pob, n_realidad, semilla_realidad)
        realidad = _con_meta(_publica(real_c, columnas_grandes), meta)
        desp = _con_meta(_publica(desp_c, columnas_grandes), meta)
    else:
        realidad = desp = None
    f_vis = None
    if pob.tipo is not None:
        def f_vis(df):
            return pob.f_visible(df, semilla_realidad)
    datos = Datos(
        ent=partes[0], val=partes[1], prueba=partes[2], realidad=realidad, despliegue=desp,
        f=pob.f_estructural, f_visible=f_vis, columnas_x=cols_x, columnas_contexto=ctx,
        oraculos=pob.nombres_oraculos(), omitidas=list(pob.omitidas), tarea=pob.tarea, K=K,
        clases=None if clases is None else np.asarray(clases), sigma2_e=pob.sigma2_e(),
        separacion=separar, despliegue_como="igual", semilla=semilla,
        semilla_realidad=semilla_realidad, descripcion=descripcion,
    )
    datos._pob = pob
    datos._grande = (n_realidad, semilla_realidad, columnas_grandes, meta)
    datos._rehacer = rehacer
    return datos


def _grandes(datos):
    """(realidad, despliegue) aunque el proceso se haya pedido con con_realidad=False."""
    if datos.realidad is not None and datos.despliegue is not None:
        return datos.realidad, datos.despliegue
    if not hasattr(datos, "_pob"):
        raise ValueError("este Datos no trae realidad ni despliegue")
    n_r, s_r, cols, meta = datos._grande
    real_c, desp_c = _poblacion_grande(datos._pob, n_r, s_r)
    return _con_meta(_publica(real_c, cols), meta), _con_meta(_publica(desp_c, cols), meta)


def _proceso(n=200, x=None, f=_f_por_omision, ruido=None, correlacion=None, endogeno=0.0,
             omitir=None, escala=None, faltantes=None, separar="azar",
             fracciones=(0.6, 0.2, 0.2), despliegue="igual", deriva=None, n_realidad=100_000,
             semilla=0, semilla_realidad=0, con_realidad=True, f_visible_cerrada=None,
             descripcion=None):
    _validar_adelantos(separar, despliegue, deriva, faltantes)
    x = {"x": uniforme(0, 1)} if x is None else x
    ruido = normal(0, 1) if ruido is None else ruido
    pob = _Poblacion(x, f, ruido, correlacion, endogeno, omitir, escala, f_visible_cerrada)
    muestra = pob.completo(int(n), np.random.default_rng([semilla, 0]))
    argumentos = dict(n=n, x=x, f=f, ruido=ruido, correlacion=correlacion, endogeno=endogeno,
                      omitir=omitir, escala=escala, faltantes=faltantes, separar=separar,
                      fracciones=fracciones, despliegue=despliegue, deriva=deriva,
                      n_realidad=n_realidad, semilla_realidad=semilla_realidad,
                      f_visible_cerrada=f_visible_cerrada, descripcion=descripcion)

    def rehacer(s):
        return _proceso(**{**argumentos, "semilla": s, "con_realidad": False})

    desc = descripcion or f"proceso con {', '.join(pob.visibles)} visibles"
    return _armar(pob, muestra, fracciones, np.random.default_rng([semilla, 3]), separar,
                  n_realidad, semilla, semilla_realidad, con_realidad, desc, rehacer)


def proceso(n=200, x={"x": uniforme(0, 1)}, f=_f_por_omision, ruido=normal(0, 1),
            correlacion=None, endogeno=0.0, omitir=None, escala=None, faltantes=None,
            separar="azar", fracciones=(0.6, 0.2, 0.2), despliegue="igual", deriva=None,
            n_realidad=100_000, semilla=0, semilla_realidad=0, con_realidad=True):
    """Genera datos y = f(x) + ε de un proceso conocido, partidos en ent, val y prueba.

    f(d) recibe un DataFrame con TODAS las variables (visibles y omitidas, sin
    escalar) y el contexto. escala solo cambia unidades; {"y": c} multiplica y.
    En 1.0: separar="azar", despliegue="igual", deriva=None, faltantes=None.
    Ejemplo: datos = ml.proceso(n=50, x={"x": ml.uniforme(0, 6)}, f=lambda d: 10 + 4 * d["x"])
    """
    # Lo que aún no funciona lanza NotImplementedError y dice qué versión lo trae:
    # separar="tiempo"|"grupo"|"estratificado", despliegue≠"igual" y deriva (clase 2);
    # faltantes (clase 4). deriva(t) devolverá un dict por variable (una Pieza o un
    # arreglo del largo de t) y puede traer la clave "f" (cambio de concepto, caso 28);
    # con despliegue="igual" deriva es un ValueError en cualquier versión.
    # endogeno = corr(x1, ε) (x1, o la primera variable si no hay "x1"):
    # ε = c·σ·z1 + sqrt(1 − c²)·u, con z1 la x1 estandarizada y u el ruido.
    # Flujos: la muestra sale de default_rng([semilla, 0]), la partición de
    # [semilla, 3], realidad de [semilla_realidad, 1] y despliegue de [semilla_realidad, 2].
    return _proceso(n=n, x=x, f=f, ruido=ruido, correlacion=correlacion, endogeno=endogeno,
                    omitir=omitir, escala=escala, faltantes=faltantes, separar=separar,
                    fracciones=fracciones, despliegue=despliegue, deriva=deriva,
                    n_realidad=n_realidad, semilla=semilla, semilla_realidad=semilla_realidad,
                    con_realidad=con_realidad)


def anillos(n=400, radio_interior=1.0, radio_exterior=2.0, grosor=0.3, ruido=0.1,
            separar="estratificado", semilla=0, fracciones=(0.6, 0.2, 0.2)):
    """Dos anillos concéntricos para clasificar (y=1 es el exterior).

    El radio de cada punto es normal alrededor de su anillo (desviación grosor)
    y cada coordenada lleva ruido; con la omisión los anillos se traslapan.
    realidad y despliegue traen el oráculo "prob" = Pr(y=1 | x).
    Ejemplo: datos = ml.anillos(n=400, fracciones=(1, 0, 0))
    """
    _validar_adelantos(separar, "igual", None, None, permitidos=("azar", "estratificado"))
    pob = _PoblacionAnillos(radio_interior, radio_exterior, grosor, ruido)
    muestra = pob.completo(int(n), np.random.default_rng([semilla, 0]))
    argumentos = dict(n=n, radio_interior=radio_interior, radio_exterior=radio_exterior,
                      grosor=grosor, ruido=ruido, separar=separar, fracciones=fracciones)

    def rehacer(s):
        return anillos(**{**argumentos, "semilla": s})

    return _armar(pob, muestra, fracciones, np.random.default_rng([semilla, 3]), separar,
                  100_000, semilla, 0, True, "dos anillos", rehacer, K=2, clases=[0, 1])


# Los procesos con nombre. Cada uno es (n=…, semilla=0, **cambios) -> Datos; cambios
# son argumentos de proceso o los parámetros propios que nombra su docstring.


def _f_entregas(d):
    return 10 + 4 * d["x"]


def _f_inverso(d):
    return 2 + 5 / d["x"]


def _f_seno(d):
    return 4 + 2 * np.sin(5 * d["x"])


def _f_mezcla_logs(d):
    x = d["x"]
    return x + np.log(x) + x * np.log(x) + 1 / x + x ** 1.3


def _f_caso_1(d):
    return d["x1"] + d["x2"] * d["x3"]


def _f_visible_caso_1(d):
    return 1.8 * d["x1"]


def _f_lluvia(d):
    return 10 + 4 * d["x1"] + 6 * d["x2"]


def _f_visible_lluvia(d):
    return 10 + 4 * d["x1"] + 3


def _con(base, cambios):
    kw = dict(base)
    kw.update(cambios)
    return kw


def _entregas(n=20, semilla=0, sigma_e=1.0, **cambios):
    """Las entregas de la clase 1: f = 10 + 4x, x ~ U(0, 6), ruido N(0, sigma_e²)."""
    return _proceso(**_con(dict(n=n, x={"x": uniforme(0, 6)}, f=_f_entregas,
                                ruido=normal(0, sigma_e), semilla=semilla,
                                descripcion="tiempo de entrega contra distancia"), cambios))


def _inverso(n=20, semilla=0, **cambios):
    """La recíproca: f = 2 + 5/x, x ~ U(0.3, 3), σ = 0.5."""
    return _proceso(**_con(dict(n=n, x={"x": uniforme(0.3, 3)}, f=_f_inverso,
                                ruido=normal(0, 0.5), semilla=semilla,
                                descripcion="la recíproca 2 + 5/x"), cambios))


def _seno(n=50, semilla=0, **cambios):
    """El seno: f = 4 + 2 sen(5x), x ~ U(0, 2), σ = 0.3."""
    return _proceso(**_con(dict(n=n, x={"x": uniforme(0, 2)}, f=_f_seno,
                                ruido=normal(0, 0.3), semilla=semilla,
                                descripcion="el seno 4 + 2 sen 5x"), cambios))


def _mezcla_logs(n=50, semilla=0, **cambios):
    """La mezcla de logaritmos: f = x + ln x + x ln x + 1/x + x^1.3, x ~ U(1, 5), σ = 1."""
    return _proceso(**_con(dict(n=n, x={"x": uniforme(1, 5)}, f=_f_mezcla_logs,
                                ruido=normal(0, 1), semilla=semilla,
                                descripcion="la mezcla de logaritmos"), cambios))


def _caso_1(n=200, semilla=0, **cambios):
    """Caso 1: y = x1 + x2·x3 + ε, corr(x1, x3) = 0.8, x2 ~ N(1, 0.5²), σ = 0.5; ve solo x1."""
    base = dict(n=n, x={"x1": normal(), "x2": normal(1, 0.5), "x3": normal()}, f=_f_caso_1,
                ruido=normal(0, 0.5), correlacion={("x1", "x3"): 0.8}, omitir=["x2", "x3"],
                fracciones=(1, 0, 0), semilla=semilla,
                descripcion="x1 + x2·x3 con x2 y x3 omitidas")
    kw = _con(base, cambios)
    if (kw["omitir"] == ["x2", "x3"] and kw["correlacion"] == {("x1", "x3"): 0.8}
            and kw["f"] is _f_caso_1 and kw["x"] is base["x"] and not kw.get("escala")):
        kw["f_visible_cerrada"] = _f_visible_caso_1  # E[y | x1] = 1.8 x1
    return _proceso(**kw)


def _lluvia(n=20, semilla=0, **cambios):
    """Caso 2: y = 10 + 4 x1 + 6 x2 + ε, x1 ~ U(0, 6), x2 ~ Bernoulli(0.5) omitida, σ = 1."""
    base = dict(n=n, x={"x1": uniforme(0, 6), "x2": categorica([0, 1])}, f=_f_lluvia,
                ruido=normal(0, 1), omitir=["x2"], fracciones=(1, 0, 0), semilla=semilla,
                descripcion="entregas con lluvia que el modelo no ve")
    kw = _con(base, cambios)
    if kw["omitir"] == ["x2"] and kw["f"] is _f_lluvia and kw["x"] is base["x"] \
            and not kw.get("escala"):
        kw["f_visible_cerrada"] = _f_visible_lluvia
    return _proceso(**kw)


def _caso_23(n=10, semilla=0, **cambios):
    """Caso 23: la recíproca con solo n = 10 datos (para polinomio(12))."""
    return _inverso(**_con(dict(n=n, semilla=semilla, fracciones=(1, 0, 0)), cambios))


PROCESOS = {
    "entregas": _entregas,
    "inverso": _inverso,
    "mezcla_logs": _mezcla_logs,
    "seno": _seno,
    "x1_mas_x2x3": _caso_1,
    "lluvia": _lluvia,
}


@dataclass
class CasoBorde:
    """Un caso que rompe algo a la vista: cómo se construye, qué preguntar y qué se ve.

    Ejemplo: ml.CASOS_BORDE[2].pregunta
    """

    numero: int
    nombre: str
    clase: int
    construir: object
    pregunta: str
    que_se_ve: str


CASOS_BORDE = {
    1: CasoBorde(
        1, "omitida_correlacionada", 1, _caso_1,
        "Ajustas y contra x1: ¿cuánto vale el coeficiente estimado si el de f es 1? "
        "¿Es un mal predictor?",
        "El coeficiente estructural de x1 es 1, pero E[y | x1] = 1.8·x1 y mínimos cuadrados "
        "va a 1.8: sesgado como coeficiente, óptimo como predictor con lo que ve. "
        "El piso con lo visible es 0.86."),
    2: CasoBorde(
        2, "lluvia", 1, _lluvia,
        "¿Por qué tu mejor recta no baja de 10?",
        "La lluvia x2 está en f y el modelo no la ve: el piso es 10 sin x2 y 1 con x2, "
        "y la pendiente de x1 sigue cerca de 4."),
    23: CasoBorde(
        23, "mas_parametros_que_datos", 1, _caso_23,
        "¿Qué hace el ajuste cuando hay más coeficientes que datos?",
        "polinomio(12) con 10 datos interpola (error de entrenamiento casi 0); ajustar avisa "
        "que usó la pseudoinversa, que da el ajuste de norma mínima, y el riesgo es enorme."),
}


def caso(numero_o_nombre, **cambios):
    """Construye un caso borde por número o por nombre; cambios van a su proceso.

    Ejemplo: datos = ml.caso("lluvia", omitir=None)
    """
    if isinstance(numero_o_nombre, str):
        for c in CASOS_BORDE.values():
            if c.nombre == numero_o_nombre:
                return c.construir(**cambios)
        raise ValueError(f"no hay caso llamado {numero_o_nombre!r}; los de esta versión: "
                         f"{[c.nombre for c in CASOS_BORDE.values()]}")
    if numero_o_nombre not in CASOS_BORDE:
        raise ValueError(f"no hay caso {numero_o_nombre!r} en esta versión: {sorted(CASOS_BORDE)}")
    return CASOS_BORDE[numero_o_nombre].construir(**cambios)


# === 3 · Separaciones ===
# separar, pliegues y Particion llegan con la versión de la clase 2. En 1.0 la
# partición vive dentro de proceso (_partir_indices).

# === 4 · Representaciones φ ===


class Phi:
    """Una transformación de las columnas en la matriz de diseño Φ.

    ajustar(df_ent) aprende lo que haga falta (rango, categorías) SOLO con ent y
    devuelve una copia ajustada; llamarla da la matriz. Nunca modifica el DataFrame.
    Ejemplo: Phi = ml.polinomio(3).ajustar(datos.ent)(datos.ent)
    """

    nombres = []

    def ajustar(self, df_ent):
        nueva = copy.deepcopy(self)
        nueva._aprender(df_ent)
        nueva._ajustada = True
        return nueva

    def _aprender(self, df_ent):
        pass

    def __call__(self, df):
        if not getattr(self, "_ajustada", False):
            raise ValueError("esta Φ no está ajustada: llama primero .ajustar(df_ent)")
        return self._matriz(df)

    def _matriz(self, df):
        raise NotImplementedError

    def __repr__(self):
        return f"{type(self).__name__.strip('_').lower()}({', '.join(self.nombres)})"


def _columna(df, nombre):
    if nombre not in df.columns:
        if nombre in ("r", "theta"):
            raise ValueError(f'no hay columna "{nombre}": el radio lo calcula '
                             'polares(incluir=("r",))' if nombre == "r" else
                             f'no hay columna "{nombre}": el ángulo lo calcula polares()')
        raise ValueError(f'no hay columna "{nombre}" en los datos')
    return df[nombre].to_numpy(dtype=float)


class _Identidad(Phi):
    def __init__(self, columnas_x):
        self.nombres = list(columnas_x)

    def _matriz(self, df):
        return pd.DataFrame({c: _columna(df, c) for c in self.nombres}, index=df.index)


class _Polinomio(Phi):
    def __init__(self, N, variable, escalar):
        if int(N) != N or N < 1:
            raise ValueError("el grado N de polinomio es un entero >= 1")
        self.N, self.variable, self.escalar = int(N), variable, escalar
        self.nombres = [variable if k == 1 else f"{variable}^{k}" for k in range(1, self.N + 1)]
        self.rango = None

    def _aprender(self, df_ent):
        if self.escalar:
            x = _columna(df_ent, self.variable)
            lo, hi = float(np.min(x)), float(np.max(x))
            self.rango = (lo, hi if hi > lo else lo + 1.0)

    def _matriz(self, df):
        x = _columna(df, self.variable)
        if self.escalar:
            lo, hi = self.rango
            x = 2 * (x - lo) / (hi - lo) - 1
        return pd.DataFrame({nm: x ** k for k, nm in enumerate(self.nombres, start=1)},
                            index=df.index)


def polinomio(N, variable="x", escalar=True):
    """Las potencias x, x², …, x^N de una variable.

    Con escalar=True, x se lleva a [−1, 1] con el rango de ent ANTES de elevar
    (los coeficientes son de esa x escalada); escalar=False usa x tal cual.
    Ejemplo: m = ml.ajustar(datos, phi=ml.polinomio(4))
    """
    return _Polinomio(N, variable, escalar)


_FUNCIONES = {"log": np.log, "exp": np.exp, "sqrt": np.sqrt, "sin": np.sin, "sen": np.sin,
              "cos": np.cos, "abs": np.abs, "tan": np.tan}


def _evaluar_expresion(nodo, df):
    if isinstance(nodo, ast.Expression):
        return _evaluar_expresion(nodo.body, df)
    if isinstance(nodo, ast.Constant) and isinstance(nodo.value, (int, float)):
        return float(nodo.value)
    if isinstance(nodo, ast.Name):
        return _columna(df, nodo.id)
    if isinstance(nodo, ast.UnaryOp) and isinstance(nodo.op, (ast.USub, ast.UAdd)):
        v = _evaluar_expresion(nodo.operand, df)
        return -v if isinstance(nodo.op, ast.USub) else v
    if isinstance(nodo, ast.BinOp):
        a, b = _evaluar_expresion(nodo.left, df), _evaluar_expresion(nodo.right, df)
        ops = {ast.Add: np.add, ast.Sub: np.subtract, ast.Mult: np.multiply,
               ast.Div: np.divide, ast.Pow: np.power}
        for tipo, op in ops.items():
            if isinstance(nodo.op, tipo):
                return op(a, b)
    if (isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name)
            and nodo.func.id in _FUNCIONES and len(nodo.args) == 1 and not nodo.keywords):
        return _FUNCIONES[nodo.func.id](_evaluar_expresion(nodo.args[0], df))
    raise ValueError("expresión no permitida: solo columnas, números, + − * / ** y "
                     f"{sorted(_FUNCIONES)}")


class _Columnas(Phi):
    def __init__(self, expresiones):
        if not expresiones:
            raise ValueError("columnas() necesita al menos una expresión")
        self.nombres = list(expresiones)
        self._arboles = []
        for e in expresiones:
            try:
                arbol = ast.parse(e, mode="eval")
            except SyntaxError as err:
                raise ValueError(f"no entiendo la expresión {e!r}") from err
            _validar_arbol(arbol)
            self._arboles.append(arbol)

    def _matriz(self, df):
        n = len(df)
        return pd.DataFrame({nm: np.broadcast_to(_evaluar_expresion(a, df), (n,)).astype(float)
                             for nm, a in zip(self.nombres, self._arboles)}, index=df.index)

    def _aprender(self, df_ent):
        self._matriz(df_ent)  # falla aquí si una columna no existe


def _validar_arbol(arbol):
    permitidos = (ast.Expression, ast.Constant, ast.Name, ast.Load, ast.UnaryOp, ast.USub,
                  ast.UAdd, ast.BinOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Call)
    for nodo in ast.walk(arbol):
        if not isinstance(nodo, permitidos):
            raise ValueError("expresión no permitida en columnas()")
        if isinstance(nodo, ast.Call) and not (isinstance(nodo.func, ast.Name)
                                               and nodo.func.id in _FUNCIONES):
            raise ValueError(f"función no permitida; usa una de {sorted(_FUNCIONES)}")
        if isinstance(nodo, ast.Name) and nodo.id.startswith("__"):
            raise ValueError("nombre no permitido en columnas()")


def columnas(*expresiones):
    """Columnas por nombre o expresiones simples, con un lector seguro (sin eval).

    Solo lee columnas que existen: columnas("r") no calcula el radio.
    Ejemplo: phi = ml.columnas("x1", "1/x2", "x1*x3", "log(x1)")
    """
    return _Columnas(expresiones)


class _Polares(Phi):
    def __init__(self, x1, x2, incluir):
        incluir = tuple(incluir) if not isinstance(incluir, str) else (incluir,)
        if incluir not in (("r", "theta"), ("r",), ("theta",)):
            raise ValueError('incluir es una tupla no vacía de ("r", "theta"), en ese orden: '
                             '("r", "theta"), ("r",) o ("theta",)')
        self.x1, self.x2, self.nombres = x1, x2, list(incluir)

    def _matriz(self, df):
        a, b = _columna(df, self.x1), _columna(df, self.x2)
        valores = {"r": np.hypot(a, b), "theta": np.arctan2(b, a)}
        return pd.DataFrame({k: valores[k] for k in self.nombres}, index=df.index)


def polares(x1="x1", x2="x2", *, incluir=("r", "theta")):
    """Radio r = sqrt(x1² + x2²) y ángulo theta = arctan2(x2, x1), calculados en cada llamada.

    incluir=("r",) es «solo radio». No agrega columnas a los datos.
    Ejemplo: m = ml.ajustar(datos, phi=ml.polares(incluir=("r",)), tarea="clasificacion")
    """
    return _Polares(x1, x2, incluir)


class _Periodicas(Phi):
    def __init__(self, variable, periodo, armonicos):
        if periodo <= 0 or int(armonicos) != armonicos or armonicos < 1:
            raise ValueError("periodo > 0 y armonicos entero >= 1")
        self.variable, self.periodo, self.armonicos = variable, float(periodo), int(armonicos)
        self.nombres = [f"{fn}{k}({variable})" for k in range(1, self.armonicos + 1)
                        for fn in ("sen", "cos")]

    def _matriz(self, df):
        x = _columna(df, self.variable)
        cols = {}
        for k in range(1, self.armonicos + 1):
            ang = 2 * math.pi * k * x / self.periodo
            cols[f"sen{k}({self.variable})"] = np.sin(ang)
            cols[f"cos{k}({self.variable})"] = np.cos(ang)
        return pd.DataFrame(cols, index=df.index)


def periodicas(variable="x", periodo=1.0, armonicos=1):
    """Senos y cosenos de la variable con ese periodo (k = 1 … armonicos).

    Ejemplo: phi = ml.periodicas("x", periodo=2, armonicos=3)
    """
    return _Periodicas(variable, periodo, armonicos)


class _Dummies(Phi):
    def __init__(self, variable, quitar_una, codificacion):
        if codificacion not in ("base", "efectos"):
            raise ValueError('codificacion es "base" o "efectos"')
        if codificacion == "efectos" and not quitar_una:
            raise ValueError('codificacion="efectos" ya quita una: no admite quitar_una=False')
        self.variable, self.quitar_una, self.codificacion = variable, quitar_una, codificacion
        self.categorias = None
        self.nombres = []

    def _aprender(self, df_ent):
        if self.variable not in df_ent.columns:
            raise ValueError(f'no hay columna "{self.variable}" en los datos')
        self.categorias = list(pd.unique(df_ent[self.variable]))
        if self.codificacion == "efectos":
            self.categorias = sorted(self.categorias, key=lambda c: str(c))
        usadas = self.categorias[1:] if self.quitar_una else self.categorias
        self.nombres = [f"{self.variable}={c}" for c in usadas]

    def _matriz(self, df):
        v = df[self.variable].to_numpy()
        nuevas = sorted({c for c in pd.unique(v) if c not in self.categorias}, key=str)
        if nuevas and self.codificacion == "base":
            raise ValueError(f"categoría no vista en el ajuste: {nuevas[0]!r} en "
                             f"{self.variable!r}; usa codificacion=\"efectos\" para tratarla "
                             "como el grupo promedio")
        if nuevas:
            warnings.warn("categoría no vista: se trata como el grupo promedio "
                          f"({', '.join(map(str, nuevas))})", UserWarning, stacklevel=3)
        usadas = self.categorias[1:] if self.quitar_una else self.categorias
        cols = {f"{self.variable}={c}": (v == c).astype(float) for c in usadas}
        if self.codificacion == "efectos":
            ref = (v == self.categorias[0])
            for nm in cols:
                cols[nm] = np.where(ref, -1.0, cols[nm])
        return pd.DataFrame(cols, index=df.index)


def dummies(variable, quitar_una=True, codificacion="base"):
    """Indicadoras de una variable categórica (aprende las categorías en ent).

    "base": K−1 columnas; una categoría no vista es ValueError. "efectos": K−1
    columnas de suma cero; una no vista es una fila de ceros (grupo promedio) y aviso.
    Ejemplo: phi = ml.combinar(ml.columnas("x1"), ml.dummies("lluvia"))
    """
    return _Dummies(variable, quitar_una, codificacion)


class _Combinar(Phi):
    def __init__(self, phis, intercepto):
        if not phis:
            raise ValueError("combinar() necesita al menos una Φ")
        self.phis, self.intercepto = list(phis), bool(intercepto)
        self.nombres = []

    def _aprender(self, df_ent):
        self.phis = [p.ajustar(df_ent) for p in self.phis]
        self.nombres = (["1"] if self.intercepto else []) + [nm for p in self.phis
                                                             for nm in p.nombres]

    def _matriz(self, df):
        partes = [p(df) for p in self.phis]
        M = pd.concat(partes, axis=1)
        if self.intercepto:
            M.insert(0, "1", 1.0)
        return M


def combinar(*phis, intercepto=True):
    """Junta varias Φ en una sola matriz (con la columna "1" si intercepto).

    Ejemplo: phi = ml.combinar(ml.polinomio(2), ml.periodicas())
    """
    return _Combinar(phis, intercepto)


def taylor(funcion="seno", centro=0.5, N=3):
    """Polinomio de Taylor de grado N, centrado en centro, de una f del laboratorio.

    "seno" es 4 + 2 sen(5x) (PROCESOS["seno"]); "inverso" es 2 + 5/x
    (PROCESOS["inverso"]). Devuelve una función de un arreglo.
    Ejemplo: t = ml.taylor("inverso", centro=1.0, N=3); t(np.array([1.5]))
    """
    if funcion not in ("seno", "inverso"):
        raise ValueError('funcion es "seno" o "inverso"')
    if int(N) != N or N < 0:
        raise ValueError("N es un entero >= 0")
    c = float(centro)
    coef = []
    for k in range(int(N) + 1):
        if funcion == "seno":
            d = 2 * 5 ** k * math.sin(5 * c + k * math.pi / 2) + (4 if k == 0 else 0)
        else:
            if c == 0:
                raise ValueError("2 + 5/x no tiene Taylor en 0")
            d = 5 * (-1) ** k * math.factorial(k) / c ** (k + 1) + (2 if k == 0 else 0)
        coef.append(d / math.factorial(k))

    def polinomio_de_taylor(x):
        x = np.asarray(x, float)
        return sum(a * (x - c) ** k for k, a in enumerate(coef))

    polinomio_de_taylor.__name__ = f"taylor_{funcion}_{N}"
    return polinomio_de_taylor


# === 5 · Ajuste ===


class Modelo:
    """Lo que devuelve ajustar: predice, mide su pérdida y, si es lineal, muestra Φ y β̂.

    predecir (reg: ŷ; clf: la etiqueta con umbral 0.5), predecir_prob (n×K, en el
    orden de clases), predecir_p (binaria: Pr(y = clases[1])), L(df) sin ponderar.
    Ejemplo: m.predecir(datos.val); m.beta_gorro
    """

    familia = None
    tarea = None
    K = None
    clases = None
    columnas_x = []
    hiperparametros = {}
    pesos = None
    es_lineal = False
    phi = None
    beta_gorro = None

    def predecir(self, df):
        raise NotImplementedError

    def predecir_prob(self, df):
        if self.tarea != "clasificacion":
            raise NoAplica("predecir_prob es de clasificación; en regresión usa predecir")
        p = self.predecir_p(df)
        return np.column_stack([1 - p, p])

    def predecir_p(self, df):
        raise NoAplica("predecir_p es de clasificación binaria")

    def L(self, df, perdida=None, pesos=None):
        return _evaluar_perdida(self, df, perdida, pesos)

    def Phi(self, df):
        raise NoAplica(f"un modelo de familia {self.familia!r} no tiene matriz de diseño")

    def n_parametros(self):
        raise NoAplica(f"un modelo de familia {self.familia!r} no tiene un β que contar")

    def __repr__(self):
        return f"Modelo({self.familia}, {self.tarea}, {self.hiperparametros})"


def _disenar(phi, df, intercepto):
    M = phi(df)
    if "1" in M.columns:
        if not intercepto:
            raise ValueError('la Φ ya trae la columna "1" y pediste intercepto=False')
        return M[["1"] + [c for c in M.columns if c != "1"]]
    if intercepto:
        M = M.copy()
        M.insert(0, "1", 1.0)
    return M


class _ModeloLineal(Modelo):
    es_lineal = True

    def __init__(self, familia, tarea, clases, columnas_x, hiperparametros, phi, beta,
                 intercepto, nombres):
        self.familia, self.tarea = familia, tarea
        self.clases = None if clases is None else np.asarray(clases)
        self.K = None if clases is None else len(clases)
        self.columnas_x = list(columnas_x)
        self.hiperparametros = hiperparametros
        self.pesos = None
        self.phi = phi
        self.intercepto = intercepto
        self.beta_gorro = pd.Series(beta, index=nombres, dtype=float)

    def Phi(self, df):
        M = _disenar(self.phi, df, self.intercepto)
        return M[list(self.beta_gorro.index)]

    def n_parametros(self):
        return len(self.beta_gorro)

    def _eta(self, df):
        return self.Phi(df).to_numpy() @ self.beta_gorro.to_numpy()

    def predecir_p(self, df):
        if self.tarea != "clasificacion":
            raise NoAplica("predecir_p es de clasificación binaria")
        return special.expit(self._eta(df))

    def predecir(self, df):
        if self.tarea == "regresion":
            return self._eta(df)
        return np.where(self.predecir_p(df) >= 0.5, self.clases[1], self.clases[0])


class _ModeloVecinos(Modelo):
    familia = "vecinos"

    def __init__(self, tarea, clases, columnas_x, n_vecinos, estimador):
        self.tarea, self.columnas_x = tarea, list(columnas_x)
        self.clases = None if clases is None else np.asarray(clases)
        self.K = None if clases is None else len(clases)
        self.hiperparametros = {"n_vecinos": n_vecinos}
        self._est = estimador

    def _X(self, df):
        return np.column_stack([_columna(df, c) for c in self.columnas_x])

    def predecir(self, df):
        return self._est.predict(self._X(df))

    def predecir_p(self, df):
        if self.tarea != "clasificacion" or self.K != 2:
            raise NoAplica("predecir_p es de clasificación binaria")
        prob = self._est.predict_proba(self._X(df))
        j = list(self._est.classes_).index(self.clases[1]) if self.clases[1] in \
            self._est.classes_ else None
        return prob[:, j] if j is not None else np.zeros(len(df))


def _entrada(datos_o_df, columnas_x, tarea):
    df = datos_o_df.ent if isinstance(datos_o_df, Datos) else datos_o_df
    if not isinstance(df, pd.DataFrame):
        raise ValueError("ajustar recibe un Datos o un DataFrame")
    meta = df.attrs.get("ml")
    if meta:
        cols = list(columnas_x) if columnas_x is not None else list(meta["columnas_x"])
        if tarea is not None and tarea != meta["tarea"]:
            raise ValueError(f"los datos son de {meta['tarea']} y pediste tarea={tarea!r}")
        return df, cols, meta["tarea"], meta.get("clases")
    faltan = [nm for nm, v in (("columnas_x", columnas_x), ("tarea", tarea)) if v is None]
    if faltan:
        raise ValueError("este DataFrame no trae attrs['ml']: di " + " y ".join(
            f"{nm}=" for nm in faltan) + " (la tarea nunca se adivina por los valores de y)")
    if tarea not in ("regresion", "clasificacion"):
        raise ValueError('tarea es "regresion" o "clasificacion"')
    return df, list(columnas_x), tarea, None


def _pesos_balanceados(y, clases):
    """w_y = n / (K n_y), contado en y; clases es la lista de todas las del problema."""
    y = np.asarray(y)
    n, K = len(y), len(clases)
    return {c: n / (K * np.sum(y == c)) for c in clases if np.sum(y == c) > 0}


def _suave(c, umbral):
    return math.copysign(max(abs(c) - umbral, 0.0), c)


def _coordenadas(Phi, z, v, mu, r, pen, beta, tol=1e-13, max_vueltas=200_000):
    """Descenso por coordenadas para (1/n) Σ v_i (z_i − Φ_i β)² + μ(r|β|₁ + (1−r)‖β‖²)."""
    n, q = Phi.shape
    a = (v[:, None] * Phi ** 2).sum(axis=0) / n
    vPhi = v[:, None] * Phi
    res = z - Phi @ beta
    for vuelta in range(max_vueltas):
        cambio = 0.0
        for j in range(q):
            if a[j] == 0:
                continue
            bj = beta[j]
            c = vPhi[:, j] @ res / n + a[j] * bj
            nuevo = _suave(c, mu * r / 2) / (a[j] + mu * (1 - r)) if pen[j] else c / a[j]
            if nuevo != bj:
                res -= Phi[:, j] * (nuevo - bj)
                beta[j] = nuevo
                cambio = max(cambio, abs(nuevo - bj))
        if vuelta % 50 == 49:
            res = z - Phi @ beta
        if cambio < tol * (1 + np.max(np.abs(beta))):
            break
    return beta


def _absoluta(Phi, y, w, mu, pen):
    n, q = Phi.shape
    p = int(pen.sum())
    idx = np.flatnonzero(pen)
    c = np.concatenate([np.zeros(q), w / n, w / n, np.full(p, mu)])
    A_eq = np.hstack([Phi, np.eye(n), -np.eye(n), np.zeros((n, p))])
    filas = []
    for k, j in enumerate(idx):
        for s in (1, -1):
            fila = np.zeros(q + 2 * n + p)
            fila[j] = s
            fila[q + 2 * n + k] = -1
            filas.append(fila)
    A_ub = np.array(filas) if filas else None
    b_ub = np.zeros(len(filas)) if filas else None
    cotas = [(None, None)] * q + [(0, None)] * (2 * n + p)
    sol = optimize.linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=y, bounds=cotas,
                           method="highs")
    if sol.status != 0:
        raise RuntimeError("no pude resolver el ajuste con pérdida absoluta")
    return sol.x[:q]


def _separables(Phi, y01):
    s = 2 * y01 - 1
    sol = optimize.linprog(np.zeros(Phi.shape[1]), A_ub=-(s[:, None] * Phi),
                           b_ub=-np.ones(len(s)), bounds=[(None, None)] * Phi.shape[1],
                           method="highs")
    return sol.status == 0


def _logistica(Phi, y, w, mu, r, pen, intercepto):
    n, q = Phi.shape
    beta = np.zeros(q)
    if intercepto:
        ybar = np.clip(np.average(y, weights=w), 1e-6, 1 - 1e-6)
        beta[0] = math.log(ybar / (1 - ybar))
    separado = mu == 0 and _separables(Phi, y)
    if separado:
        warnings.warn("los datos se separan perfectamente: sin penalización no hay "
                      "coeficientes óptimos finitos; los que ves son donde se detuvo el "
                      "algoritmo, no un óptimo", UserWarning, stacklevel=3)
    D = pen.astype(float)

    def objetivo(b):
        eta = Phi @ b
        return (np.mean(w * (np.logaddexp(0, eta) - y * eta))
                + mu * (r * np.abs(b * D).sum() + (1 - r) * ((b * D) ** 2).sum()))

    maximo = 30 if separado else 500
    for _ in range(maximo):
        eta = Phi @ beta
        p = special.expit(eta)
        s = np.clip(p * (1 - p), 1e-12, None)
        if r == 0:
            g = Phi.T @ (w * (p - y)) / n + 2 * mu * D * beta
            H = Phi.T @ ((w * s)[:, None] * Phi) / n + 2 * mu * np.diag(D)
            delta = np.linalg.lstsq(H, -g, rcond=None)[0]
        else:
            z = eta + (y - p) / s
            nuevo = _coordenadas(Phi, z, w * s / 2, mu, r, pen, beta.copy())
            delta = nuevo - beta
        f0, t = objetivo(beta), 1.0
        while objetivo(beta + t * delta) > f0 + 1e-15 * abs(f0) and t > 1e-10:
            t /= 2
        beta = beta + t * delta
        if np.max(np.abs(t * delta)) < 1e-12 * (1 + np.max(np.abs(beta))):
            break
    return beta


def _resolver(Phi, y, w, mu, penalizacion, rho, tarea, intercepto, perdida="cuadratica"):
    """β̂ ∈ argmin (1/n) Σ w_i ℓ_i(β) + μ Ω(β), sin penalizar el intercepto (columna 0)."""
    Phi = np.asarray(Phi, float)
    y = np.asarray(y, float)
    w = np.ones(len(y)) if w is None else np.asarray(w, float)
    n, q = Phi.shape
    pen = np.ones(q, dtype=bool)
    if intercepto:
        pen[0] = False
    if penalizacion is None or mu == 0:
        mu, r = 0.0, 0.0
    else:
        r = {"l2": 0.0, "l1": 1.0, "elastica": float(rho)}[penalizacion]
    if tarea == "clasificacion":
        return _logistica(Phi, y, w, mu, r, pen, intercepto)
    if perdida == "absoluta":
        return _absoluta(Phi, y, w, mu, pen)
    if mu == 0:
        raiz = np.sqrt(w)
        A = raiz[:, None] * Phi
        rango = np.linalg.matrix_rank(A)
        if rango < q:
            warnings.warn(f"Φ tiene {q} columnas y rango {rango} (más parámetros que datos o "
                          "columnas repetidas): uso la pseudoinversa, que da el ajuste de "
                          "norma mínima, uno de muchos con el mismo error", UserWarning,
                          stacklevel=3)
        else:
            cond = np.linalg.cond(A)
            if cond > 1e12:
                warnings.warn(f"Φ está mal condicionada (número de condición {cond:.1e}): "
                              "los coeficientes pierden precisión; escala las columnas",
                              UserWarning, stacklevel=3)
        return np.linalg.lstsq(A, raiz * y, rcond=None)[0]
    if r == 0:
        A = Phi.T @ (w[:, None] * Phi) / n + mu * np.diag(pen.astype(float))
        return np.linalg.lstsq(A, Phi.T @ (w * y) / n, rcond=None)[0]
    beta = np.zeros(q)
    if intercepto:
        beta[0] = np.average(y, weights=w)
    return _coordenadas(Phi, y, w, mu, r, pen, beta)


def ajustar(datos_o_df, phi=None, mu=0.0, penalizacion=None, rho=0.5, pesos=None,
            perdida=None, intercepto=True, columnas_x=None, tarea=None):
    """Ajusta un modelo lineal en parámetros (regresión o logística binaria) con ent.

    Resuelve β̂ ∈ argmin (1/n) Σ w_{y_i} ℓ_i(β) + μ Ω(β) con el intercepto sin penalizar:
    Ω₂ = Σ_{j≥1} β_j², Ω₁ = Σ_{j≥1} |β_j|, elástica = ρ Ω₁ + (1−ρ) Ω₂.
    Ejemplo: m = ml.ajustar(datos, phi=ml.polinomio(3), mu=0.1, penalizacion="l2")
    """
    # Equivalencias con sklearn (con la misma escala de μ): Lasso(alpha=mu/2);
    # ElasticNet(alpha=mu*(2-rho)/2, l1_ratio=rho/(2-rho)); LogisticRegression
    # (C=1/(2*mu*n), sample_weight=w) en l2, C=1/(mu*n) en l1, y con mu=0, penalty=None.
    # sklearn llama alpha (o 1/C) a nuestro mu, con otra escala. Aquí se resuelve con
    # mínimos cuadrados, forma cerrada (ridge) o descenso por coordenadas propio, y una
    # prueba comprueba que da lo mismo que sklearn y que se cumplen las condiciones KKT.
    # Qué elemento del argmin devuelve: con mu=0 y rango deficiente (o q > n), el de
    # norma mínima (pseudoinversa), con un aviso; ese ajuste predice distinto fuera de
    # la muestra según las unidades de las columnas. Ridge y elástica con rho<1 tienen
    # un solo minimizador. Lasso con columnas colineales puede tener muchos: devuelve
    # el que encuentra el algoritmo (hay otros con el mismo objetivo). Logística sin
    # penalizar con datos separables no tiene minimizador finito: avisa.
    # pesos ("balanceado" = n/(K n_y), o {y: w_y}) llega con la versión de la clase 4.
    if pesos is not None:
        raise NotImplementedError("`pesos` llega con la versión de la clase 4")
    df, cols, tarea, clases = _entrada(datos_o_df, columnas_x, tarea)
    if mu < 0:
        raise ValueError("mu es >= 0")
    if penalizacion not in (None, "l2", "l1", "elastica"):
        raise ValueError('penalizacion es None, "l2", "l1" o "elastica"')
    if mu > 0 and penalizacion is None:
        raise ValueError('con mu > 0 di la penalizacion: "l2", "l1" o "elastica"')
    if not 0 <= rho <= 1:
        raise ValueError("rho está en [0, 1]")
    if tarea == "regresion":
        perdida = perdida or "cuadratica"
        if perdida not in ("cuadratica", "absoluta"):
            raise ValueError('en regresión, perdida es "cuadratica" o "absoluta"')
        if perdida == "absoluta" and penalizacion not in (None, "l1"):
            raise ValueError('la pérdida absoluta se combina con penalizacion=None o "l1"')
        familia = "lineal"
        y = df["y"].to_numpy(dtype=float)
    else:
        perdida = perdida or "logaritmica"
        if perdida != "logaritmica":
            raise ValueError('en clasificación, ajustar minimiza la pérdida "logaritmica"')
        if clases is None:
            clases = list(np.unique(df["y"]))
        if len(clases) != 2:
            raise NotImplementedError("la clasificación con K > 2 (softmax) llega con la "
                                      "versión de la clase 4")
        familia = "logistica"
        y = (df["y"].to_numpy() == clases[1]).astype(float)
    phi_aj = (phi if phi is not None else _Identidad(cols)).ajustar(df)
    M = _disenar(phi_aj, df, intercepto)
    beta = _resolver(M.to_numpy(dtype=float), y, None, mu, penalizacion, rho, tarea,
                     intercepto, perdida)
    hiper = {"mu": mu, "penalizacion": penalizacion, "rho": rho, "perdida": perdida,
             "intercepto": intercepto, "phi": repr(phi_aj)}
    return _ModeloLineal(familia, tarea, clases, cols, hiper, phi_aj, beta, intercepto,
                         list(M.columns))


_HIPER = {"vecinos": {"n_vecinos"}, "arbol": {"profundidad"},
          "bosque": {"n_arboles", "profundidad"}, "boosting": {"etapas", "tasa", "profundidad"}}


def ajustar_otro(datos_o_df, familia="vecinos", columnas_x=None, tarea=None,
                 **hiperparametros):
    """Ajusta un modelo que no es lineal en parámetros; en 1.0, vecinos más cercanos.

    Hiperparámetros por nombre: n_vecinos (vecinos, 5 por omisión); profundidad,
    n_arboles, etapas, tasa (árbol, bosque, boosting: llegan con la clase 5).
    columnas_x puede nombrar una columna de contexto; sin él, nunca la usa.
    Ejemplo: m = ml.ajustar_otro(datos, familia="vecinos", n_vecinos=3)
    """
    if familia not in _HIPER:
        raise ValueError(f"familia es una de {sorted(_HIPER)}")
    desconocidos = set(hiperparametros) - _HIPER[familia]
    if desconocidos:
        raise ValueError(f"hiperparámetros de {familia}: {sorted(_HIPER[familia])}; "
                         f"no conozco {sorted(desconocidos)}")
    if familia != "vecinos":
        raise NotImplementedError(f'familia="{familia}" llega con la versión de la clase 5')
    from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

    df, cols, tarea, clases = _entrada(datos_o_df, columnas_x, tarea)
    k = int(hiperparametros.get("n_vecinos", 5))
    if not 1 <= k <= len(df):
        raise ValueError(f"n_vecinos va de 1 a {len(df)} (el tamaño de ent)")
    X = np.column_stack([_columna(df, c) for c in cols])
    if tarea == "regresion":
        est = KNeighborsRegressor(n_neighbors=k).fit(X, df["y"].to_numpy(float))
    else:
        if clases is None:
            clases = list(np.unique(df["y"]))
        est = KNeighborsClassifier(n_neighbors=k).fit(X, df["y"].to_numpy())
    return _ModeloVecinos(tarea, clases, cols, k, est)


# === 6 · Pérdidas y métricas ===

Criterio = str  # "cuadratica" | "absoluta" | "logaritmica" (pérdidas) | "aciertos" (métrica)

SENTIDO = {"cuadratica": "min", "absoluta": "min", "logaritmica": "min", "aciertos": "max"}

_PERDIDAS = ("cuadratica", "absoluta", "logaritmica")
_METRICAS_FUTURAS = ("mcc", "aciertos_balanceados", "brier")


def perdida(y, y_gorro, tipo="cuadratica"):
    """La pérdida ℓ_i de cada observación (un arreglo, no un promedio).

    "logaritmica": y es 0/1 y y_gorro la probabilidad de 1.
    Ejemplo: ml.perdida(df["y"], m.predecir(df)).mean()
    """
    y, g = np.asarray(y, float), np.asarray(y_gorro, float)
    if tipo == "cuadratica":
        return (y - g) ** 2
    if tipo == "absoluta":
        return np.abs(y - g)
    if tipo == "logaritmica":
        with np.errstate(divide="ignore", invalid="ignore"):
            return -(np.where(y == 1, np.log(g), 0.0) + np.where(y == 1, 0.0, np.log1p(-g)))
    raise ValueError(f"tipo es uno de {_PERDIDAS}")


def mse(y, y_gorro):
    """Error cuadrático medio. Ejemplo: ml.mse(df["y"], m.predecir(df))"""
    return float(np.mean(perdida(y, y_gorro, "cuadratica")))


def aciertos(y, y_gorro):
    """Fracción de etiquetas acertadas. Ejemplo: ml.aciertos(df["y"], m.predecir(df))"""
    return float(np.mean(np.asarray(y) == np.asarray(y_gorro)))


def _w_eval(modelo_clases, y, pesos):
    if pesos is None:
        return np.ones(len(y))
    if pesos == "balanceado":
        if modelo_clases is None:
            raise ValueError('pesos="balanceado" es de clasificación')
        w = _pesos_balanceados(y, list(modelo_clases))
    elif isinstance(pesos, dict):
        w = pesos
    else:
        raise ValueError('pesos es None, "balanceado" o un dict {clase: peso}')
    return np.array([w.get(v, 0.0) for v in np.asarray(y)], float)


def _evaluar_perdida(modelo, df, criterio, pesos):
    if len(df) == 0:
        return float("nan")
    crit = criterio or ("cuadratica" if modelo.tarea == "regresion" else "logaritmica")
    if crit in _METRICAS_FUTURAS:
        raise NotImplementedError(f'"{crit}" llega con la versión de la clase 4')
    if crit not in SENTIDO:
        raise ValueError(f"criterio es uno de {sorted(SENTIDO)}")
    y = df["y"].to_numpy()
    w = _w_eval(modelo.clases, y, pesos)
    if crit == "aciertos":
        if modelo.tarea != "clasificacion":
            raise ValueError('"aciertos" es de clasificación')
        return float(np.mean(w * (modelo.predecir(df) == y)))
    if modelo.tarea == "clasificacion":
        if crit != "logaritmica":
            raise ValueError(f'"{crit}" no es una pérdida de clasificación en esta versión')
        y01 = (y == modelo.clases[1]).astype(float)
        return float(np.mean(w * perdida(y01, modelo.predecir_p(df), "logaritmica")))
    if crit == "logaritmica":
        raise ValueError('la pérdida "logaritmica" es de clasificación')
    return float(np.mean(w * perdida(y, modelo.predecir(df), crit)))


def evaluar(modelo, df, criterio=None, pesos=None):
    """La pérdida promedio o la métrica de un modelo en un DataFrame, sin ponderar.

    criterio=None es la pérdida natural (cuadrática o logarítmica). Ponderar es
    explícito (pesos=dict o "balanceado") y nunca lee modelo.pesos.
    Ejemplo: ml.evaluar(m, datos.val, "aciertos")
    """
    return _evaluar_perdida(modelo, df, criterio, pesos)


def L(modelo, df, perdida=None, pesos=None):
    """L del modelo en df: la pérdida promedio sin ponderar (= modelo.L(df)).

    Ejemplo: L_ent = ml.L(m, datos.ent)
    """
    return modelo.L(df, perdida, pesos)


def _muestra_grande(datos, contra):
    if contra not in ("despliegue", "realidad"):
        raise ValueError('contra es "despliegue" o "realidad"')
    real, desp = _grandes(datos)
    return desp if contra == "despliegue" else real


def riesgo(modelo, datos, criterio=None, contra="despliegue"):
    """R: la pérdida sin ponderar en la muestra enorme de despliegue (o de realidad).

    Solo pérdidas; una métrica sale de desempeno. Ejemplo: R = ml.riesgo(m, datos)
    """
    if criterio is not None and criterio not in _PERDIDAS:
        raise ValueError(f'«{criterio}» no es un riesgo: usa desempeno(modelo, datos, "{criterio}")')
    return _evaluar_perdida(modelo, _muestra_grande(datos, contra), criterio, None)


def desempeno(modelo, datos, criterio=None, contra="despliegue"):
    """Cualquier criterio (pérdida o métrica) en la muestra enorme, sin pesos.

    Con una pérdida da lo mismo que riesgo. Ejemplo: ml.desempeno(m, datos, "aciertos")
    """
    return _evaluar_perdida(modelo, _muestra_grande(datos, contra), criterio, None)


def piso(datos, perdida="cuadratica"):
    """R_Bayes: el menor riesgo posible con las variables visibles, en despliegue.

    Es un ínfimo: inf si es infinito (ruido sin segundo momento); nan solo si no se
    puede calcular, con el aviso «piso desconocido».
    Ejemplo: ml.piso(ml.caso(2))  # 10: la lluvia no se ve
    """
    # Cuadrática: E[Var(y | x visibles)] = E[(f + E[ε|x] − f_visible)²] + E[Var(ε|x)].
    # Con omitidas independientes de lo visible, f_visible promedia 200 sorteos
    # estratificados de las omitidas y la primera parte es la varianza de f con 16
    # sorteos frescos por fila, promediada en despliegue; con forma cerrada, directo. Con
    # endogeno ≠ 0 vale para ruido normal; con otro ruido, nan. Absoluta: E|ε − mediana|
    # si no hay omitidas y el ruido es simétrico y conocido; si no, nan.
    pob = getattr(datos, "_pob", None)
    if pob is None:
        raise ValueError("piso necesita un Datos hecho por ml_lab")
    n_r, s_r, _, _ = datos._grande
    desp = _poblacion_grande(pob, n_r, s_r)[1]
    if perdida not in _PERDIDAS:
        raise ValueError(f"perdida es una de {_PERDIDAS}")
    valor = pob.piso(desp, perdida)
    if valor is None:
        warnings.warn("piso desconocido: con lo que registra este proceso no se puede calcular",
                      UserWarning, stacklevel=2)
        return float("nan")
    return valor


def benchmarks(datos_o_df, df_eval, tarea=None, criterios=None):
    """Los puntos de comparación sin x, ajustados en ent y evaluados en df_eval.

    Regresión: filas media y mediana. Clasificación: moda y proporcion (predice la
    proporción p de ent). criterios=None: la pérdida natural y, en clasificación, "aciertos".
    Ejemplo: ml.benchmarks(datos, datos.despliegue)
    """
    ent = datos_o_df.ent if isinstance(datos_o_df, Datos) else datos_o_df
    meta = ent.attrs.get("ml", {})
    tarea = tarea or meta.get("tarea")
    if tarea not in ("regresion", "clasificacion"):
        raise ValueError('di tarea="regresion" o "clasificacion"')
    y_ent = ent["y"].to_numpy()
    y = df_eval["y"].to_numpy()
    if tarea == "regresion":
        criterios = list(criterios or ["cuadratica"])
        filas = {"media": float(np.mean(y_ent)), "mediana": float(np.median(y_ent))}
    else:
        criterios = list(criterios or ["logaritmica", "aciertos"])
        clases = meta.get("clases") or list(np.unique(y_ent))
        p = float(np.mean(y_ent == clases[1]))
        moda = clases[1] if p > 0.5 else clases[0]
        filas = {"moda": (moda, 1.0 if moda == clases[1] else 0.0),
                 "proporcion": (clases[1] if p >= 0.5 else clases[0], p)}
    tabla = pd.DataFrame(index=list(filas), columns=criterios, dtype=float)
    for c in criterios:
        if c in _METRICAS_FUTURAS:
            raise NotImplementedError(f'el criterio "{c}" llega con la versión de la clase 4')
        if c not in SENTIDO:
            raise ValueError(f"criterio es uno de {sorted(SENTIDO)}")
        for fila, pred in filas.items():
            if tarea == "regresion":
                if c not in ("cuadratica", "absoluta"):
                    raise ValueError(f'"{c}" no es un criterio de regresión')
                tabla.loc[fila, c] = float(np.mean(perdida(y, np.full(len(y), pred), c)))
            else:
                etiqueta, prob = pred
                if c == "aciertos":
                    tabla.loc[fila, c] = aciertos(y, np.full(len(y), etiqueta))
                elif c == "logaritmica":
                    y01 = (y == clases[1]).astype(float)
                    tabla.loc[fila, c] = float(np.mean(perdida(y01, np.full(len(y), prob), c)))
                else:
                    raise ValueError(f'"{c}" no es un criterio de clasificación en esta versión')
    tabla.index.name = "benchmark"
    return tabla


# === 7 · Medir: EE, CV, selección ===
# error_estandar, validacion_cruzada, elegir y repetir llegan con la versión de la clase 2.

# === 8 · Capacidad, sesgo y varianza ===


def curva_capacidad(datos, candidatos, conjuntos=("ent", "realidad"), k=None):
    """L de cada candidato en cada conjunto, con su EE, en formato largo.

    candidatos = {valor: construir(df) -> Modelo}; conjuntos de "ent", "val",
    "prueba", "realidad", "despliegue" ("cv" llega con la clase 2).
    Ejemplo: ml.curva_capacidad(datos, {N: lambda df, N=N: ml.ajustar(df, phi=ml.polinomio(N)) for N in range(1, 9)})
    """
    validos = ("ent", "val", "prueba", "realidad", "despliegue", "cv")
    for c in conjuntos:
        if c not in validos:
            raise ValueError(f"conjuntos son de {validos}")
        if c == "cv":
            raise NotImplementedError('conjunto "cv" llega con la versión de la clase 2')
    filas = []
    for valor, construir in candidatos.items():
        modelo = construir(datos.ent)
        for c in conjuntos:
            df = _muestra_grande(datos, c) if c in ("realidad", "despliegue") else getattr(datos, c)
            if len(df) == 0:
                filas.append((valor, c, float("nan"), float("nan")))
                continue
            if modelo.tarea == "regresion":
                l_i = perdida(df["y"], modelo.predecir(df), "cuadratica")
            else:
                y01 = (df["y"].to_numpy() == modelo.clases[1]).astype(float)
                l_i = perdida(y01, modelo.predecir_p(df), "logaritmica")
            ee = float(np.std(l_i, ddof=1) / math.sqrt(len(l_i))) if len(l_i) > 1 else float("nan")
            filas.append((valor, c, float(np.mean(l_i)), ee))
    return pd.DataFrame(filas, columns=["candidato", "conjunto", "L", "ee"])


# === 9 · Regularización ===


def beta_verdadero(datos, phi):
    """Los coeficientes estructurales: proyección de f (sin ruido) en realidad sobre
    las columnas de phi MÁS las omitidas.

    El índice son las columnas de phi ("1" primero); las omitidas van en
    .attrs["omitidas"]; .attrs["exacto"] es True si f es lineal en ese espacio.
    Ejemplo: ml.beta_verdadero(ml.caso(1), None)["x1"]  # 1
    """
    real, _ = _grandes(datos)
    phi_aj = (phi if phi is not None else _Identidad(datos.columnas_x)).ajustar(datos.ent)
    M = _disenar(phi_aj, real, True)
    O = real[datos.omitidas].to_numpy(float) if datos.omitidas else np.empty((len(real), 0))
    X = np.hstack([M.to_numpy(float), O])
    f = (real["f"] if "f" in real else real["prob"]).to_numpy(float)
    coef = np.linalg.lstsq(X, f, rcond=None)[0]
    resto = f - X @ coef
    serie = pd.Series(coef[:M.shape[1]], index=list(M.columns), dtype=float)
    serie.attrs["omitidas"] = dict(zip(datos.omitidas, coef[M.shape[1]:].tolist()))
    serie.attrs["exacto"] = bool(np.sqrt(np.mean(resto ** 2)) < 1e-8 * (1 + np.sqrt(np.mean(f ** 2))))
    return serie


# === 10 · Clasificación: calibración y conformal ===
# Llegan con la versión de la clase 4.

# === 11 · Supuestos y fugas ===
# Llegan con la versión de la clase 5.

# === 12 · Gráficas ===


def _horneado(color, fondo, alfa):
    c = [int(color[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(fondo[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(alfa * x + (1 - alfa) * y):02x}" for x, y in zip(c, b))


# Un rol por concepto: marcador, trazo y color en los dos temas. El color nunca es la
# única señal. "sitio" son los colores del skin; "claro", la paleta colorblind de seaborn.
ROLES = {
    "entrenamiento": {"marcador": "o", "trazo": "", "claro": "#0173b2", "sitio": "#64dce3"},
    "validacion": {"marcador": "^", "trazo": "", "claro": "#de8f05", "sitio": "#ffd166"},
    "prueba": {"marcador": "s", "trazo": "", "claro": "#d55e00", "sitio": "#ff87ad"},
    "realidad": {"marcador": "", "trazo": "--", "claro": "#333333", "sitio": "#fff8ed"},
    "f": {"marcador": "", "trazo": "-", "ancho": 2.8, "claro": "#029e73", "sitio": "#a9e88f"},
    "f_gorro": {"marcador": "", "trazo": "-", "ancho": 1.4, "claro": "#0173b2",
                "sitio": "#64dce3"},
    "piso": {"marcador": "", "trazo": ":", "claro": "#949494", "sitio": "#dfd0e8"},
    "observaciones_nuevas": {"marcador": ".", "trazo": "", "claro": "#8c8c8c",
                             "sitio": _horneado("#fff8ed", "#211033", 0.55)},
    "benchmark": {"marcador": "", "trazo": "-.", "claro": "#cc78bc", "sitio": "#f04cff"},
}

_TEMAS = {"claro": {"fondo": "#ffffff", "panel": "#ffffff", "texto": "#222222",
                    "rejilla": "#dddddd"},
          "sitio": {"fondo": "#211033", "panel": "#2e1945", "texto": "#fff8ed",
                    "rejilla": "#4a3166"}}


def _validar_tema(tema_):
    if tema_ not in _TEMAS:
        raise ValueError('tema es "claro" (notebooks) o "sitio" (generador de figuras)')
    return _TEMAS[tema_]


def _color(rol, tema_):
    return ROLES[rol][tema_]


def tema(nombre="claro"):
    """Fija el estilo de las gráficas: "claro" (notebooks) o "sitio" (fondo del curso).

    Ejemplo: ml.tema("claro")
    """
    t = _validar_tema(nombre)
    import seaborn as sns

    if nombre == "claro":
        sns.set_theme(style="whitegrid", palette="colorblind")
    else:
        sns.set_theme(style="darkgrid", palette="colorblind")
        plt.rcParams.update({"figure.facecolor": t["fondo"], "axes.facecolor": t["panel"],
                             "axes.edgecolor": t["rejilla"], "grid.color": t["rejilla"],
                             "text.color": t["texto"], "axes.labelcolor": t["texto"],
                             "xtick.color": t["texto"], "ytick.color": t["texto"],
                             "savefig.facecolor": t["fondo"]})


def _ejes(ax, tema_, n=1, tamano=(6.4, 4.2)):
    t = _validar_tema(tema_)
    if ax is None:
        fig, ejes = plt.subplots(1, n, figsize=(tamano[0] * (1 if n == 1 else 0.75 * n), tamano[1]))
        ejes = [ejes] if n == 1 else list(ejes)
    else:
        ejes = [ax] if n == 1 else list(ax)
        if len(ejes) != n:
            raise ValueError(f"esta gráfica pide {n} ejes en ax")
        fig = ejes[0].figure
    fig.set_facecolor(t["fondo"])
    for a in ejes:
        a.set_facecolor(t["panel"])
        for lado in a.spines.values():
            lado.set_color(t["rejilla"])
        a.tick_params(colors=t["texto"])
        a.xaxis.label.set_color(t["texto"])
        a.yaxis.label.set_color(t["texto"])
        a.title.set_color(t["texto"])
    return fig, (ejes[0] if n == 1 else ejes)


def _leyenda(ax, tema_):
    t = _TEMAS[tema_]
    if ax.get_legend_handles_labels()[0]:
        ley = ax.legend(frameon=False)
        for texto in ley.get_texts():
            texto.set_color(t["texto"])


def _nota(ax, texto, tema_):
    ax.text(0.02, 0.97, texto, transform=ax.transAxes, va="top", fontsize=9,
            color=_TEMAS[tema_]["texto"])


def _malla(datos, variable, ventana=None, puntos=400):
    if ventana is not None:
        lo, hi = ventana
    else:
        x = datos.ent[variable].to_numpy(float)
        lo, hi = float(np.min(x)), float(np.max(x))
    return np.linspace(lo, hi, puntos)


def _dispersion(ax, df, variable, rol, tema_, gid=None, etiqueta=None, tamano=28):
    marca = ROLES[rol]["marcador"]
    c = ax.scatter(df[variable], df["y"], marker=marca, s=tamano if marca != "." else 10,
                   color=_color(rol, tema_), label=etiqueta, zorder=3)
    c.set_gid(gid)
    return c


_ROL_CONJUNTO = {"ent": "entrenamiento", "val": "validacion", "prueba": "prueba",
                 "cv": "validacion", "realidad": "realidad", "despliegue": "realidad"}


def dibujar_proceso(datos, mostrar_f=True, conjuntos=("ent",), color_por=None,
                    realizaciones=1, puntos_realidad=0, ax=None, tema="claro"):
    """La nube de la muestra contra la primera x visible y, si se puede, la f verdadera.

    realizaciones=3 dibuja tres muestras (semillas semilla, semilla+1, …) con la
    misma f; puntos_realidad dibuja casos nuevos de realidad (observaciones nuevas).
    Ejemplo: ml.dibujar_proceso(datos, realizaciones=3)
    """
    fig, ax = _ejes(ax, tema)
    var = datos.columnas_x[0]
    muestras = [datos] + [datos._rehacer(datos.semilla + i) for i in range(1, int(realizaciones))]
    if color_por is not None:
        col = datos.ent[color_por] if color_por in datos.ent else None
        if col is None:
            raise ValueError(f"color_por: no hay columna {color_por!r} en ent")
        categorica_ = (col.dtype == object or str(col.dtype) == "category" or col.dtype == bool
                       or (np.issubdtype(col.dtype, np.integer) and col.nunique() <= 10))
        if not categorica_:
            raise ValueError("color_por pide una columna categórica (texto o pocos enteros)")
    for i, d in enumerate(muestras):
        for c in conjuntos:
            df = getattr(d, c)
            if len(df) == 0:
                continue
            rol = _ROL_CONJUNTO[c]
            gid = "muestra" if c == "ent" else f"conjunto_{c}"
            if color_por is not None and c == "ent":
                marcas = "osD^vP"
                for j, (valor, trozo) in enumerate(df.groupby(color_por)):
                    s = ax.scatter(trozo[var], trozo["y"], marker=marcas[j % len(marcas)], s=28,
                                   label=f"{color_por} = {valor}" if i == 0 else None, zorder=3)
                    s.set_gid(gid)
                continue
            etiqueta = {"ent": "entrenamiento", "val": "validación", "prueba": "prueba"}[c]
            _dispersion(ax, df, var, rol, tema, gid, etiqueta if i == 0 else None)
    if puntos_realidad:
        real, _ = _grandes(datos)
        rng = np.random.default_rng([datos.semilla_realidad, 9])
        sub = real.iloc[rng.choice(len(real), size=min(int(puntos_realidad), len(real)),
                                   replace=False)]
        _dispersion(ax, sub, var, "observaciones_nuevas", tema, "observaciones_nuevas",
                    "observaciones nuevas")
    if mostrar_f and len(datos.columnas_x) == 1 and datos.f_visible is not None \
            and datos.tarea == "regresion":
        x = _malla(datos, var)
        malla = pd.DataFrame({var: x})
        etiqueta = "f verdadera" if not datos.omitidas else "E[y | lo visible]"
        ln, = ax.plot(x, datos.f_visible(malla), color=_color("f", tema),
                      lw=ROLES["f"]["ancho"], ls="-", label=etiqueta, zorder=2)
        ln.set_gid("f")
    ax.set_xlabel(var)
    ax.set_ylabel("y")
    _leyenda(ax, tema)
    return ax


def _como_dict(modelos):
    if isinstance(modelos, Modelo):
        return {_rotulo(modelos): modelos}
    if isinstance(modelos, (list, tuple)):
        return {_rotulo(m): m for m in modelos}
    if isinstance(modelos, dict):
        return dict(modelos)
    raise ValueError("modelos es un Modelo, una lista de Modelo o un dict {rótulo: Modelo o función}")


def _rotulo(m):
    h = {k: v for k, v in m.hiperparametros.items() if k in ("mu", "n_vecinos", "phi") and v}
    return f"{m.familia} " + ", ".join(f"{k}={v}" for k, v in h.items())


def dibujar_ajuste(modelos, datos=None, ventana=None, ax=None, tema="claro"):
    """Una o varias curvas ajustadas contra la primera x; con ventana, la extrapolación
    sombreada.

    modelos: un Modelo, una lista de Modelo o un dict {rótulo: Modelo o función de x}.
    Ejemplo: ml.dibujar_ajuste({"Taylor": ml.taylor("seno"), "datos": m}, datos)
    """
    fig, ax = _ejes(ax, tema)
    curvas = _como_dict(modelos)
    var = None
    if datos is not None:
        var = datos.columnas_x[0]
    else:
        for m in curvas.values():
            if isinstance(m, Modelo):
                var = m.columnas_x[0]
                break
    var = var or "x"
    if datos is None and ventana is None:
        raise ValueError("pasa datos o ventana=(desde, hasta) para saber dónde dibujar")
    x = _malla(datos, var, ventana)
    malla = pd.DataFrame({var: x})
    estilos = ["-", "--", "-.", ":"]
    for i, (rotulo, m) in enumerate(curvas.items()):
        if isinstance(m, Modelo):
            y = m.predecir_p(malla) if m.tarea == "clasificacion" else m.predecir(malla)
        else:
            y = np.asarray(m(x), float)
        color = _color("f_gorro", tema) if i == 0 else None
        ln, = ax.plot(x, y, ls=estilos[i % len(estilos)], lw=ROLES["f_gorro"]["ancho"],
                      color=color, label=str(rotulo), zorder=4)
        ln.set_gid("ajuste")
    if datos is not None:
        _dispersion(ax, datos.ent, var, "entrenamiento", tema, "muestra", "entrenamiento")
        if ventana is not None:
            lo, hi = datos.ent[var].min(), datos.ent[var].max()
            gris = _TEMAS[tema]["rejilla"]
            if ventana[0] < lo:
                ax.axvspan(ventana[0], lo, color=gris, alpha=0.35, lw=0)
            if ventana[1] > hi:
                ax.axvspan(hi, ventana[1], color=gris, alpha=0.35, lw=0)
    ax.set_xlabel(var)
    ax.set_ylabel("ŷ")
    _leyenda(ax, tema)
    return ax


def dibujar_frontera(modelo, df, vista="cartesianas", ax=None, tema="claro"):
    """La frontera de decisión (Pr = 0.5) de un clasificador binario sobre x1, x2.

    vista="polares" dibuja lo mismo con ejes ángulo y radio.
    Ejemplo: ml.dibujar_frontera(m, datos.ent, vista="polares")
    """
    if vista not in ("cartesianas", "polares"):
        raise ValueError('vista es "cartesianas" o "polares"')
    fig, ax = _ejes(ax, tema)
    a, b = (df.attrs.get("ml", {}).get("columnas_x") or ["x1", "x2"])[:2]
    xa, xb = df[a].to_numpy(float), df[b].to_numpy(float)
    y = df["y"].to_numpy()
    clases = modelo.clases if modelo.clases is not None else np.unique(y)
    if vista == "cartesianas":
        pa = (xa.max() - xa.min()) * 0.08
        pb = (xb.max() - xb.min()) * 0.08
        ga, gb = np.meshgrid(np.linspace(xa.min() - pa, xa.max() + pa, 200),
                             np.linspace(xb.min() - pb, xb.max() + pb, 200))
        malla = pd.DataFrame({a: ga.ravel(), b: gb.ravel()})
        P, U, V = modelo.predecir_p(malla).reshape(ga.shape), ga, gb
        puntos = (xa, xb)
        ax.set_xlabel(a)
        ax.set_ylabel(b)
    else:
        r, th = np.hypot(xa, xb), np.arctan2(xb, xa)
        gth, gr = np.meshgrid(np.linspace(-math.pi, math.pi, 200), np.linspace(0, r.max() * 1.08, 200))
        malla = pd.DataFrame({a: gr.ravel() * np.cos(gth.ravel()), b: gr.ravel() * np.sin(gth.ravel())})
        P, U, V = modelo.predecir_p(malla).reshape(gr.shape), gth, gr
        puntos = (th, r)
        ax.set_xlabel("theta (ángulo)")
        ax.set_ylabel("r (radio)")
    ax.contourf(U, V, P, levels=[0, 0.5, 1], colors=[_color("entrenamiento", tema),
                                                     _color("validacion", tema)], alpha=0.12)
    cs = ax.contour(U, V, P, levels=[0.5], colors=[_TEMAS[tema]["texto"]], linewidths=1.6)
    cs.set_gid("frontera")
    for clase, marca, rol in zip(clases, ("o", "^"), ("entrenamiento", "validacion")):
        sel = y == clase
        ax.scatter(puntos[0][sel], puntos[1][sel], marker=marca, s=18,
                   color=_color(rol, tema), label=f"y = {clase}", zorder=3)
    _leyenda(ax, tema)
    return ax


def imprimir_Phi(modelo, df, filas=5):
    """Muestra las primeras filas de la matriz de diseño Φ ("1" primero) del modelo.

    Ejemplo: ml.imprimir_Phi(m, datos.ent)
    """
    M = modelo.Phi(df).head(filas)
    print(M.to_string(index=False))
    print(f"Φ con columnas {list(M.columns)}: con otra Φ es el mismo ajuste lineal, "
          "β̂ = argmin de la misma pérdida.")


def _tabla_benchmark(benchmark):
    if benchmark is None:
        return None, None
    if isinstance(benchmark, pd.DataFrame):
        fila = next(f for f in ("media", "proporcion", "moda") if f in benchmark.index)
        return float(benchmark.loc[fila].iloc[0]), None
    if isinstance(benchmark, (tuple, list)):
        return float(benchmark[0]), float(benchmark[1])
    return float(benchmark), None


def _linea_piso(ax, piso_, tema_):
    if piso_ is None:
        return
    if math.isinf(piso_):
        _nota(ax, "piso infinito", tema_)
    elif math.isnan(piso_):
        _nota(ax, "piso desconocido", tema_)
    else:
        ln = ax.axhline(piso_, ls=":", color=_color("piso", tema_), lw=1.6, label="piso R_Bayes")
        ln.set_gid("piso")


def _linea_benchmark(ax, benchmark, tema_):
    valor, ee = _tabla_benchmark(benchmark)
    if valor is None:
        return
    ln = ax.axhline(valor, ls="-.", color=_color("benchmark", tema_), lw=1.4, label="benchmark")
    ln.set_gid("benchmark")
    if ee is not None and np.isfinite(ee):
        ax.axhspan(valor - 2 * ee, valor + 2 * ee, color=_color("benchmark", tema_), alpha=0.12,
                   lw=0)


def dibujar_curva_capacidad(tabla, brecha=True, zonas=True, optimo=True, piso=None,
                            benchmark=None, marcar=None, ax=None, tema="claro"):
    """La curva de capacidad: L de entrenamiento y R (u otro conjunto) por candidato.

    piso: un número; benchmark: un número, (valor, ee) o una tabla de benchmarks;
    marcar: el candidato actual.
    Ejemplo: ml.dibujar_curva_capacidad(tabla, piso=ml.piso(datos), marcar=4)
    """
    fig, ax = _ejes(ax, tema)
    candidatos = list(dict.fromkeys(tabla["candidato"]))
    numerico = all(isinstance(c, (int, float, np.integer, np.floating)) for c in candidatos)
    pos = {c: (c if numerico else i) for i, c in enumerate(candidatos)}
    series = {}
    for conjunto, trozo in tabla.groupby("conjunto", sort=False):
        rol = _ROL_CONJUNTO[conjunto]
        xs = [pos[c] for c in trozo["candidato"]]
        estilo = dict(color=_color(rol, tema), marker=ROLES[rol]["marcador"] or None,
                      ls=ROLES[rol]["trazo"] or "-", lw=1.6,
                      label={"ent": "L_ent", "val": "L_val", "prueba": "L_prueba", "cv": "CV_k",
                             "realidad": "R (realidad)", "despliegue": "R"}[conjunto])
        if conjunto in ("val", "prueba", "cv"):
            ax.errorbar(xs, trozo["L"], yerr=2 * trozo["ee"], capsize=3, **estilo)
        else:
            ax.plot(xs, trozo["L"], **estilo)
        series[conjunto] = (np.array(xs, float), trozo["L"].to_numpy(float))
    curva_R = series.get("despliegue") or series.get("realidad")
    if brecha and "ent" in series and curva_R is not None:
        ax.fill_between(series["ent"][0], series["ent"][1], curva_R[1],
                        color=_color("realidad", tema), alpha=0.08, lw=0)
    if curva_R is not None and np.isfinite(curva_R[1]).any():
        i = int(np.nanargmin(curva_R[1]))
        if optimo:
            ln, = ax.plot([curva_R[0][i]], [curva_R[1][i]], marker="*", ms=14, ls="",
                          color=_color("f", tema), label="menor R")
            ln.set_gid("optimo")
        if zonas and 0 < i < len(curva_R[0]) - 1:
            alto = ax.get_ylim()[1]
            ax.text(curva_R[0][0], alto, "subajuste", va="top", fontsize=8,
                    color=_TEMAS[tema]["texto"])
            ax.text(curva_R[0][-1], alto, "sobreajuste", va="top", ha="right", fontsize=8,
                    color=_TEMAS[tema]["texto"])
    _linea_piso(ax, piso, tema)
    _linea_benchmark(ax, benchmark, tema)
    if marcar is not None and marcar in pos:
        base = curva_R if curva_R is not None else next(iter(series.values()))
        j = list(base[0]).index(pos[marcar]) if pos[marcar] in list(base[0]) else None
        if j is not None:
            ln, = ax.plot([base[0][j]], [base[1][j]], marker="o", ms=13, mfc="none", ls="",
                          color=_TEMAS[tema]["texto"], label="actual")
            ln.set_gid("marcar")
    if not numerico:
        ax.set_xticks(range(len(candidatos)))
        ax.set_xticklabels([str(c) for c in candidatos])
    ax.set_xlabel("candidato (capacidad →)")
    ax.set_ylabel("pérdida")
    _leyenda(ax, tema)
    return ax


def dibujar_tres_paneles(modelo, df, ax=None, tema="claro"):
    """ŷ contra y, histograma de residuales y residual contra la primera x (tres ejes).

    Ejemplo: ml.dibujar_tres_paneles(m, datos.val)
    """
    fig, (a1, a2, a3) = _ejes(ax, tema, n=3)
    y = df["y"].to_numpy(float)
    yg = modelo.predecir(df)
    res = y - yg
    c = _color("entrenamiento", tema)
    a1.scatter(yg, y, s=14, color=c)
    lo, hi = min(yg.min(), y.min()), max(yg.max(), y.max())
    a1.plot([lo, hi], [lo, hi], ls="--", color=_color("realidad", tema))
    a1.set_xlabel("ŷ")
    a1.set_ylabel("y")
    a2.hist(res, bins=20, color=c)
    a2.set_xlabel("residual y − ŷ")
    var = modelo.columnas_x[0]
    a3.scatter(df[var], res, s=14, color=c)
    a3.axhline(0, ls="--", color=_color("realidad", tema))
    a3.set_xlabel(var)
    a3.set_ylabel("residual")
    return fig


def dibujar_piso(datos, modelos, perdida="cuadratica", ax=None, tema="claro"):
    """El riesgo de varios modelos contra la línea del piso R_Bayes de esa pérdida.

    Ejemplo: ml.dibujar_piso(datos, {"recta": m1, "cúbica": m3})
    """
    fig, ax = _ejes(ax, tema)
    curvas = _como_dict(modelos)
    valores = [riesgo(m, datos, perdida) for m in curvas.values()]
    barras = ax.bar(range(len(valores)), valores, color=_color("entrenamiento", tema),
                    label="R de cada modelo")
    for b in barras:
        b.set_gid("riesgo")
    ax.set_xticks(range(len(valores)))
    ax.set_xticklabels(list(curvas))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        valor_piso = piso(datos, perdida)
    _linea_piso(ax, valor_piso, tema)
    ax.set_ylabel(f"R ({perdida})")
    _leyenda(ax, tema)
    return ax


def dibujar_perdida_1d(datos_o_df, phi, coeficiente, valores, ax=None, tema="claro"):
    """El perfil de L_ent al mover un coeficiente con los demás fijos en β̂; marca el mínimo.

    Ejemplo: ml.dibujar_perdida_1d(datos, None, "x", np.linspace(0, 8, 81))
    """
    fig, ax = _ejes(ax, tema)
    m = ajustar(datos_o_df, phi=phi)
    if m.tarea != "regresion" and m.tarea != "clasificacion":
        raise ValueError("tarea desconocida")
    df = datos_o_df.ent if isinstance(datos_o_df, Datos) else datos_o_df
    if coeficiente not in m.beta_gorro.index:
        raise ValueError(f"coeficiente es una de {list(m.beta_gorro.index)}")
    M = m.Phi(df).to_numpy(float)
    j = list(m.beta_gorro.index).index(coeficiente)
    y = df["y"].to_numpy()
    if m.tarea == "clasificacion":
        y = (y == m.clases[1]).astype(float)

    def L_ent(v):
        b = m.beta_gorro.to_numpy(float).copy()
        b[j] = v
        eta = M @ b
        if m.tarea == "regresion":
            return float(np.mean((y - eta) ** 2))
        return float(np.mean(np.logaddexp(0, eta) - y * eta))

    vals = np.asarray(valores, float)
    ax.plot(vals, [L_ent(v) for v in vals], color=_color("entrenamiento", tema), lw=1.8,
            label="L_ent")
    bj = float(m.beta_gorro.iloc[j])
    ln, = ax.plot([bj], [L_ent(bj)], marker="*", ms=14, ls="", color=_color("f", tema),
                  label=f"mínimo en β̂ = {bj:.3g}")
    ln.set_gid("minimo")
    ax.set_xlabel(f"coeficiente de {coeficiente}")
    ax.set_ylabel("L_ent")
    _leyenda(ax, tema)
    return ax


# === 13 · Interactividad y taller ===


class _Control:
    def __init__(self, etiqueta, valor, opciones=None):
        self.etiqueta, self.value, self.opciones = etiqueta, valor, opciones

    def __repr__(self):
        return f"control({self.etiqueta!r}, {self.value!r})"


def _widgets():
    if os.environ.get("ML_LAB_PRUEBA") == "1":
        return None
    try:
        import ipywidgets
    except ImportError:
        return None
    return ipywidgets


def deslizador(etiqueta, minimo, maximo, paso, valor):
    """Un deslizador con etiqueta en español (entero si todo es entero).

    Ejemplo: N = ml.deslizador("grado N", 1, 9, 1, 3)
    """
    w = _widgets()
    if w is None:
        return _Control(etiqueta, valor)
    enteros = all(isinstance(v, int) and not isinstance(v, bool)
                  for v in (minimo, maximo, paso, valor))
    clase = w.IntSlider if enteros else w.FloatSlider
    return clase(description=etiqueta, min=minimo, max=maximo, step=paso, value=valor,
                 continuous_update=False, style={"description_width": "initial"})


def selector(etiqueta, opciones, valor=None):
    """Un menú: opciones es una lista o un dict {lo que se lee: lo que se pasa}.

    Ejemplo: f = ml.selector("función", {"recíproca": "inverso", "seno": "seno"})
    """
    pares = list(opciones.items()) if isinstance(opciones, dict) else [(str(o), o) for o in opciones]
    if not pares:
        raise ValueError("selector necesita al menos una opción")
    valor = pares[0][1] if valor is None else valor
    w = _widgets()
    if w is None:
        return _Control(etiqueta, valor, pares)
    return w.Dropdown(description=etiqueta, options=pares, value=valor,
                      style={"description_width": "initial"})


def interruptor(etiqueta, valor=False):
    """Una casilla de sí/no. Ejemplo: ruido = ml.interruptor("con ruido", True)"""
    w = _widgets()
    if w is None:
        return _Control(etiqueta, bool(valor))
    return w.Checkbox(description=etiqueta, value=bool(valor),
                      style={"description_width": "initial"})


def _mostrar():
    if "agg" not in plt.get_backend().lower():
        plt.show()


def laboratorio(funcion, **controles):
    """Corre funcion con controles interactivos (se recalcula al soltar el control).

    Sin ipywidgets, o con ML_LAB_PRUEBA=1, la corre una vez con los valores iniciales.
    Ejemplo: ml.laboratorio(dibuja, N=ml.deslizador("grado N", 1, 9, 1, 3))
    """
    w = _widgets()
    if w is None:
        funcion(**{k: (c.value if hasattr(c, "value") else c) for k, c in controles.items()})
        return None
    argumentos = {k: (c if isinstance(c, w.ValueWidget) else w.fixed(c))
                  for k, c in controles.items()}

    def envoltura(**valores):
        funcion(**valores)
        _mostrar()

    w.interact(envoltura, **argumentos)
    return None


def _buscar_caso(c):
    if isinstance(c, CasoBorde):
        return c
    if isinstance(c, str):
        for cb in CASOS_BORDE.values():
            if cb.nombre == c:
                return cb
        raise ValueError(f"no hay caso llamado {c!r}")
    if c not in CASOS_BORDE:
        raise ValueError(f"no hay caso {c!r} en esta versión: {sorted(CASOS_BORDE)}")
    return CASOS_BORDE[c]


def _correr_caso(cb, clase, opciones):
    print(f"Caso {cb.numero} · {cb.nombre}")
    print(cb.pregunta)
    datos = cb.construir()
    ANALISIS_TALLER[clase](datos, **opciones)
    _mostrar()


def galeria(clase, casos=None, **opciones):
    """Un botón por caso borde: lo carga, lo dibuja con el análisis de la clase y pregunta.

    casos=None: los de esa clase; casos=[1, "lluvia"]: esos, de cualquier clase.
    Ejemplo: ml.galeria(1)
    """
    if clase not in ANALISIS_TALLER:
        raise ValueError(f"la clase {clase} todavía no registra su análisis en ANALISIS_TALLER")
    lista = ([cb for _, cb in sorted(CASOS_BORDE.items()) if cb.clase == clase]
             if casos is None else [_buscar_caso(c) for c in casos])
    if not lista:
        raise ValueError(f"no hay casos de la clase {clase} en esta versión")
    w = _widgets()
    if w is None:
        _correr_caso(lista[0], clase, opciones)
        print("Qué se ve: " + lista[0].que_se_ve)
        return None
    from IPython.display import display

    salida = w.Output()
    botones = []
    for cb in lista:
        boton = w.Button(description=f"Caso {cb.numero}", tooltip=cb.nombre)

        def al_pulsar(_, cb=cb):
            salida.clear_output(wait=True)
            with salida:
                _correr_caso(cb, clase, opciones)
                revelar = w.Button(description="¿Qué se ve?")
                texto = w.Output()

                def mostrar(_):
                    with texto:
                        print(cb.que_se_ve)

                revelar.on_click(mostrar)
                display(w.VBox([revelar, texto]))

        boton.on_click(al_pulsar)
        botones.append(boton)
    display(w.VBox([w.HBox(botones), salida]))
    return None


def taller(datos, clase, **opciones):
    """Corre el análisis de esa clase sobre tus datos (ANALISIS_TALLER[clase]).

    Ejemplo: ml.taller(ml.proceso(n=40, f=lambda d: d["x"] ** 2), 1, N_max=8)
    """
    if clase not in ANALISIS_TALLER:
        raise ValueError(f"la clase {clase} todavía no registra su análisis en ANALISIS_TALLER")
    return ANALISIS_TALLER[clase](datos, **opciones)


def _taller_c1(datos, phi=None, N_max=10):
    """Clase 1. Regresión: la nube con f y el piso, la curva de capacidad de los
    polinomios N ≤ N_max (L_ent, R, piso y benchmark) y, si das phi, su Φ y su R.
    Clasificación: logística con y sin phi, su frontera y los aciertos en el
    despliegue contra los de la moda."""
    if datos.tarea == "regresion":
        dibujar_proceso(datos)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            valor_piso = piso(datos)
        if len(datos.columnas_x) == 1:
            var = datos.columnas_x[0]
            candidatos = {N: (lambda df, N=N: ajustar(df, phi=polinomio(N, variable=var)))
                          for N in range(1, int(N_max) + 1)}
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                tabla = curva_capacidad(datos, candidatos, conjuntos=("ent", "despliegue"))
            dibujar_curva_capacidad(tabla, piso=valor_piso,
                                    benchmark=benchmarks(datos, _grandes(datos)[1]))
        if phi is not None:
            m = ajustar(datos, phi=phi)
            imprimir_Phi(m, datos.ent)
            print(f"L_ent = {L(m, datos.ent):.3f} · R = {riesgo(m, datos):.3f} · "
                  f"piso = {valor_piso:.3f}")
        return None
    modelos = {"cartesianas": ajustar(datos, tarea="clasificacion")}
    if phi is not None:
        modelos["con tu φ"] = ajustar(datos, phi=phi, tarea="clasificacion")
    moda = benchmarks(datos, _grandes(datos)[1]).loc["moda", "aciertos"]
    for nombre, m in modelos.items():
        ax = dibujar_frontera(m, datos.ent)
        ax.set_title(nombre)
        print(f"{nombre}: aciertos en el despliegue = {desempeno(m, datos, 'aciertos'):.3f} "
              f"(la moda: {moda:.3f})")
    return None


ANALISIS_TALLER = {1: _taller_c1}


# Bitácora técnica para el curioso: qué cambió en cada versión.
CAMBIOS = {
    "1.0": "Núcleo: piezas, procesos con realidad y despliegue, casos 1, 2 y 23, las Φ de "
           "la clase 1, ajustar (regresión y logística binaria) con la convención de μ, "
           "vecinos, pérdidas, aciertos, piso, benchmarks, curva de capacidad, "
           "beta_verdadero, las gráficas de la clase 1 y el taller.",
}


# --- Superficie pública (la lee tools/test_aprendizaje_maquina.py) ---------


def _repr_estable(valor):
    return re.sub(r" at 0x[0-9a-fA-F]+", "", repr(valor))


def _firma(objeto):
    try:
        sig = inspect.signature(objeto)
    except (TypeError, ValueError):
        return "()"
    partes, estrella = [], False
    for p in sig.parameters.values():
        if p.kind is p.VAR_POSITIONAL:
            texto, estrella = "*" + p.name, True
        elif p.kind is p.VAR_KEYWORD:
            texto = "**" + p.name
        else:
            if p.kind is p.KEYWORD_ONLY and not estrella:
                partes.append("*")
                estrella = True
            texto = p.name
        if p.default is not p.empty:
            texto += "=" + _repr_estable(p.default)
        partes.append(texto)
    return "(" + ", ".join(partes) + ")"


def _superficie():
    salida = {}
    modulo = globals()
    for nombre in __all__:
        objeto = modulo[nombre]
        if inspect.isclass(objeto):
            if objeto.__module__ != __name__:
                salida[nombre] = "alias:" + objeto.__name__
            elif issubclass(objeto, BaseException):
                salida[nombre] = "excepcion"
            else:
                metodos = {"__init__": _firma(objeto)}
                for m in sorted(vars(objeto)):
                    if not m.startswith("_") and callable(getattr(objeto, m)):
                        metodos[m] = _firma(getattr(objeto, m))
                salida[nombre] = metodos
        elif callable(objeto):
            salida[nombre] = _firma(objeto)
        else:
            salida[nombre] = "constante:" + type(objeto).__name__
    salida["__claves__"] = {
        "PROCESOS": sorted(modulo["PROCESOS"]),
        "CASOS_BORDE": sorted(modulo["CASOS_BORDE"]),
        "ANALISIS_TALLER": sorted(modulo["ANALISIS_TALLER"]),
    }
    return salida
