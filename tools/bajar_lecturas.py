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

import html as _html
import re
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
                    None, r"Significance\s+of\s+the\s+development\s+of\s+fixed\s+capital"),
               ]),
        Fuente("ccru_swarmachines_en.txt", "",
               "CCRU · archivo público del propio colectivo, ccru.net",
               "situationists",
               html=("http://www.ccru.net/swarm1/1_swarm.htm",
                     r"[Tt]he\s+situationists", r"maximum\s+slogan\s+density")),
        Fuente("land_meltdown_en.txt", "",
               "Nick Land · archivo público de CCRU, ccru.net",
               "meltdown",
               html=("http://www.ccru.net/swarm1/1_melt.htm",
                     r"The story goes like this", r"References\s+Cs1")),
        Fuente("barbrook_cameron_californian_ideology_en.txt", "",
               "Barbrook y Cameron · imaginaryfutures.net, sitio de los autores",
               "Californian Ideology",
               html=("http://www.imaginaryfutures.net/2007/04/17/the-californian-ideology-2/",
                     r"Not\s+to\s+lie\s+about\s+the\s+future",
                     r"Notes\s+and\s+References|—{5,}")),
    ],
    # Modulo 2 · The Left Takes the Future Back. Dos de las cuatro lecturas
    # tienen fuente primaria abierta; las otras dos siguen en derechos y se
    # toman de PDF de la edicion citada (ver PDFS en tools/lecturas.py).
    "filosofia_ia/clase_2": [
        Fuente("williams_srnicek_manifesto_en.txt", "",
               "Williams y Srnicek · criticallegalthinking.com, 14 de mayo de 2013",
               "The command of The Plan must be married to the improvised order of The Network.",
               html=("https://criticallegalthinking.com/2013/05/14/accelerate-manifesto-for-an-accelerationist-politics/",
                     r"01\.\s*INTRODUCTION:\s*On\s+the\s+Conjuncture",
                     r"Sharing\s+Options")),
        Fuente("terranova_red_stack_en.txt", "",
               "Tiziana Terranova · euronomade.info",
               "three levels of socio-technical innovation: virtual money, social networks, and bio-hypermedia",
               html=("http://www.euronomade.info/?p=2268",
                     r"This\s+essay\s+is\s+the\s+outcome\s+of\s+a\s+research\s+process",
                     r"Condividere")),
    ],
}


def _pedir(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8", errors="ignore")


# ccru.net usa entidades de letras acentuadas como comillas —un truco de
# codificacion de los noventa—. Decodificarlas con html.unescape daria «æ» y
# «ö» en medio de las frases, asi que se mapean ANTES.
COMILLAS_CCRU = {"&aelig;": "\u2018", "&AElig;": "\u2018",
                 "&ouml;": "\u2019", "&ocirc;": "\u201c", "&Ouml;": "\u201d"}

# Bloques que los sitios insertan alrededor del ensayo y que no son el ensayo.
BASURA = [
    # Indice completo de la revista, pegado a media lectura en ccru.net. Los
    # patrones usan \s* en todas las junturas: el HTML original mete saltos de
    # linea en medio de los nombres, y un patron con espacios literales falla.
    r"swarm\s*1\s*Nick\s*Land[\s\S]{0,3000}?Ccru\s*-\s*Glossary",
    # Barra de navegacion de ccru.net
    r"Cybernetic\s+culture\s+research\s+unit[\s\S]{0,160}?occultu\s*-?\s*res",
    r"\bswarm1\b\s*\d?\s*\.?\s*(?:Nick\s*Land\s*-?\s*Meltdown|Ccru\s*-?\s*Swarmachines)",
    # Cabecera y pie del archivo Marx/Engels
    r"<?\s*Previous\s*\|\s*Contents\s*\|\s*Next\s*>?",
    r"Marx/Engels\s+Archive",
    r"Economic\s+Manuscripts:\s*Grundrisse\s*\d+",
    r"Grundrisse:\s*Notebook\s+[IVX]+\s*[-–]\s*The\s+Chapter\s+on\s+Capital",
    # Cromo de WordPress en imaginaryfutures
    r"Home\s+The\s+Book\s+Reviews\s+Other\s+Works\s+News\s+Gallery\s+Biographies\s+HRC\s+Archive",
    r"Print\s+this\s+page",
    r"Author:\s*Richard\s+Barbrook\s+and\s+Andy\s+Cameron",
    r"CALIFORNIAN\s+IDEOLOGY\s+by[\s\S]{0,80}?Imaginary\s+Futures",
]

# Lo que NUNCA debe sobrevivir a la limpieza. Si algo de esto queda, la
# descarga falla: es preferible detenerse a publicar un texto ilegible.
PROHIBIDO = [
    (r"&[a-zA-Z]{2,10};", "entidad HTML sin decodificar"),
    (r"&#\d{2,5};", "entidad numérica sin decodificar"),
    (r"\[\[\s*\]\]", "marcador [[ ]] sin convertir"),
    (r"Cybernetic\s+culture\s+research", "barra de navegación de ccru.net"),
    (r"Kodwo\s*Eshun\s*-?\s*Motion\s*Capture|Cthulhu\s*Club", "índice de la revista CCRU"),
    (r"Print this page|HRC Archive", "cromo de WordPress"),
    (r"Marx/Engels Archive|Previous \| Contents", "pie del archivo Marx/Engels"),
    (r"\b[A-Z] [a-z]{2,}\b(?= [a-z])", "palabra partida por espacio, tipo «T he»"),
]


def _limpiar(texto: str) -> str:
    """Decodifica, quita el cromo del sitio y repara los artefactos del raspado."""
    for ent, comilla in COMILLAS_CCRU.items():
        texto = texto.replace(ent, comilla)
    for _ in range(3):                      # entidades dobles: &amp;#8211;
        nuevo_t = _html.unescape(texto)
        if nuevo_t == texto:
            break
        texto = nuevo_t
    # Normalizar ANTES de buscar: las fuentes traen espacios dobles y saltos de
    # linea en medio de las frases, y un patron con espacios literales no
    # coincide. Fue exactamente el fallo que dejo pasar el pie de Marx.
    texto = texto.replace("\u00a0", " ")
    texto = re.sub(r"[^\S\n]+", " ", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    for patron in BASURA:
        texto = re.sub(patron, " ", texto, flags=re.S | re.I)
    texto = re.sub(r"\[\[\s*\]\]", "\n\n* * *\n\n", texto)
    # guion de corte de linea que el HTML dejo dentro de la palabra
    texto = re.sub(r"(\w)-\s+(\w{2,})", r"\1\2", texto)
    # inicial separada del resto: «T he» -> «The»
    texto = re.sub(r"\b([A-Z]) ([a-z]{2,})\b", r"\1\2", texto)
    texto = re.sub(r"\s+([.,;:!?])", r"\1", texto)
    texto = texto.replace("\u00a0", " ")
    return re.sub(r"[ \t]{2,}", " ", texto)


def revisar(nombre: str, texto: str) -> list[str]:
    """Devuelve los defectos que sobrevivieron. Vacia = el texto esta limpio."""
    fallos = []
    for patron, descripcion in PROHIBIDO:
        m = re.search(patron, texto)
        if m:
            ctx = " ".join(texto[max(0, m.start() - 40):m.start() + 60].split())
            fallos.append(f"{nombre}: {descripcion} → «…{ctx}…»")
    return fallos


def _de_html(url: str, desde: str | None = None, hasta: str | None = None) -> str:
    """Extrae el cuerpo legible de una pagina.

    `desde` y `hasta` son obligatorios en la practica: sin ellos entra el menu
    de navegacion del sitio, su pie, y en ccru.net el indice completo de la
    revista. Cada fuente declara donde empieza y termina su ensayo.
    """
    h = _pedir(url)
    h = re.sub(r"<(script|style|nav|header|footer|form)\b.*?</\1>", "", h, flags=re.S | re.I)
    h = re.sub(r"<br\s*/?>|</p>|</div>|</h[1-6]>|</li>", "\n\n", h, flags=re.I)
    t = _limpiar(re.sub(r"<[^>]+>", " ", h))
    t = "\n\n".join(" ".join(b.split()) for b in t.split("\n\n") if b.strip())

    if desde:
        m = re.search(desde, t)
        if not m:
            raise SystemExit(f"  ✗ no se halló el inicio {desde!r} en {url}")
        t = t[m.start():]
    if hasta:
        m = re.search(hasta, t[1:])
        if not m:
            raise SystemExit(f"  ✗ no se halló el final {hasta!r} en {url}")
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
        fallos = revisar(f.archivo, texto)
        if fallos:
            print("✗")
            raise SystemExit("  Quedó basura en el texto:\n    " + "\n    ".join(fallos))
        (destino / f.archivo).write_text(texto, encoding="utf-8")
        print(f"{len(texto.split()):>7} palabras  ✓  {f.licencia}")


if __name__ == "__main__":
    modulo = sys.argv[1] if len(sys.argv) > 1 else "filosofia_ia/clase_1"
    if modulo not in FUENTES:
        raise SystemExit(f"módulo desconocido: {modulo}. Opciones: {list(FUENTES)}")
    print(f"Descargando fuentes de {modulo}\n")
    bajar(modulo)
    print("\nListo. Ahora: python3 tools/lecturas.py " + modulo)
