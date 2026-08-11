#!/usr/bin/env python3
"""Arma el cuadernillo de lecturas de una clase a partir de fuentes descargadas.

Toma textos planos de dominio publico, recorta la seccion que se lee en clase,
la maqueta con la paleta del curso y une todo en un solo PDF por modulo.

    python3 tools/lecturas.py filosofia_ia/clase_1

La lista de lecturas es declarativa: agregar una es agregar una entrada a
LECTURAS, no tocar el codigo. Cada entrada dice de donde sale su texto, que
tramo se recorta y por que se lee.

Depende de weasyprint (HTML a PDF) y pypdf (intercala las paginas de las
lecturas en derechos en su lugar dentro del cuadernillo). Ver tools/README.md.
"""
from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LECTURAS_DIR = RAIZ / "lecturas"

# Paleta del skin eva-cyberpunk, la misma del sitio.
PALETA = {
    "papel": "#faf7fd",
    "tinta": "#1a0d26",
    "suave": "#5c4a6e",
    "acento": "#8b1a9e",
    "borde": "#d8c9e8",
}


@dataclass
class Recorte:
    """Como aislar la seccion que se lee dentro de un texto completo."""

    desde: str | None = None   # regex donde empieza
    hasta: str | None = None   # regex donde termina
    palabras_max: int | None = None  # tope, cortando en parrafo completo

    def aplicar(self, texto: str) -> str:
        inicio = 0
        if self.desde:
            m = re.search(self.desde, texto, re.M)
            if not m:
                raise ValueError(f"no se hallo el inicio: {self.desde!r}")
            inicio = m.start()
        fin = len(texto)
        if self.hasta:
            m = re.search(self.hasta, texto[inicio + 1 :], re.M)
            if not m:
                raise ValueError(f"no se hallo el final: {self.hasta!r}")
            fin = inicio + 1 + m.start()
        fragmento = texto[inicio:fin].strip()
        if self.palabras_max:
            fragmento = _cortar_en_parrafo(fragmento, self.palabras_max)
        return fragmento


def _cortar_en_parrafo(texto: str, tope: int) -> str:
    """Corta al llegar al tope sin partir un parrafo por la mitad."""
    parrafos, acumuladas, salida = texto.split("\n\n"), 0, []
    for p in parrafos:
        n = len(p.split())
        if acumuladas + n > tope and salida:
            break
        salida.append(p)
        acumuladas += n
    return "\n\n".join(salida)


@dataclass
class LecturaPDF:
    """Lectura que llega como PDF y se recorta por rango de paginas.

    Sirve para textos que no existen en fuente abierta y hay que tomar de la
    edicion citada. El archivo va en fuentes/ y NO se versiona: `.gitignore`
    excluye los PDF con derechos. Si el archivo no esta, la construccion sigue
    sin el y lo reporta, en vez de fallar.
    """

    orden: int
    id: str
    titulo: str
    autor: str
    anio: str
    fuente: str                 # archivo dentro de fuentes/
    paginas: tuple[int, int]    # inclusivo, 1-indexado, como las cita el temario
    edicion: str
    introduccion: str      # ficha de cuatro apartados; ver introduccion.md

    def recortar(self, fuentes: Path, destino: Path) -> Path | None:
        import pypdf
        origen = fuentes / self.fuente
        if not origen.is_file():
            return None
        lector = pypdf.PdfReader(origen)
        a, b = self.paginas
        if b > len(lector.pages):
            raise ValueError(
                f"{self.id}: se piden páginas {a}-{b} pero el PDF tiene "
                f"{len(lector.pages)}. ¿Es la edición correcta?"
            )
        escritor = pypdf.PdfWriter()
        for i in range(a - 1, b):
            escritor.add_page(lector.pages[i])
        salida = destino / f"{self.id}.pdf"
        with salida.open("wb") as f:
            escritor.write(f)
        return salida


@dataclass
class Lectura:
    orden: int
    id: str
    titulo: str
    autor: str
    anio: str
    fuente: str            # archivo dentro de fuentes/
    procedencia: str       # de donde se descargo
    licencia: str
    introduccion: str      # ficha de cuatro apartados; ver introduccion.md
    recorte: Recorte = field(default_factory=Recorte)

    @property
    def cita(self) -> str:
        return f"{self.autor} ({self.anio}). *{self.titulo}*"


# ── Módulo 1 · ¿Accelerate What? ──────────────────────────────────────────────
# El temario pide seis lecturas con la paginación de la antología #Accelerate
# (Urbanomic, 2014). Cuatro existen en fuentes primarias abiertas y van en el
# cuadernillo; dos siguen en derechos y se toman de PDF de la edición citada.
# Hoy las seis están presentes y se intercalan en el orden acordado. El texto
# es el mismo; la numeración de páginas es la de la antología y no la de aquí.

LECTURAS: dict[str, list[Lectura]] = {
    "filosofia_ia/clase_1": [
        Lectura(
            orden=1,
            id="marx-fragmento-maquinas",
            titulo="Fragmento sobre las máquinas",
            autor="Karl Marx",
            anio="1858",
            fuente="marx_fragmento_maquinas_en.txt",
            procedencia="Grundrisse, cuadernos VI–VII · Marxists Internet Archive",
            licencia="Dominio público",
            introduccion=(
                "**Qué vas a leer.** Marx mirando la fábrica: la máquina absorbe "
                "el saber acumulado de la sociedad entera y el obrero queda al "
                "lado del proceso, vigilándolo. Son cuadernos de trabajo —los "
                "*Grundrisse*—, no un libro que Marx haya publicado.\n\n"
                "**Palabras clave.** *General intellect*: el saber colectivo "
                "depositado en máquinas. *Capital fijo*: lo invertido en "
                "maquinaria e instalaciones, frente a lo pagado en salarios. "
                "*Tiempo de trabajo*: la medida del valor, y el problema del "
                "texto.\n\n"
                "**Qué retener.** Dos cosas. El obrero deja de ser quien usa la "
                "herramienta y pasa a ser apéndice de la máquina. Y la "
                "contradicción que Marx ve venir: cuando la riqueza la produce "
                "el saber colectivo, seguir midiéndola en horas trabajadas se "
                "vuelve absurdo.\n\n"
                "**Es difícil, y está bien.** Frases largas, paréntesis, cambios "
                "de tema: Marx escribe para sí mismo. Si un párrafo se te "
                "cierra, sigue de largo — la tesis vuelve tres o cuatro veces "
                "con otras palabras."
            ),
            recorte=Recorte(desde=r"automatic system of machinery", palabras_max=4600),
        ),
        Lectura(
            orden=5,
            id="ccru-swarmachines",
            titulo="Swarmachines",
            autor="CCRU",
            anio="1996",
            fuente="ccru_swarmachines_en.txt",
            procedencia="Cybernetic Culture Research Unit · ccru.net",
            licencia="Publicado abiertamente por el propio colectivo",
            introduccion=(
                "**Qué vas a leer.** El colectivo del que Land formaba parte, "
                "escribiendo sobre la insurrección como enjambre: sin líder, "
                "sin centro, propagándose. La prosa está averiada a propósito "
                "— neologismos, cortes, ritmo de música de baile.\n\n"
                "**Palabras clave.** *Enjambre*: orden colectivo sin nadie que "
                "mande. *Acéntrico*: sin centro que dirija. *CCRU*: la "
                "Cybernetic Culture Research Unit, el grupo de Warwick de los "
                "noventa donde se cocinó todo esto.\n\n"
                "**Qué retener.** Una política sin sujeto: no un partido que "
                "dirige a las masas, sino un proceso que se contagia. Es la "
                "misma forma que Land le atribuye al capital, aplicada aquí a "
                "la revuelta.\n\n"
                "**Es difícil, y está bien.** Es el texto más difícil del "
                "cuadernillo, y lo es deliberadamente: está escrito para sonar "
                "como aquello que describe. Son cinco páginas. Léelo como quien "
                "escucha música — no lo traduzcas frase por frase."
            ),
        ),
        Lectura(
            orden=3,
            id="land-meltdown",
            titulo="Meltdown",
            autor="Nick Land",
            anio="1994",
            fuente="land_meltdown_en.txt",
            procedencia="Cybernetic Culture Research Unit · ccru.net",
            licencia="Publicado abiertamente en el archivo de CCRU",
            introduccion=(
                "**Qué vas a leer.** Land describe el capitalismo no como un "
                "sistema que alguien administra, sino como un proceso que se "
                "corre solo y se desarma hacia adelante. Está escrito a "
                "propósito como una avería: fragmentos, fechas, mayúsculas.\n\n"
                "**Palabras clave.** *Meltdown*: la fusión del núcleo, el "
                "colapso ya en curso. *Cibernética*: sistemas que se regulan "
                "solos por retroalimentación. *Desterritorialización* (de "
                "Deleuze y Guattari, que acabas de leer): arrancar algo de su "
                "lugar y ponerlo a circular.\n\n"
                "**Qué retener.** Una sola tesis: el capital no necesita "
                "sujeto. Lo demás es estilo.\n\n"
                "**Es difícil, y está bien.** Nadie lo entiende entero a la "
                "primera. No te detengas en las referencias que no reconozcas; "
                "subraya dos frases que te choquen y trae esas a clase."
            ),
        ),
        Lectura(
            orden=6,
            id="barbrook-cameron-californian",
            titulo="La ideología californiana",
            autor="Richard Barbrook y Andy Cameron",
            anio="1995",
            fuente="barbrook_cameron_californian_ideology_en.txt",
            procedencia="imaginaryfutures.net, sitio de los autores",
            licencia="Publicado abiertamente por los autores",
            introduccion=(
                "**Qué vas a leer.** Dos británicos mirando Silicon Valley en "
                "1995 y nombrando su mezcla: contracultura hippie más libre "
                "mercado, unidas por la fe en la tecnología. El ensayo que le "
                "puso nombre a la «ideología californiana».\n\n"
                "**Palabras clave.** *Ideología californiana*: la fusión de "
                "bohemia y negocio. *Clase virtual*: los trabajadores del "
                "conocimiento que se piensan artistas y son empleados. "
                "*Determinismo tecnológico*: creer que la tecnología decide la "
                "historia por su cuenta.\n\n"
                "**Qué retener.** Cuánto de 2026 ya estaba escrito en 1995 — "
                "incluida la deuda con el dinero público (ARPA, universidades) "
                "que el relato del emprendedor solitario borra. Es la lectura "
                "más útil para discutir e/acc.\n\n"
                "**Es difícil, y está bien.** Esta no lo es: es periodismo y se "
                "lee sola. Es la más larga, eso sí — quince páginas. Trae "
                "referencias de 1995 (Gingrich, el Minitel francés, *Wired*) "
                "que no hace falta reconocer para seguir el argumento."
            ),
        ),
    ]
}

# Sin fuente abierta verificable. Si consigues el PDF de la edicion citada y lo
# dejas en fuentes/ con este nombre, la siguiente construccion lo recorta y lo
# intercala en su lugar dentro del cuadernillo. Si no esta, se construye sin
# el y se reporta.
PDFS: dict[str, list[LecturaPDF]] = {
    "filosofia_ia/clase_1": [
        LecturaPDF(
            orden=2, id="deleuze-guattari-antiedipo",
            titulo="El Anti-Edipo, pp. 239–240",
            autor="Gilles Deleuze y Félix Guattari", anio="1972",
            fuente="deleuze_guattari_antiedipo_paidos.pdf",
            paginas=(247, 247),
            edicion=("Paidós, ed. española. El temario cita Minnesota 1983 "
                     "pp. 239–240; el pasaje equivalente cabe en la p. 247 de "
                     "esta edición, más densa."),
            introduccion=(
                "**Qué vas a leer.** Una sola página, la más citada del "
                "aceleracionismo. Deleuze y Guattari preguntan cuál es la vía "
                "revolucionaria y contestan que no es retirarse del mercado "
                "mundial, sino ir «aún más lejos» en el movimiento de "
                "descodificación y desterritorialización.\n\n"
                "**Palabras clave.** *Desterritorialización*: arrancar algo de "
                "su lugar y ponerlo a circular. *Flujos*: dinero, deseo, "
                "mercancías, entendidos como corrientes antes que como cosas. "
                "*Catexis de deseo*: dónde se invierte el deseo — para ellos, "
                "en la economía, no en la ideología.\n\n"
                "**Qué retener.** «Acelerar el proceso» —frase que le atribuyen "
                "a Nietzsche— es lo que el movimiento entero tomó como divisa. "
                "Aquí la lees en su sitio: llega como pregunta, y trae un «tal "
                "vez» que casi siempre se borra al citarla.\n\n"
                "**Es difícil, y está bien.** Es la página más densa del "
                "cuadernillo; léela dos veces, que es una sola. El pasaje "
                "termina en «todavía no hemos visto nada». Lo que sigue después "
                "de los asteriscos es otro tema —la escritura y el "
                "capitalismo— y no hace falta para la sesión."
            ),
        ),
        LecturaPDF(
            orden=4, id="fisher-terminator-avatar",
            titulo="Terminator vs Avatar",
            autor="Mark Fisher", anio="2012",
            fuente="fisher_terminator_vs_avatar.pdf",
            paginas=(1, 12),
            edicion=("#Accelerate: The Accelerationist Reader, Urbanomic, 2014, "
                     "pp. 335–346. El archivo ya es ese extracto: 12 páginas."),
            introduccion=(
                "**Qué vas a leer.** Fisher toma a Land en serio —lo considera "
                "el mejor diagnóstico del capitalismo disponible— y luego le da "
                "la vuelta: acepta que el capital es un proceso desatado, y "
                "rechaza que haya que celebrarlo. De aquí sale la pregunta que "
                "da nombre al módulo.\n\n"
                "**Palabras clave.** *Economía libidinal* (de Lyotard): el goce "
                "que la crítica no confiesa. *Aceleracionismo de izquierda*: "
                "acelerar la tecnología, no el capital. *Terminator y Avatar*: "
                "dos fantasías opuestas —la máquina implacable y el regreso a "
                "la naturaleza— que Fisher rechaza por igual.\n\n"
                "**Qué retener.** Acelerar **qué**. Land contesta: el capital. "
                "Fisher contesta que capital y tecnología no son la misma cosa, "
                "y que confundirlos es el error fatal.\n\n"
                "**Es difícil, y está bien.** Es el texto más claro del "
                "cuadernillo, y por eso está aquí y no al final: úsalo como "
                "llave. Si *Meltdown* te dejó perdido, vuelve sobre él desde "
                "aquí — Fisher lo cita y lo explica."
            ),
        ),
    ]
}

# En derechos vigentes: no se redistribuyen, se leen de la antología.
ENLACES: dict[str, list[dict[str, str]]] = {
    "filosofia_ia/clase_1": [
        {
            "cita": "Gilles Deleuze y Félix Guattari (1972). *El Anti-Edipo*, ed. Minnesota 1983, pp. 239–240",
            "url": "",
        },
        {
            "cita": "Mark Fisher (2012). «Terminator vs Avatar», *#Accelerate*, pp. 335–346",
            "url": "",
        },
    ]
}


HOJA_DE_ESTILO = """
@page { size: letter; margin: 2.4cm 2.6cm 2.2cm; background: %(papel)s;
        @bottom-center { content: counter(page); font: 9pt system-ui; color: %(suave)s; } }
body { font: 11.5pt/1.62 Georgia, "Times New Roman", serif; color: %(tinta)s;
       background: %(papel)s; hyphens: auto; text-align: justify; }
.portadilla { page-break-after: always; padding-top: 5cm; text-align: left; }
.portadilla .modulo { font: 600 10pt system-ui; letter-spacing:.14em;
                      text-transform: uppercase; color: %(acento)s; }
.portadilla h1 { font: 700 27pt/1.2 Georgia, serif; margin:.5cm 0 .3cm; }
.portadilla .sub { font: 13pt system-ui; color: %(suave)s; }
.portadilla ol { margin: 1.6cm 0 0; padding-left: 1.1em; font: 11pt/1.7 system-ui; }
.portadilla ol b { font-weight: 600; }
.portadilla .nota { margin-top: 1.4cm; padding: .55cm .7cm; font: 10pt/1.55 system-ui;
                    color: %(suave)s; border-left: 3px solid %(acento)s; }
.lectura { page-break-before: always; }
.cabecera { border-bottom: 1.5px solid %(borde)s; padding-bottom: .45cm; margin-bottom: .8cm; }
.cabecera .num { font: 600 9.5pt system-ui; letter-spacing:.12em;
                 text-transform: uppercase; color: %(acento)s; }
.cabecera h2 { font: 700 19pt/1.25 Georgia, serif; margin:.18cm 0 .1cm; }
.cabecera .meta { font: 10pt system-ui; color: %(suave)s; }
.intro h2 { font: 700 20pt/1.25 Georgia, serif; margin: 0 0 .7cm;
            color: %(acento)s; }
.intro p, .intro li { text-indent: 0; text-align: left; }
.intro ul { margin: 0 0 .5cm; padding-left: 1.1em; }
.intro li { margin-bottom: .3em; }
.ficha { border-left: 3px solid %(acento)s; padding-left: .6cm;
         margin-bottom: .9cm; font: 10.5pt/1.55 system-ui; color: %(suave)s; }
.ficha p { margin: 0 0 .45em; text-indent: 0; text-align: left; }
.ficha p:last-child { margin-bottom: 0; }
.ficha strong { color: %(acento)s; font-weight: 600; }
.ficha em { font-style: italic; }
p { margin: 0 0 .42em; text-indent: 1.2em; }
p:first-of-type { text-indent: 0; }
.fuente { margin-top: 1cm; padding-top: .4cm; border-top: 1px solid %(borde)s;
          font: 9pt/1.5 system-ui; color: %(suave)s; text-align: left; }
.hueco { page-break-before: always; }
""" % PALETA


def _inline(texto: str) -> str:
    """Escapa el texto y aplica el enfasis de linea: **negritas** y *cursivas*."""
    t = html.escape(texto)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", t)


def _markdown_basico(md: str) -> str:
    """El subconjunto de Markdown que usan introduccion.md y las fichas.

    Parrafos, un encabezado `## `, listas con `- ` (con lineas de continuacion
    indentadas), y el enfasis de linea. Los wikilinks `[[destino]]` se reducen a
    texto: en el PDF no hay a donde enlazar, y la pagina del curso recibe el
    Markdown crudo, donde `raya` si los resuelve.
    """
    md = re.sub(r"\[\[[^\]|]+\|([^\]]+)\]\]", r"\1", md)
    md = re.sub(r"\[\[([^\]]+)\]\]", r"\1", md)
    salida = []
    for bloque in [b.strip() for b in re.split(r"\n\s*\n", md) if b.strip()]:
        lineas = bloque.splitlines()
        if lineas[0].startswith("## "):
            salida.append(f"<h2>{_inline(lineas[0][3:].strip())}</h2>")
        elif lineas[0].lstrip().startswith("- "):
            items, actual = [], []
            for linea in lineas:
                if linea.lstrip().startswith("- "):
                    if actual:
                        items.append(" ".join(actual))
                    actual = [linea.lstrip()[2:].strip()]
                else:
                    actual.append(linea.strip())
            items.append(" ".join(actual))
            celdas = "".join(f"<li>{_inline(i)}</li>" for i in items)
            salida.append(f"<ul>{celdas}</ul>")
        else:
            salida.append(f"<p>{_inline(' '.join(bloque.split()))}</p>")
    return "\n".join(salida)


def _introduccion(modulo: str) -> str:
    return (LECTURAS_DIR / modulo / "introduccion.md").read_text(encoding="utf-8")


CARTA_ANCHO, CARTA_ALTO = 612.0, 792.0  # letter, en puntos: el tamano del resto del cuadernillo


def _sustituir_huecos(destino: Path, recortes: dict[str, Path]) -> None:
    """Cambia cada pagina hueco por la pagina real del PDF externo, escalada
    a carta y centrada.

    Se busca la marca en el texto extraido con los espacios quitados: al
    extraer, el PDF puede partir la marca en varios fragmentos. Si dos marcas
    caen en la misma pagina, o si el numero de sustituciones hechas no
    coincide con el numero de paginas externas esperado, se aborta con
    ValueError en vez de dejar pasar una marca ##HUECO: visible en el PDF
    final o una pagina duplicada/perdida en silencio.

    Cada pagina externa se escala con un solo factor —
    min(CARTA_ANCHO/ancho, CARTA_ALTO/alto) — para no deformar el texto, y se
    centra en una pagina en blanco del tamano de carta.
    """
    import pypdf
    from pypdf import Transformation

    lector = pypdf.PdfReader(destino)
    externos = {i: pypdf.PdfReader(p) for i, p in recortes.items()}
    esperadas = sum(len(r.pages) for r in externos.values())
    escritor = pypdf.PdfWriter()
    sustituidas = 0
    for pagina in lector.pages:
        texto = re.sub(r"\s+", "", pagina.extract_text() or "")
        coincidencias = RE_MARCA.findall(texto)
        if len(coincidencias) > 1:
            raise ValueError(
                f"dos o mas marcas de hueco cayeron en la misma pagina: "
                f"{coincidencias}"
            )
        m = RE_MARCA.search(texto)
        if m:
            origen = externos[m.group(1)].pages[int(m.group(2))]
            ancho_o, alto_o = float(origen.mediabox.width), float(origen.mediabox.height)
            factor = min(CARTA_ANCHO / ancho_o, CARTA_ALTO / alto_o)
            tx = (CARTA_ANCHO - ancho_o * factor) / 2
            ty = (CARTA_ALTO - alto_o * factor) / 2
            centrada = pypdf.PageObject.create_blank_page(
                width=CARTA_ANCHO, height=CARTA_ALTO
            )
            centrada.merge_transformed_page(
                origen, Transformation().scale(factor).translate(tx, ty)
            )
            escritor.add_page(centrada)
            sustituidas += 1
        else:
            escritor.add_page(pagina)
    if sustituidas != esperadas:
        raise ValueError(
            f"se esperaban {esperadas} paginas externas sustituidas y se "
            f"hicieron {sustituidas}: alguna marca ##HUECO: no se reconocio"
        )
    temporal = destino.with_suffix(".tmp.pdf")
    with temporal.open("wb") as fh:
        escritor.write(fh)
    temporal.replace(destino)


def _parrafos_html(texto: str) -> str:
    bloques = [b.strip() for b in re.split(r"\n\s*\n", texto) if b.strip()]
    return "\n".join(
        f"<p>{html.escape(' '.join(b.split()))}</p>" for b in bloques
    )


# Marca de pagina hueco. El documento de WeasyPrint emite una pagina por cada
# pagina del PDF externo que va en ese lugar; despues pypdf las sustituye por
# las reales. Asi el folio corre continuo por todo el cuadernillo y las lecturas
# de edicion citada quedan en su posicion, no al final.
MARCA = "##HUECO:%s:%d##"
RE_MARCA = re.compile(r"##HUECO:([a-z0-9-]+):(\d+)##")


def _cabecera(x) -> str:
    return f"""<div class="cabecera">
    <div class="num">Lectura {x.orden}</div>
    <h2>{html.escape(x.titulo)}</h2>
    <div class="meta">{html.escape(x.autor)} · {x.anio}</div>
  </div>"""


def _seccion_lectura(l: "Lectura", texto: str) -> str:
    return f"""<section class="lectura">
  {_cabecera(l)}
  <div class="ficha">{_markdown_basico(l.introduccion)}</div>
  {_parrafos_html(texto)}
  <div class="fuente">Fuente: {html.escape(l.procedencia)}. {html.escape(l.licencia)}.</div>
</section>"""


def _seccion_externa(lp: "LecturaPDF") -> str:
    """Portadilla de la lectura anexada, seguida de sus paginas hueco."""
    paginas = lp.paginas[1] - lp.paginas[0] + 1
    huecos = "".join(
        f'<div class="hueco">{MARCA % (lp.id, i)}</div>' for i in range(paginas)
    )
    return f"""<section class="lectura">
  {_cabecera(lp)}
  <div class="ficha">{_markdown_basico(lp.introduccion)}</div>
  <div class="fuente">Se reproduce de: {html.escape(lp.edicion)}</div>
</section>{huecos}"""


def construir_html(modulo: str, lecturas: list[Lectura], textos: dict[str, str],
                   enlaces: list[dict[str, str]],
                   anexadas: list["LecturaPDF"] | None,
                   intro: str) -> str:
    """El indice de la portadilla lista TODAS las lecturas del cuadernillo, en su
    orden, incluidas las que llegan como PDF externo intercalado. Se arma
    despues de saber cuales se anexaron: antes listaba solo las de texto y
    quedaba incompleto."""
    todas = sorted(list(lecturas) + list(anexadas or []), key=lambda x: x.orden)
    indice = "\n".join(
        f"<li><b>{html.escape(x.titulo)}</b> — {html.escape(x.autor)}, {x.anio}</li>"
        for x in todas
    )
    extra = ""
    if enlaces:
        filas = "\n".join(
            f"<li>{_inline(e['cita'])}</li>" for e in enlaces
        )
        extra = (
            "<div class='nota'><b>Las dos que faltan.</b> Siguen en derechos y no "
            "se reproducen aquí. Se leen de la antología <i>#Accelerate</i> "
            "(Urbanomic, 2014) o de la edición citada; su paginación es la que "
            f"aparece en el temario.<ol>{filas}</ol></div>"
        )

    cuerpo = [
        _seccion_lectura(x, textos[x.id]) if isinstance(x, Lectura)
        else _seccion_externa(x)
        for x in todas
    ]

    titulo, subtitulo = _titulos(modulo)
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>{html.escape(titulo)}</title><style>{HOJA_DE_ESTILO}</style></head><body>
<div class="portadilla">
  <div class="modulo">Inteligencia Artificial · Otoño 2026 · ITAM</div>
  <h1>{html.escape(titulo)}</h1>
  <div class="sub">{html.escape(subtitulo)}</div>
  <ol>{indice}</ol>
  {extra}
</div>
<section class="intro">{_markdown_basico(intro)}</section>
{"".join(cuerpo)}
</body></html>"""


def _titulos(modulo: str) -> tuple[str, str]:
    return {
        "filosofia_ia/clase_1": (
            "¿Accelerate What?",
            "Filosofía de la IA · Módulo 1 — Aceleracionismo, de Marx al valle",
        )
    }.get(modulo, (modulo, ""))


def construir(modulo: str) -> Path:
    base = LECTURAS_DIR / modulo
    fuentes, salida = base / "fuentes", base / "lecturas"
    salida.mkdir(parents=True, exist_ok=True)

    lecturas = sorted(LECTURAS[modulo], key=lambda l: l.orden)
    textos: dict[str, str] = {}
    for l in lecturas:
        crudo = (fuentes / l.fuente).read_text(encoding="utf-8", errors="ignore")
        recortado = l.recorte.aplicar(crudo)
        if len(recortado.split()) < 100:
            raise ValueError(f"{l.id}: el recorte quedó en {len(recortado.split())} palabras")
        textos[l.id] = recortado
        print(f"  {l.orden}. {l.titulo[:46]:<46} {len(recortado.split()):>6} palabras")

    pdfs = sorted(PDFS.get(modulo, []), key=lambda x: x.orden)
    presentes = [lp for lp in pdfs if (fuentes / lp.fuente).is_file()]
    ausentes = [lp for lp in pdfs if lp not in presentes]
    recortes: dict[str, Path] = {}
    for lp in presentes:
        recortes[lp.id] = lp.recortar(fuentes, salida)
        print(f"  {lp.orden}. {lp.titulo[:46]:<46} {lp.paginas[0]}-{lp.paginas[1]} (PDF)")

    faltan_enlaces = [e for e in ENLACES.get(modulo, [])
                      if any(x.autor.split()[-1] in e["cita"] for x in ausentes)]
    doc = construir_html(modulo, lecturas, textos, faltan_enlaces, presentes,
                         _introduccion(modulo))
    (salida / "cuadernillo.html").write_text(doc, encoding="utf-8")

    from weasyprint import HTML
    destino = salida / f"{modulo.replace('/', '_')}_cuadernillo.pdf"
    HTML(string=doc, base_url=str(salida)).write_pdf(destino)

    if recortes:
        _sustituir_huecos(destino, recortes)
        print(f"  + {len(recortes)} lectura(s) intercalada(s) en su posición")
    for lp in ausentes:
        print(f"  · falta {lp.fuente} → se omite «{lp.titulo}» "
              f"(pp. {lp.paginas[0]}-{lp.paginas[1]})")

    import pypdf
    paginas = len(pypdf.PdfReader(destino).pages)
    print(f"\n  → {destino.relative_to(RAIZ)}  ({paginas} páginas, "
          f"{destino.stat().st_size // 1024} KB)")
    return destino


if __name__ == "__main__":
    modulo = sys.argv[1] if len(sys.argv) > 1 else "filosofia_ia/clase_1"
    if modulo not in LECTURAS:
        raise SystemExit(f"módulo desconocido: {modulo}. Opciones: {list(LECTURAS)}")
    print(f"Construyendo {modulo}\n")
    construir(modulo)
