"""Captura la vista previa del generador de texto de la unidad 8.

course/8_markov/_assets/generador_texto.html es el interactivo de la clase
8.1 (GENERAR con memoria h sobre el Quijote). La página que lo anuncia lo
hace con una figura: una captura del interactivo a media generación que lo
abre al pulsarla, en el mismo estado (fragmento #h=2&semilla=2034&...).

La captura no se dibuja: se toma de la página misma con Chrome sin interfaz
(Playwright), así que se ve exactamente como lo que abre el alumno. Por eso
este script NO corre en CI ni lo corre la suite: un PNG capturado depende de
las fuentes de la máquina y no es reproducible byte a byte. Lo que ata la
captura al interactivo es la huella del HTML que escribe en
tools/vista_generador.json: tools/test_generador_markov.py falla si
generador_texto.html cambió desde la última captura (por ejemplo, porque
gen_generador_markov.py reescribió sus tablas). Entonces hay que volver a
correr:

    uv run --python 3.12 --with playwright --with pillow \
        python tools/gen_vista_generador.py

Antes de capturar abre la página y exige que la autoprueba diga «ok» (el
texto que escribe el JS es el de markov.generar): si no, sale con error y no
escribe nada. Ese es también el chequeo en Chrome de la reproducibilidad, que
la suite no puede hacer sin navegador.

Necesita Chrome instalado (usa /usr/bin/google-chrome, no el Chromium de
Playwright). La captura se reduce a 256 colores, como gen_vistas_traza.py.
"""
import hashlib
import json
import shutil
import sys
from io import BytesIO
from pathlib import Path

from unidades import ASSETS_MARKOV

RAIZ = Path(__file__).resolve().parent.parent
HTML = ASSETS_MARKOV / "generador_texto.html"
HUELLA = RAIZ / "tools/vista_generador.json"
ANCHO, ALTO = 1280, 900

# (archivo, fragmento). Memoria 2 con la semilla de la página, a media
# generación (148 de 198 símbolos): el texto ya tiene palabras, y en el paso
# (contexto «ce») sale «s», el tercero más probable, con u = 0.715 a media
# fila: se ven la fila, el resto y dónde cae u en la suma acumulada.
VISTA = ("mkv-c1-generador.png", "h=2&semilla=2034&largo=200&paso=148")


def huella_html():
    return hashlib.sha256(HTML.read_bytes()).hexdigest()


# Colores planos del interactivo (su :root, copiado del skin, y los tonos de
# la fila acumulada). El octree los aproxima; aquí vuelven al valor exacto.
PALETA = ["#12061f", "#211033", "#f7f2ff", "#c8b9d8", "#f04cff", "#42164f",
          "#78419e", "#a8ff5a", "#ffd166", "#55ddff", "#a273d6", "#3a2255",
          "#4d2d6c", "#6a4594"]


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

    archivo, fragmento = VISTA
    with sync_playwright() as pw:
        navegador = pw.chromium.launch(executable_path=_navegador())
        pagina = navegador.new_page(viewport={"width": ANCHO, "height": ALTO},
                                    device_scale_factor=1, reduced_motion="reduce")
        errores = []
        pagina.on("pageerror", lambda e: errores.append(str(e)))
        pagina.goto(f"{HTML.as_uri()}#{fragmento}")
        pagina.wait_for_load_state("load")
        pagina.wait_for_timeout(400)
        autoprueba = pagina.inner_text("#autoprueba")
        if errores or not autoprueba.startswith("autoprueba: ok"):
            navegador.close()
            sys.exit(f"la autoprueba no dice ok: {autoprueba!r} {errores}")
        print(autoprueba)
        # hasta el borde inferior de los dos paneles de la reja, con margen
        fondo = pagina.evaluate(
            "Math.max(...[...document.querySelectorAll('.reja .panel')]"
            ".map(e => e.getBoundingClientRect().bottom))")
        alto = min(ALTO, int(fondo) + 10)
        png = pagina.screenshot(clip={"x": 0, "y": 0, "width": ANCHO, "height": alto})
        navegador.close()
    img = Image.open(BytesIO(png)).convert("RGB").quantize(
        colors=256, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.NONE)
    _ajustar_a_la_paleta(img)
    img.save(ASSETS_MARKOV / archivo, optimize=True)
    print(f"{archivo}: {ANCHO}×{alto}")

    HUELLA.write_text(json.dumps(
        {"html": str(HTML.relative_to(RAIZ)), "sha256": huella_html(),
         "vista": {"archivo": archivo, "fragmento": fragmento}},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    capturar()
