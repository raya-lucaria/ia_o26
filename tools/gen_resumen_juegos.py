"""Recuadro «Lo que ya viste» de las páginas de algoritmo de juegos.

Siete páginas de `course/7_juegos/` cierran, justo antes de «## Lo que hay
que llevarse», con un recuadro visible que resume los algoritmos vistos hasta
ahí y lista los que vienen. El texto sale de UNA fuente, `ALGORITMOS`, en el
orden del curso: cada página muestra el prefijo de la lista que termina en su
algoritmo, con su fila en negrita y «(estás aquí)», y en «Lo que viene» los
que siguen, en palabras llanas y sin símbolos que aún no se presentan.

El bloque se reconoce sin comentarios HTML (Raya los publica): empieza en el
renglón `> [!NOTE]` cuyo siguiente renglón empieza con `> **Lo que ya viste`,
y termina en el primer renglón en blanco. Si la página aún no lo tiene, se
inserta antes de «## Lo que hay que llevarse».

    python3 tools/gen_resumen_juegos.py          # reescribe los bloques
    python3 tools/gen_resumen_juegos.py --check  # sale con 1 si alguno difiere

`contenido(archivo, texto)` es pura; `tools/test_resumen_juegos.py` compara
con ella sin escribir.
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
UNIDAD = RAIZ / "course/7_juegos"

J2 = "2_mirar_todo_y_podar"
J3 = "3_cuando_no_cabe"

# Orden del curso. `archivo`: la página que lleva su ficha (relativa a la
# unidad). `numero`: la celda «Qué número da» del recuadro; dice qué número
# sale y si el algoritmo garantiza $V$, con la convención de la fila
# «¿Garantiza $V$?» de las fichas. `garantiza`: «Sí» o «No», el arranque de
# esa fila en la ficha y de la segunda mitad de `numero` (la prueba los ata).
# El recuadro tiene dos columnas: dentro del callout, a 390 px, quedan ~298 px
# y una tercera se escondía tras el scroll. `mira` ya no sale en el recuadro:
# la lee la tabla «Cómo busca cada algoritmo» de «Qué número da cada uno»
# (test_prosa_comparar_8.py), y la ficha la dice en su primera fila.
# `viene`: la línea de «Lo que viene» que leen las páginas anteriores, sin
# símbolos.
ALGORITMOS = [
    dict(
        nombre="Minimax",
        archivo=f"{J2}/2_minimax_como_algoritmo.md",
        mira="Los finales",
        numero="$V$; lo garantiza",
        garantiza="Sí",
        viene="mirar todo el árbol hasta los finales",
        clase=2, enlace="minimax-como-algoritmo", titulo="Minimax como algoritmo",
    ),
    dict(
        nombre="Expectiminimax",
        archivo=f"{J2}/3_cuando_decide_un_dado.md",
        mira="Los finales",
        numero="El $V$ del juego con dado; lo garantiza",
        garantiza="Sí",
        viene="lo mismo cuando un dado o una moneda decide algunas jugadas; "
              "ahí se promedia en vez de elegir",
        clase=2, enlace="cuando-decide-un-dado", titulo="Cuando decide un dado",
    ),
    dict(
        nombre="Alfa-beta",
        archivo=f"{J2}/5_alfa_beta_como_algoritmo.md",
        mira="Los finales, sin las ramas que ya no deciden",
        numero="$V$ en la raíz; lo garantiza",
        garantiza="Sí",
        viene="la misma jugada que mirar todo, sin generar las ramas que ya "
              "no pueden cambiar la decisión",
        clase=2, enlace="alfa-beta", titulo="Alfa-beta a mano",
    ),
    dict(
        nombre="Minimax con corte",
        archivo=f"{J3}/2_minimax_con_corte.md",
        mira="$d$ jugadas",
        numero="Valor con corte; no garantiza $V$, salvo si llega a los finales",
        garantiza="No",
        viene="mirar unas cuantas jugadas y estimar a ojo lo que queda debajo, "
              "para cuando el árbol no cabe",
        clase=3, enlace="cortar-y-evaluar", titulo="Cortar y evaluar a mano",
    ),
    dict(
        nombre="Búsqueda de quietud",
        archivo=f"{J3}/3_mas_alla_del_horizonte.md",
        mira="$d$ jugadas, luego solo capturas",
        numero="Valor con quietud; no garantiza $V$, salvo si "
               "llega a los finales antes de cortar",
        garantiza="No",
        viene="no detenerse a estimar a mitad de un intercambio de capturas",
        clase=3, enlace="mas-alla-del-horizonte", titulo="Más allá del horizonte",
    ),
    dict(
        nombre="Profundización iterativa",
        archivo=f"{J3}/4_jugar_contra_el_reloj.md",
        mira="$d=1,2,3,\\dots$ mientras haya reloj",
        numero="Valor con corte de la última búsqueda; no garantiza $V$, salvo si "
               "llega a los finales",
        garantiza="No",
        viene="buscar cada vez un poco más hondo, con una jugada siempre "
              "lista para cuando se acabe el tiempo",
        clase=3, enlace="jugar-contra-el-reloj", titulo="Jugar contra el reloj",
    ),
    dict(
        nombre="Monte Carlo plano",
        archivo=f"{J3}/5_simular_en_vez_de_evaluar.md",
        mira="Los finales, jugando al azar; sin árbol",
        numero="$\\bar u$; no garantiza $V$",
        garantiza="No",
        viene="estimar cada jugada jugando muchas partidas al azar hasta el "
              "final, sin escribir ninguna estimación",
        clase=3, enlace="simular-en-vez-de-evaluar", titulo="Simular en vez de evaluar",
    ),
    dict(
        nombre="MCTS con UCT",
        archivo=f"{J3}/5_simular_en_vez_de_evaluar.md",
        mira="Un árbol que crece; debajo, partidas al azar",
        numero="$\\bar u$; no garantiza $V$ (con tiempo sin límite converge a él, "
               "con cualquier $c>0$)",
        garantiza="No",
        viene="construye un árbol: elige por puntaje dentro de él, lo hace "
              "crecer, simula desde la hoja y sube el resultado; manda más "
              "partidas a lo que va mejor sin dejar de probar lo otro",
        clase=3, enlace="simular-en-vez-de-evaluar", titulo="Simular en vez de evaluar",
    ),
]

# Páginas con recuadro, en orden de navegación (sin repetir).
PAGINAS = list(dict.fromkeys(a["archivo"] for a in ALGORITMOS))

# Cuando ya no queda ningún algoritmo por ver.
SIN_PENDIENTES = ("Ya viste todos los algoritmos de la clase. "
                  "[[de-donde-sale-el-bono|De dónde sale el bono]] explica la "
                  "regla con que MCTS reparte las partidas.")

ENCABEZADO = "| Algoritmo | Qué número da |"
INICIO = "> [!NOTE]"
TITULO = "> **Lo que ya viste"
CIERRE = "## Lo que hay que llevarse"


def vistos(archivo: str) -> list[dict]:
    """El prefijo de ALGORITMOS que termina en el último de `archivo`."""
    ultimo = max(i for i, a in enumerate(ALGORITMOS) if a["archivo"] == archivo)
    return ALGORITMOS[: ultimo + 1]


def pendientes(archivo: str) -> list[dict]:
    return ALGORITMOS[len(vistos(archivo)):]


def _negrita(celda: str) -> str:
    return f"**{celda}**"


def fila(alg: dict, aqui: bool) -> str:
    celdas = [alg["nombre"], alg["numero"]]
    if aqui:
        celdas[0] += " (estás aquí)"
        celdas = [_negrita(c) for c in celdas]
    return "| " + " | ".join(celdas) + " |"


def bloque(archivo: str) -> str:
    """El recuadro completo de `archivo`, sin renglón en blanco al final."""
    lineas = [
        INICIO,
        "> **Lo que ya viste.** Los algoritmos de la unidad hasta esta página, "
        "en el orden del curso.",
        ">",
        "> " + ENCABEZADO,
        "> |---|---|",
    ]
    lineas += ["> " + fila(a, a["archivo"] == archivo) for a in vistos(archivo)]
    lineas += [">", "> **Lo que viene.**", ">"]
    resto = pendientes(archivo)
    if resto:
        for a in resto:
            lineas.append(
                f"> - **{a['nombre']}**: {a['viene']}. Clase {a['clase']}, "
                f"[[{a['enlace']}|{a['titulo']}]]."
            )
    else:
        lineas.append("> " + SIN_PENDIENTES)
    return "\n".join(lineas)


def localizar(lineas: list[str]) -> tuple[int, int] | None:
    """(inicio, fin) del bloque actual, fin exclusivo; None si no hay."""
    for i, s in enumerate(lineas[:-1]):
        if s.rstrip() == INICIO and lineas[i + 1].startswith(TITULO):
            j = i + 1
            while j < len(lineas) and lineas[j].strip():
                j += 1
            return i, j
    return None


def contenido(archivo: str, texto: str) -> str:
    """El texto de la página con su recuadro al día. Pura."""
    lineas = texto.split("\n")
    nuevo = bloque(archivo).split("\n")
    lugar = localizar(lineas)
    if lugar:
        i, j = lugar
        lineas[i:j] = nuevo
    else:
        k = lineas.index(CIERRE)
        while k > 0 and not lineas[k - 1].strip():
            k -= 1
        lineas[k:k] = [""] + nuevo
    return "\n".join(lineas)


def main(argv: list[str]) -> int:
    revisar = "--check" in argv
    distintos = []
    for archivo in PAGINAS:
        ruta = UNIDAD / archivo
        viejo = ruta.read_text(encoding="utf-8")
        nuevo = contenido(archivo, viejo)
        if nuevo != viejo:
            distintos.append(archivo)
            if not revisar:
                ruta.write_text(nuevo, encoding="utf-8")
    for archivo in distintos:
        print(("difiere: " if revisar else "escrito: ") + archivo)
    return 1 if (revisar and distintos) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
