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
    "memorizar": "memorizar (la vista más cercana)",
    "recta": "la recta 11 + 3.6x",
    "promedio": "el promedio, 20 min",
}


def _leyenda(y, x0=14, con_nuevas=True, tam=12):
    """Leyenda en renglones para un lienzo de 300 px (cabe en el celular):
    una regla por renglon y, en el ultimo, las marcas."""
    out = []
    for k, regla in enumerate(REGLAS):
        yy = y + 20 * k
        out.append(_muestra_linea(x0, yy - 4, regla))
        out.append(texto(x0 + 32, yy, NOMBRE_LEYENDA[regla], tam=tam, anclaje="start"))
    y2 = y + 20 * len(REGLAS)
    x = x0
    out.append(f'<circle cx="{_n(x + 6)}" cy="{_n(y2 - 4)}" r="{_n(R_VISTA)}" '
               f'fill="{C_VISTAS}" stroke="{FONDO}" stroke-width="1.5"/>')
    out.append(texto(x + 16, y2, "vistas", tam=tam, anclaje="start"))
    x += 62
    if con_nuevas:
        out.append(f'<circle cx="{_n(x + 6)}" cy="{_n(y2 - 4)}" r="{_n(R_NUEVA)}" '
                   f'fill="{C_NUEVAS}"/>')
        out.append(texto(x + 16, y2, "nuevas", tam=tam, anclaje="start"))
    y3 = y2 + 20
    out.append(f'<circle cx="{_n(x0 + 6)}" cy="{_n(y3 - 4)}" r="4" fill="{PANEL}" '
               f'stroke="{SUAVE}" stroke-width="2"/>')
    out.append(texto(x0 + 16, y3, "lo que anuncia una regla", tam=tam, anclaje="start"))
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


ANCHO_DATOS = 300   # cabe sin scroll en el cuerpo de figura a 390 px (~305 px)


def _desconocidas(e, y):
    """Franja bajo el eje x, alineada con «llegan después», con las dos
    nuevas: se sabe su distancia y no su tiempo, asi que no se dibujan dentro
    de la grafica de tiempo (ahi el eje y les inventaria un valor)."""
    alto = 34
    x1, x2 = e.px(4.5), e.px(XLIM[1])
    out = [caja(x1, y, x2 - x1, alto, relleno=BANDA, borde=LINEA, radio=4, grosor=1),
           texto(x1 - 8, y + 13, "distancia conocida,", color=SUAVE, tam=12,
                 anclaje="end"),
           texto(x1 - 8, y + 29, "tiempo desconocido →", color=SUAVE, tam=12,
                 anclaje="end")]
    for i in NUEVAS:
        km = PARES[i][0]
        # r2: el punto va en su distancia (5 y 6 km); solo el «?» se corre
        out.append(f'<circle cx="{_n(e.px(km))}" cy="{_n(y + alto / 2)}" '
                   f'r="{_n(R_NUEVA)}" fill="{C_NUEVAS}"/>')
        out.append(texto(e.px(km) + 11, y + alto / 2 + 5, "?", color=TEXTO, tam=13,
                         peso="700"))
    return out


def fig_tres_reglas_en_lo_visto():
    # r2: 532 de alto deja la ultima linea base de la leyenda (518) a 14 px
    # del borde; con 520 las colas de la q y la g se recortaban.
    W, H = ANCHO_DATOS, 532
    e = Ejes(40, 34, 248, 210, XLIM, YLIM)
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
    out += _desconocidas(e, e.y0 + e.h + 44)
    out += _renglones_mae(e.x0, 352, "mae_vistas", "error medio en las 4 vistas (min)",
                          ancho=200)
    out += _leyenda(438)
    return svg(W, H, ALT_F1A, "Tres reglas en las cuatro entregas que vio", out)


# ------------------------------------------------------------ F1b ---

ALT_F1B = (
    "Arriba: las cuatro entregas vistas; error medio de memorizar "
    f"{f(C['memorizar']['mae_vistas'])}, de la recta {f(C['recta']['mae_vistas'])} y "
    f"del promedio {f(C['promedio']['mae_vistas'])}. Abajo: las dos nuevas, de 5 y "
    f"6 km, tardaron {PARES[NUEVAS[0]][1]} y {PARES[NUEVAS[1]][1]} min; memorizar "
    f"anuncia {f(C['memorizar']['anuncios_nuevas'][0])} y falla en promedio por "
    f"{f(C['memorizar']['mae_nuevas'])}; el promedio anuncia "
    f"{f(C['promedio']['anuncios_nuevas'][0])} y falla por "
    f"{f(C['promedio']['mae_nuevas'])}; la recta anuncia "
    f"{f(C['recta']['anuncios_nuevas'][0])} y {f(C['recta']['anuncios_nuevas'][1])} "
    f"y falla por {f(C['recta']['mae_nuevas'])}."
)


# Los segmentos de error de cada regla se corren a un lado de su distancia
# para no taparse; el anuncio y el tiempo real se quedan en 5 y 6 km, y dos
# conectores cortos dicen a que distancia pertenece cada segmento.
DESPLAZA = {"memorizar": -0.27, "recta": 0.0, "promedio": 0.27}


def _segmento_de_error(e, km, anun, real, regla):
    xx = km + DESPLAZA[regla]
    color = COLOR_REGLA[regla]
    out = []
    if xx != km:
        for yy in (anun, real):
            out.append(linea(e.px(km), e.py(yy), e.px(xx), e.py(yy), color=color,
                             grosor=1.2, guiones="2 2"))
    out.append(linea(e.px(xx), e.py(anun), e.px(xx), e.py(real), color=color, grosor=2.5))
    return out


def fig_memorizar_contra_ajustar():
    W, H = ANCHO_DATOS, 832
    arriba = Ejes(40, 44, 248, 170, XLIM, YLIM)
    abajo = Ejes(40, 390, 248, 200, XLIM, YLIM)
    out = [texto(W / 2, 20, "Las 4 que vio", tam=15, peso="700"),
           texto(W / 2, 362, "Las 2 nuevas: tiempos reales", tam=15, peso="700")]
    for e, rot in ((arriba, "llegan después"), (abajo, "ya llegaron")):
        out += e.fondo(XT, YT, "distancia (km)", "min")
        out += e.banda(4.5, 6.5, rot, arriba=True)
        out += e.promedio(PROM)
        out += e.escalones()
        out += e.recta(B0, B1)
        for i in VISTAS:
            out.append(e.vista(*PARES[i], r=4.5))
    # abajo: el segmento de error de cada regla, del anuncio al tiempo real
    for k, i in enumerate(NUEVAS):
        km, real = PARES[i]
        for regla in REGLAS:
            out += _segmento_de_error(abajo, km, C[regla]["anuncios_nuevas"][k], real, regla)
        for regla in REGLAS:
            out.append(abajo.anuncio(km, C[regla]["anuncios_nuevas"][k], COLOR_REGLA[regla]))
        out.append(abajo.nueva(km, real, r=5))
        out.append(texto(abajo.px(km), abajo.py(real) - 10, f"{real} min", color=TEXTO,
                         tam=12, peso="700"))
    out += _renglones_mae(arriba.x0, 272, "mae_vistas", "error medio en las 4 vistas (min)",
                          ancho=200)
    out += _renglones_mae(abajo.x0, 648, "mae_nuevas", "error medio en las 2 nuevas (min)",
                          ancho=200)
    out += _leyenda(738)
    return svg(W, H, ALT_F1B, "Cero error en lo que vio, siete minutos en lo nuevo", out)


# ------------------------------------------------------------- F2 ---

P = cifras.cifras_c0_paquetes()
AGR = P["agrupaciones"]

ALT_F2 = (
    "Arriba: tabla con zona, distancia, paquetes y tiempo, y tiempo contra "
    f"distancia con la recta {f(B0)} + {f(B1)}x. Abajo: la misma tabla sin la "
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
    W, H = ANCHO_DATOS, 816
    out = [texto(W / 2, 20, "Con respuesta", tam=15, peso="700")]
    out += _tabla(28, 64, True)
    con = Ejes(44, 210, 244, 150, XLIM, YLIM)
    out += con.fondo(XT, (10, 20, 30), "distancia (km)", "tiempo (min)")
    out += con.recta(B0, B1)
    for km, minutos in PARES:
        out.append(con.vista(km, minutos, r=5))
    out.append(linea(14, 412, W - 14, 412, color=LINEA, grosor=1))
    out.append(texto(W / 2, 440, "Sin respuesta", tam=15, peso="700"))
    out += _tabla(28, 484, False)
    sin = Ejes(44, 640, 244, 130, XLIM, (0, 12))
    out += sin.fondo(XT, (0, 3, 6, 9, 12), "distancia (km)", "paquetes")
    cd = AGR["por distancia"]["corte"]
    cp = AGR["por paquetes"]["corte"]
    out.append(linea(sin.px(cd), sin.y0, sin.px(cd), sin.y0 + sin.h, color=SEPARADOR,
                     grosor=2, guiones="6 4"))
    out.append(linea(sin.x0, sin.py(cp), sin.x0 + sin.w, sin.py(cp), color=SEPARADOR,
                     grosor=2, guiones="6 4"))
    for r, (km, _) in enumerate(PARES):
        out.append(sin.vista(km, P["paquetes"][r], r=5))
    # rotulos de las dos agrupaciones, junto a su linea
    out.append(texto(sin.px(cd), sin.y0 - 24, "por distancia", tam=12, color=TEXTO,
                     peso="700"))
    out.append(texto(sin.px(cd) - 5, sin.y0 - 8, "cerca ←", tam=12, anclaje="end",
                     color=SUAVE))
    out.append(texto(sin.px(cd) + 5, sin.y0 - 8, "→ lejos", tam=12, anclaje="start",
                     color=SUAVE))
    xr = sin.x0 + sin.w - 6
    out.append(texto(xr, sin.py(cp) - 7, "por paquetes: muchos ↑", tam=12, anclaje="end",
                     color=TEXTO, peso="700"))
    out.append(texto(xr, sin.py(cp) + 17, "pocos ↓", tam=12, anclaje="end",
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
    """r2: a 300 px de ancho (cabe a 390 px sin scroll). Las cinco ramas en
    una rejilla de 2 + 2 + 1, con la de aprendizaje maquina sola abajo y el
    zoom debajo de ella."""
    W, H = ANCHO_DATOS, 500
    out = [caja(8, 8, W - 16, 204, relleno="none", borde=LINEA, radio=12),
           texto(20, 30, "Inteligencia artificial", tam=15, peso="700", anclaje="start")]
    ancho, alto = 126, 44
    pos = [(20, 44), (154, 44), (20, 96), (154, 96), (87, 152)]
    for k, ((l1, l2), (x, y)) in enumerate(zip(RAMAS, pos)):
        ml = k == len(RAMAS) - 1
        out.append(caja(x, y, ancho, alto, relleno=PANEL,
                        borde=ACENTO if ml else LINEA, grosor=2.5 if ml else 1.5, radio=8))
        for j, l in enumerate((l1, l2)):
            out.append(texto(x + ancho / 2, y + 19 + 15 * j, l, tam=12, peso="700",
                             color=TEXTO if ml else SUAVE))
    xm, ym = pos[-1]
    # zoom: de la caja de aprendizaje maquina al rectangulo grande
    zx, zy, zw, zh = 8, 246, W - 16, 180
    out.append(linea(xm, ym + alto, zx, zy, color=ACENTO, grosor=1.5, guiones="5 4"))
    out.append(linea(xm + ancho, ym + alto, zx + zw, zy, color=ACENTO, grosor=1.5,
                     guiones="5 4"))
    out.append(texto(W / 2, 234, "de cerca:", tam=12, color=SUAVE))
    for k, (nombre, ejemplo) in enumerate(NIVELES):
        rx, ry = zx + 10 * k, zy + 56 * k
        rw, rh = zw - 20 * k, zh - 64 * k
        out.append(caja(rx, ry, rw, rh, relleno=mezclar(ACENTO, 0.07 + 0.08 * k),
                        borde=ACENTO, grosor=2, radio=10))
        out.append(texto(rx + 10, ry + 21, nombre, tam=13, peso="700", anclaje="start"))
        out.append(texto(rx + 10, ry + 39, f"ej.: {ejemplo}", tam=12, anclaje="start",
                         color=SUAVE))
    out.append(texto(W / 2, zy + zh + 24, "Solo aquí dentro hay anidamiento.",
                     tam=13, peso="700", color=ACENTO))
    out.append(texto(W / 2, zy + zh + 44, "Las cinco ramas de arriba son hermanas:",
                     tam=12, color=SUAVE))
    out.append(texto(W / 2, zy + zh + 60, "ninguna contiene a las demás.",
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
PHI = "\u03d5"
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
    """r2: a 300 px de ancho (cabe a 390 px sin scroll). Cada tira en dos
    renglones: arriba la entrada y lo que el modelo ve de ella, abajo el
    predictor y la salida."""
    W, H = ANCHO_DATOS, 764
    out = []
    # U+03D5 (PHI SYMBOL), la forma con trazo recto: es la que MathJax dibuja
    # para \phi en la prosa; U+03C6 sale con la otra forma y el alumno veria
    # dos dibujos para el mismo simbolo.
    phi = [(PHI, _IT), "(", ("x", _IT), ")"]
    yhat = [("ŷ", _IT)]
    tiras = [
        ("1 · Reglas", 22),
        ("2 · Aprendizaje de máquina clásico", 152),
        ("3 · Aprendizaje de representaciones", 366),
        ("4 · Aprendizaje profundo", 580),
    ]
    for nombre, y in tiras:
        out.append(texto(8, y, nombre, tam=14, peso="700", anclaje="start", color=ACENTO))
    # tira 1: entrada -> programa a mano -> salida
    out.append(texto(40, 48, "entrada", tam=15, peso="700", anclaje="start"))
    out.append(flecha(66, 54, 66, 72))
    out += _bloque(40, 76, 160, ["programa escrito"], False)
    out.append(flecha(202, 101, 222, 101))
    out.append(texto(228, 106, "salida", tam=15, peso="700", anclaje="start"))

    def salida(y):
        o = _bloque(44, y, 218, [PREDICTOR], True)
        o.append(flecha(264, y + 25, 279, y + 25))
        o.append(texto(290, y + 30, yhat, tam=16, peso="700"))
        return o

    def tira_phi(y, phi_datos, rotulo_phi):
        o = [texto(24, y + 30, [("x", _IT)], tam=16, peso="700")]
        o.append(flecha(34, y + 25, 52, y + 25))
        o += _bloque(56, y, 180, [phi + [f" {rotulo_phi}"]], phi_datos)
        o.append(flecha(146, y + 52, 146, y + 68))
        o += salida(y + 72)
        return o

    out += tira_phi(164, False, "elegida")
    out += tira_phi(378, True, "aprendida")
    # tira 4: capas en etapas, que juntas forman phi(x)
    y = 592
    out.append(texto(24, y + 30, [("x", _IT)], tam=16, peso="700"))
    out.append(flecha(34, y + 25, 52, y + 25))
    out += _bloque(56, y, 70, ["capa 1"], True, alto=50)
    out.append(flecha(128, y + 25, 138, y + 25))
    out += _bloque(142, y, 70, ["capa 2"], True, alto=50)
    out.append(flecha(214, y + 25, 222, y + 25))
    out.append(texto(232, y + 30, "…", tam=16, peso="700"))
    out.append(linea(242, y + 25, 250, y + 25, color=ACENTO, grosor=2))
    out.append(flecha(250, y + 24, 250, y + 102))
    # llave bajo las capas
    yl = y + 56
    out.append(f'<path d="M 56 {_n(yl)} Q 56 {_n(yl + 8)} 68 {_n(yl + 8)} L 124 {_n(yl + 8)} '
               f'Q 132 {_n(yl + 8)} 134 {_n(yl + 16)} Q 136 {_n(yl + 8)} 144 {_n(yl + 8)} '
               f'L 200 {_n(yl + 8)} Q 212 {_n(yl + 8)} 212 {_n(yl)}" fill="none" '
               f'stroke="{SUAVE}" stroke-width="1.5"/>')
    out.append(texto(126, yl + 32, ["juntas forman ", *phi, ", con datos"], tam=13,
                     peso="700"))
    out += salida(y + 106)
    # los dos criterios, entre las tiras que separan
    for yc, (s1, s2) in ((322, (f"↕ cambia quién elige {PHI}:", "una persona o el ajuste")),
                         (536, (f"↕ cambia si {PHI} se arma", "en una etapa o en varias"))):
        out.append(linea(8, yc - 18, W - 8, yc - 18, color=LINEA, grosor=1))
        out.append(texto(W / 2, yc, s1, tam=12, color=SUAVE, peso="700"))
        out.append(texto(W / 2, yc + 16, s2, tam=12, color=SUAVE, peso="700"))
    return svg(W, H, ALT_F4, "Quién elige qué: cuatro maneras de construir un sistema", out)


FIGURAS_C0 = {
    "ml-c0-tres-reglas-en-lo-visto": fig_tres_reglas_en_lo_visto,
    "ml-c0-memorizar-contra-ajustar": fig_memorizar_contra_ajustar,
    "ml-c0-con-y-sin-y": fig_con_y_sin_y,
    "ml-c0-jerarquia": fig_jerarquia,
    "ml-c0-quien-elige-phi": fig_quien_elige_phi,
}
