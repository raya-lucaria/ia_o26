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


FUENTES: dict[str, list[Fuente]] = {
    "filosofia_ia/clase_1": [
        Fuente("hobbes_leviathan_en.txt",
               "https://www.gutenberg.org/ebooks/3207.txt.utf-8",
               "Dominio público · Project Gutenberg",
               "OF REASON, AND SCIENCE"),
        Fuente("lamettrie_hombre_maquina_en.txt",
               "https://www.gutenberg.org/ebooks/52090.txt.utf-8",
               "Dominio público · Project Gutenberg",
               "MAN A MACHINE"),
        Fuente("descartes_discurso_v_es.txt", "",
               "Dominio público · Wikisource",
               "máquina",
               wikisource=("es", "Discurso del método (Wikisource tr.)/Quinta parte")),
        Fuente("leibniz_monadologia_en.txt", "",
               "Dominio público · Wikisource, tr. G. M. Duncan",
               "machine so constructed as to cause thought",
               wikisource=("en", "Monadology (Leibniz, tr. Duncan)")),
    ]
}


def _pedir(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8", errors="ignore")


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
        texto = _de_wikisource(*f.wikisource) if f.wikisource else _pedir(f.url)

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
