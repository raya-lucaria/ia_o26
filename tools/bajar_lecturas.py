#!/usr/bin/env python3
"""Descarga las fuentes de un modulo de lecturas y verifica lo que llego.

    python3 tools/bajar_lecturas.py filosofia_ia/clase_1

Solo se descargan obras de dominio publico desde repositorios que las
distribuyen legitimamente. Lo que sigue en derechos NO se descarga aqui: se
enlaza desde tools/lecturas.py, en la lista ENLACES.

Cada fuente declara que debe contener, y la descarga falla ruidosamente si el
archivo que llego no es el que se pidio. Eso ya evito un error real: el ebook
17147 de Gutenberg es la Teodicea, no la Monadologia.
"""
from __future__ import annotations

import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
AGENTE = "ia-o26-curso/1.0 (material educativo ITAM)"


@dataclass
class Fuente:
    archivo: str
    url: str
    licencia: str
    #  Cadena que DEBE aparecer en el texto descargado. Es la guarda contra
    #  bajar la obra equivocada bajo el nombre correcto.
    debe_contener: str
    wikisource: tuple[str, str] | None = None   # (idioma, titulo)
    html: tuple[str, str | None, str | None] | None = None  # (url, desde, hasta)
    concatenar: list[tuple[str, str | None, str | None]] | None = None


FUENTES: dict[str, list[Fuente]] = {
    # Modulo 1 · ¿Accelerate What? Las lecturas que el temario pide, tomadas de
    # fuentes primarias abiertas: el archivo del propio CCRU, el sitio de los
    # autores, y el archivo Marx/Engels. La paginacion del temario es la de la
    # antologia #Accelerate; aqui el texto es el mismo, la numeracion no.
    "filosofia_ia/clase_1": [
        Fuente("marx_fragmento_maquinas_en.txt", "",
               "Dominio público · Marxists Internet Archive",
               "general intellect",
               concatenar=[
                   ("https://www.marxists.org/archive/marx/works/1857/grundrisse/ch13.htm",
                    r"automatic system of machinery", None),
                   ("https://www.marxists.org/archive/marx/works/1857/grundrisse/ch14.htm",
                    None, r"Real economy — saving — consists"),
               ]),
        Fuente("ccru_swarmachines_en.txt", "",
               "CCRU · archivo público del propio colectivo, ccru.net",
               "situationists",
               html=("http://www.ccru.net/swarm1/1_swarm.htm", r"Swarmachines", None)),
        Fuente("land_meltdown_en.txt", "",
               "Nick Land · archivo público de CCRU, ccru.net",
               "meltdown",
               html=("http://www.ccru.net/swarm1/1_melt.htm", r"Meltdown", None)),
        Fuente("barbrook_cameron_californian_ideology_en.txt", "",
               "Barbrook y Cameron · imaginaryfutures.net, sitio de los autores",
               "Californian Ideology",
               html=("http://www.imaginaryfutures.net/2007/04/17/the-californian-ideology-2/",
                     r"As the sun sets|Californian Ideology", r"Bibliography|References")),
    ]
}


def _pedir(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8", errors="ignore")


def _de_html(url: str, desde: str | None = None, hasta: str | None = None) -> str:
    """Extrae el texto legible de una pagina. Sirve para sitios de autor y
    archivos historicos como ccru.net, que no ofrecen otra forma de obtenerlo."""
    import re
    h = _pedir(url)
    h = re.sub(r"<(script|style|nav|header|footer)\b.*?</\1>", "", h, flags=re.S | re.I)
    h = re.sub(r"<br\s*/?>|</p>|</div>|</h[1-6]>", "\n\n", h, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", h)
    t = (t.replace("&nbsp;", " ").replace("&amp;", "&")
          .replace("&#8217;", "'").replace("&#8216;", "'")
          .replace("&#8220;", '"').replace("&#8221;", '"')
          .replace("&#8212;", "—").replace("&quot;", '"'))
    t = "\n\n".join(" ".join(b.split()) for b in t.split("\n\n") if b.strip())
    if desde:
        m = re.search(desde, t, re.I)
        if not m:
            raise SystemExit(f"  ✗ no se halló el inicio {desde!r} en {url}")
        t = t[m.start():]
    if hasta:
        m = re.search(hasta, t[1:], re.I)
        if m:
            t = t[: 1 + m.start()]
    return t.strip()


def _de_wikisource(idioma: str, titulo: str) -> str:
    """Wikisource sirve el wikitexto crudo; hay que quitarle el marcado."""
    import re
    url = (f"https://{idioma}.wikisource.org/wiki/"
           f"{urllib.parse.quote(titulo.replace(' ', '_'))}?action=raw")
    t = _pedir(url)
    t = re.sub(r"\{\{[^{}]*\}\}", "", t)
    t = re.sub(r"<ref[^>]*>.*?</ref>|<[^>]+>", "", t, flags=re.S)
    t = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[\[([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"'{2,}", "", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()


def bajar(modulo: str) -> None:
    destino = RAIZ / "lecturas" / modulo / "fuentes"
    destino.mkdir(parents=True, exist_ok=True)

    for f in FUENTES[modulo]:
        print(f"  {f.archivo:<38} ", end="", flush=True)
        if f.concatenar:
            texto = "\n\n".join(_de_html(*c) for c in f.concatenar)
        elif f.html:
            texto = _de_html(*f.html)
        elif f.wikisource:
            texto = _de_wikisource(*f.wikisource)
        else:
            texto = _pedir(f.url)

        if f.debe_contener not in texto:
            raise SystemExit(
                f"\n  ✗ el archivo descargado no contiene {f.debe_contener!r}. "
                f"La fuente cambió o apunta a la obra equivocada; revísala antes de usarla."
            )
        (destino / f.archivo).write_text(texto, encoding="utf-8")
        print(f"{len(texto.split()):>7} palabras  ✓  {f.licencia}")


if __name__ == "__main__":
    modulo = sys.argv[1] if len(sys.argv) > 1 else "filosofia_ia/clase_1"
    if modulo not in FUENTES:
        raise SystemExit(f"módulo desconocido: {modulo}. Opciones: {list(FUENTES)}")
    print(f"Descargando fuentes de {modulo}\n")
    bajar(modulo)
    print("\nListo. Ahora: python3 tools/lecturas.py " + modulo)
