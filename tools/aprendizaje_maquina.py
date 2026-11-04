"""ml_lab · el laboratorio de la unidad de aprendizaje de máquina.

Un solo archivo que se lee de arriba abajo: piezas aleatorias, procesos que
generan datos con una f conocida, representaciones Φ, el ajuste, las pérdidas
y las gráficas que usan las páginas y los notebooks. Todo lo aleatorio recibe
una `semilla`; la población (la muestra enorme `realidad` y la de uso
`despliegue`) no cambia con ella.

Uso: import ml_lab as ml; datos = ml.PROCESOS["entregas"](); m = ml.ajustar(datos)
"""

# === 0 · Versión y tema ===

VERSION = "1.2"

import ast  # noqa: E402
import copy  # noqa: E402
import hashlib  # noqa: E402
import inspect  # noqa: E402
import math  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import warnings  # noqa: E402
from collections import OrderedDict  # noqa: E402
from dataclasses import dataclass  # noqa: E402
from fractions import Fraction  # noqa: E402
from typing import Callable, Union  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import optimize, special, stats  # noqa: E402

__all__ = [
    "VERSION", "CAMBIOS", "NoAplica", "requiere",
    # 1 · piezas
    "Pieza", "Mecanismo", "normal", "uniforme", "categorica", "ar1", "efecto_grupo",
    # 2 · procesos
    "Datos", "proceso", "proceso_clasificacion", "anillos", "PROCESOS", "CasoBorde",
    "CASOS_BORDE", "caso", "entregas_curvas",
    # 3 · separaciones
    "separar", "pliegues", "Particion",
    # 4 · representaciones
    "Phi", "polinomio", "columnas", "polares", "periodicas", "dummies", "combinar", "taylor",
    # 5 · ajuste
    "Modelo", "ajustar", "ajustar_otro",
    # 6 · pérdidas y métricas
    "perdida", "Criterio", "SENTIDO", "evaluar", "L", "riesgo", "desempeno", "piso", "mse",
    "aciertos", "benchmarks",
    # 7 · medir
    "repetir", "error_por_zona", "no_free_lunch", "error_estandar", "intervalo",
    "validacion_cruzada", "ResultadoCV", "diferencia_pareada", "diferencia_por_pliegue",
    "elegir", "Seleccion", "cv_anidada", "optimismo_por_seleccion", "capacidad_elegida",
    "reparto",
    # 8 · capacidad
    "curva_capacidad", "sesgo_varianza", "SesgoVarianza", "curva_aprendizaje",
    # 9 · regularización
    "beta_verdadero",
    # 12 · gráficas
    "ROLES", "tema", "dibujar_proceso", "dibujar_ajuste", "dibujar_frontera", "imprimir_Phi",
    "dibujar_curva_capacidad", "dibujar_tres_paneles", "dibujar_piso", "dibujar_perdida_1d",
    "dibujar_elecciones", "dibujar_no_free_lunch", "dibujar_pliegues",
    "dibujar_histograma_estimaciones", "dibujar_cv", "dibujar_abanico", "dibujar_sesgo_varianza",
    "dibujar_curva_aprendizaje", "dibujar_cajas_pliegues", "dibujar_diana", "dibujar_contratos",
    "dibujar_reparto",
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


class _Ar1(Mecanismo):
    def __init__(self, persistencia, desv):
        if not -1 < persistencia < 1:
            raise ValueError("la persistencia de ar1 está en (-1, 1): con |a| >= 1 no es estacionario")
        if desv < 0:
            raise ValueError("la desviación de ar1 no puede ser negativa")
        self.persistencia, self.desv = float(persistencia), float(desv)
        self.varianza = self.desv ** 2 / (1 - self.persistencia ** 2)
        self.nombre, self.crea = "ar1", ["t"]

    def preparar(self, n, rng):
        return {"t": np.arange(int(n))}

    def muestrear(self, df, rng):
        from scipy.signal import lfilter

        orden = np.argsort(np.asarray(df["t"]), kind="stable")
        u = rng.normal(0, self.desv, len(df))
        if len(df):
            u[0] = rng.normal(0, math.sqrt(self.varianza))  # arranca en la estacionaria
        eps = np.empty(len(df))
        eps[orden] = lfilter([1.0], [1.0, -self.persistencia], u)
        return eps

    def varianza_en(self, df):
        return np.full(len(df), self.varianza)

    def __repr__(self):
        return f"ar1(persistencia={self.persistencia}, desv={self.desv})"


_SEMILLA_GRUPOS = 20_261_102
_BLOQUE_GRUPOS = 1024


class _EfectoGrupo(Mecanismo):
    def __init__(self, n_grupos, desv_grupo, desv):
        if int(n_grupos) < 1:
            raise ValueError("n_grupos es un entero >= 1")
        if desv_grupo < 0 or desv < 0:
            raise ValueError("las desviaciones de efecto_grupo no pueden ser negativas")
        self.n_grupos, self.desv_grupo, self.desv = int(n_grupos), float(desv_grupo), float(desv)
        self.varianza = self.desv_grupo ** 2 + self.desv ** 2
        self.nombre, self.crea = "efecto_grupo", ["grupo"]

    def preparar(self, n, rng):
        return {"grupo": rng.permutation(np.arange(int(n)) % self.n_grupos)}

    def preparar_nuevos(self, n, rng):
        """Grupos que la muestra nunca vio (ids desde n_grupos), unas 10 filas por grupo."""
        return {"grupo": self.n_grupos + rng.permutation(np.arange(int(n)) // 10)}

    def _efecto(self, grupos):
        """El efecto de cada grupo es parte de la población: lo fija su id, no la semilla."""
        g = np.asarray(grupos, dtype=np.int64)
        salida = np.empty(len(g))
        for b in np.unique(g // _BLOQUE_GRUPOS):
            z = np.random.default_rng([_SEMILLA_GRUPOS, int(b)]).normal(size=_BLOQUE_GRUPOS)
            dentro = g // _BLOQUE_GRUPOS == b
            salida[dentro] = z[g[dentro] % _BLOQUE_GRUPOS]
        return self.desv_grupo * salida

    def muestrear(self, df, rng):
        return self._efecto(df["grupo"]) + rng.normal(0, self.desv, len(df))

    def varianza_en(self, df):
        return np.full(len(df), self.varianza)

    def __repr__(self):
        return (f"efecto_grupo(n_grupos={self.n_grupos}, desv_grupo={self.desv_grupo}, "
                f"desv={self.desv})")


def ar1(persistencia=0.8, desv=1.0):
    """Ruido con memoria: crea "t" y saca ε_t = a·ε_{t−1} + u_t en el orden de t.

    u ~ N(0, desv²); arranca en la estacionaria, Var(ε) = desv² / (1 − a²).
    Desde: 1.2 (clase 2). Ejemplo: ml.proceso(n=240, ruido=ml.ar1(0.95, 3))
    """
    return _Ar1(persistencia, desv)


def efecto_grupo(n_grupos=20, desv_grupo=1.0, desv=1.0):
    """Ruido por grupo: crea "grupo"; ε = efecto del grupo + ruido individual.

    Var(ε) = desv_grupo² + desv². Los efectos son de la población (no cambian con la semilla).
    Desde: 1.2 (clase 2). Ejemplo: ml.proceso(n=240, ruido=ml.efecto_grupo(24, 4, 1))
    """
    return _EfectoGrupo(n_grupos, desv_grupo, desv)


class _Mezcla(Pieza):
    """Varias piezas en proporciones fijas: n·p filas de cada una (redondeo al final)."""

    def __init__(self, piezas, probs):
        self.piezas, self.probs = list(piezas), np.asarray(probs, float)
        self.nombre = "mezcla"
        medias = np.array([p.media for p in self.piezas], float)
        varianzas = np.array([p.varianza for p in self.piezas], float)
        self.media = float(self.probs @ medias)
        self.varianza = float(self.probs @ (varianzas + medias ** 2) - self.media ** 2)

    def muestrear(self, n, rng):
        cuentas = np.floor(self.probs * n).astype(int)
        cuentas[0] += int(n) - cuentas.sum()
        trozos = [np.asarray(p.muestrear(int(c), rng), float) for p, c in zip(self.piezas, cuentas)]
        return rng.permutation(np.concatenate(trozos))

    def __repr__(self):
        return f"mezcla({self.piezas!r}, {self.probs.tolist()!r})"


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

    def rehacer(self, semilla: int, con_realidad: bool = False) -> "Datos":
        """Otra muestra del mismo proceso con otra semilla; la población (realidad,
        despliegue) no cambia. Es una fabrica(semilla) lista para sesgo_varianza.

        Desde: 1.2 (clase 2). Ejemplo: otra = datos.rehacer(7)
        """
        if getattr(self, "_rehacer", None) is None:
            raise ValueError("este Datos no lo hizo un proceso de ml_lab: no sé rehacerlo")
        return self._rehacer(int(semilla), con_realidad)

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


_SEMILLA_HUELLA = 20_261_104
_N_HUELLA = 64


def _huella(objeto, muestra):
    """Identidad, clase, estado y lo que devolvió con el generador fijo de la huella."""
    try:
        estado = repr(sorted((k, repr(v)) for k, v in vars(objeto).items()))
    except TypeError:
        estado = ""
    arreglo = np.asarray(muestra).reshape(-1)
    try:
        crudo = np.ascontiguousarray(arreglo, dtype=float).tobytes()
    except (TypeError, ValueError):
        crudo = repr(arreglo.tolist()).encode()
    tipo = type(objeto)
    return (id(objeto), tipo.__module__, tipo.__qualname__, estado,
            hashlib.sha1(crudo).hexdigest())


def _validar_reservados(x, reservados):
    """Los nombres que ml_lab escribe en las tablas no pueden ser variables de x."""
    for nombre in x:
        if nombre in reservados or str(nombre).startswith("_"):
            raise ValueError(f"x no puede llamar {nombre!r} a una variable: ml_lab usa ese nombre "
                             f"para su columna (reservados: {', '.join(reservados)} y los que "
                             "empiezan con _)")


def _aplicar_deriva(deriva, t, xs, n, rng, f):
    """Aplica deriva(t) sobre las variables de xs (en su lugar) y devuelve la f que vale."""
    cambios = deriva(t)
    if not isinstance(cambios, dict):
        raise ValueError('deriva(t) devuelve un dict: {"x": ml.uniforme(4, 9)} o {"f": nueva_f}')
    for k, v in cambios.items():
        if k == "f":
            if not callable(v):
                raise ValueError('la clave "f" de deriva es una función f(d) -> arreglo')
            f = v
        elif k not in xs:
            raise ValueError(f"deriva nombra {k!r}, que no es una variable de x ({list(xs)})")
        elif isinstance(v, Pieza):
            xs[k] = np.asarray(v.muestrear(n, rng))
        else:
            v = np.asarray(v)
            if v.shape != (n,):
                raise ValueError(f"deriva[{k!r}] es una Pieza o un arreglo del largo de t ({n})")
            xs[k] = v
    return f


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
        _validar_reservados(self.x, ("y", "f", "f_visible"))
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
        """Identifica la población por lo que HACE, no por su repr: una pieza del
        taller con la plantilla tiene repr «nombre()» sin sus parámetros. Cada pieza,
        el ruido y f entran con su identidad, su estado y una huella de lo que
        devuelven con un generador fijo; así dos piezas con el mismo nombre y otro
        parámetro, una pieza cambiada en su lugar o una f cuya global cambió no
        comparten la caché."""
        rng = np.random.default_rng(_SEMILLA_HUELLA)
        xs = self._x(_N_HUELLA, rng)
        ctx = self.mecanismo.preparar(_N_HUELLA, rng) if self.mecanismo is not None else {}
        todo = pd.DataFrame({**xs, **ctx})
        if self.mecanismo is not None:
            ruido = self.mecanismo.muestrear(todo, np.random.default_rng(_SEMILLA_HUELLA))
        else:
            ruido = self.ruido.muestrear(_N_HUELLA, np.random.default_rng(_SEMILLA_HUELLA))
        return ("reg", _huella(self.f, self._evaluar_f(todo)), id(self.cerrada),
                tuple((k, _huella(v, xs[k])) for k, v in self.x.items()),
                _huella(self.ruido, ruido),
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
            return float(getattr(self.mecanismo, "varianza", float("nan"))) * self.c_y ** 2
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

    def _contexto(self, n, rng, cambio):
        """Las columnas de contexto; con cambio, las del despliegue (t que sigue, grupos nuevos)."""
        if self.mecanismo is None:
            return {}
        if cambio and cambio.get("nuevos"):
            if not hasattr(self.mecanismo, "preparar_nuevos"):
                raise ValueError('despliegue="grupos_nuevos" pide un ruido que sepa crear grupos '
                                 "nuevos, como efecto_grupo")
            ctx = self.mecanismo.preparar_nuevos(n, rng)
        else:
            ctx = self.mecanismo.preparar(n, rng)
        if cambio and cambio.get("t0") is not None and "t" in ctx:
            ctx = {**ctx, "t": int(cambio["t0"]) + np.asarray(ctx["t"])}
        return ctx

    def completo(self, n, rng, cambio=None):
        """n filas completas (con las columnas privadas _f, _m, _v). cambio = {"t0": primer t
        (la muestra y el despliegue de "futuro"), "nuevos": grupos nuevos, "deriva": deriva,
        "t_realidad": t de una x llamada t en realidad}."""
        xs = self._x(n, rng)
        ctx = self._contexto(n, rng, cambio)
        f_usar = self.f
        if cambio and "t" in self.x:
            if cambio.get("t0") is not None:
                xs["t"] = int(cambio["t0"]) + np.arange(int(n))
            elif cambio.get("t_realidad") is not None:
                xs["t"] = np.arange(int(n)) % int(cambio["t_realidad"])
        if cambio and cambio.get("deriva") is not None:
            t = ctx.get("t", xs.get("t"))
            f_usar = _aplicar_deriva(cambio["deriva"], None if t is None else np.asarray(t),
                                     xs, n, rng, self.f)
        todo = pd.DataFrame({**xs, **ctx})
        fval = np.asarray(f_usar(todo), dtype=float).reshape(-1) * np.ones(len(todo))
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
            if k in self.visibles and k in d:  # las omitidas nunca se escalaron
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

    def f_visible_es_f(self):
        """E[y | lo visible] = f solo sin omitidas, sin endogeneidad y con ruido de media 0."""
        if self.omitidas or self.endogeno:
            return False
        if self.mecanismo is not None:
            return True
        m = float(self.ruido.media)
        return not np.isfinite(m) or m == 0.0

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


def _poblacion_grande(pob, n_realidad, semilla_realidad, uso=None):
    """Las dos muestras enormes (completas, con columnas privadas), en caché.

    uso = (despliegue_como, n de la muestra, deriva): de qué proceso sale despliegue."""
    uso = uso or ("igual", None, None)
    como, n_muestra, deriva = uso
    llave = (pob.llave(), n_realidad, semilla_realidad, como,
             n_muestra if como == "futuro" else None, id(deriva) if deriva is not None else None)
    if llave in _CACHE:
        _CACHE.move_to_end(llave)
        return _CACHE[llave][1]
    salida = []
    for flujo in (1, 2):
        rng = np.random.default_rng([semilla_realidad, flujo])
        if hasattr(pob, "grande"):
            c = pob.grande(n_realidad, rng, flujo)
        elif como == "igual":
            c = pob.completo(n_realidad, rng)
        elif flujo == 1:
            c = pob.completo(n_realidad, rng, {"t_realidad": n_muestra} if como == "futuro" else None)
        else:
            c = pob.completo(n_realidad, rng, {"t0": n_muestra if como == "futuro" else None,
                                               "nuevos": como == "grupos_nuevos", "deriva": deriva})
        for k, v in pob.oraculos(c, semilla_realidad).items():
            c[k] = v
        if flujo == 2 and deriva is not None and pob.tipo not in ("directa",) \
                and "f_visible" in c:  # f_visible de forma cerrada o Monte Carlo ya no vale
            c["f_visible"] = np.nan
            if "_varmc" in c:
                c["_varmc"] = np.nan
        salida.append(c)
    _CACHE[llave] = (pob, tuple(salida), deriva)  # guarda pob y deriva para que su id no se reuse
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


def _estratos(y, tarea=None):
    """Clases en clasificación; en regresión (o y continua) deciles de y."""
    y = np.asarray(y)
    continua = tarea == "regresion" or (tarea is None and y.dtype.kind == "f"
                                        and len(np.unique(y)) > max(10, len(y) // 5))
    if not continua:
        return y
    rangos = stats.rankdata(y, method="ordinal") - 1
    return np.minimum((rangos * 10) // max(len(y), 1), 9)


def _partir_por_tiempo(t, fracciones):
    """En orden de t: ent lo más viejo, luego val, prueba lo más reciente."""
    fr = _validar_fracciones(fracciones)
    orden = np.argsort(np.asarray(t), kind="stable")
    n = len(orden)
    a = int(round(n * fr[0]))
    b = n if fr[2] == 0 else min(n, a + int(round(n * fr[1])))
    if fr[1] == 0 and fr[2] == 0:
        a = b = n
    return tuple(np.sort(orden[i:j]) for i, j in ((0, a), (a, b), (b, n)))


def _partir_por_grupo(grupos, fracciones, rng):
    """Grupos enteros en cada parte, en orden al azar, hasta llenar cada fracción de filas."""
    fr = _validar_fracciones(fracciones)
    grupos = np.asarray(grupos)
    unicos = np.unique(grupos)
    unicos = unicos[rng.permutation(len(unicos))]
    tamanos = np.array([np.sum(grupos == g) for g in unicos], float)
    centro = (np.cumsum(tamanos) - tamanos / 2) / max(tamanos.sum(), 1)
    corte = np.where(centro < fr[0], 0, np.where(centro < fr[0] + fr[1], 1, 2))
    for k in range(3):  # una parte pedida vacía nunca recibe grupos por redondeo
        if fr[k] == 0:
            corte[corte == k] = max(j for j in range(3) if fr[j] > 0)
    return tuple(np.flatnonzero(np.isin(grupos, unicos[corte == k])) for k in range(3))


def _validar_fracciones(fracciones):
    fr = tuple(float(v) for v in fracciones)
    if len(fr) != 3 or min(fr) < 0 or not math.isclose(sum(fr), 1.0, abs_tol=1e-9):
        raise ValueError("fracciones son tres números no negativos que suman 1, p. ej. (0.6, 0.2, 0.2)")
    return fr


def _indices_de_separar(df, como, fracciones, rng, columna_y="y", columna_tiempo="t",
                        columna_grupo="grupo", tarea=None):
    if como not in _SEPARAR:
        raise ValueError(f"separar es uno de {_SEPARAR}, no {como!r}"
                         + (' ("temporal" es de pliegues)' if como == "temporal" else ""))
    if como == "azar":
        return _partir_indices(len(df), fracciones, rng)
    if como == "estratificado":
        if columna_y not in df:
            raise ValueError(f'separar="estratificado" necesita la columna {columna_y!r}')
        return _partir_indices(len(df), fracciones, rng, _estratos(df[columna_y], tarea))
    if como == "tiempo":
        if columna_tiempo not in df:
            raise ValueError(f'separar="tiempo" necesita una columna {columna_tiempo!r}: un ruido '
                             'que la cree (ar1) o una x llamada "t"')
        return _partir_por_tiempo(df[columna_tiempo], fracciones)
    if columna_grupo not in df:
        raise ValueError(f'separar="grupo" necesita una columna {columna_grupo!r}: un ruido que '
                         "la cree (efecto_grupo)")
    return _partir_por_grupo(df[columna_grupo], fracciones, rng)


def _validar_despliegue(despliegue, deriva, columnas):
    if deriva is not None and despliegue == "igual":
        raise ValueError('`deriva` solo vale con despliegue="futuro" u "otra_poblacion"')
    if despliegue not in _DESPLIEGUE:
        raise ValueError(f"despliegue debe ser uno de {_DESPLIEGUE}, no {despliegue!r}")
    if deriva is not None and despliegue == "grupos_nuevos":
        raise ValueError('`deriva` solo vale con despliegue="futuro" u "otra_poblacion"')
    if deriva is not None and not callable(deriva):
        raise ValueError("deriva es una función deriva(t) -> dict")
    if despliegue == "futuro" and "t" not in columnas:
        raise ValueError('despliegue="futuro" exige una columna t: un ruido que la cree (ar1) '
                         'o una x llamada "t"')
    if despliegue == "grupos_nuevos" and "grupo" not in columnas:
        raise ValueError('despliegue="grupos_nuevos" exige una columna grupo: un ruido que la '
                         "cree (efecto_grupo)")


def _armar(pob, muestra, fracciones, rng_particion, separar, n_realidad, semilla,
           semilla_realidad, con_realidad, descripcion, rehacer, K=None, clases=None,
           indices=None, despliegue_como="igual", uso=None):
    cols_x = list(pob.visibles)
    ctx = list(pob.contexto)
    meta = _meta(cols_x, ctx, pob.tarea, K, clases)
    publicas = cols_x + ["y"] + ctx
    if indices is not None:
        i_ent, i_val, i_pru = indices
    elif separar in ("azar", "estratificado") and pob.tarea != "regresion":
        estratos = muestra["y"].to_numpy() if separar == "estratificado" else None
        i_ent, i_val, i_pru = _partir_indices(len(muestra), fracciones, rng_particion, estratos)
    else:
        i_ent, i_val, i_pru = _indices_de_separar(muestra, separar, fracciones, rng_particion,
                                                  tarea=pob.tarea)
    partes = [_con_meta(muestra.iloc[i][publicas].copy(), meta) for i in (i_ent, i_val, i_pru)]
    columnas_grandes = cols_x + list(pob.omitidas) + ctx + ["y"] + pob.nombres_oraculos()
    if con_realidad:
        real_c, desp_c = _poblacion_grande(pob, n_realidad, semilla_realidad, uso)
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
        separacion=separar, despliegue_como=despliegue_como, semilla=semilla,
        semilla_realidad=semilla_realidad, descripcion=descripcion,
    )
    datos._pob = pob
    datos._grande = (n_realidad, semilla_realidad, columnas_grandes, meta, uso)
    datos._rehacer = rehacer
    return datos


def _grandes(datos):
    """(realidad, despliegue) aunque el proceso se haya pedido con con_realidad=False."""
    if datos.realidad is not None and datos.despliegue is not None:
        return datos.realidad, datos.despliegue
    if not hasattr(datos, "_pob"):
        raise ValueError("este Datos no trae realidad ni despliegue")
    n_r, s_r, cols, meta, uso = datos._grande
    real_c, desp_c = _poblacion_grande(datos._pob, n_r, s_r, uso)
    return _con_meta(_publica(real_c, cols), meta), _con_meta(_publica(desp_c, cols), meta)


def _proceso(n=200, x=None, f=_f_por_omision, ruido=None, correlacion=None, endogeno=0.0,
             omitir=None, escala=None, faltantes=None, separar="azar",
             fracciones=(0.6, 0.2, 0.2), despliegue="igual", deriva=None, n_realidad=100_000,
             semilla=0, semilla_realidad=0, con_realidad=True, f_visible_cerrada=None,
             descripcion=None):
    if faltantes is not None:
        raise NotImplementedError("`faltantes` llega con la versión de la clase 4")
    if separar not in _SEPARAR:
        raise ValueError(f"separar debe ser uno de {_SEPARAR}, no {separar!r}")
    x = {"x": uniforme(0, 1)} if x is None else x
    ruido = normal(0, 1) if ruido is None else ruido
    pob = _Poblacion(x, f, ruido, correlacion, endogeno, omitir, escala, f_visible_cerrada)
    _validar_despliegue(despliegue, deriva, list(pob.x) + pob.contexto)
    if separar == "tiempo" and "t" not in list(pob.x) + pob.contexto:
        raise ValueError('separar="tiempo" necesita una columna t: un ruido que la cree (ar1) '
                         'o una x llamada "t"')
    if separar == "grupo" and "grupo" not in pob.contexto:
        raise ValueError('separar="grupo" necesita una columna grupo: un ruido que la cree '
                         "(efecto_grupo)")
    cambio = {"t0": 0} if despliegue == "futuro" else None
    muestra = pob.completo(int(n), np.random.default_rng([semilla, 0]), cambio)
    argumentos = dict(n=n, x=x, f=f, ruido=ruido, correlacion=correlacion, endogeno=endogeno,
                      omitir=omitir, escala=escala, faltantes=faltantes, separar=separar,
                      fracciones=fracciones, despliegue=despliegue, deriva=deriva,
                      n_realidad=n_realidad, semilla_realidad=semilla_realidad,
                      f_visible_cerrada=f_visible_cerrada, descripcion=descripcion)

    def rehacer(s, con_realidad=False):
        return _proceso(**{**argumentos, "semilla": s, "con_realidad": con_realidad})

    desc = descripcion or f"proceso con {', '.join(pob.visibles)} visibles"
    return _armar(pob, muestra, fracciones, np.random.default_rng([semilla, 3]), separar,
                  n_realidad, semilla, semilla_realidad, con_realidad, desc, rehacer,
                  despliegue_como=despliegue, uso=(despliegue, int(n), deriva))


def proceso(n=200, x={"x": uniforme(0, 1)}, f=_f_por_omision, ruido=normal(0, 1),
            correlacion=None, endogeno=0.0, omitir=None, escala=None, faltantes=None,
            separar="azar", fracciones=(0.6, 0.2, 0.2), despliegue="igual", deriva=None,
            n_realidad=100_000, semilla=0, semilla_realidad=0, con_realidad=True):
    """Genera datos y = f(x) + ε de un proceso conocido, partidos en ent, val y prueba.

    f(d) recibe un DataFrame con TODAS las variables (visibles y omitidas, sin
    escalar) y el contexto. escala solo cambia unidades; {"y": c} multiplica y.
    separar dice cómo se parte la muestra; despliegue, de dónde sale la muestra de uso.
    Ejemplo: datos = ml.proceso(n=50, x={"x": ml.uniforme(0, 6)}, f=lambda d: 10 + 4 * d["x"])

    separar: "azar"; "estratificado" (clases, o deciles de y en regresión); "tiempo"
    (lo más reciente a prueba; pide t); "grupo" (grupos enteros en cada parte; pide
    grupo). despliegue: "igual" (otra muestra de la misma población); "futuro" (pide
    t: la muestra ocupa t = 0…n−1 y despliegue los n_realidad pasos que siguen,
    t = n…n+n_realidad−1, con OTRA realización estacionaria del ruido, así que R es
    el riesgo a largo plazo, sin aprovechar el ruido reciente; en los primeros pasos
    el error real puede ser menor si el ruido recuerda); "grupos_nuevos" (grupos que
    la muestra no vio); "otra_poblacion" (con deriva). deriva(t) recibe los t de
    despliegue (None si no hay t) y devuelve un dict: variable → Pieza (nueva
    distribución) o arreglo del largo de t; la clave "f" reemplaza a f (cambio de
    concepto, caso 28). Con despliegue="igual", deriva es un ValueError. Con deriva y
    f_visible de forma cerrada o por Monte Carlo, el despliegue la trae como nan.
    Una x llamada t con "futuro" pasa a ser 0…n−1 en la muestra, n… en despliegue y
    0…n−1 repetido en realidad. Desde: 1.2 (clase 2) para todo lo anterior;
    faltantes lanza NotImplementedError hasta la versión de la clase 4.
    endogeno = corr(x1, ε) (x1, o la primera variable si no hay "x1"):
    ε = c·σ·z1 + sqrt(1 − c²)·u, con z1 la x1 estandarizada y u el ruido.
    Flujos: la muestra sale de default_rng([semilla, 0]), la partición de
    [semilla, 3], realidad de [semilla_realidad, 1] y despliegue de [semilla_realidad, 2].
    """
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
    if separar not in ("azar", "estratificado"):
        raise ValueError('anillos separa "azar" o "estratificado" (no tiene t ni grupo)')
    pob = _PoblacionAnillos(radio_interior, radio_exterior, grosor, ruido)
    muestra = pob.completo(int(n), np.random.default_rng([semilla, 0]))
    argumentos = dict(n=n, radio_interior=radio_interior, radio_exterior=radio_exterior,
                      grosor=grosor, ruido=ruido, separar=separar, fracciones=fracciones)

    def rehacer(s, con_realidad=False):
        return anillos(**{**argumentos, "semilla": s})

    return _armar(pob, muestra, fracciones, np.random.default_rng([semilla, 3]), separar,
                  100_000, semilla, 0, True, "dos anillos", rehacer, K=2, clases=[0, 1])


def _puntaje_por_omision(d):
    return 1.5 * d["x1"] + 1.0 * d["x2"]


class _PoblacionClasificacion:
    """Binaria: z = puntaje(d) y Pr(y=1 | x) = σ(z). Sin omitidas ni contexto (1.1)."""

    tarea = "clasificacion"
    omitidas = []
    contexto = []
    tipo = "directa"
    c_y = 1.0

    def __init__(self, x, puntaje):
        self.x = dict(x)
        if not self.x:
            raise ValueError("x necesita al menos una variable")
        for nombre, pieza in self.x.items():
            if not isinstance(pieza, Pieza):
                raise ValueError(f"x[{nombre!r}] debe ser una Pieza (normal, uniforme, ...)")
        _validar_reservados(self.x, ("y", "prob"))
        if not callable(puntaje):
            raise ValueError("puntaje es una función de los datos: lambda d: 2 * d['x1']")
        self.puntaje = puntaje
        self.visibles = list(self.x)

    def _xs(self, n, rng):
        return pd.DataFrame({v: np.asarray(p.muestrear(n, rng)) for v, p in self.x.items()})

    def _z(self, df):
        return np.asarray(self.puntaje(df), dtype=float).reshape(-1) * np.ones(len(df))

    def llave(self):
        df = self._xs(_N_HUELLA, np.random.default_rng(_SEMILLA_HUELLA))
        return ("clf", _huella(self.puntaje, self._z(df)),
                tuple((k, _huella(v, df[k])) for k, v in self.x.items()))

    def sigma2_e(self):
        return float("nan")

    def prob(self, df):
        return special.expit(self._z(df[self.visibles]))

    def completo(self, n, rng, cambio=None):
        """Con cambio (despliegue de clase 2): una x llamada t sigue a la muestra y deriva
        cambia variables o, con la clave "f", el puntaje."""
        if cambio and cambio.get("nuevos"):
            raise ValueError('despliegue="grupos_nuevos" pide una columna grupo; '
                             "proceso_clasificacion la tendrá con ruido (clase 4)")
        xs = {v: np.asarray(p.muestrear(n, rng)) for v, p in self.x.items()}
        if cambio and "t" in self.x:
            if cambio.get("t0") is not None:
                xs["t"] = int(cambio["t0"]) + np.arange(int(n))
            elif cambio.get("t_realidad") is not None:
                xs["t"] = np.arange(int(n)) % int(cambio["t_realidad"])
        puntaje = self.puntaje
        if cambio and cambio.get("deriva") is not None:
            puntaje = _aplicar_deriva(cambio["deriva"], xs.get("t"), xs, n, rng, puntaje)
        df = pd.DataFrame(xs)
        p = special.expit(np.asarray(puntaje(df), float).reshape(-1) * np.ones(len(df)))
        df["y"] = (rng.uniform(size=n) < p).astype(int)
        df["_prob"] = p
        return df

    def f_estructural(self, df):
        return self.prob(df)

    def f_visible(self, df, semilla_realidad=0):
        return self.prob(df)

    def oraculos(self, completo, semilla_realidad):
        if "_prob" in completo:
            return {"prob": completo["_prob"].to_numpy()}
        return {"prob": self.prob(completo)}

    def nombres_oraculos(self):
        return ["prob"]

    piso = _PoblacionAnillos.piso


def proceso_clasificacion(n=500, x={"x1": normal(0, 1), "x2": normal(0, 1)},
                          puntaje=_puntaje_por_omision, K=2, puntajes=None, proporcion=None,
                          ruido_etiquetas=0.0, separar="estratificado",
                          fracciones=(0.6, 0.2, 0.2), despliegue="igual", deriva=None,
                          n_realidad=100_000, semilla=0, semilla_realidad=0, faltantes=None,
                          ruido=None, con_realidad=True):
    """Datos de clasificación binaria con Pr(y=1 | x) = σ(puntaje(d)), conocida.

    realidad y despliegue traen el oráculo "prob". Desde: 1.1 (clase 1).
    Ejemplo: datos = ml.proceso_clasificacion(n=400, puntaje=lambda d: 2 * d["x1"] - d["x2"])

    Es un adelanto con la firma completa (§5.5): funcionan K=2, puntaje,
    separar="azar"|"estratificado" y, desde 1.2 (clase 2), despliegue y deriva con la
    semántica de proceso ("futuro" pide una x llamada t; la clave "f" de deriva
    reemplaza al puntaje; "grupos_nuevos" no tiene grupo hasta la clase 4: ValueError).
    Lanzan NotImplementedError con la versión que los trae: proporcion,
    ruido_etiquetas≠0, K>2 (con puntajes), faltantes, ruido (se sumará al puntaje) y
    separar="tiempo"|"grupo" (clase 4). deriva con despliegue="igual" es ValueError.
    Flujos: los de proceso (muestra [semilla, 0], partición [semilla, 3], realidad y
    despliegue [semilla_realidad, 1] y [semilla_realidad, 2]).
    """
    if deriva is not None and despliegue == "igual":
        raise ValueError('`deriva` solo vale con despliegue="futuro" u "otra_poblacion"')
    if separar not in _SEPARAR:
        raise ValueError(f"separar debe ser uno de {_SEPARAR}, no {separar!r}")
    if despliegue not in _DESPLIEGUE:
        raise ValueError(f"despliegue debe ser uno de {_DESPLIEGUE}, no {despliegue!r}")
    if not isinstance(K, (int, np.integer)) or K < 2:
        raise ValueError("K es el número de clases: un entero >= 2")
    if K > 2 or puntajes is not None:
        raise NotImplementedError("K > 2 (con puntajes) llega con la versión de la clase 4")
    if proporcion is not None:
        raise NotImplementedError("`proporcion` llega con la versión de la clase 4")
    if ruido_etiquetas != 0:
        raise NotImplementedError("`ruido_etiquetas` llega con la versión de la clase 4")
    if faltantes is not None:
        raise NotImplementedError("`faltantes` llega con la versión de la clase 4")
    if ruido is not None:
        raise NotImplementedError("`ruido` (sumado al puntaje) llega con la versión de la clase 4")
    if separar in ("tiempo", "grupo"):
        raise NotImplementedError(f'separar="{separar}" llega con la versión de la clase 4')
    pob = _PoblacionClasificacion(x, puntaje)
    _validar_despliegue(despliegue, deriva, list(pob.x))
    cambio = {"t0": 0} if despliegue == "futuro" else None
    muestra = pob.completo(int(n), np.random.default_rng([semilla, 0]), cambio)
    muestra = muestra.drop(columns="_prob")
    argumentos = dict(n=n, x=x, puntaje=puntaje, separar=separar, fracciones=fracciones,
                      despliegue=despliegue, deriva=deriva,
                      n_realidad=n_realidad, semilla_realidad=semilla_realidad)

    def rehacer(s, con_realidad=False):
        return proceso_clasificacion(**{**argumentos, "semilla": s,
                                        "con_realidad": con_realidad})

    return _armar(pob, muestra, fracciones, np.random.default_rng([semilla, 3]), separar,
                  n_realidad, semilla, semilla_realidad, con_realidad,
                  f"clasificación binaria con {', '.join(pob.visibles)}", rehacer,
                  K=2, clases=[0, 1], despliegue_como=despliegue, uso=(despliegue, int(n), deriva))


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


# Lo único que un caso con forma cerrada de f_visible deja cambiar sin perderla: el
# tamaño, las semillas, la partición y un ruido centrado e independiente de x.
_CAMBIOS_QUE_CONSERVAN_LA_FORMA = {"n", "semilla", "fracciones", "n_realidad",
                                   "semilla_realidad", "con_realidad", "descripcion",
                                   "separar", "ruido", "endogeno"}


def _conserva_forma_cerrada(cambios):
    """True si la forma cerrada registrada sigue valiendo con estos cambios: E[ε | x] = 0
    exige endogeno = 0 y un ruido Pieza de media 0; todo lo demás (x, f, omitir,
    correlacion, escala…) la invalida y el caso cae a Monte Carlo o a «desconocido»."""
    if set(cambios) - _CAMBIOS_QUE_CONSERVAN_LA_FORMA:
        return False
    if cambios.get("endogeno", 0.0) != 0:
        return False
    if "ruido" in cambios:
        ruido = cambios["ruido"]
        return isinstance(ruido, Pieza) and float(ruido.media) == 0.0
    return True


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
    if _conserva_forma_cerrada(cambios):
        kw["f_visible_cerrada"] = _f_visible_caso_1  # E[y | x1] = x1 + E[x2]·0.8 x1 = 1.8 x1
    return _proceso(**kw)


def _lluvia(n=20, semilla=0, **cambios):
    """Caso 2: y = 10 + 4 x1 + 6 x2 + ε, x1 ~ U(0, 6), x2 ~ Bernoulli(0.5) omitida, σ = 1."""
    base = dict(n=n, x={"x1": uniforme(0, 6), "x2": categorica([0, 1])}, f=_f_lluvia,
                ruido=normal(0, 1), omitir=["x2"], fracciones=(1, 0, 0), semilla=semilla,
                descripcion="entregas con lluvia que el modelo no ve")
    kw = _con(base, cambios)
    if _conserva_forma_cerrada(cambios):
        kw["f_visible_cerrada"] = _f_visible_lluvia  # E[y | x1] = 10 + 4 x1 + 6·0.5
    return _proceso(**kw)


def _caso_23(n=10, semilla=0, **cambios):
    """Caso 23: la recíproca con solo n = 10 datos (para polinomio(12))."""
    return _inverso(**_con(dict(n=n, semilla=semilla, fracciones=(1, 0, 0)), cambios))


class _PoblacionRecursiva(_Poblacion):
    """y_t = 0.8·y_{t−1} + g(x_t) + ε_t, g la mezcla de logaritmos, x_t creciente en [1, 5].

    Visibles: x y y_anterior (el y observado un paso antes); contexto: t. Cada fila
    de realidad y despliegue sale de una serie completa nueva: realidad toma los t
    de entrenamiento (t < n) y despliegue los del futuro (t >= n), a un paso."""

    PERSISTENCIA = 0.8

    def __init__(self, n, futuro, sigma_e):
        super().__init__({"x": uniforme(1, 5), "y_anterior": normal()}, self._f,
                         normal(0, sigma_e), None, 0.0, None, None, None)
        self.contexto = ["t"]
        self.n, self.futuro = int(n), int(futuro)
        if self.n < 2 or self.futuro < 1:
            raise ValueError("recursivo pide n >= 2 pasos de entrenamiento y futuro >= 1")
        self.T = self.n + self.futuro

    @classmethod
    def _f(cls, d):
        return cls.PERSISTENCIA * d["y_anterior"] + _f_mezcla_logs(d)

    def llave(self):
        return ("recursivo", self.n, self.futuro, float(self.ruido.desv))

    def _series(self, replicas, rng):
        """replicas series de largo T; devuelve (t, x, y_anterior, y, f) en matrices."""
        paso = 4 / (self.T - 1)
        t = np.arange(self.T)
        x = 1 + paso * t + rng.uniform(-0.25 * paso, 0.25 * paso, (replicas, self.T))
        g = np.asarray(_f_mezcla_logs({"x": x}))
        eps = rng.normal(0, self.ruido.desv, (replicas, self.T))
        y = np.empty((replicas, self.T))
        ant = np.empty((replicas, self.T))
        previo = g[:, 0] / (1 - self.PERSISTENCIA)
        for k in range(self.T):
            ant[:, k] = previo
            y[:, k] = self.PERSISTENCIA * previo + g[:, k] + eps[:, k]
            previo = y[:, k]
        return np.broadcast_to(t, x.shape), x, ant, y, self.PERSISTENCIA * ant + g

    def _tabla(self, t, x, ant, y, f):
        v = float(self.ruido.varianza)
        return pd.DataFrame({"x": x.ravel(), "y_anterior": ant.ravel(), "t": t.ravel(),
                             "y": y.ravel(), "_f": f.ravel(), "_m": 0.0, "_v": v})

    def completo(self, n, rng):
        return self._tabla(*self._series(1, rng))

    def grande(self, n_realidad, rng, flujo):
        """Cada fila sale de una réplica nueva, en un t estratificado uniforme en su tramo
        (realidad t < n, despliegue t >= n); se simula por bloques para no llenar la memoria."""
        lo, hi = (0, self.n) if flujo == 1 else (self.n, self.T)
        total = int(n_realidad)
        u = (rng.permutation(total) + rng.uniform(size=total)) / total
        t_fila = lo + np.minimum((u * (hi - lo)).astype(int), hi - lo - 1)
        partes = []
        for inicio in range(0, total, 20_000):
            t_b = t_fila[inicio:inicio + 20_000]
            matrices = self._series(len(t_b), rng)
            fila = np.arange(len(t_b))
            partes.append(self._tabla(*(m[fila, t_b] for m in matrices)))
        return pd.concat(partes, ignore_index=True)


_CAMBIOS_RECURSIVO = {"n_realidad", "semilla_realidad", "con_realidad", "descripcion"}


def _recursivo(n=60, semilla=0, *, futuro=20, sigma_e=1.0, **cambios):
    """Una serie: y_t = 0.8 y_{t−1} + g(x_t) + ε, g la mezcla de logaritmos, x creciente.

    ent son los primeros n pasos y prueba los futuro siguientes (en orden); x va de
    1 a 5 en los n + futuro pasos. Visibles x y y_anterior; despliegue es el futuro,
    a un paso. Desde: 1.1 (clase 1). Ejemplo: datos = ml.PROCESOS["recursivo"]()
    """
    otros = set(cambios) - _CAMBIOS_RECURSIVO
    if otros:
        raise ValueError(f"recursivo no acepta {sorted(otros)}: la serie se parte en el tiempo; "
                         f"acepta n, semilla, futuro, sigma_e y {sorted(_CAMBIOS_RECURSIVO)}")
    n_realidad = cambios.get("n_realidad", 100_000)
    semilla_realidad = cambios.get("semilla_realidad", 0)
    pob = _PoblacionRecursiva(n, futuro, sigma_e)
    muestra = pob.completo(pob.T, np.random.default_rng([semilla, 0]))
    indices = (np.arange(pob.n), np.arange(0), np.arange(pob.n, pob.T))

    def rehacer(s, con_realidad=False):
        return _recursivo(n=n, semilla=s, futuro=futuro, sigma_e=sigma_e,
                          **{**cambios, "con_realidad": con_realidad})

    return _armar(pob, muestra, (1, 0, 0), None, "tiempo", n_realidad, semilla,
                  semilla_realidad, cambios.get("con_realidad", True),
                  cambios.get("descripcion", "una serie que recuerda su paso anterior"),
                  rehacer, indices=indices, despliegue_como="futuro")


def _caso_3(n=20, semilla=0, **cambios):
    """Caso 3: la recíproca 2 + 5/x con x ~ U(0.05, 3) (llega muy cerca de cero), σ = 0.5."""
    return _proceso(**_con(dict(n=n, x={"x": uniforme(0.05, 3)}, f=_f_inverso,
                                ruido=normal(0, 0.5), fracciones=(1, 0, 0), semilla=semilla,
                                descripcion="la recíproca cerca de cero"), cambios))


def _caso_4(n=100, semilla=0, **cambios):
    """Caso 4: el proceso del caso 3 con n = 100 (para polinomio(25, escalar=False))."""
    return _caso_3(**_con(dict(n=n, semilla=semilla), cambios))


def _caso_5(n=50, semilla=0, **cambios):
    """Caso 5: el seno 4 + 2 sen(5x), x ~ U(0, 2), σ = 0.3; el «fuera» es la zona [2, 3]."""
    return _seno(**_con(dict(n=n, semilla=semilla, fracciones=(1, 0, 0)), cambios))


def _f_entregas_curvas(d, joroba=4.0, centro=3.0, ancho=0.5):
    x = np.asarray(d["x"], float)
    return 10 + 12 * np.log1p(x) + joroba * np.exp(-(x - centro) ** 2 / ancho)


def entregas_curvas(n=60, semilla=0, **cambios):
    """Las entregas de la clase 1 con f curva: x~U(0,6) km, tramo urbano, vía rápida y
    una zona de tráfico a 3 km (f=10+12·ln(1+x)+4·exp(−(x−3)²/0.5)), ruido normal de desv. 3.

    Parámetros propios por nombre: sigma_e=3, joroba=4, centro=3, ancho=0.5; los demás
    cambios van a proceso. Desde: 1.2 (clase 2). Ejemplo: ml.PROCESOS["entregas_curvas"](n=120)
    """
    sigma_e = cambios.pop("sigma_e", 3.0)
    forma = {k: float(cambios.pop(k)) for k in ("joroba", "centro", "ancho") if k in cambios}
    if forma.get("ancho", 1.0) <= 0:
        raise ValueError("ancho de la joroba es > 0")
    f = _f_entregas_curvas if not forma else _ParcialF(_f_entregas_curvas, forma)
    return _proceso(**_con(dict(n=n, x={"x": uniforme(0, 6)}, f=f, ruido=normal(0, sigma_e),
                                semilla=semilla,
                                descripcion="tiempo de entrega contra distancia, con tráfico"),
                           cambios))


class _ParcialF:
    """f con parámetros fijos; dos iguales comparten la caché (vars entra en la huella)."""

    def __init__(self, f, kw):
        self.f, self.kw = f, dict(sorted(kw.items()))

    def __call__(self, d):
        return self.f(d, **self.kw)

    def __eq__(self, otro):
        return isinstance(otro, _ParcialF) and (self.f, self.kw) == (otro.f, otro.kw)

    __hash__ = None


def _caso_13(n=240, semilla=0, **cambios):
    """Caso 13: el hilo con ruido que recuerda (ar1 0.95, desv 3), separado al azar y
    desplegado en el futuro. Cambios propios: persistencia, desv."""
    ruido = ar1(cambios.pop("persistencia", 0.95), cambios.pop("desv", 3.0))
    return _proceso(**_con(dict(n=n, x={"x": uniforme(0, 6)}, f=_f_entregas_curvas, ruido=ruido,
                                separar="azar", despliegue="futuro", semilla=semilla,
                                descripcion="las entregas del mes que viene"), cambios))


def _caso_14(n=240, semilla=0, **cambios):
    """Caso 14: el hilo con efecto de paciente (24 grupos, desv_grupo 4, desv 1), separado
    al azar y desplegado en pacientes nuevos. Cambios propios: n_grupos, desv_grupo, desv."""
    ruido = efecto_grupo(cambios.pop("n_grupos", 24), cambios.pop("desv_grupo", 4.0),
                         cambios.pop("desv", 1.0))
    return _proceso(**_con(dict(n=n, x={"x": uniforme(0, 6)}, f=_f_entregas_curvas, ruido=ruido,
                                separar="azar", despliegue="grupos_nuevos", semilla=semilla,
                                descripcion="pacientes que vuelven y pacientes nuevos"), cambios))


def _deriva_otra_ciudad(t):
    return {"x": uniforme(4, 9)}


def _caso_15(n=120, semilla=0, **cambios):
    """Caso 15: el hilo en una ciudad (x en 0–6) y desplegado en otra (x en 4–9)."""
    return _proceso(**_con(dict(n=n, x={"x": uniforme(0, 6)}, f=_f_entregas_curvas,
                                ruido=normal(0, 3), separar="azar", despliegue="otra_poblacion",
                                deriva=_deriva_otra_ciudad, semilla=semilla,
                                descripcion="las entregas de otra ciudad"), cambios))


def _caso_16(n=50, semilla=0, **cambios):
    """Caso 16: 48 entregas en 0–4 km y 2 lejanas en 5.5–6 km (proporciones 0.96 y 0.04)."""
    x = {"x": _Mezcla([uniforme(0, 4), uniforme(5.5, 6)], [0.96, 0.04])}
    return _proceso(**_con(dict(n=n, x=x, f=_f_entregas_curvas, ruido=normal(0, 3),
                                fracciones=(1, 0, 0), semilla=semilla,
                                descripcion="entregas con dos lejanas"), cambios))


PROCESOS = {
    "entregas": _entregas,
    "inverso": _inverso,
    "mezcla_logs": _mezcla_logs,
    "seno": _seno,
    "x1_mas_x2x3": _caso_1,
    "lluvia": _lluvia,
    "recursivo": _recursivo,
    "entregas_curvas": entregas_curvas,
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
    opciones: dict = None  # (1.1) lo que la galería pasa al análisis del taller


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
    3: CasoBorde(
        3, "inverso_cerca_de_cero", 1, _caso_3,
        "¿Por qué ningún grado alcanza a (1, 1/x)?",
        "Cerca de cero, 5/x se dispara y ningún polinomio de grado <= 10 la sigue: el riesgo "
        "del mejor polinomio es varias veces el de la representación (1, 1/x).",
        {"N_max": 10}),
    4: CasoBorde(
        4, "potencias_sin_escalar", 1, _caso_4,
        "Más columnas y el error de entrenamiento subió: ¿qué se rompió?",
        "Sin escalar, x^25 y x^1 viven en escalas que la computadora ya no distingue: Φ está "
        "mal condicionada (no hay más parámetros que datos) y L_ent de N = 25 queda arriba "
        "de la de N = 10. Con escalar=True la curva vuelve a bajar.",
        {"N_max": 25, "escalar": False}),
    5: CasoBorde(
        5, "seno_extrapolar", 1, _caso_5,
        "Acertaba en la zona de datos: ¿por qué falla fuera?",
        "El polinomio de grado 7 sigue al seno en [0, 2], donde hubo datos; en [2, 3] no lo "
        "ata nada y el error por zona es más de diez veces el de dentro.",
        {"N_max": 7, "zonas": {"dentro": (0, 2), "fuera": (2, 3)}}),
    13: CasoBorde(
        13, "ar1_al_azar", 2, _caso_13,
        "¿Por qué la prueba al azar promete menos error del que darás el mes que viene?",
        "Con un modelo que usa el tiempo (vecinos en x y t), la prueba al azar tiene vecinos "
        "del mismo momento y su L_prueba queda muy por debajo de R en el futuro; separando "
        "por tiempo, la prueba se acerca a R. Con una recta en x, que no usa t, no miente."),
    14: CasoBorde(
        14, "pacientes_al_azar", 2, _caso_14,
        "¿Por qué ver al mismo paciente en los dos lados abarata la prueba?",
        "El modelo con un efecto por paciente memoriza a cada uno: al azar, la prueba trae "
        "pacientes que ya vio y su error es casi el ruido individual; con pacientes nuevos "
        "se le suma la variación entre pacientes. Separar por grupo lo imita."),
    15: CasoBorde(
        15, "otra_ciudad", 2, _caso_15,
        "¿Por qué ninguna separación de tu muestra te avisa?",
        "La prueba es honesta para la ciudad de origen; en la otra ciudad las distancias "
        "llegan a 9 km y el modelo extrapola: R es varias veces L_prueba. Ninguna separación "
        "de la muestra lo ve: solo se puede declarar el alcance."),
    16: CasoBorde(
        16, "pliegue_anomalo", 2, _caso_16,
        "¿Qué tiene el pliegue raro que no tienen los otros?",
        "Las dos entregas lejanas caen en un pliegue: el grado 8, ajustado sin ellas, "
        "extrapola y ese pliegue tiene un error varias veces el de los otros; la recta "
        "casi no lo nota."),
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
Particion = Union[str, Callable[[pd.DataFrame], list]]
# Un particionador: el nombre de `como` de pliegues (con k) o una función df -> pliegues.
_COMO_PLIEGUES = ("azar", "estratificado", "grupo", "temporal")


def separar(df, como="azar", fracciones=(0.6, 0.2, 0.2), columna_y="y", columna_tiempo="t",
            columna_grupo="grupo", semilla=0):
    """Parte un DataFrame en (ent, val, prueba); conserva attrs["ml"].

    como: "azar", "estratificado" (clases; deciles de y si es continua), "tiempo"
    (prueba es lo más reciente) o "grupo" (nunca un grupo en dos lados).
    Desde: 1.2 (clase 2). Ejemplo: ent, val, prueba = ml.separar(df, como="grupo")
    """
    tarea = df.attrs.get("ml", {}).get("tarea")
    idx = _indices_de_separar(df, como, fracciones, np.random.default_rng(semilla), columna_y,
                              columna_tiempo, columna_grupo, tarea)
    salida = []
    for i in idx:
        parte = df.iloc[np.sort(i)].copy()
        parte.attrs = copy.deepcopy(df.attrs)
        salida.append(parte)
    return tuple(salida)


def pliegues(df, k=5, como="azar", semilla=0, *, estratificar=False):
    """Los k pliegues de CV: una lista de (índices de ajuste, índices de validación),
    en posiciones (iloc). Cada fila valida exactamente una vez.

    como="estratificado": cada pliegue conserva la proporción de cada clase (sin
    attrs["ml"], estratifica por "y"; en regresión, por deciles de y).
    Desde: 1.2 (clase 2); "grupo", "temporal" y estratificar llegan con la clase 5.
    Ejemplo: part = ml.pliegues(df, k=5, como="estratificado")
    """
    if como not in _COMO_PLIEGUES:
        raise ValueError(f"como es uno de {_COMO_PLIEGUES}, no {como!r}"
                         + (' ("tiempo" es de separar; aquí es "temporal")' if como == "tiempo"
                            else ""))
    if estratificar and como != "grupo":
        raise ValueError('estratificar=True solo vale con como="grupo"')
    if como in ("grupo", "temporal") or estratificar:
        raise NotImplementedError(f'pliegues(como="{como}") llega con la versión de la clase 5')
    n = len(df)
    k = int(k)
    if not 2 <= k <= n:
        raise ValueError(f"k va de 2 a {n} (el número de filas)")
    rng = np.random.default_rng(semilla)
    if como == "azar":
        orden = rng.permutation(n)
        asignado = np.empty(n, int)
        for m, trozo in enumerate(np.array_split(orden, k)):
            asignado[trozo] = m
    else:
        tarea = df.attrs.get("ml", {}).get("tarea")
        estratos = _estratos(df["y"], tarea)
        asignado = np.empty(n, int)
        inicio = 0
        for v in np.unique(estratos):
            idx = np.flatnonzero(estratos == v)
            idx = idx[rng.permutation(len(idx))]
            asignado[idx] = (inicio + np.arange(len(idx))) % k  # reparte en turno
            inicio = (inicio + len(idx)) % k
    todos = np.arange(n)
    return [(todos[asignado != m], todos[asignado == m]) for m in range(k)]


def _particion(df, particion, k, semilla):
    """Los pliegues que pide una Particion (nombre de como, o función)."""
    if callable(particion):
        part = particion(df)
    elif isinstance(particion, str):
        part = pliegues(df, k, como=particion, semilla=semilla)
    else:
        raise ValueError('particion es "azar", "estratificado", "grupo", "temporal" o una '
                         "función df -> pliegues")
    part = [(np.asarray(a, int), np.asarray(b, int)) for a, b in part]
    if not part:
        raise ValueError("la partición no trajo pliegues")
    return part

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
        if int(N) != N or N < 0:
            raise ValueError("el grado N de polinomio es un entero >= 0 (0: solo el intercepto)")
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
    (1.2) N=0 no tiene columnas: con el intercepto, el modelo es la media de ent.
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
        M = pd.DataFrame(np.column_stack([np.ones(len(M)), M.to_numpy(dtype=float)]),
                         index=M.index, columns=["1"] + list(M.columns))
    if M.shape[1] == 0:
        raise ValueError("la matriz de diseño no tiene columnas: pide intercepto=True")
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
        nombres = list(self.beta_gorro.index)
        return M if list(M.columns) == nombres else M[nombres]

    def n_parametros(self):
        return len(self.beta_gorro)

    def _eta(self, df):
        # einsum y no @: con BLAS en varios hilos, @ de una matriz chica tarda 15 veces más
        return np.einsum("ij,j->i", self.Phi(df).to_numpy(dtype=float), self.beta_gorro.to_numpy())

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

    def predecir_prob(self, df):
        """(n, K) en el orden de self.clases; una clase que ent no vio tiene columna 0."""
        if self.tarea != "clasificacion":
            raise NoAplica("predecir_prob es de clasificación; en regresión usa predecir")
        prob = self._est.predict_proba(self._X(df))
        salida = np.zeros((len(df), self.K))
        vistas = list(self._est.classes_)
        for j, c in enumerate(self.clases):
            if c in vistas:
                salida[:, j] = prob[:, vistas.index(c)]
        return salida

    def predecir_p(self, df):
        if self.tarea != "clasificacion" or self.K != 2:
            raise NoAplica("predecir_p es de clasificación binaria")
        return self.predecir_prob(df)[:, 1]


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
    """¿Hay una dirección β con s_i·Φ_i β >= 0 para todos y > 0 para alguno (s = ±1)?

    Eso es separación completa o cuasicompleta (empates justo en la frontera): en
    los dos casos avanzar por β baja la pérdida sin fin y no hay minimizador finito.
    Se resuelve como programa lineal con Σ s_i·Φ_i β = 1 para excluir β = 0. Φ se
    normaliza por columnas para que la tolerancia no dependa de las unidades."""
    s = 2 * y01 - 1
    normas = np.linalg.norm(Phi, axis=0)
    M = s[:, None] * (Phi / np.where(normas > 0, normas, 1.0))
    sol = optimize.linprog(np.zeros(Phi.shape[1]), A_ub=-M, b_ub=np.zeros(len(s)),
                           A_eq=M.sum(axis=0)[None, :], b_eq=[1.0],
                           bounds=[(None, None)] * Phi.shape[1], method="highs")
    return sol.status == 0


def _logistica(Phi, y, w, mu, r, pen, intercepto):
    n, q = Phi.shape
    beta = np.zeros(q)
    if intercepto:
        ybar = np.clip(np.average(y, weights=w), 1e-6, 1 - 1e-6)
        beta[0] = math.log(ybar / (1 - ybar))
    separado = mu == 0 and _separables(Phi, y)
    if separado:
        warnings.warn("los datos se separan perfectamente (o con empates justo en la "
                      "frontera): sin penalización no hay "
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


_COND_MAXIMA = 1e12


def _avisar_rango(A, n):
    """Separa las dos causas por las que mínimos cuadrados no tiene un β̂ limpio.

    Pseudoinversa (norma mínima, un elemento del argmin): más columnas que datos, o
    columnas que repiten o combinan EXACTAMENTE otras; normalizar las columnas no
    les devuelve el rango. Mal condicionamiento: el rango «falta» solo en la
    aritmética, porque las columnas viven en escalas muy distintas (potencias sin
    escalar): normalizarlas sube el rango, o el número de condición pasa de 1e12."""
    q = A.shape[1]
    if q > n:
        warnings.warn(f"Φ tiene {q} columnas y solo {n} datos (más parámetros que datos): "
                      "uso la pseudoinversa, que da el ajuste de norma mínima, uno de muchos "
                      "con el mismo error", UserWarning, stacklevel=4)
        return
    normas = np.linalg.norm(A, axis=0)
    rango = np.linalg.matrix_rank(A)
    rango_normalizado = np.linalg.matrix_rank(A / np.where(normas > 0, normas, 1.0))
    if rango < q and rango_normalizado <= rango:
        warnings.warn(f"Φ tiene {q} columnas y rango {rango} (columnas repetidas o que son "
                      "combinación exacta de otras): uso la pseudoinversa, que da el ajuste "
                      "de norma mínima, uno de muchos con el mismo error", UserWarning,
                      stacklevel=4)
        return
    cond = np.linalg.cond(A)
    if rango < q or cond > _COND_MAXIMA:
        vivas = normas[normas > 0]
        warnings.warn(f"Φ está mal condicionada (número de condición {cond:.1e}; la norma de "
                      f"sus columnas va de {vivas.min():.1e} a {vivas.max():.1e}): la "
                      "aritmética pierde precisión y los coeficientes no son confiables; "
                      "escala las columnas", UserWarning, stacklevel=4)


def _ridge(Phi, y, w, mu, pen, intercepto):
    """Ridge sin armar Φ'WΦ: con el intercepto libre, centra (con pesos) y resuelve
    el sistema aumentado [√(w/n)·Φc; √mu·I] β = [√(w/n)·yc; 0] por mínimos
    cuadrados. Armar las ecuaciones normales eleva al cuadrado el número de
    condición y, con escalas dispares (x ~ 1e9), lstsq tiraba el intercepto."""
    n, q = Phi.shape
    if intercepto:
        media_x = np.average(Phi[:, 1:], axis=0, weights=w)
        media_y = np.average(y, weights=w)
        X, z = Phi[:, 1:] - media_x, y - media_y
        libres = pen[1:]
    else:
        X, z, libres = Phi, y, pen
    raiz = np.sqrt(w / n)
    pena = np.diag(np.where(libres, math.sqrt(mu), 0.0))
    A = np.vstack([raiz[:, None] * X, pena])
    b = np.concatenate([raiz * z, np.zeros(X.shape[1])])
    beta = np.linalg.lstsq(A, b, rcond=None)[0]
    if not intercepto:
        return beta
    return np.concatenate([[media_y - media_x @ beta], beta])


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
        _avisar_rango(A, int(np.sum(w > 0)))
        return np.linalg.lstsq(A, raiz * y, rcond=None)[0]
    if r == 0:
        return _ridge(Phi, y, w, mu, pen, intercepto)
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

    Qué elemento del argmin devuelve. Con mu=0 y rango deficiente (o q > n), uno
    de muchos: el de norma mínima (pseudoinversa), con un aviso; sus predicciones
    fuera de la muestra dependen de las unidades de las columnas. Si el rango solo
    falta en la aritmética (columnas en escalas muy distintas), avisa de mal
    condicionamiento. Ridge y elástica con rho<1 tienen un solo minimizador. Lasso
    con columnas colineales puede tener muchos: devuelve el que encuentra el
    algoritmo (hay otros con el mismo objetivo). Logística sin penalizar con datos
    separados (o con empates en la frontera) no tiene minimizador finito: avisa.
    Conversión a sklearn (llama alpha o 1/C a nuestro mu, con otra escala):
    Lasso(alpha=mu/2); ElasticNet(alpha=mu*(2-rho)/2, l1_ratio=rho/(2-rho));
    LogisticRegression(C=1/(2*mu*n)) en l2, C=1/(mu*n) en l1,
    C=1/(mu*(2-rho)*n) con l1_ratio=rho/(2-rho) en elástica, penalty=None con mu=0.
    pesos ("balanceado" = n/(K n_y), o {y: w_y}) llega con la versión de la clase 4.
    """
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


def _perdida_log_i(modelo, df):
    """ℓ_i logarítmica de un clasificador. La logística la saca del puntaje η con
    logaddexp (pasar por p = expit(η) redondea p a 1 y da infinito donde ℓ = η);
    los demás, de Pr(y_i) con K clases."""
    y = df["y"].to_numpy()
    if getattr(modelo, "familia", None) == "logistica" and hasattr(modelo, "_eta"):
        eta = modelo._eta(df)
        y01 = (y == modelo.clases[1]).astype(float)
        return np.logaddexp(0, eta) - y01 * eta
    P = modelo.predecir_prob(df)
    clases = list(modelo.clases)
    idx = np.array([clases.index(v) if v in clases else -1 for v in y])
    p_y = np.where(idx >= 0, P[np.arange(len(y)), np.maximum(idx, 0)], 0.0)
    with np.errstate(divide="ignore"):
        return -np.log(p_y)


def _promedio_ponderado(w, l_i):
    """(1/n) Σ w_i ℓ_i, con w_i = 0 aportando 0 aunque ℓ_i sea infinita."""
    return float(np.mean(w * np.where(w == 0, 0.0, l_i)))


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
        return _promedio_ponderado(w, (modelo.predecir(df) == y).astype(float))
    if modelo.tarea == "clasificacion":
        if crit != "logaritmica":
            raise ValueError(f'"{crit}" no es una pérdida de clasificación en esta versión')
        return _promedio_ponderado(w, _perdida_log_i(modelo, df))
    if crit == "logaritmica":
        raise ValueError('la pérdida "logaritmica" es de clasificación')
    return _promedio_ponderado(w, perdida(y, modelo.predecir(df), crit))


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
    n_r, s_r, _, _, uso = datos._grande
    desp = _poblacion_grande(pob, n_r, s_r, uso)[1]
    if perdida not in _PERDIDAS:
        raise ValueError(f"perdida es una de {_PERDIDAS}")
    valor = pob.piso(desp, perdida)
    if valor is None or math.isnan(valor):
        warnings.warn("piso desconocido: con lo que registra este proceso no se puede calcular",
                      UserWarning, stacklevel=2)
        return float("nan")
    return valor


def benchmarks(datos_o_df, df_eval, tarea=None, criterios=None):
    """Los puntos de comparación sin x, ajustados en ent y evaluados en df_eval.

    Regresión: filas media y mediana. Clasificación (K clases): moda y proporcion
    (predice las proporciones de ent; un empate lo gana la última clase, como en
    predecir). criterios=None: la pérdida natural y, en clasificación, "aciertos".
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
        clases = list(meta.get("clases") or np.unique(y_ent))
        p = np.array([np.mean(y_ent == c) for c in clases], float)
        # la clase más frecuente; un empate lo gana la última, como predecir con p >= 0.5
        j = len(p) - 1 - int(np.argmax(p[::-1]))
        uno = np.eye(len(clases))[j]
        filas = {"moda": (clases[j], uno), "proporcion": (clases[j], p)}
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
                    p_y = np.array([prob[clases.index(v)] if v in clases else 0.0 for v in y])
                    with np.errstate(divide="ignore"):
                        tabla.loc[fila, c] = float(np.mean(-np.log(p_y)))
                else:
                    raise ValueError(f'"{c}" no es un criterio de clasificación en esta versión')
    tabla.index.name = "benchmark"
    return tabla


# === 7 · Medir: EE, CV, selección ===
# repetir se adelantó en 1.1 (la usa la clase 1); lo demás llega con 1.2 (clase 2).


def repetir(experimento, repeticiones=500, semilla=0):
    """Corre experimento(semilla_i) con semilla_i = semilla + i y apila los dict que devuelve.

    La base de todos los «500 veces»: una fila por repetición, con repeticion y semilla.
    Desde: 1.1 (clase 1). Ejemplo: ml.repetir(lambda s: {"R": mi_R(s)}, repeticiones=200)
    """
    if isinstance(repeticiones, bool) or not isinstance(repeticiones, (int, np.integer)) \
            or repeticiones < 0:
        raise ValueError(f"repeticiones es un entero >= 0, no {repeticiones!r}")
    filas = []
    for i in range(int(repeticiones)):
        s = int(semilla) + i
        r = experimento(s)
        if not isinstance(r, dict):
            raise TypeError("experimento(semilla) debe devolver un dict {nombre: valor}")
        if "repeticion" in r or "semilla" in r:
            raise ValueError("el dict de experimento no puede traer las claves 'repeticion' "
                             "ni 'semilla': repetir las agrega")
        filas.append({"repeticion": i, "semilla": s, **r})
    if not filas:
        return pd.DataFrame(columns=["repeticion", "semilla"])
    return pd.DataFrame(filas)


def _var_y_dado_x(pob, malla, semilla_realidad):
    """Var(y | lo visible) en cada punto de la malla, o ValueError si no se sabe."""
    if not isinstance(pob, _Poblacion) or pob.mecanismo is not None:
        raise ValueError("error_por_zona no sabe Var(y | x) de este proceso: su ruido "
                         "depende de un contexto que la malla no trae")
    if math.isinf(pob.ruido.varianza):
        return np.full(len(malla), np.inf)
    cruzadas = any((a in pob.omitidas) != (b in pob.omitidas) for a, b in pob.correlacion)
    if cruzadas or (pob.endogeno and pob.var_endogena in pob.omitidas):
        raise ValueError("error_por_zona no sabe Var(y | x) de este proceso: lo omitido "
                         "depende de lo visible (correlación o endogeneidad)")
    d = pob._sin_escala(malla)
    var = pob.var_endogena if pob.endogeno else pob.visibles[0]
    v = pob._media_ruido({var: d[var].to_numpy()})[1]
    if pob.omitidas:  # omitidas independientes de lo visible: los mismos sorteos de f_visible
        v = v + pob._repetir_f(d, pob._sorteos_omitidas(semilla_realidad), pob.J).var(axis=1)
    return np.asarray(v, float) * pob.c_y ** 2


def error_por_zona(modelo, datos, zonas, puntos=1000, variable="x"):
    """El riesgo cuadrático si el uso cayera uniforme en cada zona: media en una malla de
    (E[y | x] − f̂)² más la de Var(y | x). No toca despliegue. Solo regresión de una variable.

    Columnas: zona, desde, hasta, dif2, var_y_dado_x (= sigma2_e si nada se omite), R_zona.
    Desde: 1.1 (clase 1). Ejemplo: ml.error_por_zona(m, datos, {"dentro": (0, 2), "fuera": (2, 3)})
    """
    if datos.tarea != "regresion" or len(datos.columnas_x) != 1:
        raise ValueError("error_por_zona es para regresión de una variable")
    if variable != datos.columnas_x[0]:
        raise ValueError(f"variable es la x visible de estos datos: {datos.columnas_x[0]!r}")
    if datos.f_visible is None:
        raise ValueError("este proceso no sabe E[y | x]: no hay contra qué medir")
    if isinstance(puntos, bool) or not isinstance(puntos, (int, np.integer)) or puntos < 2:
        raise ValueError(f"puntos es un entero >= 2 (los de la malla de cada zona), no {puntos!r}")
    pob = getattr(datos, "_pob", None)
    filas = []
    for nombre, (lo, hi) in zonas.items():
        lo, hi = float(lo), float(hi)
        if not (math.isfinite(lo) and math.isfinite(hi)):
            raise ValueError(f"la zona {nombre!r} pide límites finitos")
        if not hi > lo:
            raise ValueError(f"la zona {nombre!r} pide desde < hasta")
        malla = pd.DataFrame({variable: np.linspace(lo, hi, int(puntos))})
        malla.attrs["ml"] = copy.deepcopy(datos.ent.attrs.get("ml", {}))
        with np.errstate(all="ignore"):
            e_y = np.asarray(datos.f_visible(malla), float)
            pred = np.asarray(modelo.predecir(malla), float)
            var = _var_y_dado_x(pob, malla, datos.semilla_realidad)
        if not (np.all(np.isfinite(e_y)) and np.all(np.isfinite(pred))) or np.any(np.isnan(var)):
            raise ValueError(f"en la zona {nombre!r} E[y | x], la predicción o Var(y | x) "
                             "quedan indefinidos (¿la zona sale del dominio de f?)")
        dif2 = float(np.mean((e_y - pred) ** 2))
        v = float(np.mean(var))
        filas.append((nombre, lo, hi, dif2, v, dif2 + v))
    return pd.DataFrame(filas, columns=["zona", "desde", "hasta", "dif2", "var_y_dado_x",
                                        "R_zona"])


_REGLAS_NFL = ("vecino", "mayoria", "siempre_1")


def no_free_lunch(reglas=("vecino", "mayoria", "siempre_1"), bits=3, entrenamiento=(0, 3, 5, 6)):
    """Todas las funciones booleanas de bits bits: qué fracción aciertan las reglas fuera
    de los puntos de entrenamiento. Promediada sobre todas las funciones, toda regla da 1/2.

    aciertos_fuera es una Fraction exacta; rugosidad = aristas del cubo con etiquetas
    distintas. vecino desempata por el índice menor; mayoria, a favor de 1.
    Desde: 1.1 (clase 1). Ejemplo: ml.no_free_lunch()
    """
    for r in reglas:
        if r not in _REGLAS_NFL:
            raise ValueError(f"cada regla es una de {_REGLAS_NFL}, no {r!r}")
    if not 1 <= int(bits) <= 4:
        raise ValueError("bits va de 1 a 4 (con 4 ya son 65 536 funciones)")
    m = 2 ** int(bits)
    ent = sorted({int(i) for i in entrenamiento})
    if not ent or ent[0] < 0 or ent[-1] >= m or len(ent) == m:
        raise ValueError(f"entrenamiento son índices distintos en 0…{m - 1}, sin cubrirlos todos")
    fuera = [i for i in range(m) if i not in ent]
    distancia = lambda a, b: bin(a ^ b).count("1")  # noqa: E731
    vecino_de = {i: min(ent, key=lambda j: (distancia(i, j), j)) for i in fuera}
    aristas = [(a, a | (1 << k)) for a in range(m) for k in range(int(bits)) if not a >> k & 1]
    filas = []
    for funcion in range(2 ** m):
        f = [(funcion >> i) & 1 for i in range(m)]
        rugosidad = sum(f[a] != f[b] for a, b in aristas)
        unos = sum(f[j] for j in ent)
        for regla in reglas:
            if regla == "vecino":
                pred = {i: f[vecino_de[i]] for i in fuera}
            elif regla == "mayoria":
                pred = dict.fromkeys(fuera, 1 if 2 * unos >= len(ent) else 0)
            else:
                pred = dict.fromkeys(fuera, 1)
            aciertos = sum(pred[i] == f[i] for i in fuera)
            filas.append((funcion, regla, Fraction(aciertos, len(fuera)), rugosidad))
    return pd.DataFrame(filas, columns=["funcion", "regla", "aciertos_fuera", "rugosidad"])


def error_estandar(perdidas_i):
    """EE de una pérdida promedio: s_ℓ / √n (observaciones independientes).

    Desde: 1.2 (clase 2). Ejemplo: ml.error_estandar(ml.perdida(df["y"], m.predecir(df)))
    """
    l_i = np.asarray(perdidas_i, float)
    if len(l_i) < 2:
        return float("nan")
    return float(np.std(l_i, ddof=1) / math.sqrt(len(l_i)))


def intervalo(valor, ee, veces=2.0):
    """valor ± veces·EE, como tupla (bajo, alto).

    Desde: 1.2 (clase 2). Ejemplo: ml.intervalo(4.1, 0.3)  # (3.5, 4.7)
    """
    return (float(valor) - veces * float(ee), float(valor) + veces * float(ee))


def _perdidas_i(modelo, df, criterio):
    """ℓ_i de cada fila (o el acierto 0/1 si el criterio es "aciertos")."""
    crit = criterio or ("cuadratica" if modelo.tarea == "regresion" else "logaritmica")
    if crit in _METRICAS_FUTURAS:
        raise NotImplementedError(f'"{crit}" llega con la versión de la clase 4')
    if crit not in SENTIDO:
        raise ValueError(f"criterio es uno de {sorted(SENTIDO)}")
    y = df["y"].to_numpy()
    if crit == "aciertos":
        if modelo.tarea != "clasificacion":
            raise ValueError('"aciertos" es de clasificación')
        return (modelo.predecir(df) == y).astype(float), crit
    if modelo.tarea == "clasificacion":
        if crit != "logaritmica":
            raise ValueError(f'"{crit}" no es una pérdida de clasificación en esta versión')
        return _perdida_log_i(modelo, df), crit
    if crit == "logaritmica":
        raise ValueError('la pérdida "logaritmica" es de clasificación')
    return perdida(y, modelo.predecir(df), crit), crit


@dataclass
class ResultadoCV:
    """Lo que devuelve validacion_cruzada (y cv_anidada).

    por_pliegue: L de cada pliegue; media: CV_k (promedio de los k); ee: desviación de
    los k entre √k (aproximado: los pliegues no son independientes); pliegues: los
    usados; por_pliegue_estadistico: estadistico(y, ŷ) de cada pliegue, tal cual
    (nan incluido), o None; perdidas_fuera: ver validacion_cruzada.
    """

    por_pliegue: np.ndarray
    media: float
    ee: float
    pliegues: list
    por_pliegue_estadistico: object = None
    perdidas_fuera: object = None


def _desarrollo(datos_o_df):
    """ent ∪ val de un Datos (los datos de desarrollo), o el DataFrame tal cual."""
    if isinstance(datos_o_df, Datos):
        df = pd.concat([datos_o_df.ent, datos_o_df.val])
        df.attrs = copy.deepcopy(datos_o_df.ent.attrs)
        return df
    if not isinstance(datos_o_df, pd.DataFrame):
        raise ValueError("se espera un Datos o un DataFrame")
    return datos_o_df


def validacion_cruzada(df, construir, k=5, particion="azar", criterio=None, estadistico=None,
                       semilla=0):
    """CV_k: ajusta construir(df sin el pliegue m) y mide en el pliegue m, m = 1…k.

    Con un Datos usa ent ∪ val. estadistico(y, ŷ) recibe y del pliegue y
    ŷ = modelo_m.predecir(df_m) (etiquetas en clasificación, nunca probabilidades) y
    se guarda tal cual, nan incluido. Desde: 1.2 (clase 2).
    Ejemplo: cv = ml.validacion_cruzada(datos, lambda df: ml.ajustar(df, phi=ml.polinomio(4)))

    perdidas_fuera: la pérdida de cada observación de desarrollo con el modelo del
    pliegue que no la vio, en el orden de las filas. Es DESCRIPTIVA: esas pérdidas
    dependen entre sí (los entrenamientos se superponen), así que no se pasan a
    diferencia_pareada para afirmar una mejora; para comparar por CV, usa
    diferencia_por_pliegue.
    """
    df = _desarrollo(df)
    part = _particion(df, particion, k, semilla)
    por_pliegue, est, fuera = [], [], np.full(len(df), np.nan)
    for ajuste, valida in part:
        tramo = df.iloc[ajuste].copy()
        tramo.attrs = copy.deepcopy(df.attrs)
        modelo = construir(tramo)
        df_m = df.iloc[valida]
        l_i, _ = _perdidas_i(modelo, df_m, criterio)
        fuera[valida] = l_i
        por_pliegue.append(float(np.mean(l_i)) if len(l_i) else float("nan"))
        if estadistico is not None:
            est.append(estadistico(df_m["y"].to_numpy(), np.asarray(modelo.predecir(df_m))))
    por = np.asarray(por_pliegue, float)
    kk = len(por)
    ee = float(np.std(por, ddof=1) / math.sqrt(kk)) if kk > 1 else float("nan")
    return ResultadoCV(por_pliegue=por, media=float(np.mean(por)), ee=ee, pliegues=part,
                       por_pliegue_estadistico=None if estadistico is None else
                       np.asarray(est, dtype=float),
                       perdidas_fuera=fuera)


def diferencia_pareada(perdidas_a, perdidas_b):
    """(media de a − b, EE = desviación de las diferencias / √n), fila por fila.

    Inferencia aproximada SOLO con dos modelos fijados antes y evaluados en una reserva
    que no tocó ninguna decisión (prueba, o validación que no eligió nada), con
    observaciones independientes. Nunca con perdidas_fuera de CV.
    Desde: 1.2 (clase 2). Ejemplo: ml.diferencia_pareada(l_modelo, l_benchmark)
    """
    a, b = np.asarray(perdidas_a, float), np.asarray(perdidas_b, float)
    if a.shape != b.shape or a.ndim != 1:
        raise ValueError("diferencia_pareada compara dos arreglos del mismo largo, fila por fila "
                         f"(llegaron {a.shape} y {b.shape})")
    d = a - b
    return float(np.mean(d)), error_estandar(d)


def _mismas_particiones(a, b):
    if len(a) != len(b):
        return False
    return all(np.array_equal(np.sort(va), np.sort(vb)) for (_, va), (_, vb) in zip(a, b))


def diferencia_por_pliegue(cv_a, cv_b):
    """Columnas pliegue y diferencia (media de a − b en cada pliegue) y la fila "media".

    Descriptivo: las diferencias de los pliegues dependen entre sí; una señal se
    confirma en una reserva independiente. Desde: 1.2 (clase 2).
    Ejemplo: ml.diferencia_por_pliegue(cv_modelo, cv_benchmark)
    """
    if not _mismas_particiones(cv_a.pliegues, cv_b.pliegues):
        raise ValueError("compara con la misma partición: los pliegues de los dos ResultadoCV "
                         "no coinciden")
    d = np.asarray(cv_a.por_pliegue, float) - np.asarray(cv_b.por_pliegue, float)
    tabla = pd.DataFrame({"pliegue": list(range(1, len(d) + 1)) + ["media"],
                          "diferencia": list(d) + [float(cv_a.media - cv_b.media)]})
    tabla.attrs["nota"] = ("descriptivo: las diferencias de los pliegues dependen entre sí; una "
                           "señal se confirma en una reserva independiente")
    return tabla


@dataclass
class Seleccion:
    """Lo que devuelve elegir.

    tabla (candidato, valor, ee); elegido: el del mínimo (con empate, el más simple);
    elegido_un_ee: el más simple dentro de un EE del mejor (None sin EE); modelo: el
    que dice regla, reajustado con lo que tocó la elección; modelo_final: el mismo
    reajustado con ent ∪ val; costo_ajustes; cv: {candidato: ResultadoCV} con "cv";
    con: el conjunto con que se eligió.
    """

    tabla: pd.DataFrame
    elegido: object
    elegido_un_ee: object
    modelo: object
    modelo_final: object
    criterio: str
    sentido: str
    costo_ajustes: int
    cv: object = None
    con: str = None


def _orden(candidatos, orden_complejidad):
    if orden_complejidad is None:
        return list(candidatos)
    orden = list(orden_complejidad)
    if sorted(map(repr, orden)) != sorted(map(repr, candidatos)):
        raise ValueError("orden_complejidad lista exactamente los candidatos, del más simple "
                         "al más complejo")
    return orden


def _elegir_de_tabla(valores, ees, orden, sentido):
    """(elegido por el mínimo, elegido por un EE o None)."""
    signo = 1.0 if sentido == "min" else -1.0
    v = {c: signo * valores[c] for c in orden}
    finitos = [c for c in orden if np.isfinite(v[c])]
    if not finitos:
        raise ValueError("ningún candidato tiene un valor finito")
    mejor = min(v[c] for c in finitos)
    elegido = next(c for c in orden if v[c] == mejor)  # empate: el primero, el más simple
    ee = ees[elegido]
    un_ee = None
    if ee is not None and np.isfinite(ee):
        umbral = mejor + ee
        un_ee = next(c for c in orden if np.isfinite(v[c]) and v[c] <= umbral)
    return elegido, un_ee


def elegir(datos_o_df, candidatos, con="ent", k=5, particion="azar", criterio=None,
           regla="minimo", orden_complejidad=None, semilla=0):
    """Elige un candidato {valor: construir(df) -> Modelo} con ent, val, prueba o CV.

    Escribe el dict de simple a complejo (N creciente; μ decreciente) o da
    orden_complejidad. Empate exacto: el más simple. regla="un_ee" (solo con "cv"):
    el más simple dentro de un EE del mejor, leído por la media.
    Desde: 1.2 (clase 2). Ejemplo: ml.elegir(datos, {N: lambda df, N=N: ml.ajustar(df, phi=ml.polinomio(N)) for N in range(13)}, con="cv")

    con="ent": ajusta y mide en ent; "val": ajusta en ent, mide en val; "cv": CV_k
    sobre ent ∪ val (o sobre el DataFrame); "prueba": ajusta en ent y mide en prueba,
    solo para ver el engaño (avisa). modelo nunca se reajusta con prueba.
    """
    if con not in ("ent", "val", "prueba", "cv"):
        raise ValueError('con es "ent", "val", "prueba" o "cv"')
    if regla not in ("minimo", "un_ee"):
        raise ValueError('regla es "minimo" o "un_ee"')
    if regla == "un_ee" and con != "cv":
        raise ValueError('la regla de un EE necesita el EE de la CV: usa con="cv"')
    if not candidatos:
        raise ValueError("candidatos es un dict {valor: construir} con al menos uno")
    orden = _orden(candidatos, orden_complejidad)
    es_datos = isinstance(datos_o_df, Datos)
    if con != "cv" and not es_datos:
        raise ValueError(f'con="{con}" necesita un Datos (con ent, val y prueba)')
    if con == "prueba":
        warnings.warn('elegir con la prueba: la cifra del elegido queda optimista (es el engaño '
                      "que muestra la clase 2); en la práctica, elige con validación o CV",
                      UserWarning, stacklevel=2)
    meta_crit = criterio
    valores, ees, cvs, ajustados = {}, {}, {}, {}
    if con == "cv":
        df = _desarrollo(datos_o_df)
        part = _particion(df, particion, k, semilla)
        for c in orden:
            r = validacion_cruzada(df, candidatos[c], particion=lambda _, p=part: p,
                                   criterio=criterio)
            cvs[c], valores[c], ees[c] = r, r.media, r.ee
        costo = len(orden) * len(part) + 1
    else:
        evalua = getattr(datos_o_df, con)
        for c in orden:
            m = candidatos[c](datos_o_df.ent)
            ajustados[c] = m
            l_i, _ = _perdidas_i(m, evalua, criterio)
            valores[c], ees[c] = float(np.mean(l_i)) if len(l_i) else float("nan"), None
        costo = len(orden) + 1
    tarea = (datos_o_df.tarea if es_datos else
             _desarrollo(datos_o_df).attrs.get("ml", {}).get("tarea", "regresion"))
    crit = meta_crit or ("cuadratica" if tarea == "regresion" else "logaritmica")
    sentido = SENTIDO[crit]
    elegido, un_ee = _elegir_de_tabla(valores, ees, orden, sentido)
    toma = un_ee if regla == "un_ee" else elegido
    desarrollo = _desarrollo(datos_o_df)
    if con == "cv":
        modelo = candidatos[toma](desarrollo)
        modelo_final = modelo
    else:
        modelo = ajustados[toma]
        modelo_final = candidatos[toma](desarrollo)
    tabla = pd.DataFrame({"candidato": orden, "valor": [valores[c] for c in orden],
                          "ee": [ees[c] if ees[c] is not None else float("nan") for c in orden]})
    return Seleccion(tabla=tabla, elegido=elegido, elegido_un_ee=un_ee, modelo=modelo,
                     modelo_final=modelo_final, criterio=crit, sentido=sentido,
                     costo_ajustes=costo, cv=cvs or None, con=con)


def cv_anidada(df, candidatos, particion_externa="azar", k_externo=5, particion_interna="azar",
               k_interno=5, criterio=None, regla="minimo", orden_complejidad=None, semilla=0):
    """CV anidada: en cada pliegue externo elige con CV interna y mide al elegido fuera.

    Estima el riesgo de TODO el procedimiento de selección (con un Datos, sobre ent ∪ val).
    Desde: 1.2 (clase 2). Ejemplo: ml.cv_anidada(datos, candidatos).media
    """
    df = _desarrollo(df)
    externos = _particion(df, particion_externa, k_externo, semilla)
    por, fuera = [], np.full(len(df), np.nan)
    for ajuste, valida in externos:
        dentro = df.iloc[ajuste].copy()
        dentro.attrs = copy.deepcopy(df.attrs)
        s = elegir(dentro, candidatos, con="cv", k=k_interno, particion=particion_interna,
                   criterio=criterio, regla=regla, orden_complejidad=orden_complejidad,
                   semilla=semilla + 1)
        l_i, _ = _perdidas_i(s.modelo, df.iloc[valida], criterio)
        fuera[valida] = l_i
        por.append(float(np.mean(l_i)))
    por = np.asarray(por, float)
    ee = float(np.std(por, ddof=1) / math.sqrt(len(por))) if len(por) > 1 else float("nan")
    return ResultadoCV(por_pliegue=por, media=float(np.mean(por)), ee=ee, pliegues=externos,
                       perdidas_fuera=fuera)


def _todas_las_filas(datos):
    df = pd.concat([datos.ent, datos.val, datos.prueba])
    df.attrs = copy.deepcopy(datos.ent.attrs)
    return df


def optimismo_por_seleccion(fabrica, candidatos, repeticiones=500, semilla=0, detalle=False):
    """El engaño de elegir con la prueba, repetido: fabrica(semilla) da cada muestra.

    Por repetición: con_prueba = L_prueba del elegido por L_prueba (lo que anuncias si
    eliges con la prueba); con_val_y_prueba = L_prueba del elegido por L_val; R_real =
    R del elegido con la prueba; R_val = R del elegido con val (los dos sin reajuste).
    detalle=True: formato largo (repeticion, candidato, L_ent, L_val, L_prueba, R,
    R_final, L_prueba_final); las cuatro primeras del ajuste con ent, las _final del
    candidato reajustado con ent ∪ val. Desde: 1.2 (clase 2).
    Ejemplo: ml.optimismo_por_seleccion(lambda s: ml.PROCESOS["entregas_curvas"](semilla=s), cands, 100)
    """
    filas = []
    for i in range(int(repeticiones)):
        d = fabrica(int(semilla) + i)
        desarrollo = _desarrollo(d)
        for c, construir in candidatos.items():
            m = construir(d.ent)
            mf = construir(desarrollo)
            filas.append({"repeticion": i, "candidato": c, "L_ent": L(m, d.ent),
                          "L_val": L(m, d.val), "L_prueba": L(m, d.prueba),
                          "R": riesgo(m, d), "R_final": riesgo(mf, d),
                          "L_prueba_final": L(mf, d.prueba)})
    largo = pd.DataFrame(filas, columns=["repeticion", "candidato", "L_ent", "L_val", "L_prueba",
                                         "R", "R_final", "L_prueba_final"])
    return largo if detalle else _optimismo_agregado(largo)


def _optimismo_agregado(largo):
    filas = []
    for i, g in largo.groupby("repeticion", sort=True):
        g = g.reset_index(drop=True)
        ip = int(np.argmin(g["L_prueba"].to_numpy()))
        iv = int(np.argmin(g["L_val"].to_numpy()))
        filas.append({"repeticion": i, "con_prueba": g.loc[ip, "L_prueba"],
                      "con_val_y_prueba": g.loc[iv, "L_prueba"], "R_real": g.loc[ip, "R"],
                      "R_val": g.loc[iv, "R"]})
    return pd.DataFrame(filas, columns=["repeticion", "con_prueba", "con_val_y_prueba",
                                        "R_real", "R_val"])


def _pool(fabrica, s, n_minimo, nombre):
    d = fabrica(int(s))
    pool = _todas_las_filas(d)
    if len(pool) < n_minimo:
        raise ValueError(f"{nombre}: la fábrica da {len(pool)} filas y pides {n_minimo}; "
                         "pídele una muestra más grande, p. ej. "
                         "lambda s: ml.PROCESOS['entregas_curvas'](n=960, semilla=s)")
    return d, pool


def capacidad_elegida(fabrica, candidatos, ns, k=5, regla="minimo", repeticiones=20, semilla=0):
    """El hiperparámetro que elige la CV para cada n (columnas n, repeticion, elegido).

    Cada repetición toma una muestra de fabrica de al menos max(ns) filas y, para cada
    n, elige con CV_k sobre sus primeras n filas. Desde: 1.2 (clase 2).
    Ejemplo: ml.capacidad_elegida(fab, cands, ns=[30, 120, 480])
    """
    filas = []
    ns = [int(v) for v in ns]
    for i in range(int(repeticiones)):
        _, pool = _pool(fabrica, int(semilla) + i, max(ns), "capacidad_elegida")
        for n in ns:
            df = pool.iloc[:n].copy()
            df.attrs = copy.deepcopy(pool.attrs)
            s = elegir(df, candidatos, con="cv", k=k, regla=regla, semilla=int(semilla) + i)
            filas.append({"n": n, "repeticion": i,
                          "elegido": s.elegido_un_ee if regla == "un_ee" else s.elegido})
    return pd.DataFrame(filas, columns=["n", "repeticion", "elegido"])


def reparto(fabrica, construir, fracciones_prueba=(0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4,
                                                   0.45, 0.5), repeticiones=100, semilla=0):
    """Calidad del modelo contra precisión de la medición, según cuánto va a prueba.

    Cada repetición toma TODAS las filas de una muestra de fabrica, deja una fracción al
    azar como prueba y ajusta con el resto. Columnas fraccion, repeticion, R, L_prueba,
    error = L_prueba − R, ee. Desde: 1.2 (clase 2).
    Ejemplo: ml.reparto(lambda s: ml.PROCESOS["entregas_curvas"](n=240, semilla=s), construir)
    """
    filas = []
    for i in range(int(repeticiones)):
        s = int(semilla) + i
        d, pool = _pool(fabrica, s, 2, "reparto")
        for fr in fracciones_prueba:
            if not 0 < fr < 1:
                raise ValueError("cada fracción de prueba está en (0, 1)")
            rng = np.random.default_rng([s, 7, int(round(1000 * fr))])
            perm = rng.permutation(len(pool))
            n_p = max(1, int(round(len(pool) * fr)))
            ent = pool.iloc[np.sort(perm[n_p:])].copy()
            pru = pool.iloc[np.sort(perm[:n_p])]
            ent.attrs = copy.deepcopy(pool.attrs)
            m = construir(ent)
            l_i, _ = _perdidas_i(m, pru, None)
            R = riesgo(m, d)
            Lp = float(np.mean(l_i))
            filas.append({"fraccion": float(fr), "repeticion": i, "R": R, "L_prueba": Lp,
                          "error": Lp - R, "ee": error_estandar(l_i)})
    return pd.DataFrame(filas, columns=["fraccion", "repeticion", "R", "L_prueba", "error", "ee"])


# === 8 · Capacidad, sesgo y varianza ===


def curva_capacidad(datos, candidatos, conjuntos=("ent", "realidad"), k=None):
    """L de cada candidato en cada conjunto, con su EE, en formato largo.

    candidatos = {valor: construir(df) -> Modelo}; conjuntos de "ent", "val",
    "prueba", "realidad", "despliegue" y, desde 1.2 (clase 2), "cv": CV_k al azar
    (k=5 si k es None, semilla 0) sobre ent ∪ val, con su EE entre pliegues.
    Ejemplo: ml.curva_capacidad(datos, {N: lambda df, N=N: ml.ajustar(df, phi=ml.polinomio(N)) for N in range(1, 9)})
    """
    validos = ("ent", "val", "prueba", "realidad", "despliegue", "cv")
    for c in conjuntos:
        if c not in validos:
            raise ValueError(f"conjuntos son de {validos}")
    filas = []
    for valor, construir in candidatos.items():
        modelo = construir(datos.ent)
        for c in conjuntos:
            if c == "cv":
                r = validacion_cruzada(datos, construir, k=5 if k is None else k)
                filas.append((valor, c, r.media, r.ee))
                continue
            df = _muestra_grande(datos, c) if c in ("realidad", "despliegue") else getattr(datos, c)
            if len(df) == 0:
                filas.append((valor, c, float("nan"), float("nan")))
                continue
            if modelo.tarea == "regresion":
                l_i = perdida(df["y"], modelo.predecir(df), "cuadratica")
            else:
                l_i = _perdida_log_i(modelo, df)
            ee = float(np.std(l_i, ddof=1) / math.sqrt(len(l_i))) if len(l_i) > 1 else float("nan")
            filas.append((valor, c, float(np.mean(l_i)), ee))
    return pd.DataFrame(filas, columns=["candidato", "conjunto", "L", "ee"])


@dataclass
class SesgoVarianza:
    """Lo que devuelve sesgo_varianza.

    tabla: candidato, ruido, sesgo2, varianza, total (promedios sobre la malla);
    predicciones: {candidato: matriz repeticiones × puntos de la malla}; malla: los
    puntos x (DataFrame); verdad: E[y | x] en la malla; ruido_x: Var(y | x) en la malla.
    """

    tabla: pd.DataFrame
    predicciones: dict
    malla: pd.DataFrame
    verdad: np.ndarray
    ruido_x: np.ndarray


def _malla_sv(datos, x_malla):
    cols = list(datos.columnas_x)
    meta = datos.ent.attrs.get("ml", {})
    if x_malla is None:
        real, _ = _grandes(datos)
        malla = real[cols].iloc[:1000].sort_values(cols[0]).reset_index(drop=True)
    elif isinstance(x_malla, pd.DataFrame):
        malla = x_malla[cols].reset_index(drop=True)
    else:
        if len(cols) != 1:
            raise ValueError("con varias x, x_malla es un DataFrame con esas columnas")
        malla = pd.DataFrame({cols[0]: np.asarray(x_malla, float)})
    malla = malla.copy()
    malla.attrs["ml"] = copy.deepcopy(meta)
    return malla


def sesgo_varianza(fabrica, construir_por_candidato, repeticiones=100, x_malla=None, semilla=0):
    """Descompone el error esperado: ruido + sesgo² + varianza, por candidato.

    Ajusta cada candidato con el ent de fabrica(semilla + i), i < repeticiones, y mide
    en la malla contra E[y | x] (f_visible). sesgo² = (media de f̂ − E[y|x])²; varianza =
    la de f̂ entre repeticiones (divisor repeticiones); ruido = Var(y | x). x_malla=None:
    1000 puntos de realidad (así el promedio es E_x). Desde: 1.2 (clase 2).
    Ejemplo: sv = ml.sesgo_varianza(datos.rehacer, {N: lambda df, N=N: ml.ajustar(df, phi=ml.polinomio(N)) for N in range(13)})
    """
    primero = fabrica(int(semilla))
    if primero.f_visible is None:
        raise ValueError("este proceso no sabe E[y | x]: no hay contra qué medir el sesgo")
    malla = _malla_sv(primero, x_malla)
    verdad = np.asarray(primero.f_visible(malla), float)
    pob = getattr(primero, "_pob", None)
    try:
        ruido_x = _var_y_dado_x(pob, malla, primero.semilla_realidad)
    except (ValueError, AttributeError):
        ruido_x = np.full(len(malla), float(primero.sigma2_e))
    preds = {c: np.empty((int(repeticiones), len(malla))) for c in construir_por_candidato}
    modelos = {c: [] for c in construir_por_candidato}
    for i in range(int(repeticiones)):
        d = primero if i == 0 else fabrica(int(semilla) + i)
        for c, construir in construir_por_candidato.items():
            m = construir(d.ent)
            modelos[c].append(m)
            preds[c][i] = np.asarray(m.predecir(malla), float)
    filas = []
    for c, P in preds.items():
        media = P.mean(axis=0)
        sesgo2 = float(np.mean((media - verdad) ** 2))
        var = float(np.mean(P.var(axis=0)))
        ruido = float(np.mean(ruido_x))
        filas.append((c, ruido, sesgo2, var, ruido + sesgo2 + var))
    sv = SesgoVarianza(tabla=pd.DataFrame(filas, columns=["candidato", "ruido", "sesgo2",
                                                          "varianza", "total"]),
                       predicciones=preds, malla=malla, verdad=verdad, ruido_x=ruido_x)
    sv._modelos = modelos
    sv._f_visible = primero.f_visible
    return sv


def curva_aprendizaje(fabrica, construir, ns, repeticiones=50, semilla=0):
    """Error contra n: L_ent y R de cada candidato con n datos de entrenamiento.

    construir es una función o un dict {candidato: construir}. Cada repetición toma una
    muestra de fabrica de al menos max(ns) filas y ajusta con sus primeras n (subconjuntos
    anidados); R se mide en despliegue. Columnas candidato, n, repeticion, L_ent, R.
    Desde: 1.2 (clase 2). Ejemplo: ml.curva_aprendizaje(lambda s: ml.PROCESOS["entregas_curvas"](n=960, semilla=s), cands, ns=[30, 60, 120])
    """
    construir = construir if isinstance(construir, dict) else {"modelo": construir}
    ns = [int(v) for v in ns]
    filas = []
    for i in range(int(repeticiones)):
        d, pool = _pool(fabrica, int(semilla) + i, max(ns), "curva_aprendizaje")
        for n in ns:
            df = pool.iloc[:n].copy()
            df.attrs = copy.deepcopy(pool.attrs)
            for c, f in construir.items():
                m = f(df)
                filas.append((c, n, i, L(m, df), riesgo(m, d)))
    return pd.DataFrame(filas, columns=["candidato", "n", "repeticion", "L_ent", "R"])



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
        pob = getattr(datos, "_pob", None)
        es_f = pob.f_visible_es_f() if hasattr(pob, "f_visible_es_f") else not datos.omitidas
        etiqueta = "f verdadera" if es_f else "E[y | lo visible]"
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
        salida = {}
        for m in modelos:  # dos modelos con los mismos hiperparámetros no se pisan
            base = _rotulo(m)
            rotulo, k = base, 2
            while rotulo in salida:
                rotulo, k = f"{base} ({k})", k + 1
            salida[rotulo] = m
        return salida
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


def dibujar_elecciones(tabla, columnas=("N_ent", "N_R"), ax=None, tema="claro"):
    """Dos histogramas de enteros lado a lado: cuántas veces se eligió cada valor (dos ejes).

    Barras = value_counts de cada columna. Desde: 1.1 (clase 1).
    Ejemplo: ml.dibujar_elecciones(ml.repetir(experimento, repeticiones=200))
    """
    if len(columnas) != 2 or any(c not in tabla.columns for c in columnas):
        raise ValueError(f"columnas son dos columnas de la tabla: {list(tabla.columns)}")
    fig, ejes = _ejes(ax, tema, n=2)
    roles = ("entrenamiento", "realidad")
    valores = pd.concat([tabla[c] for c in columnas])
    lo, hi = int(valores.min()), int(valores.max())
    for a, col, rol in zip(ejes, columnas, roles):
        cuentas = tabla[col].value_counts().sort_index()
        color = _color(rol, tema) if rol != "realidad" else _color("f", tema)
        barras = a.bar(cuentas.index.astype(int), cuentas.to_numpy(), width=0.8, color=color)
        for b in barras:
            b.set_gid(f"barra-{col}")
        a.set_xlim(lo - 0.6, hi + 0.6)
        a.set_xticks(range(lo, hi + 1, max(1, (hi - lo + 1) // 12)))
        a.set_xlabel(f"valor elegido ({col})")
        a.set_ylabel("veces")
        a.set_title(col)
    return ejes


def dibujar_no_free_lunch(tabla, ax=None, tema="claro"):
    """Aciertos fuera de la muestra de cada regla, en promedio por rugosidad, con la línea
    de 1/2 y el promedio global (sobre funciones, no media de medias) en la leyenda.

    Desde: 1.1 (clase 1). Ejemplo: ml.dibujar_no_free_lunch(ml.no_free_lunch())
    """
    fig, ax = _ejes(ax, tema)
    estilos = [("entrenamiento", "o", "-"), ("validacion", "^", "--"), ("prueba", "s", ":")]
    for k, (regla, trozo) in enumerate(tabla.groupby("regla", sort=False)):
        rol, marca, trazo = estilos[k % len(estilos)]
        valores = trozo["aciertos_fuera"].astype(float)  # Fraction exacta → float al dibujar
        medias = valores.groupby(trozo["rugosidad"]).mean()
        global_ = float(sum(trozo["aciertos_fuera"]) / len(trozo))
        ln, = ax.plot(medias.index, medias.to_numpy(), marker=marca, ls=trazo, lw=1.6,
                      color=_color(rol, tema), label=f"{regla} (promedio {global_:.3f})")
        ln.set_gid(f"regla-{regla}")
    ln = ax.axhline(0.5, ls=":", color=_color("piso", tema), lw=1.6, label="1/2")
    ln.set_gid("medio")
    ax.set_xlabel("rugosidad (aristas del cubo con etiquetas distintas)")
    ax.set_ylabel("aciertos fuera de la muestra")
    ax.set_ylim(-0.05, 1.05)
    _leyenda(ax, tema)
    return ax


# --- Gráficas de la clase 2 (1.2) ---


def _rectangulos(ax, filas, color, gid, alto=0.8, borde=None, rayado=None):
    """filas = [(y, [(inicio, largo), ...])]: una barra rota por fila."""
    for y, tramos in filas:
        if tramos:
            b = ax.broken_barh(tramos, (y - alto / 2, alto), facecolors=color,
                               edgecolors=borde or color, hatch=rayado, lw=0.4)
            b.set_gid(gid)


def _tramos(posiciones):
    """Posiciones enteras → tramos contiguos (inicio, largo)."""
    p = np.sort(np.asarray(posiciones, int))
    if len(p) == 0:
        return []
    cortes = np.flatnonzero(np.diff(p) != 1) + 1
    return [(int(g[0]), int(len(g))) for g in np.split(p, cortes)]


def dibujar_pliegues(n, k, m_activo=None, prueba=True, *, y=None, particion=None, ax=None,
                     tema="claro"):
    """Los k pliegues: en cada vuelta, qué filas ajustan (●) y cuáles validan (▲, rayado).

    particion: la lista que devolvió pliegues(...) (se dibuja lo que se usó; n y k deben
    coincidir); sin ella, bloques contiguos. y: marca la clase menos frecuente y cuenta
    los pliegues de validación sin ningún caso. Desde: 1.2 (clase 2).
    Ejemplo: ml.dibujar_pliegues(48, 5, m_activo=2, particion=ml.pliegues(df, 5))
    """
    n, k = int(n), int(k)
    if particion is not None:
        if len(particion) != k:
            raise ValueError(f"particion trae {len(particion)} pliegues y k = {k}")
        validas = [np.asarray(v, int) for _, v in particion]
        total = sorted(np.concatenate(validas).tolist())
        if total != list(range(n)):
            raise ValueError(f"particion no reparte las {n} filas (¿otro n?)")
    else:
        validas = [np.asarray(v, int) for v in np.array_split(np.arange(n), k)]
    fig, ax = _ejes(ax, tema)
    t = _TEMAS[tema]
    c_ent, c_val = _color("entrenamiento", tema), _color("validacion", tema)
    for m, val in enumerate(validas, start=1):
        fila = k - m
        ajuste = np.setdiff1d(np.arange(n), val)
        activo = m_activo is None or m == m_activo
        tenue = (lambda c: c) if activo else (lambda c: _horneado(c, t["panel"], 0.35))
        _rectangulos(ax, [(fila, _tramos(ajuste))], tenue(c_ent), f"ajuste-{m}")
        _rectangulos(ax, [(fila, _tramos(val))], tenue(c_val), f"valida-{m}", rayado="///")
        ax.text(-0.01 * n, fila, f"vuelta {m}", ha="right", va="center", fontsize=8,
                color=t["texto"], fontweight="bold" if m == m_activo else None)
    if prueba:
        ancho = max(1, n // 4)
        b = ax.broken_barh([(n + 0.04 * n, ancho)], (-0.4, k - 0.2),
                           facecolors=_color("prueba", tema), hatch="xx", lw=0.4)
        b.set_gid("prueba")
        ax.text(n + 0.04 * n + ancho / 2, k - 0.35, "prueba\n(cerrada)", ha="center", va="bottom",
                fontsize=8, color=t["texto"])
    if y is not None:
        y = np.asarray(y)
        if len(y) != n:
            raise ValueError(f"y trae {len(y)} valores y n = {n}")
        valores, cuentas = np.unique(y, return_counts=True)
        rara = valores[int(np.argmin(cuentas))]
        pos = np.flatnonzero(y == rara)
        for m, val in enumerate(validas, start=1):
            dentro = np.intersect1d(val, pos)
            ln, = ax.plot(dentro + 0.5, np.full(len(dentro), k - m), ls="", marker="*", ms=7,
                          color=t["texto"])
            ln.set_gid(f"rara-{m}")
        vacios = sum(len(np.intersect1d(v, pos)) == 0 for v in validas)
        ax.set_title(f"★ = clase {rara}: {vacios} de {k} pliegues de validación sin ninguno",
                     fontsize=9, color=t["texto"])
    ax.set_xlim(-0.14 * n, n * (1.35 if prueba else 1.02))
    ax.set_ylim(-0.7, k - 0.3 + (0.6 if prueba else 0))
    ax.set_yticks([])
    ax.set_xlabel("filas de desarrollo (● ajusta · ▲ valida)")
    return ax


def dibujar_histograma_estimaciones(valores, verdadero, etiqueta, ax=None, tema="claro"):
    """Una o varias series de estimaciones repetidas contra el valor verdadero.

    valores: un arreglo o un dict {nombre: arreglo} (un histograma por serie, misma
    línea verdadera para todas). Desde: 1.2 (clase 2).
    Ejemplo: ml.dibujar_histograma_estimaciones(L_pruebas, verdadero=R, etiqueta="L_prueba")
    """
    fig, ax = _ejes(ax, tema)
    series = dict(valores) if isinstance(valores, dict) else {etiqueta: valores}
    roles = ["prueba", "validacion", "entrenamiento"]
    rayas = [None, "///", "\\\\"]
    todos = np.concatenate([np.asarray(v, float)[np.isfinite(np.asarray(v, float))]
                            for v in series.values()])
    bordes = np.histogram_bin_edges(todos, bins=30) if len(todos) else 10
    for i, (nombre, v) in enumerate(series.items()):
        v = np.asarray(v, float)
        color = _color(roles[i % 3], tema)
        _, _, barras = ax.hist(v[np.isfinite(v)], bins=bordes, histtype="step", lw=1.8,
                               color=color, hatch=rayas[i % 3], label=str(nombre))
        for b in barras:
            b.set_gid(f"serie-{nombre}")
    ln = ax.axvline(float(verdadero), color=_color("realidad", tema), ls="--", lw=1.8,
                    label="verdadero")
    ln.set_gid("verdadero")
    ax.set_xlabel(etiqueta)
    ax.set_ylabel("repeticiones")
    _leyenda(ax, tema)
    return ax


def _serie(obj, conjuntos=("realidad", "despliegue", "ent")):
    """dict, Series o tabla de curva_capacidad → Series {candidato: valor}."""
    if obj is None:
        return None
    if isinstance(obj, pd.DataFrame):
        for c in conjuntos:
            trozo = obj[obj["conjunto"] == c]
            if len(trozo):
                return pd.Series(trozo["L"].to_numpy(float), index=list(trozo["candidato"]))
        raise ValueError(f"la tabla no trae ninguno de los conjuntos {conjuntos}")
    if isinstance(obj, pd.Series):
        return obj.astype(float)
    if isinstance(obj, dict):
        return pd.Series({k: float(v) for k, v in obj.items()})
    raise ValueError("pasa un dict {candidato: valor}, una Series o la tabla de curva_capacidad")


_SERIE_CON = {"ent": ("entrenamiento", "o", "L_ent"), "val": ("validacion", "^", "L_val"),
              "cv": ("validacion", "^", "CV_k"), "prueba": ("prueba", "s", "L_prueba")}


def dibujar_cv(seleccion, R=None, L_ent=None, piso=None, benchmark=None, *, ax=None,
               tema="claro"):
    """La curva con que se eligió (CV_k con barras, L_val, L_ent o L_prueba), el umbral
    «mínimo + 1 EE» (se lee por la media) y marcas sobre el elegido y el de un EE.

    R, L_ent: dict, Series o tabla de curva_capacidad; piso y benchmark como en
    dibujar_curva_capacidad. Desde: 1.2 (clase 2).
    Ejemplo: ml.dibujar_cv(ml.elegir(datos, cands, con="cv"), piso=ml.piso(datos))
    """
    fig, ax = _ejes(ax, tema)
    t = _TEMAS[tema]
    tabla = seleccion.tabla
    cands = list(tabla["candidato"])
    numerico = all(isinstance(c, (int, float, np.integer, np.floating)) for c in cands)
    pos = {c: (c if numerico else i) for i, c in enumerate(cands)}
    xs = np.array([pos[c] for c in cands], float)
    v = tabla["valor"].to_numpy(float)
    ee = tabla["ee"].to_numpy(float)
    rol, marca, rotulo = _SERIE_CON[seleccion.con]
    con_ee = np.isfinite(ee).any()
    estilo = dict(color=_color(rol, tema), marker=marca, ls="-", lw=1.4, ms=7, label=rotulo)
    if con_ee:
        cont = ax.errorbar(xs, v, yerr=ee, capsize=3, **estilo)
        cont[0].set_gid(f"serie-{seleccion.con}")
    else:
        ln, = ax.plot(xs, v, **estilo)
        ln.set_gid(f"serie-{seleccion.con}")
    if con_ee:
        i = cands.index(seleccion.elegido)
        signo = 1 if seleccion.sentido == "min" else -1
        umbral = v[i] + signo * ee[i]
        ln = ax.axhline(umbral, color=t["texto"], ls=(0, (1, 2)), lw=1.2,
                        label="mínimo + 1 EE" if signo == 1 else "máximo − 1 EE")
        ln.set_gid("umbral")
    i = cands.index(seleccion.elegido)
    ln, = ax.plot([xs[i]], [v[i]], marker="o", ms=15, mfc="none", mew=2, ls="",
                  color=t["texto"], label=f"elegido (mínimo): {seleccion.elegido}")
    ln.set_gid("elegido")
    if seleccion.elegido_un_ee is not None:
        j = cands.index(seleccion.elegido_un_ee)
        ln, = ax.plot([xs[j]], [v[j]], marker="D", ms=13, mfc="none", mew=2, ls="",
                      color=_color("f", tema), label=f"elegido (un EE): {seleccion.elegido_un_ee}")
        ln.set_gid("elegido-un-ee")
    if L_ent is not None:
        if seleccion.con == "ent":
            warnings.warn("con con=\"ent\" la curva ya es L_ent: ignoro el argumento L_ent",
                          UserWarning, stacklevel=2)
        else:
            s = _serie(L_ent, ("ent",))
            ln, = ax.plot([pos[c] for c in s.index], s.to_numpy(), color=_color("entrenamiento", tema),
                          marker="o", ls="-", lw=1.2, label="L_ent")
            ln.set_gid("L_ent")
    if R is not None:
        s = _serie(R)
        ln, = ax.plot([pos[c] for c in s.index], s.to_numpy(), color=_color("realidad", tema),
                      ls="--", lw=1.6, label="R (solo en el simulador)")
        ln.set_gid("R")
    _linea_piso(ax, piso, tema)
    _linea_benchmark(ax, benchmark, tema)
    if not numerico:
        ax.set_xticks(range(len(cands)))
        ax.set_xticklabels([str(c) for c in cands])
    ax.set_xlabel("candidato (más simple → más complejo)")
    ax.set_ylabel(seleccion.criterio)
    _leyenda(ax, tema)
    return ax


def _curvas_sv(sv, candidato):
    if candidato not in sv.predicciones:
        raise ValueError(f"no hay candidato {candidato!r}; hay {list(sv.predicciones)}")
    return sv.predicciones[candidato]


def dibujar_abanico(sv, candidato, ax=None, tema="claro"):
    """Las f̂ de cada repetición (delgadas), su promedio (discontinua) y E[y | x] (verde).

    Desde: 1.2 (clase 2). Ejemplo: ml.dibujar_abanico(sv, 12)
    """
    fig, ax = _ejes(ax, tema)
    var = sv.malla.columns[0]
    x = sv.malla[var].to_numpy(float)
    P = _curvas_sv(sv, candidato)
    tenue = _horneado(_color("f_gorro", tema), _TEMAS[tema]["panel"], 0.3)
    for i, fila in enumerate(P):
        ln, = ax.plot(x, fila, color=tenue, lw=0.7, label="f̂ de cada muestra" if i == 0 else None)
        ln.set_gid("repeticion")
    ln, = ax.plot(x, P.mean(axis=0), color=_color("f_gorro", tema), ls="--", lw=2.6,
                  label="promedio de las f̂")
    ln.set_gid("promedio")
    ln, = ax.plot(x, sv.verdad, color=_color("f", tema), lw=ROLES["f"]["ancho"],
                  label="E[y | x]")
    ln.set_gid("f")
    lo, hi = np.percentile(np.concatenate([P.ravel(), sv.verdad]), [1, 99])
    margen = 0.15 * (hi - lo)
    ax.set_ylim(lo - margen, hi + margen)
    ax.set_xlabel(var)
    ax.set_ylabel("predicción")
    ax.set_title(f"candidato {candidato}: {len(P)} muestras", color=_TEMAS[tema]["texto"])
    _leyenda(ax, tema)
    return ax


def dibujar_sesgo_varianza(sv, ax=None, tema="claro"):
    """Barras apiladas por candidato: ruido, sesgo² y varianza; ★ en el menor total.

    Desde: 1.2 (clase 2). Ejemplo: ml.dibujar_sesgo_varianza(sv)
    """
    fig, ax = _ejes(ax, tema)
    tabla = sv.tabla
    cands = list(tabla["candidato"])
    xs = np.arange(len(cands))
    base = np.zeros(len(cands))
    for col, rol, rayado, rotulo in (("ruido", "piso", None, "ruido σ²(x)"),
                                     ("sesgo2", "prueba", "///", "sesgo²"),
                                     ("varianza", "validacion", "\\\\\\", "varianza")):
        h = tabla[col].to_numpy(float)
        barras = ax.bar(xs, h, bottom=base, color=_color(rol, tema), hatch=rayado,
                        edgecolor=_TEMAS[tema]["panel"], lw=0.5, label=rotulo)
        for b in barras:
            b.set_gid(f"barra-{col}")
        base = base + h
    i = int(np.argmin(base))
    ln, = ax.plot([xs[i]], [base[i]], marker="*", ms=16, ls="", color=_TEMAS[tema]["texto"],
                  label=f"menor total: {cands[i]}")
    ln.set_gid("optimo")
    techo = np.sort(base)[min(len(base) - 1, max(1, len(base) // 2))] * 3
    if base.max() > techo:  # los grados que explotan no aplastan a los demás
        ax.set_ylim(0, techo)
        _nota(ax, "barras recortadas arriba: su total sale del eje", tema)
    ax.set_xticks(xs)
    ax.set_xticklabels([str(c) for c in cands])
    ax.set_xlabel("candidato (capacidad →)")
    ax.set_ylabel("error cuadrático esperado")
    _leyenda(ax, tema)
    return ax


def dibujar_curva_aprendizaje(tabla, piso=None, *, elegido=None, resumen="media", ax=None,
                              tema="claro"):
    """Error contra n (escala log): L_ent (●) y R (discontinua) de cada candidato,
    resumidos por la media o la mediana de las repeticiones; con elegido (la tabla de
    capacidad_elegida), un segundo panel abajo con el candidato elegido contra n.

    Desde: 1.2 (clase 2). Ejemplo: ml.dibujar_curva_aprendizaje(tabla, piso=9, resumen="mediana")
    """
    if resumen not in ("media", "mediana"):
        raise ValueError('resumen es "media" o "mediana"')
    paneles = 2 if elegido is not None else 1
    if ax is None and paneles == 2:
        fig, ejes = plt.subplots(2, 1, figsize=(6.4, 6.4), sharex=True,
                                 gridspec_kw={"height_ratios": [3, 1.4]})
        _, ejes = _ejes(list(ejes), tema, n=2)
    else:
        fig, ejes = _ejes(ax, tema, n=paneles)
    arriba = ejes[0] if paneles == 2 else ejes
    agrega = "median" if resumen == "mediana" else "mean"
    t = _TEMAS[tema]
    estilos = ["-", "--", "-.", ":"]
    for i, (c, g) in enumerate(tabla.groupby("candidato", sort=False)):
        r = g.groupby("n")[["L_ent", "R"]].agg(agrega)
        ln, = arriba.plot(r.index, r["L_ent"], marker="o", ls=estilos[i % 4], lw=1.0,
                          color=_color("entrenamiento", tema), label=f"L_ent · {c}")
        ln.set_gid(f"L_ent-{c}")
        ln, = arriba.plot(r.index, r["R"], marker="", ls=estilos[i % 4], lw=2.0,
                          color=_color("realidad", tema), label=f"R · {c}")
        ln.set_gid(f"R-{c}")
        arriba.text(r.index[-1], r["R"].iloc[-1], f"  {c}", va="center", fontsize=8,
                    color=t["texto"])
    _linea_piso(arriba, piso, tema)
    arriba.set_xscale("log")
    arriba.set_ylabel(f"pérdida ({resumen})")
    _leyenda(arriba, tema)
    if paneles == 2:
        abajo = ejes[1]
        e = elegido.groupby("n")["elegido"].median()
        ln, = abajo.plot(e.index, e.to_numpy(float), marker="s", color=_color("validacion", tema),
                         label="elegido por CV (mediana)")
        ln.set_gid("elegido")
        abajo.set_xscale("log")
        abajo.set_ylabel("elegido")
        abajo.set_xlabel("n")
        _leyenda(abajo, tema)
        return fig
    arriba.set_xlabel("n")
    return arriba


def _resultados_cv(resultados):
    if isinstance(resultados, Seleccion):
        if resultados.cv is None:
            raise ValueError('la Seleccion no trae CV: elige con con="cv"')
        return resultados.cv
    if isinstance(resultados, dict):
        return resultados
    raise ValueError("resultados es una Seleccion (con cv) o un dict {candidato: ResultadoCV}")


def dibujar_cajas_pliegues(resultados, estadistico=False, ax=None, tema="claro"):
    """Un triángulo por pliegue y candidato, con su media (raya); rotula el pliegue que
    más se aleja de la mediana de los otros. estadistico=True dibuja por_pliegue_estadistico.

    Desde: 1.2 (clase 2). Ejemplo: ml.dibujar_cajas_pliegues(seleccion)
    """
    fig, ax = _ejes(ax, tema)
    t = _TEMAS[tema]
    cvs = _resultados_cv(resultados)
    for i, (c, r) in enumerate(cvs.items()):
        valores = r.por_pliegue_estadistico if estadistico else r.por_pliegue
        if valores is None:
            raise ValueError("ese ResultadoCV no trae estadístico: pásalo a validacion_cruzada")
        v = np.asarray(valores, float)
        ln, = ax.plot(np.full(len(v), i), v, ls="", marker="^", ms=8,
                      color=_color("validacion", tema), label="un pliegue" if i == 0 else None)
        ln.set_gid(f"pliegues-{c}")
        media = float(np.nanmean(v))
        ln, = ax.plot([i - 0.25, i + 0.25], [media, media], color=t["texto"], lw=2,
                      label="media" if i == 0 else None)
        ln.set_gid(f"media-{c}")
        if np.isfinite(v).sum() >= 3:
            lejos = [abs(v[m] - np.nanmedian(np.delete(v, m))) for m in range(len(v))]
            m = int(np.nanargmax(lejos))
            ax.annotate(f"pliegue {m + 1}", (i, v[m]), xytext=(8, 0), textcoords="offset points",
                        fontsize=8, color=t["texto"], va="center")
    ax.set_xticks(range(len(cvs)))
    ax.set_xticklabels([str(c) for c in cvs])
    ax.set_xlabel("candidato")
    ax.set_ylabel("estadístico por pliegue" if estadistico else "L de cada pliegue")
    _leyenda(ax, tema)
    return ax


def _trazo_diana(ax, xs, ys, verdadero, promedio, tema):
    """El trazo común de las dianas (clase 2) y de β̂ repetido (clase 3): cruces por
    repetición, el verdadero en verde y el promedio en discontinua."""
    ln, = ax.plot(xs, ys, ls="", marker="x", ms=6, mew=1.2, color=_color("f_gorro", tema),
                  label="una muestra")
    ln.set_gid("repeticion")
    return ln


def dibujar_diana(sv, x0, candidatos=None, ax=None, tema="claro"):
    """Las predicciones de cada repetición en x0, su promedio y f(x0), una fila por candidato.

    La posición horizontal de cada cruz es su predicción. Desde: 1.2 (clase 2).
    Ejemplo: ml.dibujar_diana(sv, 5.0, candidatos=[1, 12])
    """
    fig, ax = _ejes(ax, tema)
    t = _TEMAS[tema]
    var = sv.malla.columns[0]
    candidatos = list(sv.predicciones) if candidatos is None else list(candidatos)
    punto = pd.DataFrame({var: [float(x0)]})
    punto.attrs = copy.deepcopy(sv.malla.attrs)
    verdad = float(np.asarray(sv._f_visible(punto), float)[0]) if hasattr(sv, "_f_visible") \
        else float(np.interp(x0, sv.malla[var], sv.verdad))
    for fila, c in enumerate(candidatos):
        if hasattr(sv, "_modelos"):
            p = np.array([float(np.asarray(m.predecir(punto))[0]) for m in sv._modelos[c]])
        else:
            P = _curvas_sv(sv, c)
            j = int(np.argmin(np.abs(sv.malla[var].to_numpy(float) - x0)))
            p = P[:, j]
        sacudida = np.random.default_rng(fila).uniform(-0.25, 0.25, len(p))
        ln = _trazo_diana(ax, p, fila + sacudida, verdad, p.mean(), tema)
        if fila:
            ln.set_label(None)
        ln, = ax.plot([p.mean()] * 2, [fila - 0.4, fila + 0.4], color=_color("f_gorro", tema),
                      ls="--", lw=2.4, label="promedio" if fila == 0 else None)
        ln.set_gid(f"promedio-{c}")
    ln = ax.axvline(verdad, color=_color("f", tema), lw=ROLES["f"]["ancho"],
                    label=f"E[y | x = {x0:g}]")
    ln.set_gid("f")
    ax.set_yticks(range(len(candidatos)))
    ax.set_yticklabels([f"candidato {c}" for c in candidatos])
    ax.set_ylim(-0.6, len(candidatos) - 0.4)
    ax.set_xlabel(f"predicción en x = {x0:g}")
    ax.tick_params(colors=t["texto"])
    _leyenda(ax, tema)
    return ax


def _panel_contratos(ax, tabla, columna, resaltar, tema):
    t = _TEMAS[tema]
    etiquetas = [f"{c}\n{s}" for c, s in zip(tabla["contrato"], tabla["separacion"])]
    xs = np.arange(len(tabla))
    est = tabla[columna].to_numpy(float)
    barras = ax.bar(xs, est, width=0.6, color=_color("prueba", tema), hatch="..",
                    edgecolor=t["panel"], label="L_prueba (lo que promete)")
    for b, c in zip(barras, tabla["contrato"]):
        b.set_gid(f"barra-{c}")
        if resaltar is not None and c == resaltar:
            b.set_edgecolor(t["texto"])
            b.set_linewidth(2.2)
    ln, = ax.plot(xs, est, ls="", marker="s", ms=7, color=_color("prueba", tema))
    ln.set_gid("estimado")
    for i, (r, bm) in enumerate(zip(tabla["R"], tabla["benchmark"])):
        ln, = ax.plot([i - 0.38, i + 0.38], [r, r], color=_color("realidad", tema), ls="--", lw=2.2,
                      label="R en el despliegue" if i == 0 else None)
        ln.set_gid("R")
        ln, = ax.plot([i - 0.38, i + 0.38], [bm, bm], color=_color("benchmark", tema), ls="-.",
                      lw=1.6, label="benchmark (media de ent)" if i == 0 else None)
        ln.set_gid("benchmark")
    ax.set_xticks(xs)
    ax.set_xticklabels(etiquetas, fontsize=8)
    ax.set_ylabel("pérdida")
    _leyenda(ax, tema)


def dibujar_contratos(tabla, resaltar=None, ax=None, tema="claro"):
    """Lo que promete la prueba contra el riesgo del despliegue, por contrato.

    tabla: contrato, separacion, L_prueba (o estimado), R, benchmark; con una columna
    modelo, un panel por modelo (ax es entonces una lista y devuelve la Figure).
    Desde: 1.2 (clase 2). Ejemplo: ml.dibujar_contratos(tabla, resaltar="el mes que viene")
    """
    columna = "L_prueba" if "L_prueba" in tabla.columns else "estimado"
    faltan = {"contrato", "separacion", columna, "R", "benchmark"} - set(tabla.columns)
    if faltan:
        raise ValueError(f"a la tabla le faltan columnas: {sorted(faltan)}")
    if "modelo" not in tabla.columns:
        fig, ax = _ejes(ax, tema)
        _panel_contratos(ax, tabla.reset_index(drop=True), columna, resaltar, tema)
        return ax
    modelos = list(dict.fromkeys(tabla["modelo"]))
    fig, ejes = _ejes(ax, tema, n=len(modelos))
    ejes = [ejes] if len(modelos) == 1 else ejes
    for a, m in zip(ejes, modelos):
        _panel_contratos(a, tabla[tabla["modelo"] == m].reset_index(drop=True), columna,
                         resaltar, tema)
        a.set_title(str(m), color=_TEMAS[tema]["texto"])
    return fig


def dibujar_reparto(tabla, marca=None, ax=None, tema="claro"):
    """Dos paneles contra la fracción de prueba: arriba R medio del modelo (con ±2 EE de
    Monte Carlo), abajo la dispersión de error = L_prueba − R. marca: una fracción.

    Desde: 1.2 (clase 2). Ejemplo: ml.dibujar_reparto(ml.reparto(fab, construir), marca=0.2)
    """
    if ax is None:
        fig, ejes = plt.subplots(2, 1, figsize=(6.4, 6.0), sharex=True)
        fig, ejes = _ejes(list(ejes), tema, n=2)
    else:
        fig, ejes = _ejes(ax, tema, n=2)
    g = tabla.groupby("fraccion")
    R = g["R"].agg(["mean", "std", "count"])
    ee = R["std"] / np.sqrt(R["count"])
    a = ejes[0]
    cont = a.errorbar(R.index, R["mean"], yerr=2 * ee, marker="o", capsize=3,
                      color=_color("realidad", tema), label="R medio del modelo")
    cont[0].set_gid("R")
    a.set_ylabel("R (calidad del modelo)")
    _leyenda(a, tema)
    b = ejes[1]
    sd = g["error"].std()
    ln, = b.plot(sd.index, sd.to_numpy(), marker="s", color=_color("prueba", tema),
                 label="desv. de L_prueba − R")
    ln.set_gid("dispersion")
    b.axhline(0, color=_TEMAS[tema]["rejilla"], lw=0.8)
    b.set_ylabel("cuánto se equivoca la prueba")
    b.set_xlabel("fracción de prueba")
    _leyenda(b, tema)
    if marca is not None:
        for e in ejes:
            ln = e.axvline(float(marca), color=_TEMAS[tema]["texto"], ls=":", lw=1.2)
            ln.set_gid("marca")
    return fig



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
    propias = (cb.opciones or {}) if cb.clase == clase else {}
    ANALISIS_TALLER[clase](datos, **{**propias, **opciones})
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


def _taller_c1(datos, phi=None, N_max=10, escalar=True, zonas=None):
    """Clase 1. Regresión: la nube con f y el piso, la curva de capacidad de los
    polinomios N ≤ N_max (L_ent, R, piso y benchmark) y, si das phi, su Φ y su R.
    (1.1) escalar pasa a polinomio; zonas = {nombre: (desde, hasta)} dibuja el
    polinomio N_max sobre todas las zonas e imprime error_por_zona.
    Clasificación: logística con y sin phi, su frontera y los aciertos en el
    despliegue contra los de la moda."""
    if datos.tarea == "regresion":
        dibujar_proceso(datos)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            valor_piso = piso(datos)
        if len(datos.columnas_x) == 1:
            var = datos.columnas_x[0]
            candidatos = {N: (lambda df, N=N: ajustar(df, phi=polinomio(N, variable=var,
                                                                        escalar=escalar)))
                          for N in range(1, int(N_max) + 1)}
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                tabla = curva_capacidad(datos, candidatos, conjuntos=("ent", "despliegue"))
            dibujar_curva_capacidad(tabla, piso=valor_piso,
                                    benchmark=benchmarks(datos, _grandes(datos)[1]))
            if zonas:
                m = candidatos[int(N_max)](datos.ent)
                bordes = [v for z in zonas.values() for v in z]
                dibujar_ajuste({f"polinomio {int(N_max)}": m,
                                "E[y | x]": lambda x: datos.f_visible(pd.DataFrame({var: x}))}, datos,
                               ventana=(min(bordes), max(bordes)))
                print(error_por_zona(m, datos, zonas, variable=var).to_string(index=False))
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


def _taller_c2(datos, que="elegir", candidatos=range(13), k=5, regla="un_ee"):
    """Clase 2 (1.2). que="elegir": CV_k de los polinomios en la primera x, N̂ por las dos
    reglas, el modelo final (reajustado con ent ∪ val), L_prueba ± 2 EE junto al
    benchmark (la media de ent) en la misma prueba, la diferencia pareada en prueba
    (caso (a)), la comparación por CV por pliegue (descriptiva), R del despliegue y
    dibujar_cv. que="descomponer": sesgo_varianza con datos.rehacer (50 repeticiones)
    y dibujar_sesgo_varianza. Cada número dice con qué conjunto se calculó."""
    if datos.tarea != "regresion":
        raise ValueError("el taller de la clase 2 es de regresión")
    if que not in ("elegir", "descomponer"):
        raise ValueError('que es "elegir" o "descomponer"')
    var = datos.columnas_x[0]
    cands = list(candidatos)
    construir = {N: (lambda df, N=N: ajustar(df, phi=polinomio(N, variable=var))) for N in cands}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        valor_piso = piso(datos)
        if que == "descomponer":
            sv = sesgo_varianza(datos.rehacer, construir, repeticiones=50)
            dibujar_sesgo_varianza(sv)
            print(sv.tabla.round(3).to_string(index=False))
            print(f"(promedios sobre x en la población; el piso es {valor_piso:.3f})")
            return None
        s = elegir(datos, construir, con="cv", k=k, regla=regla, orden_complejidad=cands)
        final = s.modelo_final
        R = riesgo(final, datos)
        curva_R = {N: riesgo(construir[N](_desarrollo(datos)), datos) for N in cands}
    print(s.tabla.round(3).to_string(index=False))
    print(f"CV_{k} sobre ent ∪ val: N̂ por el mínimo = {s.elegido}, por un EE = {s.elegido_un_ee}"
          f" (regla usada: {regla})")
    media_ent = float(datos.ent["y"].mean())
    if len(datos.prueba):
        l_mod, _ = _perdidas_i(final, datos.prueba, None)
        l_ben = perdida(datos.prueba["y"], np.full(len(datos.prueba), media_ent))
        ee_m, ee_b = error_estandar(l_mod), error_estandar(l_ben)
        print(f"prueba: L_prueba del modelo final = {l_mod.mean():.3f} ± {2 * ee_m:.3f} (2 EE); "
              f"benchmark (media de ent) = {l_ben.mean():.3f} ± {2 * ee_b:.3f}")
        d, ee_d = diferencia_pareada(l_mod, l_ben)
        gana = "sí" if d + 2 * ee_d < 0 else "no"
        print(f"prueba: modelo final − benchmark = {d:.3f} (EE {ee_d:.3f}); le gana por más de "
              f"2 EE: {gana}")
    else:
        print("prueba: vacía en estos datos (no hay L_prueba)")
    if cands[0] in s.cv and s.cv[cands[0]] is not s.cv[s.elegido]:
        tabla = diferencia_por_pliegue(s.cv[s.elegido], s.cv[cands[0]])
        print(f"CV (descriptiva) del elegido − candidato {cands[0]}, por pliegue: "
              + ", ".join(f"{v:.2f}" for v in tabla["diferencia"].iloc[:-1])
              + f"; media {tabla['diferencia'].iloc[-1]:.2f}")
    print(f"despliegue: R del modelo final = {R:.3f}; piso = {valor_piso:.3f}")
    dibujar_cv(s, R=curva_R, piso=valor_piso,
               benchmark=(s.cv[cands[0]].media, s.cv[cands[0]].ee) if cands[0] in s.cv else None)
    return None


ANALISIS_TALLER = {1: _taller_c1, 2: _taller_c2}


# Bitácora técnica para el curioso: qué cambió en cada versión.
CAMBIOS = {
    "1.0": "Núcleo: piezas, procesos con realidad y despliegue, casos 1, 2 y 23, las Φ de "
           "la clase 1, ajustar (regresión y logística binaria) con la convención de μ, "
           "vecinos, pérdidas, aciertos, piso, benchmarks, curva de capacidad, "
           "beta_verdadero, las gráficas de la clase 1 y el taller.",
    "1.1": "Lo que pide la segunda página de la clase 1: repetir, error_por_zona, "
           "no_free_lunch, dibujar_elecciones y dibujar_no_free_lunch; el proceso "
           "«recursivo»; los casos 3, 4 y 5 (CasoBorde.opciones lleva lo que la galería "
           "pasa al taller, que gana escalar y zonas); y proceso_clasificacion como "
           "adelanto con su firma completa (binaria; lo demás llega con la clase 4).",
    "1.2": "Lo que pide la clase 2: los ruidos ar1 y efecto_grupo; proceso con separar "
           "(tiempo, grupo, estratificado), despliegue (futuro, grupos_nuevos, "
           "otra_poblacion) y deriva, también en proceso_clasificacion; Datos.rehacer; "
           "entregas_curvas y los casos 13 a 16; separar, pliegues; error_estandar, "
           "intervalo, validacion_cruzada (perdidas_fuera, estadistico), diferencia_pareada, "
           "diferencia_por_pliegue, elegir (modelo_final, regla de un EE), cv_anidada, "
           "optimismo_por_seleccion, capacidad_elegida, reparto, sesgo_varianza, "
           "curva_aprendizaje y curva_capacidad con \"cv\"; polinomio(0); sus gráficas y "
           "el taller de la clase 2.",
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
        if getattr(objeto, "__module__", None) == "typing":  # un alias de tipo (Particion)
            salida[nombre] = "tipo"
        elif inspect.isclass(objeto):
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
