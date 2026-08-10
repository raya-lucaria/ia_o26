"""Genera un panorama general y una linea del tiempo por seccion desde tools/hitos.json."""
import json
from pathlib import Path
from xml.sax.saxutils import escape

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "course/1_introduccion/2_historia_ia/_assets"
DATOS = RAIZ / "tools/hitos.json"

FONDO, TEXTO, SUAVE, LINEA = "#211033", "#f7f2ff", "#c8b9d8", "#78419e"
ACENTO, VERANO, INVIERNO = "#f04cff", "#ffd166", "#55ddff"
FUENTE = "system-ui, sans-serif"
ANCHO, MARGEN = 1200, 90

TRAMOS = {
    "mitos": "Imaginar la maquina",
    "inteligencia": "Que es la inteligencia",
    "arco-1": "El arco historico: 1936-1973",
    "arco-2": "El arco historico: 1980-2022",
    "boom": "Por que el boom",
    "actual": "Estado actual",
    "raices": "Otras raices",
    "sociedad": "IA y sociedad",
}


def anio_texto(a):
    return str(a) if a > 0 else f"{abs(a)} a.C."


def envolver(texto, ancho=20):
    """Parte una etiqueta en hasta dos lineas sin cortar palabras."""
    palabras, lineas, actual = texto.split(), [], ""
    for p in palabras:
        if len(actual) + len(p) + 1 <= ancho:
            actual = f"{actual} {p}".strip()
        else:
            lineas.append(actual)
            actual = p
        if len(lineas) == 2:
            break
    if actual and len(lineas) < 2:
        lineas.append(actual)
    return lineas[:2]


def marco(alto, aria):
    # width/height explicitos (ademas de viewBox): sin ellos, el <svg> no
    # tiene tamano intrinseco y el navegador lo incrusta con el tamano por
    # omision de un elemento reemplazado (~300x150 CSS px) en vez de llenar
    # el contenedor de la figura -- el diagrama se ve minusculo e ilegible
    # (encontrado en la revision visual de la Tarea 18).
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ANCHO}" height="{alto}" '
        f'viewBox="0 0 {ANCHO} {alto}" role="img" aria-label="{escape(aria)}">'
        f'<rect x="0" y="0" width="{ANCHO}" height="{alto}" rx="16" fill="{FONDO}"/>'
    )


def dibuja(hitos, bandas, titulo, aria, alto=400):
    hitos = sorted(hitos, key=lambda h: h["anio"])
    minimo, maximo = hitos[0]["anio"], hitos[-1]["anio"]
    if minimo == maximo:
        minimo, maximo = minimo - 1, maximo + 1
    x0, x1 = MARGEN, ANCHO - MARGEN
    eje = alto // 2 + 20

    def x_de(anio):
        return x0 + (anio - minimo) / (maximo - minimo) * (x1 - x0)

    p = [marco(alto, aria)]
    p.append(
        f'<text x="{MARGEN}" y="34" fill="{TEXTO}" font-family="{FUENTE}" '
        f'font-size="17" font-weight="600">{escape(titulo)}</text>'
    )

    for b in bandas:
        if b["hasta"] < minimo or b["desde"] > maximo:
            continue
        bx0, bx1 = x_de(max(b["desde"], minimo)), x_de(min(b["hasta"], maximo))
        color = VERANO if b["tipo"] == "verano" else INVIERNO
        p.append(
            f'<rect x="{bx0:.1f}" y="{eje - 14}" width="{max(bx1 - bx0, 2):.1f}" '
            f'height="28" fill="{color}" opacity="0.16"/>'
        )
        if bx1 - bx0 > 52:
            p.append(
                f'<text x="{(bx0 + bx1) / 2:.1f}" y="{eje + 32}" fill="{color}" '
                f'font-family="{FUENTE}" font-size="11" text-anchor="middle" '
                f'opacity="0.85">{escape(b["etiqueta"])}</text>'
            )

    p.append(
        f'<line x1="{x0}" y1="{eje}" x2="{x1}" y2="{eje}" '
        f'stroke="{LINEA}" stroke-width="2"/>'
    )

    # Cuatro niveles alternados: dos arriba y dos abajo. Asi dos hitos vecinos
    # nunca comparten nivel y sus etiquetas no pueden encimarse.
    NIVELES = [(-1, 0), (1, 0), (-1, 1), (1, 1)]
    for i, h in enumerate(hitos):
        x = x_de(h["anio"])
        lado, tier = NIVELES[i % 4]
        salto = 48 + tier * 46
        p.append(f'<circle cx="{x:.1f}" cy="{eje}" r="5" fill="{ACENTO}"/>')
        y_anio = eje + lado * (salto + 14)
        p.append(
            f'<line x1="{x:.1f}" y1="{eje + lado * 8}" x2="{x:.1f}" '
            f'y2="{eje + lado * salto:.1f}" stroke="{LINEA}" stroke-width="1"/>'
        )
        p.append(
            f'<text x="{x:.1f}" y="{y_anio}" fill="{TEXTO}" font-family="{FUENTE}" '
            f'font-size="13" font-weight="600" text-anchor="middle">'
            f'{anio_texto(h["anio"])}</text>'
        )
        for j, linea in enumerate(envolver(h["etiqueta"])):
            p.append(
                f'<text x="{x:.1f}" y="{y_anio + 15 + j * 13}" fill="{SUAVE}" '
                f'font-family="{FUENTE}" font-size="11" text-anchor="middle">'
                f'{escape(linea)}</text>'
            )
    p.append("</svg>")
    return "".join(p)


def main():
    datos = json.loads(DATOS.read_text(encoding="utf-8"))
    hitos, bandas = datos["hitos"], datos["bandas"]
    ASSETS.mkdir(parents=True, exist_ok=True)
    generados = []

    anclas = [h for h in hitos if h.get("ancla")]
    (ASSETS / "v1-panorama.svg").write_text(
        dibuja(anclas, bandas, "Los veranos y los inviernos de la inteligencia artificial",
               "Panorama de la historia de la inteligencia artificial con los veranos "
               "en amarillo y los inviernos en azul", alto=400),
        encoding="utf-8")
    generados.append("v1-panorama.svg")

    for slug, titulo in TRAMOS.items():
        del_tramo = [h for h in hitos if h["tramo"] == slug]
        if not del_tramo:
            raise SystemExit(f"el tramo '{slug}' no tiene hitos en hitos.json")
        alto = 400
        nombre = f"v1-tramo-{slug}.svg"
        (ASSETS / nombre).write_text(
            dibuja(del_tramo, bandas, titulo, f"Linea del tiempo: {titulo}", alto=alto),
            encoding="utf-8")
        generados.append(nombre)

    for nombre in generados:
        print(f"  {nombre}")
    print(f"generados {len(generados)} archivos en {ASSETS}")


if __name__ == "__main__":
    main()
