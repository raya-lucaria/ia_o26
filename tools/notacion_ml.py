"""Linter de notación de la unidad 9 (contrato §4.7, D-005, D-015).

Revisa las páginas de course/9_aprendizaje_maquina/ y los guiones
tools/cuadernos_ml/*.texto.md con dos listas:

- **Lista negra común** (falla en cualquier clase): `\\boldsymbol`, `\\hat`,
  λ y alpha (salvo la nota única de `ml-c3-def-lagrangeano-capacidad`),
  «lagrangiano», «outlier» (salvo «no es un outlier»), SMOTE o
  sobremuestreo (salvo en `ml-c4-obs-por-que-no-remuestrear`), «no lineal»
  en la misma oración que «polinomio» o «grado», y `\\log` sin subíndice.
- **Lista blanca por clase de presentación.** Cada macro de LaTeX y cada
  letra griega tiene que estar en la lista y no aparecer antes de la clase
  que la presenta. La lista es la común de abajo (contrato §4.1–§4.3: lo
  heredado vale desde la clase 0) más `tools/datos/notacion_ml/cN.txt`, que
  edita `prog-cN`: una línea por símbolo, `símbolo | fuente`, y vale desde la
  clase N. Una línea sin fuente es un error (la prueba lo exige).

Las excepciones van en `tools/datos/notacion_ml/excepciones.txt`, una por
línea, `ruta | fragmento literal de la línea | regla | razón`: nunca con un
comentario en la página.

Uso:
    python3 tools/notacion_ml.py                     # toda la unidad y los guiones
    python3 tools/notacion_ml.py <archivo> [...]     # sale con 1 si hay hallazgos
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
UNIDAD = RAIZ / "course" / "9_aprendizaje_maquina"
GUIONES = RAIZ / "tools" / "cuadernos_ml"
DATOS = RAIZ / "tools" / "datos" / "notacion_ml"
CLASES = range(0, 6)
UNIDAD_ENTERA = 5            # hojas de la raíz (A_notacion, B_laboratorio): todo vale

# --- Lista blanca común ----------------------------------------------------
# Macros de formato y operadores sin significado propio: valen siempre.
NEUTRAS = set("""
frac dfrac tfrac sum prod int sqrt cdot cdots dots ldots vdots ddots times
le leq ge geq ne neq approx sim in notin subset subseteq to mapsto rightarrow
leftarrow Rightarrow Leftarrow Leftrightarrow iff infty pm mp mid left right
middle big Big bigg Bigg bigl bigr Bigl Bigr quad qquad text textbf textit
mathrm mathbf mathsf mathcal mathbb operatorname widehat widetilde bar
overline underline min max sup inf exp lim arg lVert rVert lvert rvert vert
Vert langle rangle lfloor rfloor lceil rceil begin end partial nabla forall
exists emptyset varnothing cup cap setminus land lor neg circ ast boxed
underbrace overbrace displaystyle limits tag phantom hspace colon overset
underset stackrel binom equiv propto ll gg prime top perp star checkmark
""".split())

# (símbolo, clase que lo presenta, fuente). Macros sin barra; letras griegas
# en Unicode se traducen a su macro con GRIEGAS.
COMUN = [
    ("beta", 0, "contrato §4.1"), ("ell", 0, "contrato §4.1"),
    ("sigma", 0, "contrato §4.1 (sigmoide)"), ("mu", 0, "contrato §4.1"),
    ("Pr", 0, "contrato §4.1"), ("phi", 0, "contrato §4.2 (v3, r1-03)"),
    ("varepsilon", 1, "contrato §4.2"), ("Phi", 1, "contrato §4.2"),
    ("theta", 1, "contrato §4.2 (polares)"), ("xi", 1, "contrato §4.2"),
    ("Omega", 1, "contrato §4.2"), ("ln", 1, "contrato §4.2 (r1-22)"),
    ("rho", 3, "contrato §4.2"), ("delta", 4, "contrato §4.2"),
    ("tau", 4, "contrato §4.2"),
]
# Formas compuestas con macros neutras que solo valen desde su clase.
PATRONES = [
    (r"\\operatorname\*?\{Var\}", 1, "contrato §4.2"),
    (r"\\operatorname\*?\{corr\}", 3, "contrato §4.2"),
    (r"\\operatorname\*?\{cov\}", 4, "contrato §4.2"),
    (r"\\mathcal\s*\{?\s*D", 1, "contrato §4.2"),
    (r"\\mathcal\s*\{?\s*H", 1, "contrato §4.2 (v4, r2-01)"),
    (r"\\text\{(ent)\}", 1, "contrato §4.2 (v3, r1-08)"),
    (r"\\text\{Bayes\}", 1, "contrato §4.2"),
    (r"\\mathrm\{brecha\}", 1, "contrato §4.2"),
    (r"\\operatorname\*?\{grado\}", 1, "contrato §4.2"),
    (r"\\text\{(val|prueba)\}", 2, "contrato §4.2"),
    (r"\\mathrm\{(CV|EE)\}", 2, "contrato §4.2"),
    (r"\\text\{(sesgo|varianza)\}", 2, "contrato §4.2"),
    (r"\\Omega_\{?(1|2|\\rho)", 3, "contrato §4.2"),
    (r"R\^\{?2\b", 3, "contrato §4.2 (solo con aviso)"),
    (r"\\mathrm\{(MCC|Brier)\}", 4, "contrato §4.2"),
    (r"\\text\{(bal|cal)\}", 4, "contrato §4.2"),
]

GRIEGAS = {
    "α": "alpha", "β": "beta", "γ": "gamma", "Γ": "Gamma", "δ": "delta",
    "Δ": "Delta", "ε": "varepsilon", "ϵ": "epsilon", "ζ": "zeta", "η": "eta",
    "θ": "theta", "Θ": "Theta", "ι": "iota", "κ": "kappa", "λ": "lambda",
    "Λ": "Lambda", "μ": "mu", "ν": "nu", "ξ": "xi", "Ξ": "Xi", "π": "pi",
    "Π": "Pi", "ρ": "rho", "σ": "sigma", "Σ": "Sigma", "τ": "tau",
    "υ": "upsilon", "φ": "phi", "ϕ": "phi", "Φ": "Phi", "χ": "chi",
    "ψ": "psi", "Ψ": "Psi", "ω": "omega", "Ω": "Omega", "ℓ": "ell",
}

# Bloques (por id de directiva) donde una regla de la lista negra no aplica.
BLOQUES_PERMITIDOS = {
    "lambda": "ml-c3-def-lagrangeano-capacidad",
    "alpha": "ml-c3-def-lagrangeano-capacidad",
    "smote": "ml-c4-obs-por-que-no-remuestrear",
}
REGLAS = ("boldsymbol", "hat", "lambda", "alpha", "lagrangiano", "outlier",
          "smote", "no-lineal", "log", "blanca", "antes")
FUENTE_VALIDA = re.compile(r"§\s?\d|\bD-\d{3}\b|\b[a-z]+(-[a-z0-9]+)*-\d+\b")


# --- Datos por clase y excepciones -----------------------------------------

def leer_lista_clase(texto, nombre="cN.txt"):
    """`símbolo | fuente` por línea → [(símbolo, fuente)]. Sin fuente: error."""
    filas = []
    for n, linea in enumerate(texto.split("\n"), 1):
        linea = linea.strip()
        if not linea or linea.startswith("#"):
            continue
        simbolo, _, fuente = (p.strip() for p in linea.rpartition("|"))
        if not simbolo or not fuente or not FUENTE_VALIDA.search(fuente):
            raise ValueError(f"{nombre}:{n}: cada línea es «símbolo | fuente» "
                             "(fila de contrato §4 o D-NNN): " + repr(linea))
        filas.append((simbolo, fuente))
    return filas


def leer_excepciones(texto, nombre="excepciones.txt"):
    """`ruta | fragmento | regla | razón` → [(ruta, fragmento, regla, razón)]."""
    filas = []
    for n, linea in enumerate(texto.split("\n"), 1):
        if not linea.strip() or linea.lstrip().startswith("#"):
            continue
        partes = [p.strip() for p in linea.split(" | ")]
        if len(partes) != 4 or not all(partes) or partes[2] not in REGLAS:
            raise ValueError(f"{nombre}:{n}: la excepción es «ruta | fragmento "
                             "| regla | razón», con regla de REGLAS: "
                             + repr(linea))
        filas.append(tuple(partes))
    return filas


def lista_blanca(datos=DATOS):
    """{macro: clase} y [(regex, clase)], la común más los cN.txt."""
    macros = {m: c for m, c, _ in COMUN}
    patrones = [(re.compile(p), c) for p, c, _ in PATRONES]
    for clase in CLASES:
        ruta = Path(datos) / f"c{clase}.txt"
        if not ruta.exists():
            continue
        for simbolo, _ in leer_lista_clase(ruta.read_text(encoding="utf-8"),
                                           ruta.name):
            if simbolo.startswith("re:"):
                patrones.append((re.compile(simbolo[3:]), clase))
            else:
                m = GRIEGAS.get(simbolo, simbolo.lstrip("\\"))
                macros[m] = min(clase, macros.get(m, clase))
    return macros, patrones


def excepciones(datos=DATOS):
    ruta = Path(datos) / "excepciones.txt"
    if not ruta.exists():
        return []
    return leer_excepciones(ruta.read_text(encoding="utf-8"), ruta.name)


# --- Clase de un archivo ---------------------------------------------------

def clase_de_archivo(ruta):
    """Clase cuya notación vale en `ruta` (None: no se revisa)."""
    ruta = Path(ruta).resolve()
    if ruta.name.endswith(".texto.md"):
        from gen_cuadernos_ml import clase_de
        return clase_de(ruta.name[: -len(".texto.md")])
    try:
        partes = ruta.relative_to(UNIDAD).parts
    except ValueError:
        return UNIDAD_ENTERA
    if any(p.startswith("_") for p in partes):
        return None
    if len(partes) == 1:
        return UNIDAD_ENTERA
    m = re.match(r"(\d+)_", partes[0])
    return int(m.group(1)) - 1 if m else UNIDAD_ENTERA


def archivos_por_revisar():
    paginas = sorted(UNIDAD.rglob("*.md")) if UNIDAD.exists() else []
    guiones = sorted(GUIONES.glob("*.texto.md")) if GUIONES.exists() else []
    return [r for r in paginas + guiones if clase_de_archivo(r) is not None]


# --- El análisis -----------------------------------------------------------

def _enmascarar_codigo(texto):
    """Blanquea bloques ``` y `código` en línea, conservando los saltos."""
    def blanco(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    texto = re.sub(r"^(```|~~~).*?^\1[^\n]*$", blanco, texto, flags=re.S | re.M)
    return re.sub(r"`[^`\n]*`", blanco, texto)


def _matematicas(texto):
    """[(inicio, fragmento)] de cada $$…$$ y $…$ (sin los `\\$`)."""
    tramos, ocupado = [], []
    for m in re.finditer(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$", texto, re.S):
        tramos.append((m.start(1), m.group(1)))
        ocupado.append((m.start(), m.end()))
    for m in re.finditer(r"(?<![\\$])\$(?!\$)([^$\n]+?)(?<!\\)\$", texto):
        if not any(a <= m.start() < b for a, b in ocupado):
            tramos.append((m.start(1), m.group(1)))
    return tramos


def _rangos_de_bloque(lineas, id_bloque):
    """Líneas (1-based) dentro de `::: tipo {#id_bloque …}` … `:::`."""
    rangos = set()
    for i, linea in enumerate(lineas):
        if re.match(r"^:::+\s*\w+\s*\{#" + re.escape(id_bloque) + r"\b", linea):
            for j in range(i, len(lineas)):
                rangos.add(j + 1)
                if j > i and re.match(r"^:::+\s*$", lineas[j]):
                    break
    return rangos


def _oraciones(texto):
    """[(inicio, oración)], partidas por . ! ? o párrafo."""
    salida, inicio = [], 0
    for m in re.finditer(r"[.!?](?=\s)|\n\s*\n", texto):
        salida.append((inicio, texto[inicio:m.end()]))
        inicio = m.end()
    salida.append((inicio, texto[inicio:]))
    return salida


LISTA_NEGRA = [
    ("boldsymbol", re.compile(r"\\boldsymbol\b"),
     "\\boldsymbol rompe el sitio: va \\mathbf"),
    ("hat", re.compile(r"\\hat(?![A-Za-z])"), "va \\widehat, nunca \\hat"),
    ("lambda", re.compile(r"\\lambda\b|λ"),
     "λ no aparece en la unidad: la fuerza de regularización es μ ≥ 0"),
    ("alpha", re.compile(r"\\alpha\b|α|\balpha\b"),
     "alpha no nombra la regularización: es μ (salvo la nota única)"),
    ("lagrangiano", re.compile(r"lagrangian[oa]s?\b", re.I), "va «lagrangeano»"),
    ("smote", re.compile(r"\bSMOTE\b|sobremuestre\w*", re.I),
     "SMOTE/sobremuestreo no se presenta como solución"),
    ("log", re.compile(r"\\log\b(?!_)"),
     "\\log sin subíndice: va \\ln (o \\log_{10} en ejes)"),
]


def revisar_texto(texto, clase, nombre="<texto>", blanca=None, excepcs=()):
    """Hallazgos [(línea, regla, mensaje)] de un archivo de la clase `clase`."""
    macros, patrones = blanca if blanca is not None else lista_blanca()
    lineas = texto.split("\n")
    sin_codigo = _enmascarar_codigo(texto)

    def linea_de(pos):
        return texto.count("\n", 0, pos) + 1

    hallazgos = []
    permitidas = {regla: _rangos_de_bloque(lineas, bloque)
                  for regla, bloque in BLOQUES_PERMITIDOS.items()}

    # Lista negra: sobre todo el texto (también el código de las páginas).
    for regla, rx, msg in LISTA_NEGRA:
        for m in rx.finditer(texto):
            n = linea_de(m.start())
            if n in permitidas.get(regla, ()):
                continue
            hallazgos.append((n, regla, f"{msg}: «{m.group(0)}»"))
    for m in re.finditer(r"outlier", texto, re.I):
        contexto = texto[max(0, m.start() - 10): m.end()].lower()
        if not contexto.endswith("no es un outlier"):
            hallazgos.append((linea_de(m.start()), "outlier",
                              "«outlier» solo dentro de «no es un outlier»; "
                              "una cola larga se llama cola larga"))
    for inicio, oracion in _oraciones(sin_codigo):
        nl = re.search(r"no[\s-]+lineal(es)?\b", oracion, re.I)
        if nl and re.search(r"polin[oó]mi|\bgrado", oracion, re.I):
            hallazgos.append((linea_de(inicio + nl.start()), "no-lineal",
                              "un polinomio en x es lineal en parámetros: "
                              "«curvo en x, lineal en β»"))

    # Lista blanca: macros y griegas en las matemáticas; griegas en la prosa.
    vistos = []
    for inicio, frag in _matematicas(sin_codigo):
        for m in re.finditer(r"\\([A-Za-z]+)", frag):
            vistos.append((inicio + m.start(), m.group(1)))
        for rx, desde in patrones:
            for m in rx.finditer(frag):
                if desde > clase:
                    hallazgos.append((linea_de(inicio + m.start()), "antes",
                                      f"«{m.group(0)}» se presenta en la clase "
                                      f"{desde}; este archivo es de la {clase}"))
    for m in re.finditer("|".join(GRIEGAS), sin_codigo):
        vistos.append((m.start(), GRIEGAS[m.group(0)]))
    negras = {"boldsymbol", "hat", "lambda", "alpha", "log"}
    for pos, macro in vistos:
        if macro in NEUTRAS or macro in negras:
            continue
        if macro not in macros:
            hallazgos.append((linea_de(pos), "blanca",
                              f"\\{macro} no está en la lista blanca (contrato "
                              "§4; se pide por SOLICITUD y entra en cN.txt)"))
        elif macros[macro] > clase:
            hallazgos.append((linea_de(pos), "antes",
                              f"\\{macro} se presenta en la clase "
                              f"{macros[macro]}; este archivo es de la {clase}"))

    # Excepciones declaradas para este archivo.
    propias = [(frag, regla) for ruta, frag, regla, _ in excepcs
               if Path(nombre).as_posix().endswith(ruta)]
    salida = []
    for n, regla, msg in sorted(set(hallazgos)):
        texto_linea = lineas[n - 1] if n <= len(lineas) else ""
        if any(r == regla and f in texto_linea for f, r in propias):
            continue
        salida.append((n, regla, msg))
    return salida


def revisar_archivo(ruta, clase=None, blanca=None, excepcs=None):
    ruta = Path(ruta)
    clase = clase_de_archivo(ruta) if clase is None else clase
    if clase is None:
        return []
    excepcs = excepciones() if excepcs is None else excepcs
    try:
        nombre = ruta.resolve().relative_to(RAIZ).as_posix()
    except ValueError:
        nombre = ruta.as_posix()
    return revisar_texto(ruta.read_text(encoding="utf-8"), clase, nombre,
                         blanca, excepcs)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    rutas = [Path(a) for a in argv] or archivos_por_revisar()
    blanca, excepcs, total = lista_blanca(), excepciones(), 0
    for ruta in rutas:
        for n, regla, msg in revisar_archivo(ruta, blanca=blanca,
                                             excepcs=excepcs):
            print(f"{ruta}:{n}: [{regla}] {msg}")
            total += 1
    print(f"{len(rutas)} archivo(s), {total} hallazgo(s)", file=sys.stderr)
    return 1 if total else 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    sys.exit(main())
