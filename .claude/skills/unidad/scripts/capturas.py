#!/usr/bin/env python3
"""capturas.py — compuerta 5: capturas a 390 y 1280 px, con todos los <details> abiertos.

Uso (desde cualquier directorio; normalmente lo llama capturas.sh):
    capturas.py --salida DIR RUTA [RUTA ...]
    capturas.py --salida /tmp/cap juegos/mirar-todo-y-podar/minimax/ \
        course/7_juegos/_assets/jue-t-arbol.svg \
        "course/7_juegos/_assets/traza_arbol_t.html#alfa-beta-fila-12"

RUTA es una de:
  - una ruta del sitio construido («juegos/cuando-no-cabe/»): se sirve
    artifact/site/ por HTTP en un puerto libre y se abre <ruta>/index.html;
  - un .svg: se captura a su tamaño propio (escala 2) y dentro de un <img>
    a 390 px de ancho, como lo incrusta el sitio en un teléfono;
  - un .html autocontenido de _assets/ (con #fragmento opcional): por file://.

Por cada página: captura de página completa a 390x844 y 1280x800 (cambia con
--anchos), todos los <details> del artículo abiertos y MathJax terminado. Imprime una
línea por captura con scrollWidth (> ancho = scroll horizontal) y los
errores de consola o HTTP >= 400. Sale 1 si hubo scroll horizontal o errores.

Cada captura se corta además en franjas de <= 2000 px de alto (con 80 px de
traslape), <nombre>_<ancho>_fNN.png: son las que abre la lente Render, porque
una captura de 30 000 px no cabe en una lectura de imagen. SALIDA/inventario.tsv
lleva una fila por captura: página, ancho, figuras, tablas, fórmulas display,
details del artículo (pistas y respuestas, sin los del grafo de conexiones),
nº de franjas y sus nombres. Es el {{INVENTARIO}} de prompts/lente-render.md.
Requiere playwright (python3 -c "import playwright"); usa google-chrome si está.
Construye antes: raya build (ver referencias/verificacion.md).
"""
import argparse
import functools
import http.server
import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(subprocess.run(["git", "-C", str(Path(__file__).parent), "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
SITIO = RAIZ / "artifact/site"
FONDO = "#211033"   # tokens.color.surface del skin (ver test_skin.py)

# Solo los <details> del artículo (pistas, respuestas); los del marco del sitio
# (índice, contexto) se quedan como están, o la captura mide 30 000 px.
# Los del grafo de conexiones (raya-connection-preview) son del framework: ni se
# abren ni se cuentan.
DETALLES = "#raya-article details:not(.raya-connection-preview), body > details"
FRANJA, TRASLAPE = 2000, 80
CONTAR = """() => { const a = document.querySelector('#raya-article') || document.body;
  const n = s => a.querySelectorAll(s).length;
  return [n('.raya-numbered-object--figure'), n('table'),
          n('mjx-container[display="true"]'), n('details:not(.raya-connection-preview)')]; }"""
ABRIR = f"""() => {{ document.querySelectorAll('{DETALLES}').forEach(d => d.open = true); }}"""
ESPERAR_MATH = """async () => {
  const mj = window.MathJax;
  if (mj && mj.startup && mj.startup.promise) { try { await mj.startup.promise; } catch (e) {} }
  if (mj && mj.typesetPromise) { try { await mj.typesetPromise(); } catch (e) {} }
}"""


def slug(ruta):
    s = re.sub(r"[^A-Za-z0-9]+", "-", ruta.replace("course/", "")).strip("-")
    return s or "inicio"


def servidor():
    class Callado(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    h = functools.partial(Callado, directory=str(SITIO))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def franjas(png):
    """Corta png en franjas <= FRANJA px de alto; devuelve sus nombres."""
    from PIL import Image
    im = Image.open(png)
    w, h = im.size
    nombres, y, k = [], 0, 1
    while True:
        f = png.with_name(f"{png.stem}_f{k:02d}.png")
        im.crop((0, y, w, min(y + FRANJA, h))).save(f)
        nombres.append(f.name)
        if y + FRANJA >= h:
            return nombres
        y, k = y + FRANJA - TRASLAPE, k + 1


def tam_svg(p):
    t = p.read_text(encoding="utf-8")[:2000]
    w = re.search(r'<svg[^>]*\bwidth="([\d.]+)', t)
    h = re.search(r'<svg[^>]*\bheight="([\d.]+)', t)
    return (int(float(w.group(1))), int(float(h.group(1)))) if w and h else (600, 400)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--salida", required=True)
    ap.add_argument("--anchos", default="390x844,1280x800")
    ap.add_argument("rutas", nargs="+")
    a = ap.parse_args()
    salida = Path(a.salida)
    salida.mkdir(parents=True, exist_ok=True)
    tams = [tuple(map(int, t.split("x"))) for t in a.anchos.replace(" ", ",").split(",") if t]
    srv = None
    malas = 0
    inventario = ["pagina\tancho\tfiguras\ttablas\tformulas\tdetails\tn_franjas\tfranjas"]
    chrome = shutil.which("google-chrome")
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=chrome, args=["--no-sandbox"]) if chrome else pw.chromium.launch()
        for ruta in a.rutas:
            base, _, frag = ruta.partition("#")
            p = Path(base) if Path(base).is_absolute() else RAIZ / base
            if base.endswith(".svg"):
                if not p.is_file():
                    print(f"NO EXISTE {p}"); malas += 1; continue
                w, h = tam_svg(p)
                pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2)
                pg.goto(p.as_uri()); pg.wait_for_timeout(200)
                f = salida / f"{slug(base)}_propio.png"
                pg.screenshot(path=str(f)); pg.close()
                pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
                envoltura = salida / f".{slug(base)}_390.html"   # file:// no deja a about:blank leer el SVG
                envoltura.write_text(f'<body style="margin:0;padding:16px;background:{FONDO}">'
                                     f'<img src="{p.as_uri()}" style="max-width:100%;height:auto"></body>')
                pg.goto(envoltura.as_uri()); pg.wait_for_timeout(300)
                f2 = salida / f"{slug(base)}_390.png"
                pg.screenshot(path=str(f2), full_page=True); pg.close()
                envoltura.unlink()
                fr = franjas(f2)
                inventario.append(f"{base}\t390\t-\t-\t-\t-\t{len(fr)}\t{','.join(fr)}")
                print(f"svg {w}x{h}  {f}  {f2}")
                continue
            if base.endswith(".html"):
                if not p.is_file():
                    print(f"NO EXISTE {p}"); malas += 1; continue
                url = p.as_uri() + (f"#{frag}" if frag else "")
            else:
                idx = SITIO / base.strip("/") / "index.html"
                if not idx.is_file():
                    print(f"NO CONSTRUIDA {idx} (corre raya build)"); malas += 1; continue
                srv = srv or servidor()
                url = f"http://127.0.0.1:{srv.server_address[1]}/{base.strip('/')}/index.html" \
                      + (f"#{frag}" if frag else "")
            for w, h in tams:
                pg = b.new_page(viewport={"width": w, "height": h})
                errores = []
                pg.on("console", lambda m: errores.append(m.text)
                      if m.type == "error" and "status of 404" not in m.text else None)
                pg.on("pageerror", lambda e: errores.append(str(e)))
                pg.on("response", lambda r: errores.append(f"HTTP {r.status} {r.url}")
                     if r.status >= 400 and not r.url.endswith("favicon.ico") else None)
                pg.goto(url, wait_until="networkidle")
                pg.evaluate(ABRIR)
                pg.evaluate(ESPERAR_MATH)
                pg.wait_for_timeout(600)
                sw = pg.evaluate("document.documentElement.scrollWidth")
                n = pg.evaluate(f"document.querySelectorAll('{DETALLES}').length")
                cuenta = pg.evaluate(CONTAR)
                f = salida / f"{slug(ruta)}_{w}.png"
                pg.screenshot(path=str(f), full_page=True)
                fr = franjas(f)
                inventario.append("\t".join([ruta, str(w), *map(str, cuenta), str(len(fr)), ",".join(fr)]))
                mal = sw > w or errores
                malas += bool(mal)
                print(f"{'MAL' if mal else 'ok '} {w}px scrollWidth={sw} details={n} {f}"
                      + (f"  errores={errores[:5]}" if errores else ""))
                pg.close()
        b.close()
    if srv:
        srv.shutdown()
    (salida / "inventario.tsv").write_text("\n".join(inventario) + "\n", encoding="utf-8")
    print(f"inventario: {salida / 'inventario.tsv'}")
    return 1 if malas else 0


if __name__ == "__main__":
    sys.exit(main())
