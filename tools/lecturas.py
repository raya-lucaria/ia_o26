#!/usr/bin/env python3
"""Arma el cuadernillo de lecturas de una clase a partir de fuentes descargadas.

Toma textos planos de dominio publico, recorta la seccion que se lee en clase,
la maqueta con la paleta del curso y une todo en un solo PDF por modulo.

    python3 tools/lecturas.py filosofia_ia/clase_1

La lista de lecturas es declarativa: agregar una es agregar una entrada a
LECTURAS, no tocar el codigo. Cada entrada dice de donde sale su texto, que
tramo se recorta y por que se lee.

Depende de weasyprint (HTML a PDF) y pypdf (union). Ver tools/README.md.
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
class Lectura:
    orden: int
    id: str
    titulo: str
    autor: str
    anio: str
    fuente: str            # archivo dentro de fuentes/
    procedencia: str       # de donde se descargo
    licencia: str
    por_que: str           # que aporta a la clase
    recorte: Recorte = field(default_factory=Recorte)

    @property
    def cita(self) -> str:
        return f"{self.autor} ({self.anio}). *{self.titulo}*"


# ── Clase 1 · ¿Puede pensar una máquina? ──────────────────────────────────────
# La pregunta es tres siglos anterior a la computadora. Estas cuatro lecturas
# la muestran formulandose antes de que existiera la maquina que la volveria
# urgente, y encadenan con el hilo «esencia contra comportamiento» que abre la
# unidad de historia.

LECTURAS: dict[str, list[Lectura]] = {
    "filosofia_ia/clase_1": [
        Lectura(
            orden=1,
            id="hobbes-razon-computo",
            titulo="Leviatán, I.5 — De la razón y la ciencia",
            autor="Thomas Hobbes",
            anio="1651",
            fuente="hobbes_leviathan_en.txt",
            procedencia="Project Gutenberg, ebook 3207",
            licencia="Dominio público",
            por_que=(
                "Hobbes define razonar como computar —sumar y restar— tres siglos "
                "antes de que existiera una máquina que lo hiciera. Es el origen de "
                "la idea de que pensar podría ser un proceso mecánico."
            ),
            recorte=Recorte(
                desde=r"^CHAPTER V\. OF REASON, AND SCIENCE\.",
                hasta=r"^CHAPTER VI\.",
            ),
        ),
        Lectura(
            orden=2,
            id="descartes-prueba-lenguaje",
            titulo="Discurso del método, Quinta parte",
            autor="René Descartes",
            anio="1637",
            fuente="descartes_discurso_v_es.txt",
            procedencia="Wikisource en español, traducción de Wikisource",
            licencia="Dominio público",
            por_que=(
                "Descartes concede que el cuerpo es una máquina, y propone dos "
                "pruebas que ninguna máquina pasaría: usar el lenguaje de forma "
                "creativa y actuar por entendimiento y no por disposición. Es el "
                "test de Turing planteado al revés, y tres siglos antes."
            ),
        ),
        Lectura(
            orden=3,
            id="leibniz-molino",
            titulo="Monadología, §17 — El argumento del molino",
            autor="Gottfried Wilhelm Leibniz",
            anio="1714",
            fuente="leibniz_monadologia_en.txt",
            procedencia="Wikisource en inglés, traducción de G. M. Duncan",
            licencia="Dominio público",
            por_que=(
                "Si agrandáramos una máquina pensante hasta poder pasearnos dentro, "
                "dice Leibniz, solo veríamos piezas empujándose: nunca la percepción. "
                "Es el ancestro directo del cuarto chino de Searle."
            ),
            recorte=Recorte(desde=r"^\s*17\.", hasta=r"^\s*19\."),
        ),
        Lectura(
            orden=4,
            id="lamettrie-hombre-maquina",
            titulo="El hombre máquina (extracto)",
            autor="Julien Offray de La Mettrie",
            anio="1747",
            fuente="lamettrie_hombre_maquina_en.txt",
            procedencia="Project Gutenberg, ebook 52090",
            licencia="Dominio público",
            por_que=(
                "La Mettrie toma la máquina cartesiana y le quita la excepción: si el "
                "cuerpo es mecanismo, también la mente. Cierra el arco que Descartes "
                "abrió dejando el alma fuera."
            ),
            recorte=Recorte(desde=r"^MAN A MACHINE\.", palabras_max=2600),
        ),
    ]
}

# En derechos vigentes: no se redistribuyen, se enlazan.
ENLACES: dict[str, list[dict[str, str]]] = {
    "filosofia_ia/clase_1": [
        {
            "cita": "Alan Turing (1950). «Computing Machinery and Intelligence». *Mind* LIX(236)",
            "url": "https://redirect.cs.umbc.edu/courses/471/papers/turing.pdf",
            "por_que": (
                "Turing declara mal planteada la pregunta «¿pueden pensar las "
                "máquinas?» y la sustituye por un juego de imitación. Léelo después "
                "de Descartes: es la misma prueba del lenguaje, con el veredicto "
                "invertido."
            ),
        },
        {
            "cita": "John Searle (1980). «Minds, Brains, and Programs». *BBS* 3(3)",
            "url": "https://home.csulb.edu/~cwallis/382/readings/482/searle.minds.brains.programs.bbs.1980.pdf",
            "por_que": (
                "El cuarto chino: manipular símbolos según reglas no es entender. "
                "Es el molino de Leibniz, reescrito para la era del software."
            ),
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
.porque { font: italic 10.5pt/1.55 system-ui; color: %(suave)s;
          border-left: 3px solid %(borde)s; padding-left: .6cm; margin-bottom: .9cm; }
p { margin: 0 0 .42em; text-indent: 1.2em; }
p:first-of-type { text-indent: 0; }
.fuente { margin-top: 1cm; padding-top: .4cm; border-top: 1px solid %(borde)s;
          font: 9pt/1.5 system-ui; color: %(suave)s; text-align: left; }
""" % PALETA


def _enfasis(texto: str) -> str:
    """Escapa el texto y convierte el enfasis *asi* en cursivas reales."""
    return re.sub(r"\*([^*]+)\*", r"<em>\1</em>", html.escape(texto))


def _parrafos_html(texto: str) -> str:
    bloques = [b.strip() for b in re.split(r"\n\s*\n", texto) if b.strip()]
    return "\n".join(
        f"<p>{html.escape(' '.join(b.split()))}</p>" for b in bloques
    )


def construir_html(modulo: str, lecturas: list[Lectura], textos: dict[str, str],
                   enlaces: list[dict[str, str]]) -> str:
    indice = "\n".join(
        f"<li><b>{html.escape(l.titulo)}</b> — {html.escape(l.autor)}, {l.anio}</li>"
        for l in lecturas
    )
    extra = ""
    if enlaces:
        filas = "\n".join(
            f"<li>{_enfasis(e['cita'])}</li>" for e in enlaces
        )
        extra = (
            "<div class='nota'><b>Además, en línea.</b> Estos dos textos siguen "
            "en derechos y no se reproducen aquí; el temario los enlaza a copias "
            f"abiertas de universidades.<ol>{filas}</ol></div>"
        )

    cuerpo = []
    for l in lecturas:
        cuerpo.append(
            f"""<section class="lectura">
  <div class="cabecera">
    <div class="num">Lectura {l.orden}</div>
    <h2>{html.escape(l.titulo)}</h2>
    <div class="meta">{html.escape(l.autor)} · {l.anio}</div>
  </div>
  <div class="porque">{html.escape(l.por_que)}</div>
  {_parrafos_html(textos[l.id])}
  <div class="fuente">Fuente: {html.escape(l.procedencia)}. {html.escape(l.licencia)}.</div>
</section>"""
        )

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
{"".join(cuerpo)}
</body></html>"""


def _titulos(modulo: str) -> tuple[str, str]:
    return {
        "filosofia_ia/clase_1": (
            "¿Puede pensar una máquina?",
            "Filosofía de la IA · Clase 1 — La pregunta antes de la computadora",
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

    doc = construir_html(modulo, lecturas, textos, ENLACES.get(modulo, []))
    (salida / "cuadernillo.html").write_text(doc, encoding="utf-8")

    from weasyprint import HTML
    destino = salida / f"{modulo.replace('/', '_')}_cuadernillo.pdf"
    HTML(string=doc, base_url=str(salida)).write_pdf(destino)

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
