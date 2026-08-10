"""Genera el diagrama de dispersion del computo de entrenamiento desde
tools/computo.json (analogo a gen_timeline.py con hitos.json).

Hasta esta tarea, v9-computo.svg estaba escrito a mano con las mismas seis
cifras que trae computo.json, y CREDITOS.md afirmaba (falsamente) que se
"genero a partir de datos de tools/computo.json". Este script hace que esa
afirmacion sea cierta: quien actualice el JSON corre este script y el
diagrama cambia con el.
"""
import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "course/1_introduccion/2_historia_ia/_assets"
DATOS = RAIZ / "tools/computo.json"
DESTINO = ASSETS / "v9-computo.svg"

FONDO, TEXTO, SUAVE, LINEA = "#211033", "#f7f2ff", "#c8b9d8", "#78419e"
ACENTO = "#f04cff"
COLORES_PUNTO = ["#a8ff5a", "#55ddff", "#ffd166"]
FUENTE = "system-ui, sans-serif"
ANCHO, ALTO = 1000, 560
X0, X1 = 90, 950
Y0, Y1 = 50, 460
ARIA = "Dispersion logaritmica del computo de entrenamiento de modelos de IA por anio, en FLOP"


def marco():
    # width/height explicitos ademas de viewBox: el sitio incrusta estos SVG
    # con <img>, que sin tamano intrinseco cae al tamano por omision de un
    # elemento reemplazado (~300x150 CSS px). Misma convencion que
    # gen_timeline.py (Tarea 18).
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ANCHO}" height="{ALTO}" '
        f'viewBox="0 0 {ANCHO} {ALTO}" role="img" aria-label="{escape(ARIA)}">'
        f'<rect x="0" y="0" width="{ANCHO}" height="{ALTO}" rx="16" fill="{FONDO}"/>'
    )


def regresion(pares):
    """Minimos cuadrados de y sobre x para una lista de (x, y)."""
    n = len(pares)
    mx = sum(x for x, _ in pares) / n
    my = sum(y for _, y in pares) / n
    num = sum((x - mx) * (y - my) for x, y in pares)
    den = sum((x - mx) ** 2 for x, _ in pares)
    b = num / den
    a = my - b * mx
    return a, b


def dibuja(modelos, titulo, fuente_texto, consultado):
    exp = [math.log10(m["flop"]) for m in modelos]
    anios = [m["anio"] for m in modelos]
    exp_min, exp_max = math.floor(min(exp)), math.ceil(max(exp))
    anio0, anio1 = min(anios) - 1, max(anios) + 1

    def x_de(anio):
        return X0 + (anio - anio0) / (anio1 - anio0) * (X1 - X0)

    def y_de(e):
        return Y1 - (e - exp_min) / (exp_max - exp_min) * (Y1 - Y0)

    p = [marco()]
    p.append(
        f'<text x="{X0}" y="34" fill="{TEXTO}" font-family="{FUENTE}" '
        f'font-size="17" font-weight="600">{escape(titulo)}</text>'
    )
    p.append(f'<line x1="{X0}" y1="{Y1}" x2="{X1}" y2="{Y1}" stroke="{LINEA}" stroke-width="2"/>')
    p.append(f'<line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1}" stroke="{LINEA}" stroke-width="2"/>')

    for e in range(exp_min, exp_max + 1):
        y = y_de(e)
        p.append(
            f'<line x1="{X0}" y1="{y:.1f}" x2="{X1}" y2="{y:.1f}" '
            f'stroke="{LINEA}" stroke-width="0.5" opacity="0.35"/>'
        )
        p.append(
            f'<text x="{X0 - 12}" y="{y + 4:.1f}" fill="{SUAVE}" font-family="{FUENTE}" '
            f'font-size="12" text-anchor="end">10^{e}</text>'
        )
    p.append(
        f'<text x="30" y="{(Y0 + Y1) / 2 + 5:.1f}" fill="{SUAVE}" font-family="{FUENTE}" '
        f'font-size="12" text-anchor="middle" transform="rotate(-90 30 {(Y0 + Y1) / 2 + 5:.1f})">'
        f"FLOP de entrenamiento (escala log)</text>"
    )

    for anio in sorted(set(anios)):
        x = x_de(anio)
        p.append(f'<line x1="{x:.1f}" y1="{Y1}" x2="{x:.1f}" y2="{Y1 + 8}" stroke="{LINEA}" stroke-width="1"/>')
        p.append(
            f'<text x="{x:.1f}" y="{Y1 + 26}" fill="{SUAVE}" font-family="{FUENTE}" '
            f'font-size="12" text-anchor="middle">{anio}</text>'
        )

    # Linea de tendencia: regresion de minimos cuadrados del exponente sobre
    # el anio, extendida al ancho de la grafica (no una cifra inventada: se
    # deriva de los mismos puntos que se grafican).
    a, b = regresion(list(zip(anios, exp)))
    p.append(
        f'<line x1="{x_de(anio0):.1f}" y1="{y_de(a + b * anio0):.1f}" '
        f'x2="{x_de(anio1):.1f}" y2="{y_de(a + b * anio1):.1f}" '
        f'stroke="{ACENTO}" stroke-width="1.5" stroke-dasharray="6 5" opacity="0.55"/>'
    )

    # Puntos, agrupados por anio para que las etiquetas de un mismo anio se
    # separen hacia afuera del par en vez de encimarse. Primero se calculan
    # todas las posiciones (circulo + bloque de etiqueta); las colisiones
    # horizontales entre puntos de anios distintos se resuelven despues.
    por_anio = {}
    for i, m in enumerate(modelos):
        por_anio.setdefault(m["anio"], []).append((i, m))

    circulos = []
    etiquetas = []
    for anio, grupo in por_anio.items():
        # Mayor FLOP primero: a igual anio, el punto de mayor computo cae mas
        # arriba en pixeles (escala log invertida), asi que "primera mitad"
        # y "arriba en pantalla" coinciden.
        grupo = sorted(grupo, key=lambda im: im[1]["flop"], reverse=True)
        n = len(grupo)
        mitad = (n + 1) // 2
        puntos = [(i, m, x_de(m["anio"]), y_de(math.log10(m["flop"]))) for i, m in grupo]
        y_arriba = min(y for *_, y in puntos)
        y_abajo = max(y for *_, y in puntos)

        for pos, (i, m, x, y) in enumerate(puntos):
            color = COLORES_PUNTO[i % len(COLORES_PUNTO)]
            circulos.append((x, y, color))
            # Las etiquetas de un mismo anio se apilan hacia afuera del par
            # (una arriba del punto mas alto, otra abajo del mas bajo) para
            # que ninguna cruce el punto vecino.
            if pos < mitad:
                nivel = mitad - pos
                y_valor = y_arriba - 19 - (nivel - 1) * 44
                y_nombre = y_valor - 15
            else:
                nivel = pos - mitad + 1
                y_nombre = y_abajo + 19 + (nivel - 1) * 44
                y_valor = y_nombre + 15
            etiquetas.append({
                "x": x, "y_nombre": y_nombre, "y_valor": y_valor,
                "nombre": m["modelo"], "valor": f'{m["flop_texto"]} FLOP',
                "anchor": "middle",
            })

    # Separacion horizontal: dos puntos de anios distintos pueden caer cerca
    # en x con bloques de etiqueta a una altura parecida (le paso a PaLM 540B
    # y GPT-4 con anchor="middle": sus textos se encimaban). Si dos bloques
    # vecinos en x estan a menos de UMBRAL_X y sus rangos verticales se
    # traslapan, el de la izquierda se ancla a su derecha (crece hacia la
    # izquierda) y el de la derecha se ancla a su izquierda (crece hacia la
    # derecha), alejandose uno del otro.
    # Se comparan TODOS los pares, no solo vecinos consecutivos en x: dos
    # bloques pueden colisionar sin ser adyacentes en la lista ordenada
    # cuando un tercer punto se interpone en x sin traslaparse en y con
    # ninguno de los dos (le paso a PaLM 540B / GPT-4: Gemini 1.0 Ultra, a la
    # misma x que GPT-4, quedaba entre ambos en el orden y ocultaba la
    # colision real).
    UMBRAL_X = 150
    etiquetas.sort(key=lambda e: e["x"])
    for idx, izq in enumerate(etiquetas):
        for der in etiquetas[idx + 1:]:
            if der["x"] - izq["x"] >= UMBRAL_X:
                continue
            rango_izq = (min(izq["y_nombre"], izq["y_valor"]) - 8, max(izq["y_nombre"], izq["y_valor"]) + 8)
            rango_der = (min(der["y_nombre"], der["y_valor"]) - 8, max(der["y_nombre"], der["y_valor"]) + 8)
            if rango_izq[0] > rango_der[1] or rango_der[0] > rango_izq[1]:
                continue  # no se traslapan verticalmente, no hace falta separar
            izq["anchor"], izq["dx"] = "end", -10
            der["anchor"], der["dx"] = "start", 10

    for x, y, color in circulos:
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{color}"/>')
    for e in etiquetas:
        tx = e["x"] + e.get("dx", 0)
        p.append(
            f'<text x="{tx:.1f}" y="{e["y_nombre"]:.1f}" fill="{TEXTO}" font-family="{FUENTE}" '
            f'font-size="13" font-weight="600" text-anchor="{e["anchor"]}">{escape(e["nombre"])}</text>'
        )
        p.append(
            f'<text x="{tx:.1f}" y="{e["y_valor"]:.1f}" fill="{SUAVE}" font-family="{FUENTE}" '
            f'font-size="11" text-anchor="{e["anchor"]}">{escape(e["valor"])}</text>'
        )

    p.append(
        f'<text x="{X0}" y="{ALTO - 20}" fill="{SUAVE}" font-family="{FUENTE}" font-size="11">'
        f"{escape(fuente_texto)}. Consultado el {escape(consultado)}.</text>"
    )
    p.append("</svg>")
    return "".join(p)


def main():
    datos = json.loads(DATOS.read_text(encoding="utf-8"))
    svg = dibuja(
        datos["modelos"],
        "El computo de entrenamiento crece exponencialmente",
        datos["fuente"],
        datos["consultado"],
    )
    ASSETS.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(svg, encoding="utf-8")
    print(f"{DESTINO.name}  ({DESTINO.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
