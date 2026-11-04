"""Figuras de la clase 0 de la unidad de aprendizaje de maquina (unidad 9).

Catalogo FIGURAS_C0: id -> funcion sin argumentos que devuelve el SVG
completo como cadena. tools/gen_aprendizaje_maquina.py lo une con FIGURAS_U y
los otros cinco catalogos (contrato §7.1); un id repetido entre catalogos, o
un id que no empiece por "ml-c0-", es un error.

Dueno: prog-c0. Las cinco figuras del tramo rapido son SVG escrito a mano con
las primitivas y la paleta de gen_aprendizaje_maquina:

- F3 (ml-c0-jerarquia) y F4 (ml-c0-quien-elige-phi) son diagramas
  conceptuales;
- F1a, F1b y F2 son graficas de datos de seis puntos dibujadas a mano con
  escala lineal propia: es la **excepcion nombrada** de contrato §7.1
  (plan-c0-10 punto 4), asi que no usan dibujar_* de ml_lab y este modulo no
  lo importa nunca. Las cifras salen de tools/ml_cifras_c0.py.

Ningun color de rol se copia como literal: vistas, nuevas, la recta y el
promedio leen marca, trazo y color de gen.ROLES (entrenamiento,
observaciones_nuevas, f_estimada, benchmark). El texto visible no nombra los
roles: dice «vistas», «nuevas», «la recta», «el promedio» (contrato §7.3).
La regla «memorizar» no es un rol de la unidad: lleva un color propio
(MEMORIZAR) y una forma propia (escalones continuos), y siempre su nombre.

Pruebas propias: tools/test_figuras_ml_c0.py; guardas comunes:
tools/test_gen_aprendizaje_maquina.py.
"""
import gen_aprendizaje_maquina as gen
import ml_cifras_c0 as cifras

from gen_aprendizaje_maquina import (
    ACENTO, FONDO, LINEA, PANEL, REJILLA, SUAVE, TEXTO,
    caja, flecha, linea, mezclar, svg, texto, _n,
)

ROL = gen.ROLES
C_VISTAS = ROL["entrenamiento"]["color"]
C_NUEVAS = ROL["observaciones_nuevas"]["color"]
C_RECTA = ROL["f_estimada"]["color"]
G_RECTA = ROL["f_estimada"]["grosor"]
C_PROMEDIO = ROL["benchmark"]["color"]
D_PROMEDIO = ROL["benchmark"]["guiones"]
G_PROMEDIO = ROL["benchmark"]["grosor"]
# Color propio de la regla memorizar (no es un rol): lila que pasa 4.5:1
# contra PANEL y no se parece al rosa de prueba ni al magenta del promedio.
MEMORIZAR = "#b39bff"
BANDA = mezclar(SUAVE, 0.10, PANEL)
SEPARADOR = SUAVE

R_VISTA = 5.5
R_NUEVA = 4.5

C = cifras.cifras_c0_memorizar()
PARES = cifras.ENTREGAS
VISTAS = cifras.VISTAS
NUEVAS = cifras.NUEVAS
B0, B1 = C["beta_estrella"]
PROM = C["promedio_vistas"]
f = cifras.redondeo
REGLAS = ("memorizar", "recta", "promedio")
COLOR_REGLA = {"memorizar": MEMORIZAR, "recta": C_RECTA, "promedio": C_PROMEDIO}


# ------------------------------------------------------------ ejes ---

class Ejes:
    """Escala lineal de un panel de datos dibujado a mano."""

    def __init__(self, x0, y0, w, h, xlim, ylim):
        self.x0, self.y0, self.w, self.h = x0, y0, w, h
        self.xmin, self.xmax = xlim
        self.ymin, self.ymax = ylim

    def px(self, x):
        return self.x0 + (x - self.xmin) / (self.xmax - self.xmin) * self.w

    def py(self, y):
        return self.y0 + self.h - (y - self.ymin) / (self.ymax - self.ymin) * self.h

    def fondo(self, xticks, yticks, xlab, ylab, tam=12):
        out = [caja(self.x0, self.y0, self.w, self.h, relleno=PANEL, borde=LINEA,
                    radio=0, grosor=1)]
        for t in xticks:
            out.append(linea(self.px(t), self.y0, self.px(t), self.y0 + self.h,
                             color=REJILLA, grosor=0.8))
            out.append(texto(self.px(t), self.y0 + self.h + 15, f(t), color=SUAVE, tam=tam))
        for t in yticks:
            out.append(linea(self.x0, self.py(t), self.x0 + self.w, self.py(t),
                             color=REJILLA, grosor=0.8))
            out.append(texto(self.x0 - 6, self.py(t) + 4, f(t), color=SUAVE, tam=tam,
                             anclaje="end"))
        out.append(texto(self.x0 + self.w / 2, self.y0 + self.h + 33, xlab, tam=tam))
        if ylab:
            out.append(texto(self.x0, self.y0 - 9, ylab, tam=tam, anclaje="start",
                             color=SUAVE))
        return out

    def banda(self, x1, x2, rotulo, tam=12, arriba=False):
        yt = self.y0 - 9 if arriba else self.y0 + self.h - 8
        return [caja(self.px(x1), self.y0, self.px(x2) - self.px(x1), self.h,
                     relleno=BANDA, borde="none", radio=0, grosor=0),
                texto((self.px(x1) + self.px(x2)) / 2, yt, rotulo,
                      color=SUAVE, tam=tam)]

    def recta(self, b0, b1):
        x1, x2 = self.xmin, self.xmax
        return [linea(self.px(x1), self.py(b0 + b1 * x1), self.px(x2), self.py(b0 + b1 * x2),
                      color=C_RECTA, grosor=G_RECTA + 0.5)]

    def promedio(self, valor):
        return [linea(self.px(self.xmin), self.py(valor), self.px(self.xmax), self.py(valor),
                      color=C_PROMEDIO, grosor=G_PROMEDIO, guiones=D_PROMEDIO)]

    def escalones(self):
        """Lo que anuncia memorizar en cada distancia: el tiempo de la vista
        mas cercana (escalones planos, cortes a medio camino)."""
        xs = [PARES[i][0] for i in VISTAS]
        cortes = [self.xmin] + [(a + b) / 2 for a, b in zip(xs, xs[1:])] + [self.xmax]
        d = []
        for k, i in enumerate(VISTAS):
            y = self.py(PARES[i][1])
            d.append(f"{'M' if k == 0 else 'L'} {_n(self.px(cortes[k]))} {_n(y)}")
            d.append(f"L {_n(self.px(cortes[k + 1]))} {_n(y)}")
        return [f'<path d="{" ".join(d)}" fill="none" stroke="{MEMORIZAR}" '
                f'stroke-width="2.5" stroke-linejoin="round"/>']

    def vista(self, x, y, r=R_VISTA):
        return (f'<circle cx="{_n(self.px(x))}" cy="{_n(self.py(y))}" r="{_n(r)}" '
                f'fill="{C_VISTAS}" stroke="{FONDO}" stroke-width="1.5"/>')

    def nueva(self, x, y, r=R_NUEVA):
        return (f'<circle cx="{_n(self.px(x))}" cy="{_n(self.py(y))}" r="{_n(r)}" '
                f'fill="{C_NUEVAS}"/>')

    def anuncio(self, x, y, color):
        """Lo que una regla anuncia en una distancia: aro del color de la regla."""
        return (f'<circle cx="{_n(self.px(x))}" cy="{_n(self.py(y))}" r="4" '
                f'fill="{PANEL}" stroke="{color}" stroke-width="2"/>')


def _muestra_linea(x, y, regla):
    if regla == "memorizar":
        return linea(x, y, x + 26, y, color=MEMORIZAR, grosor=2.5)
    if regla == "recta":
        return linea(x, y, x + 26, y, color=C_RECTA, grosor=G_RECTA + 0.5)
    return linea(x, y, x + 26, y, color=C_PROMEDIO, grosor=G_PROMEDIO, guiones=D_PROMEDIO)


NOMBRE_LEYENDA = {
    "memorizar": "memorizar (copia la vista más cercana)",
    "recta": "la recta 11 + 3.6x",
    "promedio": "el promedio, 20 min",
}


def _leyenda(y, x0=24, con_nuevas=True, tam=12):
    """Dos renglones: memorizar y la recta; el promedio y las marcas."""
    out = []
    out.append(_muestra_linea(x0, y - 4, "memorizar"))
    out.append(texto(x0 + 32, y, NOMBRE_LEYENDA["memorizar"], tam=tam, anclaje="start"))
    out.append(_muestra_linea(x0 + 300, y - 4, "recta"))
    out.append(texto(x0 + 332, y, NOMBRE_LEYENDA["recta"], tam=tam, anclaje="start"))
    y2 = y + 22
    out.append(_muestra_linea(x0, y2 - 4, "promedio"))
    out.append(texto(x0 + 32, y2, NOMBRE_LEYENDA["promedio"], tam=tam, anclaje="start"))
    x = x0 + 172
    out.append(f'<circle cx="{_n(x + 6)}" cy="{_n(y2 - 4)}" r="{_n(R_VISTA)}" '
               f'fill="{C_VISTAS}" stroke="{FONDO}" stroke-width="1.5"/>')
    out.append(texto(x + 18, y2, "vistas", tam=tam, anclaje="start"))
    x += 74
    if con_nuevas:
        out.append(f'<circle cx="{_n(x + 6)}" cy="{_n(y2 - 4)}" r="{_n(R_NUEVA)}" '
                   f'fill="{C_NUEVAS}"/>')
        out.append(texto(x + 18, y2, "nuevas", tam=tam, anclaje="start"))
        x += 80
    out.append(f'<circle cx="{_n(x + 6)}" cy="{_n(y2 - 4)}" r="4" fill="{PANEL}" '
               f'stroke="{SUAVE}" stroke-width="2"/>')
    out.append(texto(x + 18, y2, "lo que anuncia una regla", tam=tam, anclaje="start"))
    return out


def _renglones_mae(x, y, clave, titulo, ancho=200, tam=13):
    """Titulo y tres renglones «regla   valor», cada regla con su color."""
    out = [texto(x, y, titulo, color=SUAVE, tam=12, anclaje="start")]
    for k, regla in enumerate(REGLAS):
        yy = y + 20 + 18 * k
        out.append(texto(x, yy, regla, color=COLOR_REGLA[regla], tam=tam,
                         anclaje="start", peso="700"))
        out.append(texto(x + ancho, yy, f(C[regla][clave]), color=COLOR_REGLA[regla],
                         tam=tam, anclaje="end", peso="700"))
    return out


XT = (0, 1, 2, 3, 4, 5, 6)
YT = (10, 15, 20, 25, 30, 35)
XLIM = (0, 6.5)
YLIM = (10, 36)


# ------------------------------------------------------------ F1a ---

ALT_F1A = (
    "Cuatro entregas vistas, de 1 a 4 km, tiempo contra distancia. Memorizar "
    "copia el tiempo de la entrega vista más cercana y acierta las cuatro, error "
    f"medio {f(C['memorizar']['mae_vistas'])} min; la recta {f(B0)} + {f(B1)}x falla "
    f"en promedio por {f(C['recta']['mae_vistas'])}; el promedio fijo de {f(PROM)} "
    f"min, por {f(C['promedio']['mae_vistas'])}. A la derecha, sin sus tiempos "
    "reales, lo que cada regla anuncia para 5 y 6 km: memorizar "
    f"{f(C['memorizar']['anuncios_nuevas'][0])} y {f(C['memorizar']['anuncios_nuevas'][1])}, "
    f"el promedio {f(C['promedio']['anuncios_nuevas'][0])} y "
    f"{f(C['promedio']['anuncios_nuevas'][1])}, la recta "
    f"{f(C['recta']['anuncios_nuevas'][0])} y {f(C['recta']['anuncios_nuevas'][1])}."
)


def fig_tres_reglas_en_lo_visto():
    W, H = 600, 486
    e = Ejes(58, 36, 516, 280, XLIM, YLIM)
    out = e.fondo(XT, YT, "distancia (km)", "tiempo (min)")
    out += e.banda(4.5, 6.5, "llegan después", arriba=True)
    out += e.promedio(PROM)
    out += e.escalones()
    out += e.recta(B0, B1)
    for i in VISTAS:
        out.append(e.vista(*PARES[i]))
    # lo que cada regla anuncia en 5 y 6 km (sin los tiempos reales)
    for k, i in enumerate(NUEVAS):
        km = PARES[i][0]
        for regla in REGLAS:
            valor = C[regla]["anuncios_nuevas"][k]
            out.append(e.anuncio(km, valor, COLOR_REGLA[regla]))
            dy = -9 if regla != "promedio" else 17
            out.append(texto(e.px(km), e.py(valor) + dy, f(valor), color=COLOR_REGLA[regla],
                             tam=12, peso="700"))
        # posicion de la nueva sobre el eje: se sabe la distancia, no el tiempo
        # se sabe su distancia, no su tiempo: la marca va sobre el eje
        out.append(e.nueva(km, YLIM[0]))
        out.append(texto(e.px(km), e.py(YLIM[0]) - 10, "?", color=TEXTO,
                         tam=13, peso="700"))
    out += _renglones_mae(58, 376, "mae_vistas", "error medio en las 4 vistas (min)")
    out += _leyenda(450, x0=24)
    return svg(W, H, ALT_F1A, "Tres reglas en las cuatro entregas que vio", out)


# ------------------------------------------------------------ F1b ---

ALT_F1B = (
    "Izquierda: las cuatro entregas vistas; error medio de memorizar "
    f"{f(C['memorizar']['mae_vistas'])}, de la recta {f(C['recta']['mae_vistas'])} y "
    f"del promedio {f(C['promedio']['mae_vistas'])}. Derecha: las dos nuevas, de 5 y "
    f"6 km, tardaron {PARES[NUEVAS[0]][1]} y {PARES[NUEVAS[1]][1]} min; memorizar "
    f"anuncia {f(C['memorizar']['anuncios_nuevas'][0])} y falla en promedio por "
    f"{f(C['memorizar']['mae_nuevas'])}; el promedio anuncia "
    f"{f(C['promedio']['anuncios_nuevas'][0])} y falla por "
    f"{f(C['promedio']['mae_nuevas'])}; la recta anuncia "
    f"{f(C['recta']['anuncios_nuevas'][0])} y {f(C['recta']['anuncios_nuevas'][1])} "
    f"y falla por {f(C['recta']['mae_nuevas'])}."
)


def fig_memorizar_contra_ajustar():
    W, H = 600, 452
    paneles = (
        Ejes(44, 44, 250, 230, XLIM, YLIM),
        Ejes(340, 44, 250, 230, XLIM, YLIM),
    )
    out = []
    izq, der = paneles
    out.append(texto(izq.x0 + izq.w / 2, 22, "Las 4 que vio", tam=15, peso="700"))
    out.append(texto(der.x0 + der.w / 2, 22, "Las 2 nuevas: tiempos reales",
                     tam=15, peso="700"))
    for e, rot in ((izq, "llegan después"), (der, "ya llegaron")):
        out += e.fondo(XT, YT, "distancia (km)", "min" if e is izq else None)
        out += e.banda(4.5, 6.5, rot, arriba=True)
        out += e.promedio(PROM)
        out += e.escalones()
        out += e.recta(B0, B1)
        for i in VISTAS:
            out.append(e.vista(*PARES[i], r=4.5))
    # derecha: segmentos de error de cada regla, del anuncio al tiempo real
    desplaza = {"memorizar": -0.17, "recta": 0.0, "promedio": 0.17}
    for k, i in enumerate(NUEVAS):
        km, real = PARES[i]
        for regla in REGLAS:
            anun = C[regla]["anuncios_nuevas"][k]
            xx = km + desplaza[regla]
            out.append(linea(der.px(xx), der.py(anun), der.px(xx), der.py(real),
                             color=COLOR_REGLA[regla], grosor=2.5))
            out.append(der.anuncio(xx, anun, COLOR_REGLA[regla]))
        out.append(der.nueva(km, real, r=5))
        out.append(texto(der.px(km) - 8, der.py(real) - 9, f"{real} min", color=TEXTO,
                         tam=12, peso="700", anclaje="end"))
    out += _renglones_mae(izq.x0, 334, "mae_vistas", "error medio en las 4 vistas",
                          ancho=170)
    out += _renglones_mae(der.x0, 334, "mae_nuevas", "error medio en las 2 nuevas",
                          ancho=170)
    out += _leyenda(H - 36, x0=24)
    return svg(W, H, ALT_F1B, "Cero error en lo que vio, siete minutos en lo nuevo", out)


# ------------------------------------------------------------- F2 ---

P = cifras.cifras_c0_paquetes()
AGR = P["agrupaciones"]

ALT_F2 = (
    "Izquierda: tabla con zona, distancia, paquetes y tiempo, y tiempo contra "
    f"distancia con la recta {f(B0)} + {f(B1)}x. Derecha: la misma tabla sin la "
    "columna de tiempo, y paquetes contra distancia con dos agrupaciones marcadas, "
    f"una por distancia, cerca hasta {f(AGR['por distancia']['corte'])} km y lejos "
    f"después, y otra por paquetes, pocos, de "
    f"{min(P['paquetes'][i] for i in AGR['por paquetes']['grupos'][0])} a "
    f"{max(P['paquetes'][i] for i in AGR['por paquetes']['grupos'][0])}, y muchos, de "
    f"{min(P['paquetes'][i] for i in AGR['por paquetes']['grupos'][1])} a "
    f"{max(P['paquetes'][i] for i in AGR['por paquetes']['grupos'][1])}."
)


def _tabla(x, y, con_y):
    """Mini-tabla de las seis entregas: zona, km, paquetes, min."""
    cols = (("zona", 62, "start"), ("km", 40, "end"), ("paquetes", 70, "end"),
            ("min", 54, "end"))
    out = []
    xs, xc = [], x
    for nombre, ancho, _ in cols:
        xs.append(xc)
        xc += ancho
    xmin_col, wmin = xs[3] + 6, cols[3][1]
    alto_f = 17
    if con_y:
        out.append(caja(xmin_col, y - 16, wmin, alto_f * 7 + 8, relleno=mezclar(ACENTO, 0.22),
                        borde=ACENTO, radio=4, grosor=1.5))
        out.append(texto(xmin_col + wmin / 2, y - 22, ["respuesta ", ("y", _IT)], tam=12,
                         color=TEXTO, peso="700"))
    else:
        out.append(caja(xmin_col, y - 16, wmin, alto_f * 7 + 8, relleno=PANEL,
                        borde=SUAVE, radio=4, grosor=1.5, guiones="4 3"))
        out.append(texto(xmin_col + wmin / 2, y - 22, "no está", tam=12, color=SUAVE,
                         peso="700"))
    for (nombre, ancho, anc), x0 in zip(cols, xs):
        xt = x0 + 4 if anc == "start" else x0 + ancho - 4
        if nombre == "min":
            xt += 6
        out.append(texto(xt, y, nombre, tam=12, color=SUAVE, anclaje=anc, peso="700"))
    out.append(linea(x, y + 5, xc + 6, y + 5, color=LINEA, grosor=1))
    for r, (km, minutos) in enumerate(PARES):
        yy = y + alto_f * (r + 1) + 2
        valores = (P["zonas"][r], str(km), str(P["paquetes"][r]),
                   str(minutos) if con_y else "?")
        for (nombre, ancho, anc), x0, v in zip(cols, xs, valores):
            xt = x0 + 4 if anc == "start" else x0 + ancho - 4
            if nombre == "min":
                xt += 6
            out.append(texto(xt, yy, v, tam=12, anclaje=anc,
                             color=TEXTO if (nombre != "min" or con_y) else SUAVE))
    return out


def fig_con_y_sin_y():
    W, H = 600, 446
    out = [texto(150, 22, "Con respuesta", tam=15, peso="700"),
           texto(450, 22, "Sin respuesta", tam=15, peso="700")]
    out += _tabla(22, 72, True)
    out += _tabla(322, 72, False)
    izq = Ejes(48, 222, 236, 186, XLIM, YLIM)
    der = Ejes(348, 222, 236, 186, XLIM, (0, 12))
    out += izq.fondo(XT, (10, 20, 30), "distancia (km)", "tiempo (min)")
    out += izq.recta(B0, B1)
    for km, minutos in PARES:
        out.append(izq.vista(km, minutos, r=5))
    out += der.fondo(XT, (0, 3, 6, 9, 12), "distancia (km)", "paquetes")
    cd = AGR["por distancia"]["corte"]
    cp = AGR["por paquetes"]["corte"]
    out.append(linea(der.px(cd), der.y0, der.px(cd), der.y0 + der.h, color=SEPARADOR,
                     grosor=2, guiones="6 4"))
    out.append(linea(der.x0, der.py(cp), der.x0 + der.w, der.py(cp), color=SEPARADOR,
                     grosor=2, guiones="6 4"))
    for r, (km, _) in enumerate(PARES):
        out.append(der.vista(km, P["paquetes"][r], r=5))
    # rotulos de las dos agrupaciones, junto a su linea
    out.append(texto(der.px(cd), der.y0 - 26, "por distancia", tam=12, color=TEXTO,
                     peso="700"))
    out.append(texto(der.px(cd) - 5, der.y0 - 9, "cerca ←", tam=12, anclaje="end",
                     color=SUAVE))
    out.append(texto(der.px(cd) + 5, der.y0 - 9, "→ lejos", tam=12, anclaje="start",
                     color=SUAVE))
    xr = der.x0 + der.w - 6
    out.append(texto(xr, der.py(cp) - 7, "por paquetes: muchos ↑", tam=12, anclaje="end",
                     color=TEXTO, peso="700"))
    out.append(texto(xr, der.py(cp) + 17, "pocos ↓", tam=12, anclaje="end",
                     color=TEXTO, peso="700"))
    return svg(W, H, ALT_F2, "Las mismas seis entregas, con respuesta y sin ella", out)


# ------------------------------------------------------------- F3 ---

# Rotulos de las cinco ramas, copiados de
# course/1_introduccion/2_historia_ia/_assets/v3-taxonomia.svg (D-015: la caja
# hermana dice «Aprendizaje máquina», como historia; el zoom y la prosa dicen
# «aprendizaje de máquina»).
RAMAS = (("Búsqueda y", "planificación"), ("Lógica y", "GOFAI"),
         ("Teoría de", "juegos"), ("Sistemas", "expertos"),
         ("Aprendizaje", "máquina"))
NIVELES = (
    ("aprendizaje de máquina", "regresión logística"),
    ("aprendizaje de representaciones", "autoencoder poco profundo"),
    ("aprendizaje profundo", "red profunda de varias capas"),
)
ALT_F3 = (
    "Cinco ramas hermanas de la inteligencia artificial; la del aprendizaje de "
    "máquina se amplía y adentro muestra tres rectángulos anidados: aprendizaje de "
    "máquina con la regresión logística, aprendizaje de representaciones con un "
    "autoencoder poco profundo y aprendizaje profundo con una red de varias capas."
)


def fig_jerarquia():
    W, H = 600, 500
    out = [caja(12, 12, W - 24, 112, relleno="none", borde=LINEA, radio=12),
           texto(26, 36, "Inteligencia artificial", tam=16, peso="700", anclaje="start")]
    ancho, hueco, x = 104, 8, 26
    cajas = []
    for k, (l1, l2) in enumerate(RAMAS):
        ml = k == len(RAMAS) - 1
        out.append(caja(x, 50, ancho, 60, relleno=PANEL,
                        borde=ACENTO if ml else LINEA, grosor=2.5 if ml else 1.5, radio=8))
        out.append(texto(x + ancho / 2, 74, l1, tam=12, peso="700",
                         color=TEXTO if ml else SUAVE))
        out.append(texto(x + ancho / 2, 90, l2, tam=12, peso="700",
                         color=TEXTO if ml else SUAVE))
        cajas.append(x)
        x += ancho + hueco
    xm = cajas[-1]
    # zoom: de la caja de aprendizaje maquina al rectangulo grande
    zx, zy, zw, zh = 26, 160, W - 52, 270
    out.append(linea(xm, 110, zx, zy, color=ACENTO, grosor=1.5, guiones="5 4"))
    out.append(linea(xm + ancho, 110, zx + zw, zy, color=ACENTO, grosor=1.5, guiones="5 4"))
    out.append(texto(W / 2, 148, "de cerca:", tam=12, color=SUAVE))
    for k, (nombre, ejemplo) in enumerate(NIVELES):
        rx, ry = zx + 30 * k, zy + 62 * k
        rw, rh = zw - 60 * k, zh - 82 * k
        out.append(caja(rx, ry, rw, rh, relleno=mezclar(ACENTO, 0.07 + 0.08 * k),
                        borde=ACENTO, grosor=2, radio=10))
        out.append(texto(rx + 14, ry + 24, nombre, tam=14, peso="700", anclaje="start"))
        out.append(texto(rx + 14, ry + 42, f"ej.: {ejemplo}", tam=12, anclaje="start",
                         color=SUAVE))
    out.append(texto(W / 2, zy + zh + 26, "Solo aquí dentro hay anidamiento.",
                     tam=13, peso="700", color=ACENTO))
    out.append(texto(W / 2, zy + zh + 46,
                     "Las cinco ramas de arriba son hermanas: ninguna contiene a las demás.",
                     tam=12, color=SUAVE))
    return svg(W, H, ALT_F3, "El aprendizaje de máquina, visto de cerca dentro de la IA", out)


# ------------------------------------------------------------- F4 ---

ALT_F4 = (
    "Cuatro tiras. Reglas: todo a mano. Clásico: la representación fi de x a mano y "
    "el predictor con parámetros beta ajustado con datos. Representaciones: fi de x "
    "y el predictor, los dos con datos. Profundo: capa 1, capa 2 y más, una sobre "
    "otra, que juntas forman fi de x, y el predictor, todo con datos."
)
C_DATOS = mezclar(ACENTO, 0.24)
_IT = {"estilo": "italic"}
PREDICTOR = ["predictor con parámetros ", ("β", _IT)]


def _bloque(x, y, w, renglones, datos, alto=50):
    """Caja de una pieza: rellena de acento si se ajusta con datos, borde
    punteado si la eligio una persona. El ultimo renglon lo dice en texto."""
    if datos:
        out = [caja(x, y, w, alto, relleno=C_DATOS, borde=ACENTO, grosor=2, radio=8)]
        pie = "se ajusta con datos" if w >= 130 else "con datos"
    else:
        out = [caja(x, y, w, alto, relleno=FONDO, borde=SUAVE, grosor=2, radio=8,
                    guiones="5 4")]
        pie = "a mano"
    yy = y + alto / 2 - 7 * (len(renglones) - 1) - 1
    for r in renglones:
        out.append(texto(x + w / 2, yy, r, tam=13, peso="700"))
        yy += 15
    out.append(texto(x + w / 2, y + alto - 7, pie, tam=12,
                     color=TEXTO if datos else SUAVE))
    return out


def _cabos(x, y, s):
    return texto(x, y, s, tam=15, peso="700")


def fig_quien_elige_phi():
    W, H = 600, 524
    out = []
    phi = [("φ", _IT), "(", ("x", _IT), ")"]
    yhat = [("ŷ", _IT)]
    tiras = [
        ("1 · Reglas", 34),
        ("2 · Aprendizaje de máquina clásico", 144),
        ("3 · Aprendizaje de representaciones", 274),
        ("4 · Aprendizaje profundo", 404),
    ]
    for nombre, y in tiras:
        out.append(texto(16, y, nombre, tam=14, peso="700", anclaje="start", color=ACENTO))
    yb = 46
    # tira 1: entrada -> programa a mano -> salida
    out.append(_cabos(46, yb + 31, "entrada"))
    out.append(flecha(80, yb + 26, 168, yb + 26))
    out += _bloque(172, yb, 256, ["programa escrito"], False)
    out.append(flecha(430, yb + 26, 514, yb + 26))
    out.append(_cabos(548, yb + 31, "salida"))

    def tira_phi(y, phi_datos, rotulo_phi):
        o = [texto(26, y + 31, [("x", _IT)], tam=16, peso="700")]
        o.append(flecha(38, y + 26, 66, y + 26))
        o += _bloque(70, y, 170, [phi + [f" {rotulo_phi}"]], phi_datos)
        o.append(flecha(242, y + 26, 270, y + 26))
        o += _bloque(274, y, 246, [PREDICTOR], True)
        o.append(flecha(522, y + 26, 552, y + 26))
        o.append(texto(572, y + 31, yhat, tam=16, peso="700"))
        return o

    out += tira_phi(156, False, "elegida")
    out += tira_phi(286, True, "aprendida")
    # tira 4: capas en etapas, que juntas forman phi(x)
    y = 416
    out.append(texto(26, y + 31, [("x", _IT)], tam=16, peso="700"))
    out.append(flecha(38, y + 26, 54, y + 26))
    out += _bloque(58, y, 76, ["capa 1"], True, alto=50)
    out.append(flecha(136, y + 26, 148, y + 26))
    out += _bloque(152, y, 76, ["capa 2"], True, alto=50)
    out.append(flecha(230, y + 26, 240, y + 26))
    out.append(texto(250, y + 31, "…", tam=16, peso="700"))
    out.append(flecha(260, y + 26, 270, y + 26))
    out += _bloque(274, y, 246, [PREDICTOR], True)
    out.append(flecha(522, y + 26, 552, y + 26))
    out.append(texto(572, y + 31, yhat, tam=16, peso="700"))
    # llave bajo las capas
    yl = y + 58
    out.append(f'<path d="M 58 {_n(yl)} Q 58 {_n(yl + 8)} 70 {_n(yl + 8)} L 147 {_n(yl + 8)} '
               f'Q 157 {_n(yl + 8)} 159 {_n(yl + 16)} Q 161 {_n(yl + 8)} 171 {_n(yl + 8)} '
               f'L 248 {_n(yl + 8)} Q 260 {_n(yl + 8)} 260 {_n(yl)}" fill="none" '
               f'stroke="{SUAVE}" stroke-width="1.5"/>')
    out.append(texto(159, yl + 32, ["juntas forman ", *phi, ", con datos"], tam=13,
                     peso="700"))
    # los dos criterios, entre las tiras que separan
    for yc, s in ((252, "↕ cambia quién elige φ: una persona o el ajuste"),
                  (382, "↕ cambia si φ se arma en una etapa o en varias")):
        out.append(linea(16, yc - 4, 70, yc - 4, color=LINEA, grosor=1))
        out.append(linea(W - 70, yc - 4, W - 16, yc - 4, color=LINEA, grosor=1))
        out.append(texto(W / 2, yc, s, tam=12, color=SUAVE, peso="700"))
    return svg(W, H, ALT_F4, "Quién elige qué: cuatro maneras de construir un sistema", out)


FIGURAS_C0 = {
    "ml-c0-tres-reglas-en-lo-visto": fig_tres_reglas_en_lo_visto,
    "ml-c0-memorizar-contra-ajustar": fig_memorizar_contra_ajustar,
    "ml-c0-con-y-sin-y": fig_con_y_sin_y,
    "ml-c0-jerarquia": fig_jerarquia,
    "ml-c0-quien-elige-phi": fig_quien_elige_phi,
}
