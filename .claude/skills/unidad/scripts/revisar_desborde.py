#!/usr/bin/env python3
"""revisar_desborde.py — compuerta 5 medida: lo que se rompe a 390 px sin que validate lo vea.

Uso:
    revisar_desborde.py juegos/mirar-todo-y-podar/minimax/ juegos/notacion/
    revisar_desborde.py --unidad juegos/                 # todas las páginas bajo artifact/site/juegos/
    revisar_desborde.py --en-vivo --unidad juegos/       # contra https://rayalucaria.org/ia_o26/
    revisar_desborde.py --ancho 360 juegos/cuando-no-cabe/
    revisar_desborde.py --sitio /otra/copia/artifact/site juegos/

Por página, a 390 px (o --ancho), con los <details> del artículo abiertos:
  - SCROLL     la página entera tiene scroll horizontal (scrollWidth > ancho);
  - FUERA      un elemento del artículo se sale de la pantalla sin estar dentro
               de un contenedor con scroll propio;
  - FORMULA    una fórmula (mjx-container) más ancha que su bloque, sin
               contenedor con scroll que la recoja;
  - TABLA      un tramo de >= 4 letras partido entre renglones dentro de una
               celda (cortar justo tras un guion o una raya no cuenta), o una fórmula que se sale de su celda;
  - MATHERR    MathJax no pudo componer una fórmula (\\boldsymbol y similares).
Una tabla o figura ancha con scroll propio NO es hallazgo (es el diseño, ver
referencias/figuras.md), pero se lista como
  - AVISO      contenedor con scroll horizontal propio: selector, ancho visible
               vs total y qué tiene dentro (una tabla de 7 columnas cuyo scroll
               esconde justo las columnas a llenar solo se ve así).
La lente Render mira cada AVISO en su franja. Los avisos no cambian el código
de salida. Sale 1 si hay hallazgos. Requiere playwright.
Local: construye antes con raya build. Salida solo a stdout.
"""
import argparse
import functools
import http.server
import shutil
import subprocess
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

RAIZ = Path(subprocess.run(["git", "-C", str(Path(__file__).parent), "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
SITIO = RAIZ / "artifact/site"
EN_VIVO = "https://rayalucaria.org/ia_o26/"

JS = r"""
() => {
  const art = document.querySelector('#raya-article') || document.body;
  art.querySelectorAll('details').forEach(d => d.open = true);
  const de = document.documentElement, W = de.clientWidth, h = [];
  const conScroll = el => { for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) {
      if (['auto', 'scroll'].includes(getComputedStyle(p).overflowX) && p.scrollWidth > p.clientWidth - 1) return true; }
    return false; };
  const txt = el => (el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 60);
  if (de.scrollWidth > W) h.push(['SCROLL', `scrollWidth=${de.scrollWidth} > ${W}`]);
  const fuera = new Set();
  for (const el of art.querySelectorAll('*')) {
    const b = el.getBoundingClientRect();
    if (b.width > 0 && b.right > W + 1 && !conScroll(el)) {
      if (![...fuera].some(f => f.contains(el))) fuera.add(el);
    }
  }
  [...fuera].slice(0, 10).forEach(el => h.push(['FUERA', `<${el.tagName.toLowerCase()} class="${el.className}"> right=${Math.round(el.getBoundingClientRect().right)}: ${txt(el)}`]));
  for (const mj of art.querySelectorAll('mjx-container')) {
    if (mj.closest('td,th')) continue;
    let blo = mj.parentElement;
    while (blo && getComputedStyle(blo).display.startsWith('inline')) blo = blo.parentElement;
    const mw = mj.getBoundingClientRect().width, bw = blo ? blo.clientWidth : W;
    const dentro = mj.scrollWidth > mj.clientWidth + 1 && ['auto', 'scroll'].includes(getComputedStyle(mj).overflowX);
    if (mw > bw + 1 && !conScroll(mj) && !dentro) h.push(['FORMULA', `${Math.round(mw)}px en bloque de ${bw}px: ${txt(mj)}`]);
  }
  const rng = document.createRange();
  art.querySelectorAll('table').forEach((t, i) => {
    const malas = new Set();
    for (const c of t.querySelectorAll('td,th')) {
      const cb = c.getBoundingClientRect();
      const tw = document.createTreeWalker(c, NodeFilter.SHOW_TEXT); let x;
      while ((x = tw.nextNode())) {
        if (x.parentElement.closest('mjx-container')) continue;
        const re = /[^\s\-\u2010-\u2014\/]{4,}/g; let m;   // cortar tras guion o raya es legítimo
        while ((m = re.exec(x.textContent))) {
          rng.setStart(x, m.index); rng.setEnd(x, m.index + m[0].length);
          const tops = new Set([...rng.getClientRects()].filter(q => q.width > 0).map(q => Math.round(q.top)));
          if (tops.size > 1) malas.add(m[0]);
        }
      }
      c.querySelectorAll('mjx-container').forEach(mj => {
        if (mj.getBoundingClientRect().right > cb.right + 2) malas.add('fórmula fuera de su celda: ' + txt(mj)); });
    }
    if (malas.size) h.push(['TABLA', `tabla ${i + 1}: ${[...malas].slice(0, 6).join(' | ')}`]);
  });
  art.querySelectorAll('mjx-merror, [data-mjx-error]').forEach(e =>
    h.push(['MATHERR', e.getAttribute('data-mjx-error') || txt(e)]));
  const av = [], vistos = new Set();
  for (const el of art.querySelectorAll('*')) {
    if (!['auto', 'scroll'].includes(getComputedStyle(el).overflowX) || el.scrollWidth <= el.clientWidth + 1) continue;
    if (el.tagName.startsWith('MJX') || el.closest('mjx-container')) continue;  // fórmulas: ya las mide FORMULA
    if ([...vistos].some(v => v.contains(el))) continue;
    vistos.add(el);
    const tb = el.querySelector('table') || (el.tagName === 'TABLE' ? el : null);
    const obj = el.closest('.raya-numbered-object, .raya-static-environment');
    const tit = obj ? txt(obj.querySelector('.raya-numbered-object-heading, .raya-static-environment-heading') || obj) : '';
    const que = tb ? `tabla de ${tb.rows[0] ? tb.rows[0].cells.length : '?'} columnas` :
                el.querySelector('img,svg') ? 'figura' : el.tagName === 'PRE' || el.querySelector('pre') ? 'código' : 'otro';
    const sel = el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') +
                (typeof el.className === 'string' && el.className ? '.' + el.className.trim().split(/\s+/).join('.') : '');
    av.push(['AVISO', `${que}, visible ${el.clientWidth}px de ${el.scrollWidth}px: ${sel}${tit ? ' · ' + tit : ''}`]);
  }
  return [h, av];
}
"""


def servidor():
    class Callado(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Callado, directory=str(SITIO)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ancho", type=int, default=390)
    ap.add_argument("--en-vivo", action="store_true")
    ap.add_argument("--sitio", type=Path, help="otro artifact/site (por omisión el del repo)")
    ap.add_argument("--unidad", help="prefijo del sitio, p. ej. juegos/ (todas sus páginas construidas)")
    ap.add_argument("rutas", nargs="*")
    a = ap.parse_args()
    global SITIO
    SITIO = a.sitio.resolve() if a.sitio else SITIO
    rutas = [r.strip("/") + "/" for r in a.rutas]
    if a.unidad:
        base = SITIO / a.unidad.strip("/")
        if not base.is_dir():
            sys.exit(f"no está construida: {base} (corre raya build)")
        rutas += sorted(str(p.parent.relative_to(SITIO)) + "/" for p in base.rglob("index.html"))
    if not rutas:
        ap.error("da al menos una ruta o --unidad")
    if a.en_vivo:
        raiz = EN_VIVO
    else:
        faltan = [r for r in rutas if not (SITIO / r / "index.html").is_file()]
        if faltan:
            sys.exit(f"no construidas: {faltan} (corre raya build)")
        srv = servidor()
        raiz = f"http://127.0.0.1:{srv.server_address[1]}/"
    total = n_avisos = 0
    chrome = shutil.which("google-chrome")
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=chrome, args=["--no-sandbox"]) if chrome else pw.chromium.launch()
        pg = b.new_page(viewport={"width": a.ancho, "height": 900})
        for r in rutas:
            resp = pg.goto(raiz + r + ("" if a.en_vivo else "index.html"), wait_until="networkidle")
            if resp is None or resp.status != 200:
                print(f"HTTP {resp.status if resp else '?'}  {r}"); total += 1; continue
            pg.evaluate("""async () => { const mj = window.MathJax;
                if (mj && mj.startup && mj.startup.promise) { try { await mj.startup.promise; } catch (e) {} } }""")
            pg.wait_for_timeout(800)
            hall, avisos = pg.evaluate(JS)
            total += len(hall)
            n_avisos += len(avisos)
            print(f"{'ok ' if not hall else 'MAL'} {r}")
            for tipo, d in hall + avisos:
                print(f"    {tipo:8} {d}")
        b.close()
    print(f"{len(rutas)} página(s) a {a.ancho}px, {total} hallazgo(s), {n_avisos} aviso(s) de scroll propio")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
