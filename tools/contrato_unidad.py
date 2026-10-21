"""Contrato de lectura medible de una unidad: biblioteca y CLI.

    python3 tools/contrato_unidad.py course/7_juegos            # informe legible
    python3 tools/contrato_unidad.py course/7_juegos --json     # lista de hallazgos
    python3 tools/contrato_unidad.py course/7_juegos --estricto # sale con 1 si hay alta/media

Mide las páginas `.md` de una unidad (o de una sola clase) y devuelve
hallazgos `archivo:línea`, cada uno con regla, valor y severidad. No corrige
nada. Las páginas que no mide: `*_tarea.md` (las dispara el usuario) y todo lo
que vive bajo un directorio de soporte (`_official`, `_assets`, `_drafts`, …).

Las métricas son obligatorias solo para las unidades de `UNIDADES_CONTRATO`
(opt-in): `test_contrato_unidad.py` exige cero hallazgos alta/media en ellas.
Las demás se pueden auditar con el CLI, pero su deuda no rompe la suite.

Reglas, con su severidad
------------------------
=========================  =========  ==========================================
regla                      severidad  qué mide
=========================  =========  ==========================================
imagen-fuera-de-figure     alta       `![…](…)` sin un `::: figure` que la envuelva
ejercicio-respuestas       alta       un ejercicio con ≠ 1 `::: answer of=` suyo
of-sin-ejercicio           alta       hint/answer sin `of=` o cuyo `of=` no es un
                                      exercise/problem de la misma página
ejercicio-sin-pista        media      `::: exercise` sin ningún `::: hint of=` suyo
                                      (media, no alta: el script no distingue un
                                      micro de un paso, que puede ir sin pista,
                                      ver referencias/ejercicios.md § Excepciones)
orden-ejercicio            media      no va exercise → hint(s) → answer
frase-larga                media      una frase > `frase_max` palabras
frases-p90                 media      el p90 de las frases de la página > `frase_p90`
parrafo-largo              media      un párrafo o ítem de lista > `parrafo_max`
tabla-ancha                media      columnas > `tabla_columnas` (trazas:
                                      > `tabla_columnas_traza`)
palabras-por-minuto        media      palabras sin hint/answer ÷ estimated_time
                                      > `ppm_max`
negrita-parrafo            baja       un párrafo con > `negrita_max` negritas
negrita-media              baja       media de negritas por párrafo > `negrita_media`
sin-estimated-time         aviso      la página no declara un tiempo legible
suma-minutos               aviso      páginas de una clase ≠ índice de la clase, o
                                      clases ≠ índice de la unidad
=========================  =========  ==========================================

El parser (`parsear`)
---------------------
Recorre la página renglón por renglón con una pila de directivas:

- **Fuera de la prosa:** el frontmatter, los bloques de código (```` ``` ```` y
  `~~~`), las fórmulas `$$ … $$` (de un renglón o de varios), los comentarios
  HTML, los encabezados `#`, las reglas horizontales y las tablas (cada renglón
  que empieza con `|`). Todo lo que está dentro de `::: figure` o `::: table`
  tampoco es prosa: es leyenda o tabla.
- **Directivas:** `::: nombre {#id of="…" title="…"}` abre y `:::` solo cierra;
  se anidan. Los títulos de directiva no cuentan como prosa; su contenido sí
  (salvo figure/table), con la pila como contexto para saber si un párrafo vive
  dentro de un `hint` o un `answer`.
- **Párrafos:** renglones contiguos de prosa; un renglón en blanco los corta.
- **Listas:** cada ítem (`-`, `*`, `+`, `1.`, `1)`) es su **propia unidad**, con
  sus renglones de continuación sangrados; un ítem anidado abre otra unidad.
  Así una lista de cinco renglones cortos no se mide como un párrafo de cinco
  renglones, y un ítem largo sí se detecta. Para la media de negritas cada ítem
  cuenta como un párrafo.
- **Palabras:** antes de contar, `$…$` y `` `…` `` valen una palabra, un enlace
  `[texto](url)` o `[[id|texto]]` vale su texto, `@id` vale una palabra, y se
  quitan las marcas de énfasis y las etiquetas HTML. Una palabra es un trozo
  separado por espacios que tiene al menos una letra o dígito.
- **Frases:** se corta tras `.`, `!`, `?` o `…` seguidos de espacio y de
  mayúscula, dígito o signo de apertura (`¿`, `¡`, `«`, `(`); las abreviaturas
  de `ABREVIATURAS` no cortan. Un ítem de lista sin punto es una frase.
- **Negritas:** pares `**…**` (o `__…__`) en el texto crudo de la unidad.

Excepciones del contrato (`referencias/lectura.md`, «Excepciones»)
------------------------------------------------------------------
- **«Lo que traes» y «Lo que hay que llevarse»** son repetición útil y no
  cuentan para ningún tope de prosa: ni frases (`frase-larga`, `frases-p90`),
  ni `parrafo-largo`, ni negritas (`negrita-parrafo`, `negrita-media`), ni
  `palabras-por-minuto`. Hay dos formas:

  - una **sección** cuyo encabezado (de cualquier nivel) empieza con «Lo que
    traes» o «Lo que hay que llevarse»: todo lo que sigue hasta el próximo
    encabezado del mismo nivel o de uno mayor (menos `#`);
  - una **tarjeta en cita**: el bloque de renglones `>` contiguos cuyo primer
    renglón con texto empieza con `**Lo que traes`. La tarjeta termina en el
    primer renglón que no es cita (un renglón en blanco sin `>` la cierra).

  El parser no las descarta: marca sus unidades con `excluida=True` y las
  métricas de prosa las saltan. Las tablas, imágenes y directivas que vivan
  ahí se siguen midiendo (`tabla-ancha`, `imagen-fuera-de-figure`, ejercicios):
  la excepción es de lectura, no de estructura.
- **`**Piensa: …?**`**: una negrita cuyo contenido empieza con «Piensa:» y
  termina en «?» no cuenta como negrita, ni para `negrita-parrafo` ni para
  `negrita-media`; y una unidad que no tiene más negritas que la pregunta
  tampoco entra al denominador de la media (si entrara con cero, diluiría la
  media de las demás). La pregunta sí cuenta como frase, como párrafo y como
  palabras: la excepción es solo de negrita. El «uno por `##` explicativo» no
  se verifica aquí.

Criterios documentados
----------------------
- **Traza** (tope de columnas `tabla_columnas_traza`): una tabla cuya primera
  columna se llama `#` (las trazas del curso numeran sus filas, y los tramos
  sueltos que siguen a la primera repiten ese encabezado), o una tabla dentro
  de un `::: table` cuyo `id` o `title` contiene «traza». Las columnas se
  cuentan en el renglón separador (`|---|---:|`), que no lleva `|` dentro de
  fórmulas.
- **Insignias:** una imagen envuelta en un enlace, `[![Abrir en Colab](…)](…)`,
  es un botón y no una figura: no cuenta para `imagen-fuera-de-figure`.
- **Citas:** el `>` inicial se quita antes de todo, así que una tabla o una
  lista dentro de una cita se miden como tabla o lista.
- **Palabras por minuto:** cuenta las palabras de prosa de la página fuera de
  hint/answer (las tablas, el código y las fórmulas no cuentan) y las divide
  entre `estimated_time` en minutos (`20m`, `1h`, `2h25m`, `8h`, `90min`). El
  tipo de página no está en el frontmatter, así que hay **un solo tope por
  unidad**, `ppm_max` (90 por omisión, sobreescribible en
  `UMBRALES_POR_UNIDAD`). No se mide en los `0_index.md`: su tiempo es la suma
  de la clase, no el de su propia lectura.
- **Suma de minutos:** si la ruta tiene subdirectorios con `0_index.md`, cada
  uno es una clase: sus páginas (sin `0_index.md` ni `*_tarea.md`) deben sumar
  el `estimated_time` del índice de la clase, y las clases el del índice de la
  unidad (las páginas sueltas de la unidad, como `A_notacion.md`, no entran).
  Si no hay subdirectorios, la ruta misma es la clase. Se reporta como «aviso»
  porque no todas las unidades declaran así sus tiempos.
- **Página:** los hallazgos de página entera (p90, media de negritas,
  palabras por minuto, suma de minutos) se anclan a la línea 1.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

UMBRALES = {
    "frase_p90": 22,
    "frase_max": 40,
    "negrita_media": 1.2,
    "negrita_max": 3,
    "parrafo_max": 70,
    "tabla_columnas": 5,
    "tabla_columnas_traza": 7,
    "ppm_max": 90,
}

# Override por unidad, con la ruta relativa a la raíz del repo como clave:
# {"course/8_unidad": {"ppm_max": 110}}. Solo cambia las claves que nombra.
# Markov nace con tablas de 4 columnas (caben a 390 px) y 80 palabras por
# minuto. `umbrales_para` busca la clave exacta, así que cada clase repite la
# entrada de la unidad.
_UMBRALES_MARKOV = {"tabla_columnas": 4, "tabla_columnas_traza": 4, "ppm_max": 80}
UMBRALES_POR_UNIDAD: dict[str, dict] = {
    "course/8_markov": _UMBRALES_MARKOV,
    "course/8_markov/1_que_es_una_cadena": _UMBRALES_MARKOV,
    "course/8_markov/2_a_la_larga": _UMBRALES_MARKOV,
}

# Unidades donde el contrato es obligatorio (opt-in). Arranca vacía: las
# unidades escritas antes del contrato tienen deuda conocida y no deben romper
# la suite. Una unidad entra aquí cuando ya da cero hallazgos alta/media.
UNIDADES_CONTRATO: list[str] = ["course/8_markov"]

SEVERIDAD = {
    "imagen-fuera-de-figure": "alta",
    "ejercicio-respuestas": "alta",
    "of-sin-ejercicio": "alta",
    "ejercicio-sin-pista": "media",   # micro de un paso puede ir sin pista
    "orden-ejercicio": "media",
    "frase-larga": "media",
    "frases-p90": "media",
    "parrafo-largo": "media",
    "tabla-ancha": "media",
    "palabras-por-minuto": "media",
    "negrita-parrafo": "baja",
    "negrita-media": "baja",
    "sin-estimated-time": "aviso",
    "suma-minutos": "aviso",
}
ORDEN_SEVERIDAD = ["alta", "media", "baja", "aviso"]

DIRECTORIOS_DE_SOPORTE = {"_official", "_assets", "_drafts", "_reviewed", "_partials", "_raya"}
DIRECTIVAS_SIN_PROSA = {"figure", "table"}
DIRECTIVAS_FUERA_DE_TIEMPO = {"hint", "answer"}
ABREVIATURAS = ("p. ej.", "e. g.", "i. e.", "etc.", "núm.", "pp.", "p.", "vs.", "cap.", "fig.", "Dr.", "Dra.")


# --------------------------------------------------------------------------
# Estructuras
# --------------------------------------------------------------------------

@dataclass
class Directiva:
    nombre: str
    linea: int
    id: str | None = None
    of: str | None = None
    title: str | None = None
    fin: int | None = None


@dataclass
class Unidad:
    """Un párrafo o un ítem de lista: lo que se mide como bloque de lectura."""
    tipo: str            # "parrafo" | "lista"
    linea: int
    texto: str
    contexto: tuple      # nombres de las directivas que lo envuelven
    excluida: bool = False   # vive en «Lo que traes» / «Lo que hay que llevarse»


@dataclass
class Tabla:
    linea: int
    columnas: int
    encabezado: str
    directiva: Directiva | None


@dataclass
class Imagen:
    linea: int
    en_figure: bool


@dataclass
class Pagina:
    frontmatter: dict = field(default_factory=dict)
    linea_frontmatter: dict = field(default_factory=dict)
    unidades: list = field(default_factory=list)
    tablas: list = field(default_factory=list)
    imagenes: list = field(default_factory=list)
    directivas: list = field(default_factory=list)


@dataclass
class Hallazgo:
    archivo: str
    linea: int
    regla: str
    valor: str
    severidad: str

    def __str__(self):
        return f"{self.archivo}:{self.linea} [{self.severidad}] {self.regla}: {self.valor}"


# --------------------------------------------------------------------------
# Parser
# --------------------------------------------------------------------------

RE_ABRE = re.compile(r"^\s*:::\s*([A-Za-z][\w-]*)\s*(\{.*\})?\s*$")
RE_CIERRA = re.compile(r"^\s*:::\s*$")
RE_CERCA = re.compile(r"^\s*(```|~~~)")
RE_ITEM = re.compile(r"^(\s*)(?:[-*+]|\d+[.)])\s+(.*)$")
RE_ENCABEZADO = re.compile(r"^\s{0,3}#{1,6}\s")
RE_REGLA_H = re.compile(r"^\s{0,3}([-*_])(\s*\1){2,}\s*$")
RE_IMAGEN = re.compile(r"!\[[^\]]*\]\([^)]*\)")
RE_CITA = re.compile(r"^\s*(?:>\s?)+")
RE_SEPARADOR = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
RE_ENCABEZADO_NIVEL = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
RE_SECCION_EXCLUIDA = re.compile(r"^(?:\*\*|__)?\s*Lo que (?:traes|hay que llevarse)\b", re.IGNORECASE)
RE_TARJETA_EXCLUIDA = re.compile(r"^(?:\*\*|__)\s*Lo que traes\b", re.IGNORECASE)
RE_NEGRITA = re.compile(r"\*\*(?=\S)(.+?)(?<=\S)\*\*|__(?=\S)(.+?)(?<=\S)__")


def _atributos(llaves: str | None) -> dict:
    if not llaves:
        return {}
    attrs = {k: v for k, v in re.findall(r'([\w-]+)="([^"]*)"', llaves)}
    m = re.search(r"#([\w-]+)", llaves)
    if m:
        attrs["id"] = m.group(1)
    return attrs


def _frontmatter(lineas: list[str]) -> tuple[dict, dict, int]:
    """(datos, {clave: línea}, índice del primer renglón del cuerpo)."""
    if not lineas or lineas[0].strip() != "---":
        return {}, {}, 0
    for i in range(1, len(lineas)):
        if lineas[i].strip() == "---":
            bloque = lineas[1:i]
            try:
                import yaml
                datos = yaml.safe_load("\n".join(bloque)) or {}
            except Exception:
                datos = {}
                for r in bloque:
                    m = re.match(r"^(\w+):\s*(.*)$", r)
                    if m:
                        datos[m.group(1)] = m.group(2).strip().strip('"')
            pos = {}
            for j, r in enumerate(bloque, start=2):
                m = re.match(r"^(\w+):", r)
                if m:
                    pos.setdefault(m.group(1), j)
            return (datos if isinstance(datos, dict) else {}), pos, i + 1
    return {}, {}, 0


def parsear(texto: str) -> Pagina:
    """Parte una página en unidades de prosa, tablas, imágenes y directivas."""
    lineas = texto.splitlines()
    fm, pos_fm, inicio = _frontmatter(lineas)
    pag = Pagina(frontmatter=fm, linea_frontmatter=pos_fm)

    pila: list[Directiva] = []
    actual: dict | None = None        # unidad en construcción
    tabla: list | None = None         # [linea, renglones]
    en_cerca = en_math = en_comentario = False
    nivel_excluido: int | None = None  # nivel del encabezado «Lo que traes…» abierto
    en_tarjeta = False                 # dentro de una cita «**Lo que traes…»
    tarjeta_por_abrir = False          # cita recién abierta, aún sin texto
    en_cita = False                    # el renglón anterior era cita

    def excluida():
        return nivel_excluido is not None or en_tarjeta

    def contexto():
        return tuple(d.nombre for d in pila)

    def sin_prosa():
        return any(d.nombre in DIRECTIVAS_SIN_PROSA for d in pila)

    def cerrar_unidad():
        nonlocal actual
        if actual and actual["texto"].strip():
            pag.unidades.append(Unidad(actual["tipo"], actual["linea"],
                                       actual["texto"].strip(), actual["contexto"],
                                       actual["excluida"]))
        actual = None

    def cerrar_tabla():
        nonlocal tabla
        if tabla:
            n_linea, renglones = tabla
            sep = next((r for r in renglones[1:2] if RE_SEPARADOR.match(r)), None)
            base = sep if sep is not None else renglones[0]
            columnas = len(base.strip().strip("|").split("|"))
            directiva = next((d for d in reversed(pila) if d.nombre == "table"), None)
            pag.tablas.append(Tabla(n_linea, columnas, renglones[0].strip(), directiva))
        tabla = None

    for i in range(inicio, len(lineas)):
        n = i + 1
        crudo = lineas[i]
        s = crudo.strip()

        if en_cerca:
            if RE_CERCA.match(crudo):
                en_cerca = False
            continue
        if en_math:
            if "$$" in s:
                en_math = False
            continue
        if en_comentario:
            if "-->" in s:
                en_comentario = False
            continue

        if RE_CERCA.match(crudo):
            cerrar_unidad(); cerrar_tabla()
            en_cerca = True
            continue
        if s.startswith("$$"):
            cerrar_unidad(); cerrar_tabla()
            if not (len(s) > 2 and s.endswith("$$") and s != "$$" and s.count("$$") >= 2):
                en_math = True
            continue
        if s.startswith("<!--"):
            cerrar_unidad(); cerrar_tabla()
            if "-->" not in s:
                en_comentario = True
            continue

        m = RE_ABRE.match(crudo)
        if m:
            cerrar_unidad(); cerrar_tabla()
            attrs = _atributos(m.group(2))
            d = Directiva(m.group(1), n, attrs.get("id"), attrs.get("of"), attrs.get("title"))
            pag.directivas.append(d)
            pila.append(d)
            continue
        if RE_CIERRA.match(crudo):
            cerrar_unidad(); cerrar_tabla()
            if pila:
                pila.pop().fin = n
            continue

        cita = RE_CITA.match(crudo)
        if cita:
            crudo = crudo[cita.end():]
            s = crudo.strip()
            if not en_cita:
                en_cita = tarjeta_por_abrir = True
            if tarjeta_por_abrir and s:
                tarjeta_por_abrir = False
                if RE_TARJETA_EXCLUIDA.match(s):
                    cerrar_unidad()
                    en_tarjeta = True
        elif en_cita:
            if en_tarjeta:
                cerrar_unidad()
            en_cita = en_tarjeta = tarjeta_por_abrir = False
        if not s:
            cerrar_unidad(); cerrar_tabla()
            continue

        for im in RE_IMAGEN.finditer(crudo):
            insignia = crudo[:im.start()].endswith("[") and crudo[im.end():].startswith("](")
            if not insignia:
                pag.imagenes.append(Imagen(n, any(d.nombre == "figure" for d in pila)))

        if s.startswith("|"):
            cerrar_unidad()
            if tabla is None:
                tabla = [n, []]
            tabla[1].append(s)
            continue
        cerrar_tabla()

        if RE_ENCABEZADO.match(crudo):
            cerrar_unidad()
            me = RE_ENCABEZADO_NIVEL.match(crudo)
            nivel = len(me.group(1)) if me else 6
            if nivel_excluido is not None and nivel <= nivel_excluido:
                nivel_excluido = None
            if nivel_excluido is None and me and RE_SECCION_EXCLUIDA.match(me.group(2)):
                nivel_excluido = nivel
            continue
        if RE_REGLA_H.match(crudo):
            cerrar_unidad()
            continue
        if sin_prosa():
            continue

        linea_texto = RE_IMAGEN.sub("", crudo)
        if not linea_texto.strip():
            cerrar_unidad()
            continue

        mi = RE_ITEM.match(linea_texto)
        if mi:
            cerrar_unidad()
            actual = {"tipo": "lista", "linea": n, "texto": mi.group(2), "contexto": contexto(),
                      "excluida": excluida()}
            continue
        if actual is None:
            actual = {"tipo": "parrafo", "linea": n, "texto": linea_texto.strip(), "contexto": contexto(),
                      "excluida": excluida()}
        else:
            actual["texto"] += " " + linea_texto.strip()

    cerrar_unidad(); cerrar_tabla()
    return pag


# --------------------------------------------------------------------------
# Palabras, frases, negritas, minutos
# --------------------------------------------------------------------------

def normalizar(texto: str) -> str:
    """El texto como se lee: fórmulas, código y enlaces reducidos."""
    t = re.sub(r"\$[^$]+\$", " X ", texto)
    t = re.sub(r"`[^`]*`", " X ", t)
    t = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[\[([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"(?<![\w@])@[\w-]+", " X ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = t.replace("**", "").replace("__", "")
    t = re.sub(r"(?<!\w)[*_](?=\S)|(?<=\S)[*_](?!\w)", "", t)
    return re.sub(r"\s+", " ", t).strip()


def palabras(texto: str) -> int:
    return sum(1 for w in normalizar(texto).split() if re.search(r"\w", w))


def frases(texto: str) -> list[str]:
    t = normalizar(texto)
    for abr in ABREVIATURAS:
        t = t.replace(abr, abr.replace(".", "\x00"))
    trozos = re.split(r"(?<=[.!?…])\s+(?=[¿¡«\"(\[]?[A-ZÁÉÍÓÚÑÜ0-9])", t)
    return [f.replace("\x00", ".") for f in trozos if re.search(r"\w", f)]


def es_piensa(contenido: str) -> bool:
    """El contenido de una negrita `**Piensa: …?**` (la excepción del contrato)."""
    c = contenido.strip()
    return c.startswith("Piensa:") and c.endswith("?")


def negritas(texto: str, con_piensa: bool = True) -> int:
    """Pares de negrita; con `con_piensa=False` no cuenta los `**Piensa: …?**`."""
    return sum(1 for m in RE_NEGRITA.finditer(texto)
               if con_piensa or not es_piensa(m.group(1) or m.group(2)))


def minutos(valor) -> int | None:
    """'20m', '1h', '2h25m', '8h', '90min', 45 -> minutos; None si no se lee."""
    if valor is None:
        return None
    if isinstance(valor, (int, float)) and not isinstance(valor, bool):
        return int(valor)
    m = re.fullmatch(r"\s*(?:(\d+)\s*h)?\s*(?:(\d+)\s*(?:m|min))?\s*", str(valor))
    if not m or not (m.group(1) or m.group(2)):
        return None
    return int(m.group(1) or 0) * 60 + int(m.group(2) or 0)


def percentil_90(valores: list[int]) -> int:
    """Percentil 90 por rango más cercano."""
    orden = sorted(valores)
    return orden[max(0, math.ceil(0.9 * len(orden)) - 1)]


# --------------------------------------------------------------------------
# Métricas
# --------------------------------------------------------------------------

def umbrales_para(unidad: str | Path | None) -> dict:
    u = dict(UMBRALES)
    if unidad is not None:
        clave = _relativa(Path(unidad))
        u.update(UMBRALES_POR_UNIDAD.get(clave, {}))
    return u


def _h(archivo, linea, regla, valor):
    return Hallazgo(archivo, linea, regla, valor, SEVERIDAD[regla])


def es_traza(tabla: Tabla) -> bool:
    if tabla.encabezado.strip("| ").split("|")[0].strip() == "#":
        return True
    d = tabla.directiva
    return d is not None and "traza" in f"{d.id or ''} {d.title or ''}".lower()


def medir_pagina(texto: str, archivo: str, umbrales: dict | None = None,
                 es_indice: bool = False) -> list[Hallazgo]:
    """Todas las métricas de una página salvo la suma de minutos."""
    u = umbrales or UMBRALES
    pag = parsear(texto)
    out: list[Hallazgo] = []
    prosa = [un for un in pag.unidades if not un.excluida]

    # Frases
    largos = []
    for un in prosa:
        for f in frases(un.texto):
            n = palabras(f)
            largos.append(n)
            if n > u["frase_max"]:
                out.append(_h(archivo, un.linea, "frase-larga",
                              f"{n} palabras > {u['frase_max']}: «{f[:60]}…»"))
    if largos:
        p90 = percentil_90(largos)
        if p90 > u["frase_p90"]:
            out.append(_h(archivo, 1, "frases-p90",
                          f"p90 = {p90} palabras > {u['frase_p90']} ({len(largos)} frases)"))

    # Párrafos y negritas
    cuentas = []
    for un in prosa:
        n = palabras(un.texto)
        if n > u["parrafo_max"]:
            out.append(_h(archivo, un.linea, "parrafo-largo",
                          f"{n} palabras > {u['parrafo_max']} ({un.tipo})"))
        b = negritas(un.texto, con_piensa=False)
        if b or negritas(un.texto) == 0:
            cuentas.append(b)   # una unidad que solo es «Piensa» no diluye la media
        if b > u["negrita_max"]:
            out.append(_h(archivo, un.linea, "negrita-parrafo", f"{b} negritas > {u['negrita_max']}"))
    if cuentas:
        media = sum(cuentas) / len(cuentas)
        if media > u["negrita_media"]:
            out.append(_h(archivo, 1, "negrita-media",
                          f"{media:.2f} negritas por párrafo > {u['negrita_media']} ({len(cuentas)} párrafos)"))

    # Tablas
    for t in pag.tablas:
        traza = es_traza(t)
        tope = u["tabla_columnas_traza"] if traza else u["tabla_columnas"]
        if t.columnas > tope:
            out.append(_h(archivo, t.linea, "tabla-ancha",
                          f"{t.columnas} columnas > {tope}{' (traza)' if traza else ''}"))

    # Imágenes
    for im in pag.imagenes:
        if not im.en_figure:
            out.append(_h(archivo, im.linea, "imagen-fuera-de-figure", "imagen sin ::: figure"))

    out.extend(_ejercicios(pag, archivo))

    # Palabras por minuto
    if not es_indice:
        mins = minutos(pag.frontmatter.get("estimated_time"))
        if mins is None or mins <= 0:
            out.append(_h(archivo, 1, "sin-estimated-time",
                          f"estimated_time ilegible: {pag.frontmatter.get('estimated_time')!r}"))
        else:
            total = sum(palabras(un.texto) for un in prosa
                        if not set(un.contexto) & DIRECTIVAS_FUERA_DE_TIEMPO)
            ppm = total / mins
            if ppm > u["ppm_max"]:
                out.append(_h(archivo, pag.linea_frontmatter.get("estimated_time", 1),
                              "palabras-por-minuto",
                              f"{ppm:.0f} ppm > {u['ppm_max']} ({total} palabras / {mins} min)"))
    return out


def _ejercicios(pag: Pagina, archivo: str) -> list[Hallazgo]:
    out = []
    ejercicios = [d for d in pag.directivas if d.nombre == "exercise"]
    objetivos = {d.id for d in pag.directivas if d.nombre in ("exercise", "problem") and d.id}
    pistas = [d for d in pag.directivas if d.nombre == "hint"]
    respuestas = [d for d in pag.directivas if d.nombre == "answer"]

    for d in pistas + respuestas:
        if not d.of or d.of not in objetivos:
            out.append(_h(archivo, d.linea, "of-sin-ejercicio",
                          f"{d.nombre} #{d.id} of={d.of!r} no es un ejercicio de la página"))

    for e in ejercicios:
        mis_pistas = [p for p in pistas if e.id and p.of == e.id]
        mis_resp = [r for r in respuestas if e.id and r.of == e.id]
        if not mis_pistas:
            out.append(_h(archivo, e.linea, "ejercicio-sin-pista", f"#{e.id} sin ::: hint"))
        if len(mis_resp) != 1:
            out.append(_h(archivo, e.linea, "ejercicio-respuestas",
                          f"#{e.id} tiene {len(mis_resp)} ::: answer (debe ser 1)"))
        fuera = [p for p in mis_pistas if p.linea < e.linea]
        fuera += [r for r in mis_resp if r.linea < e.linea]
        if mis_resp:
            fuera += [p for p in mis_pistas if p.linea > mis_resp[0].linea]
        for d in fuera:
            out.append(_h(archivo, d.linea, "orden-ejercicio",
                          f"{d.nombre} #{d.id} fuera del orden exercise → hint(s) → answer de #{e.id}"))
    return out


# --------------------------------------------------------------------------
# Unidad
# --------------------------------------------------------------------------

def _relativa(ruta: Path) -> str:
    ruta = ruta.resolve()
    try:
        return ruta.relative_to(RAIZ).as_posix()
    except ValueError:
        return ruta.as_posix()


def es_medible(ruta: Path) -> bool:
    return (ruta.suffix == ".md"
            and not ruta.name.endswith("_tarea.md")
            and not set(ruta.parts) & DIRECTORIOS_DE_SOPORTE)


def paginas_de(unidad: Path) -> list[Path]:
    return sorted(p for p in unidad.rglob("*.md") if es_medible(p.relative_to(unidad)))


def _estimado(pagina: Path) -> int | None:
    fm, _, _ = _frontmatter(pagina.read_text(encoding="utf-8").splitlines())
    return minutos(fm.get("estimated_time"))


def sumas_de_minutos(unidad: Path) -> list[Hallazgo]:
    out = []
    clases = sorted(p for p in unidad.iterdir()
                    if p.is_dir() and p.name not in DIRECTORIOS_DE_SOPORTE
                    and not p.name.startswith((".", "_")) and (p / "0_index.md").exists())

    def cuadrar(indice: Path, partes: list[Path], que: str):
        declarado = _estimado(indice) if indice.exists() else None
        valores = [_estimado(p) for p in partes]
        if declarado is None or not partes or None in valores:
            return
        if sum(valores) != declarado:
            out.append(_h(_relativa(indice), 1, "suma-minutos",
                          f"{que} suman {sum(valores)} min; el índice declara {declarado} min"))

    if not clases:
        paginas = [p for p in unidad.glob("*.md") if es_medible(p) and p.name != "0_index.md"]
        cuadrar(unidad / "0_index.md", sorted(paginas), "las páginas")
        return out
    for c in clases:
        paginas = [p for p in c.glob("*.md") if es_medible(p) and p.name != "0_index.md"]
        cuadrar(c / "0_index.md", sorted(paginas), "las páginas de la clase")
    cuadrar(unidad / "0_index.md", [c / "0_index.md" for c in clases], "las clases")
    return out


def auditar_unidad(unidad: str | Path, umbrales: dict | None = None) -> list[Hallazgo]:
    """Hallazgos de todas las páginas medibles de `unidad` (unidad o clase)."""
    ruta = Path(unidad)
    if not ruta.is_absolute():
        ruta = (Path.cwd() / ruta) if (Path.cwd() / ruta).exists() else RAIZ / ruta
    ruta = ruta.resolve()
    if not ruta.is_dir():
        raise FileNotFoundError(f"no es un directorio: {unidad}")
    u = umbrales or umbrales_para(ruta)
    out = []
    for p in paginas_de(ruta):
        out.extend(medir_pagina(p.read_text(encoding="utf-8"), _relativa(p), u,
                                es_indice=p.name == "0_index.md"))
    out.extend(sumas_de_minutos(ruta))
    return out


def resumen(hallazgos: list[Hallazgo]) -> dict:
    return {
        "por_severidad": {s: sum(1 for h in hallazgos if h.severidad == s) for s in ORDEN_SEVERIDAD},
        "por_regla": dict(sorted(Counter(h.regla for h in hallazgos).items())),
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Mide el contrato de lectura de una unidad.")
    ap.add_argument("unidad", help="directorio de la unidad o de una clase, p. ej. course/7_juegos")
    ap.add_argument("--json", action="store_true", help="imprime los hallazgos como JSON")
    ap.add_argument("--estricto", action="store_true", help="sale con 1 si hay hallazgos alta o media")
    args = ap.parse_args(argv)

    hallazgos = auditar_unidad(args.unidad)
    hallazgos.sort(key=lambda h: (ORDEN_SEVERIDAD.index(h.severidad), h.archivo, h.linea))
    if args.json:
        print(json.dumps({"hallazgos": [asdict(h) for h in hallazgos], "resumen": resumen(hallazgos)},
                         ensure_ascii=False, indent=2))
    else:
        for h in hallazgos:
            print(h)
        r = resumen(hallazgos)
        print("\n" + " · ".join(f"{s}: {n}" for s, n in r["por_severidad"].items()))
        for regla, n in r["por_regla"].items():
            print(f"  {regla:<24} {n:>4}  ({SEVERIDAD[regla]})")
    graves = any(h.severidad in ("alta", "media") for h in hallazgos)
    return 1 if args.estricto and graves else 0


if __name__ == "__main__":
    sys.exit(main())
