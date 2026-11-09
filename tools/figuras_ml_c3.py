"""Figuras de la clase 3 de la unidad de aprendizaje de maquina (unidad 9).

Catalogo FIGURAS_C3: id -> funcion sin argumentos que devuelve el SVG
completo como cadena. tools/gen_aprendizaje_maquina.py lo une con FIGURAS_U y
los otros cinco catalogos (contrato §7.1); un id repetido entre catalogos, o
un id que no empiece por "ml-c3-", es un error.

Dueno: prog-c3 (lo creo vacio prog-lab en U.T3). Reglas para llenarlo:
- los diagramas conceptuales se escriben como SVG a mano con las primitivas
  y la paleta de gen_aprendizaje_maquina (marco, texto, caja, flecha, ROLES...);
- las graficas de datos se dibujan con las funciones dibujar_* de ml_lab y
  tema="sitio", y se convierten con gen.svg_de_matplotlib(fig, aria=...);
- ml_lab se pide con gen.ml_lab() dentro de la funcion de la figura, nunca
  al importar este modulo (importacion perezosa, contrato §7.1);
- ningun color de rol se copia como literal: se lee de gen.ROLES;
- las cifras que se dibujan salen de ml_lab o de tools/ml_cifras_c3.py, con
  los mismos procesos (datos_*) que citan las paginas y los notebooks.

Sus pruebas propias van en tools/test_figuras_ml_c3.py (sin prosa); las
guardas comunes, en tools/test_gen_aprendizaje_maquina.py.

Anclas por tramo (protocolo p5.2 §7.1): FIGURAS_C3 = _RAPIDO + _COMPLETO;
la rama de clase escribe solo antes del «fin tramo rapido».

Como en la clase 1, lo que ml_lab dibuja con transparencia se hornea aqui
contra el panel (`_sin_opacidad`): las guardas prohiben toda opacidad.
"""
import re

import gen_aprendizaje_maquina as gen
from gen_aprendizaje_maquina import (ACENTO, FONDO, LINEA, PANEL, SUAVE, TEXTO,
                                     caja, flecha, linea, mezclar, svg, texto)

VERDE = gen.color_rol("f_verdadera")
CIAN = gen.color_rol("f_estimada")
ORO = gen.color_rol("validacion")
# Ancho de las graficas de datos: 5.4 pulgadas = 388.8 puntos de viewBox, que
# a 600 px dan una escala de 1.54: la letra de 8 pt queda en 12.3 px.
ANCHO_IN = 5.4


# ------------------------------------------------------------ utilidades ---

_ESTILO = re.compile(r'style="([^"]*)"')


def _sin_opacidad(texto_svg, fondo=PANEL):
    """Hornea cada fill/stroke translucido contra el panel y quita la opacidad."""
    def cambiar(m):
        decl = [d.strip() for d in m.group(1).split(";") if d.strip()]
        props = {k.strip(): v.strip() for k, v in (d.split(":", 1) for d in decl)}
        general = float(props.pop("opacity", 1))
        relleno = float(props.pop("fill-opacity", 1)) * general
        trazo = float(props.pop("stroke-opacity", 1)) * general
        for clave, alfa in (("fill", relleno), ("stroke", trazo)):
            valor = props.get(clave, "")
            if alfa < 1 and valor.startswith("#") and len(valor) == 7:
                props[clave] = mezclar(valor, alfa, fondo)
        return 'style="' + "; ".join(f"{k}: {v}" for k, v in props.items()) + '"'

    return _ESTILO.sub(cambiar, texto_svg)


def _plt():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    return matplotlib, plt


def _grafica(dibujar, aria, titulo, alto_in, filas=1, columnas=1, rect=None, **subplots):
    """Arma una figura de datos con la paleta del sitio y la deja como SVG.

    Parte de los rcParams de fabrica: la figura no depende de quien corrio
    antes en el mismo proceso (la guarda compara sin escribir)."""
    matplotlib, plt = _plt()
    with matplotlib.rc_context():
        matplotlib.rcdefaults()
        matplotlib.rcParams.update(gen.RC_SITIO)
        matplotlib.rcParams.update({"font.size": 9, "axes.titlesize": 9.5,
                                    "axes.labelsize": 9, "xtick.labelsize": 8.5,
                                    "ytick.labelsize": 8.5, "legend.fontsize": 8.5})
        fig, ejes = plt.subplots(filas, columnas, figsize=(ANCHO_IN, alto_in), **subplots)
        dibujar(fig, ejes)
        from matplotlib.text import Text
        from matplotlib.ticker import FuncFormatter, NullFormatter
        for ax in fig.axes:                     # 10^k con superíndice unicode: mathtext
            for eje in (ax.xaxis, ax.yaxis):    # pone el exponente a 0.7 de la letra
                if eje.get_scale() == "log":
                    eje.set_major_formatter(FuncFormatter(_potencia))
                    eje.set_minor_formatter(NullFormatter())
        for ax in fig.axes:                     # ticks menores de un eje log incluidos
            for t in ax.get_xminorticklabels() + ax.get_yminorticklabels():
                t.set_fontsize(max(t.get_fontsize(), 8))
        from matplotlib.lines import Line2D
        for ln in fig.findobj(Line2D):          # un marcador hueco salía negro en el SVG:
            if str(ln.get_markerfacecolor()).lower() == "none":   # se rellena del panel
                ln.set_markerfacecolor(PANEL)     # y va debajo de los datos, que se ven
                ln.set_zorder(1.5)
        for t in fig.findobj(Text):
            if t.get_fontsize() < 8:
                t.set_fontsize(8)
        for ley in [ax.get_legend() for ax in fig.axes] + list(fig.legends):
            if ley is not None:
                for t in ley.get_texts():
                    t.set_fontsize(8.5)
                    t.set_color(TEXTO)
                ley.get_frame().set_facecolor(PANEL)
                ley.get_frame().set_edgecolor(LINEA)
                ley.get_frame().set_alpha(1.0)
        fig.tight_layout(rect=rect)
        crudo = gen.svg_de_matplotlib(fig, aria, titulo=titulo, ancho=600)
    return _sin_opacidad(crudo)


_SUPER = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def _potencia(v, _pos=None):
    """10ᵏ con superíndice unicode para los ejes logarítmicos."""
    import math
    if v <= 0:
        return ""
    k = math.log10(v)
    if abs(k - round(k)) > 1e-9:
        return ""
    return "10" + str(int(round(k))).translate(_SUPER)


def _cif():
    import ml_cifras_c3 as cif
    return cif


def _num(v, d=2):
    """Número con punto decimal y el signo menos tipográfico."""
    return f"{v:.{d}f}".replace("-", "−")


def _titulo(ax, s):
    ax.set_title(s, color=TEXTO, fontsize=9.5)


# Trazos para distinguir series sin depender del color (revisión c3 r1).
TRAZOS = ("-", "--", "-.", ":", (0, (6, 2, 1, 2, 1, 2)))
# Rótulos de ml_lab en ASCII -> con subíndice, como en la prosa.
ROTULOS = {"L_ent": "Lₑₙₜ", "CV_k": "CV₅", "L_val": "L_val"}


def _trazos(ax, gids, grosor=None):
    """Da a las líneas con esos gid un trazo distinto cada una (y el grosor dado)."""
    lineas = {ln.get_gid(): ln for ln in ax.get_lines()}
    for i, gid in enumerate(gids):
        if gid in lineas:
            lineas[gid].set_linestyle(TRAZOS[i % len(TRAZOS)])
            if grosor is not None:
                lineas[gid].set_linewidth(grosor[i] if isinstance(grosor, (list, tuple)) else grosor)


def _rotular(manejadores, rotulos):
    return manejadores, [ROTULOS.get(r, r) for r in rotulos]


def _rotulo_cv(r, nombre_minimo=None):
    """Rótulos cortos para la leyenda de dibujar_cv (los de ml_lab no caben)."""
    if r.startswith("elegido (mínimo)"):
        return "mínimo de CV₅" + (f" ({nombre_minimo})" if nombre_minimo else "")
    if r.startswith("elegido (un EE)"):
        return "regla de un EE"
    if r.startswith("R "):
        return "R (muestra enorme)"
    return ROTULOS.get(r, r)


def _promedio_en_rombo(ax):
    """El promedio de la diana como rombo hueco, distinto de la cruz (+) del
    coeficiente estructural y de las equis de cada muestra: así no se
    distinguen solo por el color (revisión c3 r1)."""
    for ln in ax.get_lines():
        if ln.get_gid() == "promedio":
            ln.set_marker("D")
            ln.set_markersize(12)
            ln.set_markeredgewidth(2.6)
            ln.set_markerfacecolor(PANEL)     # relleno del panel, encima de la nube
            ln.set_zorder(4)
        elif ln.get_gid() == "verdadero":
            ln.set_zorder(6)


# --- tramo rapido ---

# ----------------------------------------------------- F1 · ml-c3-mismo-rmse ---
# P1 §1. Dos modelos con el mismo RMSE de validación. Tres filas (las tres
# vistas) y dos columnas (los dos modelos): a 390 px, seis paneles en una fila
# de tres serían ilegibles (DECISIÓN prog-c3-2).

def ml_c3_mismo_rmse():
    cif = _cif()
    ml = gen.ml_lab()
    c = cif.cifras_c3_mismo_rmse()

    def dibujar(fig, ejes):
        for j, fila in enumerate(("correcto", "curva")):
            d = cif.datos_mismo_rmse(fila)
            m = ml.ajustar(d, phi=ml.columnas("x1"))
            ml.dibujar_tres_paneles(m, d.val, ax=list(ejes[:, j]), tema="sitio")
            nombre = ("A · recta correcta, ruido grande" if fila == "correcto"
                      else "B · recta a una curva, ruido chico")
            ejes[0, j].set_title(f"{nombre}\nRMSE val = {_num(c[f'rmse_val_{fila}'])}",
                                 color=TEXTO, fontsize=9)
            for ax in ejes[1:, j]:
                ax.set_title("")
            ejes[2, j].set_xlabel("x")

    aria = (f"Dos modelos con RMSE de validación {c['cita']['rmse_val']}, en tres vistas "
            "cada uno: predicción contra observación, histograma de residuales y residual "
            "contra x. A la izquierda, la recta correcta con ruido grande: el histograma es "
            "ancho y el residual contra x no tiene forma. A la derecha, una recta ajustada a "
            "una curva con ruido chico: el residual contra x forma una U.")
    return _grafica(dibujar, aria, "Dos modelos, el mismo RMSE", 7.2, filas=3, columnas=2)


# --------------------------------------------------- F2 · ml-c3-benchmarks ---

def ml_c3_benchmarks():
    cif = _cif()
    ml = gen.ml_lab()
    e, s = cif.cifras_c3_escala_y(), cif.cifras_c3_senal_debil()

    def dibujar(fig, ejes):
        for ax, d, t in ((ejes[0], ml.caso(11), "caso 11: y cerca de 1000"),
                         (ejes[1], cif.datos_senal(), "señal débil: f = 0.75x")):
            m = ml.ajustar(d)
            ml.dibujar_benchmarks(m, d, criterios=("cuadratica",), ax=ax, tema="sitio")
            _titulo(ax, t)

    aria = (f"Errores en validación en barras. Caso 11: el RMSE del modelo, {e['cita']['rmse_modelo']}, "
            f"es {e['cita']['rmse_sobre_ybar']} de y y casi iguala al de la media, "
            f"{e['cita']['rmse_media']}; la mejora sobre la media es {e['cita']['mejora']}. "
            f"Señal débil: el modelo, {s['cita']['rmse_modelo']}, casi toca la raíz del piso, "
            f"{s['cita']['raiz_piso']}, con la media en {s['cita']['rmse_media']}.")
    return _grafica(dibujar, aria, "Contra qué se mide un error", 5.0, filas=2)


# --------------------------------------------- F3 · ml-c3-media-acumulada ---

def ml_c3_media_acumulada():
    cif = _cif()
    ml = gen.ml_lab()
    c = cif.cifras_c3_colas()

    def dibujar(fig, ejes):
        ml.dibujar_media_acumulada(cif.piezas_colas(), n_max=cif.N_COLAS,
                                   trayectorias=cif.SEMILLAS_COLAS, ax=list(ejes), tema="sitio")
        for ax in ejes[:-1]:
            ax.set_xlabel("")

    aria = ("Promedio acumulado de e cuadrada contra n en 20 semillas, en escala logarítmica. "
            f"Con ruido normal las líneas se juntan (cociente máximo entre mínimo a n = 10 000: "
            f"{c['cita']['normal']}); con Pareto de exponente 1.5 y con Cauchy no se juntan "
            f"(cocientes {c['cita']['pareto']} y {c['cita']['cauchy']}).")
    return _grafica(dibujar, aria, "El MSE sin segundo momento", 6.6, filas=3)


# ------------------------------------- F4 · ml-c3-fuentes-patologias (a mano) ---
FP_W, FP_H = 600, 400
_FUENTES = (("1 · azar", "el ruido", "de siempre"),
            ("2 · variables que", "variable", "omitida"),
            ("3 · una familia", "interacción", "omitida"),
            ("4 · pocos datos", "colinealidad", ""))
_FUENTES_2 = ("", "no medimos", "equivocada", "")


def ml_c3_fuentes_patologias():
    c = [texto(16, 30, "Cuatro fuentes del error y lo que esta página rompe", tam=17,
               peso="700", anclaje="start"),
         texto(16, 52, "las cuatro fuentes de la clase 1; debajo, su patología", tam=13,
               color=SUAVE, anclaje="start")]
    w, x0, gap = 134, 16, 8
    for i, ((cab, p1, p2), cab2) in enumerate(zip(_FUENTES, _FUENTES_2)):
        x = x0 + i * (w + gap)
        cx = x + w / 2
        c.append(caja(x, 70, w, 62, relleno=PANEL, borde=LINEA, radio=8))
        c.append(texto(cx, 96, cab, tam=13, peso="700"))
        if cab2:
            c.append(texto(cx, 114, cab2, tam=13, peso="700"))
        c.append(flecha(cx, 134, cx, 168, color=ACENTO))
        c.append(caja(x, 172, w, 62, relleno=FONDO, borde=ACENTO, radio=8))
        c.append(texto(cx, 198, p1, tam=13, color=TEXTO))
        if p2:
            c.append(texto(cx, 216, p2, tam=13, color=TEXTO))
    c.append(texto(16, 268, "aparte, fuera de las cuatro:", tam=13, color=SUAVE, anclaje="start"))
    c.append(caja(16, 280, 276, 96, relleno=FONDO, borde=SUAVE, radio=8, guiones="3 4", grosor=1.5))
    c.append(texto(154, 308, "optimización", tam=13, peso="700", color=SUAVE))
    c.append(texto(154, 328, "escalas que entorpecen", tam=13, color=SUAVE))
    c.append(texto(154, 346, "al optimizador", tam=13, color=SUAVE))
    c.append(caja(308, 280, 276, 96, relleno=FONDO, borde=SUAVE, radio=8, guiones="3 4", grosor=1.5))
    c.append(texto(446, 308, "endogeneidad (caso 8)", tam=13, peso="700", color=SUAVE))
    c.append(texto(446, 328, "lineal, no se ve en el error:", tam=13, color=SUAVE))
    c.append(texto(446, 346, "rompe el coeficiente, no", tam=13, color=SUAVE))
    c.append(texto(446, 364, "la predicción con lo visible", tam=13, color=SUAVE))
    aria = ("Cuatro fuentes del error y sus patologías: azar, el ruido de siempre; variables "
            "que no medimos, la variable omitida; familia equivocada, la interacción omitida; "
            "pocos datos, la colinealidad. Aparte, la optimización (escalas que la entorpecen) "
            "y la endogeneidad lineal del caso 8, que no se ve en el error")
    return svg(FP_W, FP_H, aria, "Cuatro fuentes y sus patologías", c)


# --------------------------------------------------- F5 · ml-c3-diana-beta ---

def ml_c3_diana_beta():
    cif = _cif()
    ml = gen.ml_lab()
    c = cif.cifras_c3_diana()
    tablas = cif.tablas_diana()

    def dibujar(fig, ejes):
        for ax, (nombre, t) in zip(ejes.ravel(), tablas.items()):
            ml.dibujar_beta_repetido(t, verdadero={"x1": 1.0, "x2": 1.0},
                                     columnas=("x1", "x2"), ax=ax, tema="sitio")
            _titulo(ax, nombre)
            ax.set_xlim(-1.5, 3.5)
            ax.set_ylim(-1.5, 3.5)
            ax.set_aspect("equal", adjustable="box")
            _promedio_en_rombo(ax)
            if ax.get_legend() is not None:
                ax.get_legend().remove()
        ejes[0, 0].legend(loc="lower right")

    aria = ("Cuatro nubes de 200 estimaciones de beta 1 y beta 2; la cruz verde es el "
            "coeficiente estructural (1, 1) y el rombo cian el promedio: correcta centrada; "
            f"omitida corrida a {c['cita']['omitida']}; colineal alargada; endógena corrida a "
            f"{c['cita']['endogena']}")
    return _grafica(dibujar, aria, "La diana de los coeficientes", 5.8, filas=2, columnas=2)


# -------------------------------------------- F6 · ml-c3-interaccion-plano ---

def ml_c3_interaccion_plano():
    ml = gen.ml_lab()
    d = ml.caso(7)
    sin = ml.ajustar(d, phi=ml.columnas("x1", "x2"))
    con = ml.ajustar(d, phi=ml.combinar(ml.columnas("x1", "x2"), ml.interacciones(("x1", "x2"))))
    l_sin, l_con = ml.L(sin, d.val), ml.L(con, d.val)

    def dibujar(fig, ejes):
        for ax, m, t in ((ejes[0], sin, "sin la columna x1·x2"),
                         (ejes[1], con, "con la columna x1·x2")):
            ml.dibujar_residuales_plano(m, d.val, "x1", "x2", ax=ax, tema="sitio")
            _titulo(ax, f"{t}: L val = {_num(ml.L(m, d.val))}")
            ax.set_aspect("equal", adjustable="box")
            manejadores, _ = ax.get_legend_handles_labels()
            if ax.get_legend() is not None:
                ax.get_legend().remove()
        # la leyenda, debajo de los dos paneles: dentro tapaba la nube
        fig.legend(manejadores, ["residual e ≥ 0", "residual e < 0"], loc="lower center",
                   ncol=2, frameon=True)

    aria = ("Residuales de validación en el plano x1, x2, con triángulo hacia arriba si son "
            "positivos y hacia abajo si son negativos: sin la columna x1·x2 forman una silla; "
            f"con ella, ruido sin forma; L val {_num(l_sin)} contra {_num(l_con)}")
    return _grafica(dibujar, aria, "Una interacción es una columna más", 3.8, columnas=2,
                    rect=(0, 0.1, 1, 1))


# ------------------------------------------- F7 · ml-c3-colineal-prediccion ---

def ml_c3_colineal_prediccion():
    cif = _cif()
    ml = gen.ml_lab()
    c = cif.cifras_c3_colineal()
    t = cif.tablas_colineal()

    def dibujar(fig, ejes):
        a, b = ejes
        bins = 30
        a.hist(t[0.99]["x1"], bins=bins, color=mezclar(CIAN, 0.55, PANEL), edgecolor=CIAN,
               label="corr 0.99")
        a.hist(t[0.0]["x1"], bins=bins, color=mezclar(ORO, 0.7, PANEL), edgecolor=ORO,
               hatch="////", label="corr 0")
        a.axvline(1.0, color=VERDE, lw=2.5, label="β₁ estructural")
        a.set_xlabel("β̂₁ en 200 entrenamientos")
        a.legend(loc="upper left")
        _titulo(a, "el coeficiente")
        dentro = cif.prediccion_repetida(t[0.99], cif.DENTRO)
        fuera = cif.prediccion_repetida(t[0.99], cif.FUERA)
        b.hist(fuera, bins=bins, color=mezclar(ACENTO, 0.5, PANEL), edgecolor=ACENTO,
               hatch="////", label="fuera: x1 = 1, x2 = −1")
        b.hist(dentro, bins=bins, color=mezclar(CIAN, 0.55, PANEL), edgecolor=CIAN,
               label="dentro: x1 = x2 = 1")
        b.set_xlabel("ŷ con corr 0.99")
        b.legend(loc="upper left")
        _titulo(b, "la predicción")

    aria = (f"Con correlación 0.99 la desviación de beta 1 pasa de {c['cita']['desv_beta1_0']} "
            f"a {c['cita']['desv_beta1_99']}; la predicción dentro de la nube casi no cambia "
            f"(desviación {c['cita']['desv_y_dentro_99']}), fuera sí "
            f"({c['cita']['desv_y_fuera_99']})")
    return _grafica(dibujar, aria, "Lo que cambia al reaprender", 5.2, filas=2)


# -------------------------------------------------- F8 · ml-c3-un-coeficiente ---
MUS_F8 = (0.0, 0.5, 2.0)
B_F8 = 1.0


def ml_c3_un_coeficiente():
    ml = gen.ml_lab()

    def dibujar(fig, ejes):
        for ax, pen, t in ((ejes[0], "l2", "ridge: + μβ²"), (ejes[1], "l1", "lasso: + μ|β|")):
            ml.dibujar_encoger_1d(vista="objetivo", b=B_F8, mus=MUS_F8, penalizacion=pen,
                                  ax=ax, tema="sitio")
            _titulo(ax, t)
            # μ = 0 es L_ent: la curva gruesa y continua; las otras, con trazo propio
            _trazos(ax, [f"objetivo-{m:g}" for m in MUS_F8], grosor=[3.6, 2, 2])
            manejadores, rotulos = ax.get_legend_handles_labels()
            rotulos = ["μ = 0: Lₑₙₜ" if r == "μ = 0" else r for r in rotulos]
            ax.legend(manejadores, rotulos, loc="upper center")

    umbral = 2 * B_F8
    aria = ("La pérdida de un coeficiente más el castigo, para μ = 0, 0.5 y 2, con la pendiente "
            "sin penalizar en 1: con ridge el mínimo se acerca a 0; con lasso se queda en 0 "
            f"desde μ = {umbral:g}")
    return _grafica(dibujar, aria, "Un coeficiente y su castigo", 5.2, filas=2)


# ------------------------------------------------- F9 · ml-c3-elipse-region ---

def ml_c3_elipse_region():
    cif = _cif()
    ml = gen.ml_lab()
    c = cif.cifras_c3_regiones()
    d, phi = cif.datos_regiones(), cif.phi_regiones()

    def dibujar(fig, ejes):
        for ax, pen, t in zip(ejes.ravel(), cif.PENALIZACIONES,
                              ("disco (ridge)", "diamante (lasso)", "red elástica, ρ = 0.5")):
            ml.dibujar_regiones(d, phi, pen, cif.D_REGIONES, ax=ax, tema="sitio")
            _titulo(ax, f"{t}: μ = {c['cita'][pen]['mu']}")
            ax.set_aspect("equal", adjustable="box")
            manejadores, rotulos = ax.get_legend_handles_labels()
            if ax.get_legend() is not None:
                ax.get_legend().remove()
        libre = ejes[1, 1]
        libre.axis("off")
        libre.legend(manejadores, rotulos, loc="center", frameon=True)

    q = c["cita"]
    aria = ("Curvas de nivel de L ent y la región Ω ≤ d con d = 1: el disco toca en "
            f"({q['l2']['beta1']}, {q['l2']['beta2']}); el diamante en su esquina, beta 1 = 0; "
            f"la elástica en ({q['elastica']['beta1']}, {q['elastica']['beta2']})")
    return _grafica(dibujar, aria, "Dónde toca la elipse", 5.6, filas=2, columnas=2)


# ------------------------------------------------- F10 · ml-c3-encoger-1d ---

def ml_c3_encoger_1d():
    ml = gen.ml_lab()

    def dibujar(fig, ax):
        ml.dibujar_encoger_1d(vista="solucion", mu=1.0, ax=ax, tema="sitio")
        ax.set_aspect("equal", adjustable="box")
        _trazos(ax, ["solucion-l2", "solucion-l1", "solucion-elastica"], grosor=2.4)
        lineas = {ln.get_gid(): ln for ln in ax.get_lines()}
        lineas["sin-regularizar"].set_linestyle((0, (1, 1.5)))
        ax.legend(*ax.get_legend_handles_labels())

    aria = ("Pendiente penalizada contra la sin penalizar, μ = 1: ridge es una recta de "
            "pendiente 1/2; lasso vale 0 entre −0.5 y 0.5")
    return _grafica(dibujar, aria, "Encoger o anular", 4.4)


# ------------------------------------------------- F11 · ml-c3-grado-12-mu ---

def ml_c3_grado_12_mu():
    cif = _cif()
    ml = gen.ml_lab()
    c = cif.cifras_c3_grado12()
    d, phi = cif.datos_entregas_curvas(), cif.phi_grado12()
    sel, curva = cif.seleccion_grado12()
    grande, medio, chico = cif.mus_paneles_grado12()
    q = c["cita"]

    def dibujar(fig, ejes):
        paneles = ((ejes[0, 0], chico, "C · μ = 10⁻⁶"),
                   (ejes[0, 1], medio, f"B · μ = {q['mu_medio']}"),
                   (ejes[1, 0], grande, "A · μ = 100"))
        for ax, mu, t in paneles:
            m = ml.ajustar(d, phi=phi, mu=mu, penalizacion="l2")
            ml.dibujar_proceso(d, ax=ax, tema="sitio")
            ventana = ax.get_xlim()
            ml.dibujar_ajuste({"f̂": m}, ventana=ventana, ax=ax, tema="sitio")
            ax.set_xlim(ventana)
            ax.set_ylim(0, 45)
            ax.set_ylabel("y")
            _titulo(ax, f"{t}\nR = {_num(ml.riesgo(m, d), 1)}")
            if ax.get_legend() is not None:
                ax.get_legend().remove()
        ejes[0, 0].legend(loc="lower right")
        ml.dibujar_cv(sel, R=curva, L_ent=curva, log=True,
                      anotar={grande: "A", medio: "B", chico: "C"}, ax=ejes[1, 1], tema="sitio")
        _titulo(ejes[1, 1], "la U contra μ\n(mismos datos)")
        ejes[1, 1].set_yscale("log")
        ejes[1, 1].set_ylabel("L, CV₅ y R")
        manejadores, rotulos = _rotular(*ejes[1, 1].get_legend_handles_labels())
        if ejes[1, 1].get_legend() is not None:
            ejes[1, 1].get_legend().remove()
        # la leyenda del cuarto panel, bajo la figura: qué es cada marca
        rotulos = [_rotulo_cv(r, "B") for r in rotulos]
        fig.legend(manejadores, rotulos, loc="lower center", ncol=2, frameon=True)

    aria = ("Las entregas de la clase 2 con el mismo polinomio de grado 12: con μ 100 la recta "
            f"de la media; con μ {q['mu_medio']} una curva cercana a f en el centro que cae en el "
            "borde derecho; con μ 10⁻⁶ la curva "
            "persigue los 36 puntos y oscila, como en la clase 2. R: "
            f"{q['R']['grande']}, {q['R']['medio']}, {q['R']['chico']}. Cuarto panel: contra μ, "
            f"L ent sube; CV 5 forma una U con fondo en μ = {q['mu_medio']}; R es enorme con μ "
            "chica, no es una U limpia en medio y sube con μ grande")
    return _grafica(dibujar, aria, "El grado 12 con tres μ", 7.4, filas=2, columnas=2,
                    rect=(0, 0.13, 1, 1))


# ------------------------------------------------- F12 · ml-c3-trayectorias ---

def ml_c3_trayectorias():
    cif = _cif()
    ml = gen.ml_lab()
    c = cif.cifras_c3_trayectorias()

    def dibujar(fig, ejes):
        for ax, pen, t in zip(ejes, ("l2", "l1", "elastica"),
                              ("ridge", "lasso", "red elástica, ρ = 0.5")):
            ml.dibujar_trayectorias(cif.tabla_trayectorias(pen), utiles=list(cif.UTILES),
                                    ax=ax, tema="sitio")
            _titulo(ax, t)
            _trazos(ax, [f"coef-{u}" for u in cif.UTILES])
            manejadores, rotulos = ax.get_legend_handles_labels()
            if ax.get_legend() is not None:
                ax.get_legend().remove()
        for ax in ejes[:-1]:
            ax.set_xlabel("")
        # la leyenda, bajo los tres paneles: en el de ridge tapaba x2 y las grises
        fig.legend(manejadores, rotulos, loc="lower center", ncol=6, frameon=True)

    aria = ("Coeficientes contra μ en estos datos, 5 útiles en color y 45 espurias en gris: "
            "ridge no apaga ninguno; lasso apaga las útiles entre μ = "
            f"{c['cita']['primera_util']} y {c['cita']['ultima_util']}; la elástica en medio")
    return _grafica(dibujar, aria, "Trayectorias de los coeficientes", 7.4, filas=3,
                    rect=(0, 0.05, 1, 1))


# ------------------------------------------------- F13 · ml-c3-ridge-colineal ---

def ml_c3_ridge_colineal():
    cif = _cif()
    ml = gen.ml_lab()
    c = cif.cifras_c3_ridge_colineal()
    t = cif.tablas_ridge_colineal()

    def dibujar(fig, ejes):
        for ax, k, tt in ((ejes[0], "sin", "sin penalizar"), (ejes[1], "ridge", "ridge, μ = 0.1")):
            ml.dibujar_beta_repetido(t[k], verdadero={"x1": 1.0, "x2": 1.0},
                                     columnas=("x1", "x2"), ax=ax, tema="sitio")
            ax.set_xlim(-1.5, 3.5)
            ax.set_ylim(-1.5, 3.5)
            ax.set_aspect("equal", adjustable="box")
            _promedio_en_rombo(ax)
            _titulo(ax, tt)
            if ax.get_legend() is not None:
                ax.get_legend().remove()

    q = c["cita"]
    aria = ("Con correlación 0.99: sin penalizar la nube es larga (desviación de beta 1 "
            f"{q['sin']['desv']}); con ridge, corta ({q['ridge']['desv']}) y un poco corrida")
    return _grafica(dibujar, aria, "Ridge calma la colinealidad", 3.2, columnas=2)


# ------------------------------------------------- F14 · ml-c3-estandarizar ---
MUS_F14 = tuple(float(m) for m in __import__("numpy").logspace(-2, 1, 40))


def ml_c3_estandarizar():
    cif = _cif()
    ml = gen.ml_lab()
    c = cif.cifras_c3_estandarizar()
    d = ml.caso(10)

    def dibujar(fig, ejes):
        for ax, phi, t in ((ejes[0], ml.columnas("x1", "x2"), "sin estandarizar"),
                           (ejes[1], ml.estandarizar(ml.columnas("x1", "x2")),
                            "estandarizando con entrenamiento")):
            tabla = ml.trayectorias(d, phi, "l1", MUS_F14)
            if t == "sin estandarizar":
                # la pendiente de x2 está en unidades × 10⁶: se dibuja × 10⁶ para verla
                tabla = tabla.copy()
                tabla.loc[tabla["coeficiente"] == "x2", "valor"] *= 1e6
                tabla.loc[tabla["coeficiente"] == "x2", "coeficiente"] = "10⁶ · β̂ de x2"
            nombres = sorted(tabla["coeficiente"].unique())
            ml.dibujar_trayectorias(tabla, utiles=nombres, ax=ax, tema="sitio")
            _titulo(ax, t)
            _trazos(ax, [f"coef-{n}" for n in nombres], grosor=2.4)
            ax.legend(*ax.get_legend_handles_labels())
        ejes[0].set_xlabel("")
        ejes[0].set_ylabel("coeficiente (x2: × 10⁶)")

    q = c["cita"]
    aria = ("Dos variables igual de útiles, x2 en unidades × 10⁶: sin estandarizar x1 se "
            f"apaga en μ = {q['sin_x1']} y x2 en {q['sin_x2']}; estandarizando, juntas, en "
            f"{q['con_x1']} y {q['con_x2']}")
    return _grafica(dibujar, aria, "Estandarizar antes de penalizar", 5.0, filas=2)


# ------------------------------------------------------ F15 · ml-c3-mu-cv ---

def ml_c3_mu_cv():
    cif = _cif()
    ml = gen.ml_lab()
    c = cif.cifras_c3_mu_cv()
    d = cif.datos_muchas()
    s = cif.selecciones_mu_cv()
    curvas = cif.curvas_mu_cv()     # conteos y R del reajuste con ent ∪ val
    nz = {mu: str(v) for mu, v in curvas["no_ceros"].items()}
    marcadas = {c["mu_min"], c["mu_un_ee"]}
    anotar = {mu: v for i, (mu, v) in enumerate(sorted(nz.items()))
              if i % 4 == 0 or mu in marcadas}

    def dibujar(fig, ax):
        ml.dibujar_cv(s["minimo"], R=curvas["R"], L_ent=c["L_ent"], benchmark=c["R_media"],
                      log=True, anotar=anotar, ax=ax, tema="sitio")
        ax.set_yscale("log")
        ax.set_ylabel("pérdida cuadrática")
        _titulo(ax, "50 variables, lasso: quién elige μ")
        manejadores, rotulos = ax.get_legend_handles_labels()
        rotulos = [_rotulo_cv(r) for r in rotulos]
        if ax.get_legend() is not None:
            ax.get_legend().remove()
        fig.legend(manejadores, rotulos, loc="lower center", ncol=3, frameon=True)

    q = c["cita"]
    aria = (f"L ent sube con μ; CV 5 mínima en μ = {q['mu_min']} con {q['no_ceros_min']} "
            "variables; la línea horizontal es el mínimo más un error estándar; de μ grande a "
            f"chica, el primer triángulo bajo esa línea es μ = {q['mu_un_ee']}, con "
            f"{q['no_ceros_un_ee']} variables; R en el elegido {q['R_un_ee']}")
    return _grafica(dibujar, aria, "Elegir μ con validación cruzada", 5.2,
                    rect=(0, 0.17, 1, 1))


# ---------------------------------------------- F16 · ml-c3-recta-de-apoyo ---

def ml_c3_recta_de_apoyo():
    cif = _cif()
    ml = gen.ml_lab()
    c = cif.cifras_c3_recta_apoyo()

    def dibujar(fig, ax):
        ml.dibujar_presupuesto(cif.datos_regiones(), cif.phi_regiones(), "l1",
                               cif.rejilla_presupuesto(), d_marcado=cif.D_MARCADO, ax=ax,
                               tema="sitio")
        _titulo(ax, "el mejor L ent con presupuesto d (lasso)")

    aria = ("La mejor pérdida de entrenamiento contra el presupuesto d baja y es convexa; en "
            f"d = {c['cita']['d']} la toca una recta de pendiente −{c['cita']['mu']}: ese es μ")
    return _grafica(dibujar, aria, "μ es la pendiente de apoyo", 3.8)


_RAPIDO = {
    "ml-c3-mismo-rmse": ml_c3_mismo_rmse,
    "ml-c3-benchmarks": ml_c3_benchmarks,
    "ml-c3-media-acumulada": ml_c3_media_acumulada,
    "ml-c3-fuentes-patologias": ml_c3_fuentes_patologias,
    "ml-c3-diana-beta": ml_c3_diana_beta,
    "ml-c3-interaccion-plano": ml_c3_interaccion_plano,
    "ml-c3-colineal-prediccion": ml_c3_colineal_prediccion,
    "ml-c3-un-coeficiente": ml_c3_un_coeficiente,
    "ml-c3-elipse-region": ml_c3_elipse_region,
    "ml-c3-encoger-1d": ml_c3_encoger_1d,
    "ml-c3-grado-12-mu": ml_c3_grado_12_mu,
    "ml-c3-trayectorias": ml_c3_trayectorias,
    "ml-c3-ridge-colineal": ml_c3_ridge_colineal,
    "ml-c3-estandarizar": ml_c3_estandarizar,
    "ml-c3-mu-cv": ml_c3_mu_cv,
    "ml-c3-recta-de-apoyo": ml_c3_recta_de_apoyo,
}
# --- fin tramo rapido ---


# --- tramo completo ---
_COMPLETO = {}
# --- fin tramo completo ---


FIGURAS_C3 = {**_RAPIDO, **_COMPLETO}
