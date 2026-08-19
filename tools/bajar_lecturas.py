#!/usr/bin/env python3
"""Descarga las fuentes de un modulo de lecturas y verifica lo que llego.

    python3 tools/bajar_lecturas.py filosofia_ia/clase_1

Que se descarga y que no. Aqui solo entra texto que su autor o su editor
publican en abierto y gratis en la web, y cada fuente declara de donde sale.
Lo que se vende como edicion o vive tras un muro de pago NO se descarga: se
enlaza desde tools/lecturas.py, en la lista ENLACES, o se recorta de un PDF que
no se versiona (PDFS).

«Publicado en abierto» NO quiere decir «dominio publico», y conviene no
confundirlos al leer este archivo. Solo Marx lo es. El manifiesto de Williams y
Srnicek, el ensayo de Terranova y las cuatro lecturas del modulo 3 siguen en
derechos de sus autores; se reproducen en el cuadernillo, con la fuente al pie
de cada lectura, por ser material educativo de un curso cerrado y estar
disponibles gratis en la web. El campo `licencia` de cada Fuente dice cual es
cada caso, y no debe afirmar una licencia abierta donde no la hay.

Cada fuente declara que debe contener, y la descarga falla ruidosamente si el
archivo que llego no es el que se pidio. Eso ya evito un error real: el ebook
17147 de Gutenberg es la Teodicea, no la Monadologia.
"""
from __future__ import annotations

import html as _html
import json
import re
import shutil
import subprocess
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
    #  PDF publicado en abierto por su autor o su editor: se baja, se le saca el
    #  texto con pdftotext y se recorta igual que una pagina web. Es (url, cortes),
    #  y cada corte es un (desde, hasta), para poder tomar dos tramos del mismo
    #  archivo sin bajarlo dos veces. NO es la via de los PDF de pago: esos no se
    #  bajan aqui, van en PDFS de lecturas.py y no se versionan.
    pdf: tuple[str, list[tuple[str, str]]] | None = None
    #  Id del post en LessWrong; se trae por su API publica (ver _de_lesswrong).
    lesswrong: str | None = None


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
    # Modulo 3 · Exit, NRx & Dark Enlightenment. Las cuatro son paginas web
    # abiertas —gratis, no de dominio publico: ver el encabezado de este
    # archivo—, y ninguna llega como PDF, asi que este modulo no tiene entradas
    # en PDFS ni en ENLACES de tools/lecturas.py. De Land se toman dos de las
    # diez partes del ensayo —la 1 y la 4a— y por eso la fuente concatena dos
    # recortes de la MISMA pagina: el sitio publica el ensayo entero en una
    # sola URL, con las partes separadas solo por su encabezado.
    "filosofia_ia/clase_3": [
        # Ojo con la procedencia de esta: thedarkenlightenment.com NO es sitio
        # de Land. Es el archivo de un tercero, y el propio Land lo desautorizo
        # publicamente (ver el README del modulo). Se usa porque xenosystems.net,
        # donde el ensayo se publico, ya no existe, y porque este alojamiento
        # tiene el texto completo. `debe_contener` apunta a una frase del
        # SEGUNDO recorte, la parte 4a: la del primero seria un subconjunto
        # literal de su propio ancla `desde` y no podria fallar nunca.
        Fuente("land_dark_enlightenment_en.txt", "",
               "Nick Land · en derechos; texto completo alojado por un tercero en thedarkenlightenment.com",
               "its sub-political character: all exit and no voice",
               concatenar=[
                   ("https://www.thedarkenlightenment.com/the-dark-enlightenment-by-nick-land/",
                    r"Part 1: Neo-reactionaries head for the exit",
                    r"Part 2: The arc of history is long"),
                   ("https://www.thedarkenlightenment.com/the-dark-enlightenment-by-nick-land/",
                    r"Part 4a: A multi-part sub-digression into racial terror",
                    r"Part 4b: Obnoxious observations"),
               ]),
        # El `desde` es la primera frase del ensayo y no la linea de autoria del
        # blog: empezar en la autoria metia el titulo dos veces en el cuadernillo
        # —una en la portadilla y otra raspada del sitio—. La fecha se conserva
        # en `procedencia`, que el cuadernillo imprime al pie de la lectura.
        Fuente("yarvin_formalist_manifesto_en.txt", "",
               "Curtis Yarvin (Mencius Moldbug) · en derechos; entrada de blog en abierto, unqualified-reservations.org",
               "So this is the formalist manifesto",
               html=("https://www.unqualified-reservations.org/2007/04/formalist-manifesto-originally-posted/",
                     r"The other day I was tinkering around in my garage",
                     r"next\s*»")),
        # El temario cita esta lectura por las paginas de la recopilacion en PDF
        # que circula como libro (cap. 1, pp. 7-18). Aqui se toma del blog, que
        # es la publicacion original y esta en abierto, y que el propio sitio
        # presenta ya con numeracion de capitulos: el <title> de esta URL es
        # «Chapter 1: A Positive Vision | Patchwork: A Political System for the
        # 21st Century». El recorte NO empieza donde empieza el capitulo: las
        # primeras seis paginas son la parte propagandistica —anecdotas, Croly,
        # los valores civicos de 1911— y el temario arranca justo donde el texto
        # se vuelve de ingenieria. La ficha de la lectura resume lo que queda
        # antes, para que nadie caiga en frio.
        #
        # El `hasta` se apoya en la barra de capitulos del sitio, no en una
        # frase del texto, por la misma razon que el `next »` de la entrada de
        # 2007: el capitulo simplemente termina en su segunda nota al pie y lo
        # siguiente ya es navegacion. Falla ruidosamente si el sitio cambia.
        Fuente("yarvin_patchwork_cap1_en.txt", "",
               "Curtis Yarvin (Mencius Moldbug) · en derechos; entrada de blog en abierto, unqualified-reservations.org",
               "can of course emigrate to any other realm in the Patchwork",
               html=("https://www.unqualified-reservations.org/2008/11/patchwork-positive-vision-part-1/",
                     r"Anyway\. Enough anecdotes and generalities",
                     r"\n\nCh\. 1\n\nCh\. 2\n")),
        # El corte deja fuera la «Editor's Note» que Cato añadió despues: es un
        # texto posterior y distinto —«Your Suffrage Isn't in Danger. Your
        # Other Rights Are.»— y se enlaza desde la pagina del modulo en vez de
        # colarse dentro del ensayo como si fuera su final.
        Fuente("thiel_education_libertarian_en.txt", "",
               "Peter Thiel · en derechos; publicado en abierto por Cato Unbound, 13 de abril de 2009",
               "I no longer believe that freedom and democracy are compatible",
               html=("https://www.cato-unbound.org/2009/04/13/peter-thiel/education-libertarian/",
                     r"I remain committed to the faith of my teenage years",
                     r"Editor.s Note: Mr\. Thiel")),
    ],

    # ── Modulo 4 · Moloch, Rationality & the Long Future ──────────────────────
    # Seis lecturas. Cinco se bajan de la web y la sexta —el handout del curso,
    # handout_genealogias_en.txt— se escribe a mano y ya vive en fuentes/: no
    # tiene entrada aqui porque no hay nada que descargar ni que verificar
    # contra una fuente externa.
    #
    # Dos formas de fuente estrenan en este modulo, y las dos son de texto
    # publicado en abierto, no de material de pago:
    #   · `lesswrong=` trae el ensayo de Yudkowsky por la API publica del sitio.
    #     Su HTML devuelve 429 a un script; la API, no.
    #   · `pdf=` baja un PDF que su editor publica gratis y le saca el texto.
    #     Es el caso del articulo del Global Priorities Institute, que no se
    #     vende: se descarga de la pagina del propio instituto.
    "filosofia_ia/clase_4": [
        # El ensayo entero, partes I a VIII. El `hasta` corta en el pie del
        # blog —el aviso del podcast y del NFT—, que es lo primero que sigue al
        # ultimo verso citado de Ginsberg. Sin ese corte entrarian los miles de
        # comentarios de la entrada, que pesan seis veces mas que el ensayo.
        Fuente("alexander_moloch_en.txt", "",
               "Scott Alexander · en derechos; publicado en abierto y completo por el autor en Slate Star Codex",
               "The opposite of a trap is a garden",
               html=("https://slatestarcodex.com/2014/07/30/meditations-on-moloch/",
                     r"Allen Ginsberg.s famous poem on Moloch",
                     r"\[\s*Also available as podcast")),
        # Sin recorte: el post es exactamente la lectura, prologo del libro
        # «Rationality: From AI to Zombies» que el propio autor publica gratis.
        Fuente("yudkowsky_rationality_en.txt", "",
               "Eliezer Yudkowsky · en derechos; publicado en abierto por el autor en LessWrong",
               "systematically achieving your values",
               lesswrong="RcZCwxFiZzE6X7nsv"),
        # Las ocho proposiciones y el parrafo de procedencia que las precede.
        # No lleva `hasta`: la pagina termina en la octava.
        Fuente("humanityplus_declaracion_transhumanista_en.txt", "",
               "Humanity+ · declaracion publicada en abierto por la propia organizacion",
               "the well-being of all sentience",
               html=("https://www.humanityplus.org/the-transhumanist-declaration",
                     r"The Transhumanist Declaration was originally crafted in 1998",
                     None)),
        # El articulo completo tal como lo aloja el autor. La paginacion
        # 308-314 que cita el temario es la de Utilitas, y la propia pagina la
        # declara; el cuadernillo reproduce la version del autor, que es la
        # misma pieza sin la maqueta de la revista.
        Fuente("bostrom_astronomical_waste_en.txt", "",
               "Nick Bostrom · en derechos; publicado en abierto y completo por el autor en nickbostrom.com",
               "The Chief Goal for Utilitarians Should Be to Reduce Existential Risk",
               html=("https://nickbostrom.com/astronomical/waste",
                     r"I\. The Rate of Loss of Potential Lives",
                     None)),
        # Dos tramos del mismo PDF: el argumento (secciones 1 a 4) y las
        # conclusiones (seccion 10). Quedan fuera las objeciones tecnicas
        # —cluelessness, fanatismo, la version deontica y el apendice—, que en
        # una sesion de dos horas no se alcanzan y que la ficha dice donde
        # estan. El `debe_contener` apunta al segundo tramo a proposito: una
        # frase del primero seria subcadena de su propio `desde` y no podria
        # fallar nunca.
        Fuente("greaves_macaskill_strong_longtermism_en.txt", "",
               "Hilary Greaves y William MacAskill · en derechos; documento de trabajo publicado en abierto por el Global Priorities Institute (Oxford)",
               "The potential future of civilisation is vast",
               pdf=("https://globalprioritiesinstitute.org/wp-content/uploads/"
                    "The-Case-for-Strong-Longtermism-GPI-Working-Paper-June-2021-2-2.pdf",
                    [(r"A striking fact about the history of civilisation",
                      r"5\. Strong longtermism about individual decisions"),
                     (r"10\. Summary and conclusions\n\nThe potential future of civilisation is vast",
                      r"Appendix")])),
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

# Inicial suelta que el raspado dejo separada del resto de su palabra: «T he».
# «I» y «A» quedan fuera a proposito, porque son palabras enteras del ingles y
# no iniciales sueltas. Sin esa excepcion, un ensayo en primera persona se
# arruina entero —«Iremain committed», «Idecided to build a new ideology»— y el
# defecto ni siquiera se reporta, porque la misma regla que lo produce hace que
# el texto ya no calce con el patron de PROHIBIDO que deberia detectarlo. El
# precio es que un «I nteligencia» partido de verdad ahora sobrevive; no ha
# aparecido ninguno, y es preferible a romper cada «I» de cada lectura.
INICIAL_SUELTA = r"\b(?![IA]\b)([A-Z]) ([a-z]{2,})\b"

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
    (INICIAL_SUELTA + r"(?= [a-z])", "palabra partida por espacio, tipo «T he»"),
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
    texto = re.sub(INICIAL_SUELTA, r"\1\2", texto)
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


def _texto_de_html(h: str) -> str:
    """HTML -> texto en parrafos, ya limpio. Lo comparten la web y la API."""
    h = re.sub(r"<(script|style|nav|header|footer|form)\b.*?</\1>", "", h, flags=re.S | re.I)
    h = re.sub(r"<br\s*/?>|</p>|</div>|</h[1-6]>|</li>", "\n\n", h, flags=re.I)
    t = _limpiar(re.sub(r"<[^>]+>", " ", h))
    return "\n\n".join(" ".join(b.split()) for b in t.split("\n\n") if b.strip())


def _de_lesswrong(post_id: str) -> str:
    """Trae un ensayo de LessWrong por su API publica.

    El HTML del sitio esta detras de proteccion antibots y devuelve 429 a un
    script; la API de GraphQL, que es la via que el propio sitio documenta, no.
    """
    consulta = ('{post(input:{selector:{_id:"%s"}}){result{title contents{html}}}}' % post_id)
    req = urllib.request.Request(
        "https://www.lesswrong.com/graphql",
        data=json.dumps({"query": consulta}).encode(),
        headers={"User-Agent": AGENTE, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        datos = json.loads(r.read().decode())
    post = (datos.get("data") or {}).get("post", {}).get("result")
    if not post:
        raise SystemExit(f"  ✗ LessWrong no devolvió el post {post_id}: {datos}")
    return _texto_de_html(post["contents"]["html"])


def _de_html(url: str, desde: str | None = None, hasta: str | None = None) -> str:
    """Extrae el cuerpo legible de una pagina.

    `desde` y `hasta` son obligatorios en la practica: sin ellos entra el menu
    de navegacion del sitio, su pie, y en ccru.net el indice completo de la
    revista. Cada fuente declara donde empieza y termina su ensayo.
    """
    t = _texto_de_html(_pedir(url))

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


def _de_pdf(url: str, cortes: list[tuple[str, str]], destino: Path) -> str:
    """Saca el texto de un PDF abierto y devuelve los tramos pedidos.

    El PDF se guarda junto a las fuentes para poder auditarlo, pero no se
    versiona: `.gitignore` excluye `lecturas/**/fuentes/*.pdf`. Lo que queda en
    el repositorio es el .txt, que es lo que acaba en el cuadernillo.

    `pdftotext -layout` respeta los parrafos; sin `-layout` pega las palabras.
    """
    if shutil.which("pdftotext") is None:
        raise SystemExit("  ✗ falta pdftotext (paquete poppler-utils)")
    destino.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(req, timeout=180) as r:
        destino.write_bytes(r.read())

    salida = subprocess.run(["pdftotext", "-layout", str(destino), "-"],
                            capture_output=True, text=True, check=True).stdout

    # El numero de pagina suelto en su propia linea es lo unico que el pie de
    # este tipo de articulo deja en el texto, y partiria un parrafo en dos.
    salida = re.sub(r"^[ \t]*\d{1,3}[ \t]*$", "", salida, flags=re.M)
    t = _limpiar(salida)
    t = "\n\n".join(" ".join(b.split()) for b in t.split("\n\n") if b.strip())

    tramos = []
    for desde, hasta in cortes:
        i = re.search(desde, t)
        if not i:
            raise SystemExit(f"  ✗ no se halló el inicio {desde!r} en {url}")
        resto = t[i.start():]
        f = re.search(hasta, resto[1:])
        if not f:
            raise SystemExit(f"  ✗ no se halló el final {hasta!r} en {url}")
        tramos.append(resto[: 1 + f.start()].strip())
    return "\n\n".join(tramos)


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
        elif f.pdf:
            url, cortes = f.pdf
            texto = _de_pdf(url, cortes, destino / (Path(f.archivo).stem + ".pdf"))
        elif f.html:
            texto = _de_html(*f.html)
        elif f.lesswrong:
            texto = _de_lesswrong(f.lesswrong)
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
