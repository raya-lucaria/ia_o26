"""Captura una vista previa de cada animación de la traza de la unidad 7.

course/7_juegos/_assets/traza_arbol_t.html es la animación renglón por
renglón: el árbol, el pseudocódigo con la línea que corre y la pila de
llamadas. Las páginas la enlazaban con una sola línea de texto y se perdía en
la prosa. Ahora cada página de algoritmo (y el anexo B_animaciones.md) la
anuncia con una figura: una captura de la animación, en un paso que se ve
algo, que abre la animación al pulsarla.

Las capturas no se dibujan: se toman de la página misma con Chrome sin
interfaz (Playwright), así que se ven exactamente como lo que abre el
alumno. Por eso este script NO corre en CI ni lo corre la suite: un PNG
capturado depende de las fuentes de la máquina y no es reproducible byte a
byte. Lo que ata cada captura a la animación es la huella del HTML que
escribe en tools/vistas_traza.json: tools/test_vistas_traza.py falla si
traza_arbol_t.html cambió desde la última captura (por ejemplo, porque
gen_traza_web.py reescribió sus pasos). Entonces hay que volver a correr:

    uv run --python 3.12 --with playwright --with pillow \
        python tools/gen_vistas_traza.py

Necesita Chrome instalado (usa /usr/bin/google-chrome, no el Chromium de
Playwright). Las capturas se reducen a 256 colores para que pesen poco (unos
70 KB cada una en vez de 200): el fondo es plano y el texto, de pocos tonos.
"""
import hashlib
import json
import shutil
import sys
from io import BytesIO
from pathlib import Path

from unidades import ASSETS_JUEGOS

RAIZ = Path(__file__).resolve().parent.parent
HTML = ASSETS_JUEGOS / "traza_arbol_t.html"
HUELLA = RAIZ / "tools/vistas_traza.json"
ANCHO, ALTO = 1280, 900

# (archivo, fragmento de la animación). El fragmento elige el paso: uno en
# que la línea resaltada, la pila y el árbol cuentan algo.
VISTAS = [
    ("jue-anim-minimax.png", "minimax-fila-12"),      # pila R›C›C2, a media ejecución
    ("jue-anim-azar.png", "azar-fila-6"),             # C, de azar, empieza a sumar
    ("jue-anim-alfa-beta.png", "alfa-beta-fila-12"),  # el corte beta de C2
    ("jue-anim-corte.png", "corte-fila-8"),           # C1 y C2 se estiman con EVAL
    ("jue-anim-iterativa.png", "iterativa-fila-10"),  # d = 2 empieza por izq
]


def huella_html():
    return hashlib.sha256(HTML.read_bytes()).hexdigest()


# Colores planos de la animación (su :root, copiado del skin). El octree los
# aproxima a una o dos unidades; aquí vuelven al valor exacto, para que el
# fondo de la captura sea el mismo --page que el de la página.
PALETA = ["#12061f", "#211033", "#f7f2ff", "#c8b9d8", "#f04cff", "#42164f",
          "#78419e", "#55ddff", "#ffd166", "#a8ff5a"]


def _ajustar_a_la_paleta(img, tolerancia=4):
    plana = img.getpalette()
    exactos = [tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in PALETA]
    for k in range(len(plana) // 3):
        actual = plana[3 * k:3 * k + 3]
        for e in exactos:
            if max(abs(a - b) for a, b in zip(actual, e)) <= tolerancia:
                plana[3 * k:3 * k + 3] = e
                break
    img.putpalette(plana)


def _navegador():
    for nombre in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        if shutil.which(nombre):
            return shutil.which(nombre)
    sys.exit("No hay Chrome ni Chromium: hace falta para capturar.")


def capturar():
    from PIL import Image
    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        navegador = pw.chromium.launch(executable_path=_navegador())
        pagina = navegador.new_page(viewport={"width": ANCHO, "height": ALTO},
                                    device_scale_factor=1, reduced_motion="reduce")
        for archivo, fragmento in VISTAS:
            pagina.goto(f"{HTML.as_uri()}#{fragmento}")
            pagina.wait_for_load_state("load")
            pagina.wait_for_timeout(400)
            # hasta el borde inferior del panel más bajo, con margen
            fondo = pagina.evaluate(
                "Math.max(...[...document.querySelectorAll('.reja .panel, .reja .frase')]"
                ".map(e => e.getBoundingClientRect().bottom))")
            alto = min(ALTO, int(fondo) + 16)
            png = pagina.screenshot(clip={"x": 0, "y": 0, "width": ANCHO, "height": alto})
            # FASTOCTREE y no el corte por mediana de omisión: ése corría el
            # cian de MAX hacia verde y apagaba el amarillo de MIN
            img = Image.open(BytesIO(png)).convert("RGB").quantize(
                colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
            _ajustar_a_la_paleta(img)
            img.save(ASSETS_JUEGOS / archivo, optimize=True)
            print(f"{archivo}: {ANCHO}×{alto}")
        navegador.close()

    HUELLA.write_text(json.dumps(
        {"html": "course/7_juegos/_assets/traza_arbol_t.html",
         "sha256": huella_html(),
         "vistas": [{"archivo": a, "fragmento": f} for a, f in VISTAS]},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    capturar()
