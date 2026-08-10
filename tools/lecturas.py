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


# ── Módulo 1 · ¿Accelerate What? ──────────────────────────────────────────────
# El temario pide seis lecturas con la paginación de la antología #Accelerate
# (Urbanomic, 2014). Cuatro existen en fuentes primarias abiertas y van en el
# cuadernillo; dos siguen en derechos y van enlazadas en ENLACES. El texto es el
# mismo; la numeración de páginas es la de la antología y no la de aquí.

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
            por_que=(
                "Marx describe la máquina que absorbe el saber colectivo y vuelve "
                "marginal al obrero. De aquí sale el «general intellect», la noción "
                "que el aceleracionismo recogerá siglo y medio después para "
                "preguntarse si la tecnología puede rebasar al capital que la produjo."
            ),
            recorte=Recorte(desde=r"automatic system of machinery", palabras_max=4600),
        ),
        Lectura(
            orden=2,
            id="ccru-swarmachines",
            titulo="Swarmachines",
            autor="CCRU",
            anio="1996",
            fuente="ccru_swarmachines_en.txt",
            procedencia="Cybernetic Culture Research Unit · ccru.net",
            licencia="Publicado abiertamente por el propio colectivo",
            por_que=(
                "El CCRU lee la insurrección como enjambre: no un sujeto que dirige, "
                "sino un proceso distribuido que se propaga. Es el puente entre la "
                "teoría de sistemas y la política que define al aceleracionismo."
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
            por_que=(
                "El texto fundacional del aceleracionismo de derecha: el capital como "
                "proceso autónomo que se desmantela a sí mismo hacia adelante. Léelo "
                "junto al mapa ideológico de la unidad de historia — es la esquina de "
                "acelerar sin frenos."
            ),
        ),
        Lectura(
            orden=4,
            id="barbrook-cameron-californian",
            titulo="La ideología californiana",
            autor="Richard Barbrook y Andy Cameron",
            anio="1995",
            fuente="barbrook_cameron_californian_ideology_en.txt",
            procedencia="imaginaryfutures.net, sitio de los autores",
            licencia="Publicado abiertamente por los autores",
            por_que=(
                "La crítica que nombró la fusión de contracultura y libre mercado en "
                "Silicon Valley. Escrito en 1995, describe con precisión incómoda el "
                "e/acc de 2026: es el antecedente directo de la sección de "
                "aceleracionismos de la unidad de historia."
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
            "por_que": (
                "Dos páginas. El pasaje donde proponen no retirarse del proceso "
                "capitalista sino acelerarlo: la frase que el aceleracionismo tomó "
                "como divisa, casi siempre fuera de su contexto."
            ),
        },
        {
            "cita": "Mark Fisher (2012). «Terminator vs Avatar», *#Accelerate*, pp. 335–346",
            "url": "",
            "por_que": (
                "Fisher recupera a Land para la izquierda: acepta el diagnóstico y "
                "rechaza la conclusión. Cierra el módulo porque responde directamente "
                "a Meltdown."
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
            "<div class='nota'><b>Las dos que faltan.</b> Siguen en derechos y no "
            "se reproducen aquí. Se leen de la antología <i>#Accelerate</i> "
            "(Urbanomic, 2014) o de la edición citada; su paginación es la que "
            f"aparece en el temario.<ol>{filas}</ol></div>"
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
