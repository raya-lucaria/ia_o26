"""Recuadro «Lo que ya viste» de las páginas de algoritmo de juegos.

Siete páginas de `course/7_juegos/` (nueve algoritmos) cierran, justo antes de «## Lo que hay
que llevarse», con un recuadro visible que resume los algoritmos vistos hasta
ahí. El texto sale de UNA fuente, `ALGORITMOS`, en el orden del curso: cada
página muestra el prefijo de la lista que termina en su algoritmo, con su
fila en negrita y «(estás aquí)». No anuncia los que vienen (nombraba
conceptos aún no enseñados); la última página, sin pendientes, manda a la
radiografía.

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

# Orden del curso (el de navegación: 7.2 minimax, alfa-beta, expectiminimax;
# 7.3 corte, quietud e iterativa, Monte Carlo plano y con actualización
# minimax, MCTS con UCT). `archivo`: la página que lleva su ficha (relativa a
# la unidad). `ficha`: el encabezado `### …` de esa ficha en la página.
# `numero`: la celda «Qué número da» del recuadro; dice qué número sale y si
# el algoritmo garantiza $V$. `garantiza`: «Sí» o «No», la mitad de `numero`
# después del punto y coma. Si no, la salvedad va con la escala de la
# radiografía: el corte que llega a todos los finales da $M\cdot V$, no $V$;
# los que convergen, con sus condiciones. `garantia`: un trozo literal de
# la viñeta «**Garantía:**» de la ficha que dice lo mismo (la prueba lo busca
# ahí). El recuadro tiene dos columnas: dentro del callout, a 390 px, quedan
# ~298 px y una tercera se escondía tras el scroll. `mira` ya no sale en el
# recuadro; la ficha lo dice en su exploración. `enlace`/`titulo`: la
# página que se lee primero para ese algoritmo, con su `title` real.
ALGORITMOS = [
    dict(
        nombre="Minimax",
        archivo=f"{J2}/2_minimax_como_algoritmo.md",
        ficha="Minimax",
        mira="Los finales",
        numero="$V$; lo garantiza",
        garantiza="Sí",
        garantia="entrega $V$ y una jugada que lo alcanza",
        clase=2, enlace="minimax-como-algoritmo", titulo="Minimax como algoritmo",
    ),
    dict(
        nombre="Alfa-beta",
        archivo=f"{J2}/4_alfa_beta_como_algoritmo.md",
        ficha="Alfa-beta",
        mira="Los finales, sin las ramas que ya no deciden",
        numero="$V$ en la raíz; lo garantiza",
        garantiza="Sí",
        garantia="el mismo $V$ que minimax",
        clase=2, enlace="alfa-beta", titulo="Alfa-beta a mano",
    ),
    dict(
        nombre="Expectiminimax",
        archivo=f"{J2}/5_cuando_decide_un_dado.md",
        ficha="Expectiminimax",
        mira="Los finales",
        numero="El $V$ del juego con dado; lo garantiza",
        garantiza="Sí",
        garantia="calcula exactamente la utilidad esperada óptima",
        clase=2, enlace="cuando-decide-un-dado",
        titulo="Cuando decide un dado: expectiminimax",
    ),
    dict(
        nombre="Minimax con corte",
        archivo=f"{J3}/1_cortar_y_evaluar.md",
        ficha="Minimax con corte",
        mira="$d$ jugadas",
        numero="Valor con corte; no garantiza $V$. Con todos los finales, da $M\\cdot V$",
        garantiza="No",
        garantia="si no, nada asegura la jugada",
        clase=3, enlace="cortar-y-evaluar", titulo="Cortar y evaluar",
    ),
    dict(
        nombre="Búsqueda de quietud",
        archivo=f"{J3}/2_jugar_contra_el_reloj.md",
        ficha="Búsqueda de quietud",
        mira="$d$ jugadas, luego solo capturas",
        numero="Valor con quietud; no garantiza $V$. Con todos los finales "
               "antes de activar la quietud, da $M\\cdot V$",
        garantiza="No",
        garantia="solo si llega a los finales **antes de activar la quietud**",
        clase=3, enlace="jugar-contra-el-reloj",
        titulo="Hasta dónde mirar: profundidad, tiempo y horizonte",
    ),
    dict(
        nombre="Profundización iterativa",
        archivo=f"{J3}/2_jugar_contra_el_reloj.md",
        ficha="Profundización iterativa",
        mira="$d=1,2,3,\\dots$ mientras haya reloj",
        numero="Valor con corte de la última búsqueda; no garantiza $V$. Con "
               "todos los finales, da $M\\cdot V$",
        garantiza="No",
        garantia="no garantiza $V$, salvo si la última búsqueda completa llega a los finales",
        clase=3, enlace="jugar-contra-el-reloj",
        titulo="Hasta dónde mirar: profundidad, tiempo y horizonte",
    ),
    dict(
        nombre="Monte Carlo plano",
        archivo=f"{J3}/3_simular_en_vez_de_evaluar.md",
        ficha="Monte Carlo plano",
        mira="Los finales, jugando al azar; sin árbol",
        numero="$\\widehat Q$, que estima $Q_{\\text{azar}}$; no garantiza $V$",
        garantiza="No",
        garantia="Ningún presupuesto garantiza la jugada minimax",
        clase=3, enlace="simular-en-vez-de-evaluar",
        titulo="Simular partidas: promedios y actualización minimax",
    ),
    dict(
        nombre="Monte Carlo con actualización minimax",
        archivo=f"{J3}/3_simular_en_vez_de_evaluar.md",
        ficha="Monte Carlo con actualización minimax",
        mira="Los finales, jugando al azar; guarda lo descubierto",
        numero="$\\widehat Q$ y $\\widehat V$; no garantiza $V$ (converge a él "
               "bajo su contrato: árbol finito, todas las jugadas, finales reales)",
        garantiza="No",
        garantia="Con presupuesto finito puede equivocarse",
        clase=3, enlace="simular-en-vez-de-evaluar",
        titulo="Simular partidas: promedios y actualización minimax",
    ),
    dict(
        nombre="MCTS con UCT",
        archivo=f"{J3}/4_monte_carlo_en_un_arbol_grande.md",
        ficha="UCT",
        mira="Un árbol que crece; debajo, partidas al azar",
        numero="$\\widehat Q$; no garantiza $V$ (en un árbol finito, con $c>0$ "
               "fija y vueltas sin límite, converge a él)",
        garantiza="No",
        garantia="Con presupuesto fijo, ninguna",
        clase=3, enlace="monte-carlo-en-un-arbol-grande", titulo="MCTS con UCT",
    ),
]

# Páginas con recuadro, en orden de navegación (sin repetir).
PAGINAS = list(dict.fromkeys(a["archivo"] for a in ALGORITMOS))

# Cuando ya no queda ningún algoritmo por ver.
SIN_PENDIENTES = ("Ya viste todos los algoritmos de la unidad. "
                  "[[un-arbol-todos-los-algoritmos|Radiografía: un árbol, todos los algoritmos]] "
                  "los pone lado a lado.")

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
    # Sin «Lo que viene»: listaba conceptos que el alumno aún no ha visto
    # (EVAL, quietud, UCT) en cada página (ola 4, r1). El cierre de cada página
    # ya dice cuál sigue; solo la última, sin algoritmos por ver, manda al mapa.
    if not pendientes(archivo):
        lineas += [">", "> " + SIN_PENDIENTES]
    return "\n".join(lineas)


def localizar_todos(lineas: list[str]) -> list[tuple[int, int]]:
    """(inicio, fin) de cada bloque de la página, fin exclusivo, en orden.

    Una página que absorbió a otra (la topología de la homologación concatena
    páginas enteras) puede traer más de un recuadro: uno por ficha."""
    lugares = []
    i = 0
    while i < len(lineas) - 1:
        if lineas[i].rstrip() == INICIO and lineas[i + 1].startswith(TITULO):
            j = i + 1
            while j < len(lineas) and lineas[j].strip():
                j += 1
            lugares.append((i, j))
            i = j
        else:
            i += 1
    return lugares


def localizar(lineas: list[str]) -> tuple[int, int] | None:
    """(inicio, fin) del primer bloque, fin exclusivo; None si no hay."""
    lugares = localizar_todos(lineas)
    return lugares[0] if lugares else None


def contenido(archivo: str, texto: str) -> str:
    """El texto de la página con sus recuadros al día. Pura.

    Todos los recuadros de la página llevan el mismo bloque: el prefijo que
    termina en el último algoritmo de la página."""
    lineas = texto.split("\n")
    nuevo = bloque(archivo).split("\n")
    lugares = localizar_todos(lineas)
    if lugares:
        for i, j in reversed(lugares):
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
