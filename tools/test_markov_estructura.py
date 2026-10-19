"""La forma de la unidad de cadenas de Markov que el contrato no mide.

`contrato_unidad.py` exige pista y respuesta en todo ejercicio, pero no
cuántas pistas ni cómo se titulan. La unidad promete, en cada página de la
clase, una sección `## Ejercicios` con problemas modificados: el preámbulo
literal, exactamente dos pistas («Pista 1 · …» organiza, «Pista 2 · …»
revisa) y una respuesta «Respuesta · …», contiguas
(`.claude/skills/unidad/referencias/ejercicios.md`). Y la navegación tiene
que mostrar las páginas en el orden del recorrido: en juegos una página se
publicó fuera de su lugar con la suite verde.
"""
import json
import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
UNIDAD = RAIZ / "course/8_markov"
ARTEFACTO = RAIZ / "artifact"

CLASES = sorted(p for p in UNIDAD.iterdir() if p.is_dir() and re.match(r"\d+_", p.name))
PAGINAS = sorted(
    (p for c in CLASES for p in c.glob("*.md")
     if p.name != "0_index.md" and not p.name.endswith("_tarea.md")),
    key=lambda p: (p.parent.name, int(p.name.split("_", 1)[0])),
)

PREAMBULO = ("**Intenta formular tu propuesta sin abrir las pistas ni la respuesta y sin "
             "pedir ayuda a ChatGPT.**")

# El recorrido de la clase 1, por id estable y en orden de navegación.
CLASE_1_EN_ORDEN = [
    "mkv-lo-que-necesitas",
    "mkv-el-problema-de-markov",
    "mkv-ajustar-contando",
    "mkv-predecir",
    "mkv-generar-texto",
]

RE_DIRECTIVA = re.compile(r"^::: (\w+) \{([^}]*)\}\s*$", re.M)
RE_ATRIBUTO = re.compile(r'(\w+)="([^"]*)"')


def seccion(texto, titulo):
    """El texto bajo el `##` que empieza por `titulo`, hasta el siguiente `##`."""
    m = re.search(r"^## " + re.escape(titulo) + r".*?$\n(.*?)(?=^## |\Z)", texto, re.M | re.S)
    return m.group(1) if m else None


def directivas(texto):
    """[(familia, atributos, posición)] de cada `::: familia {…}` en orden."""
    salida = []
    for m in RE_DIRECTIVA.finditer(texto):
        atributos = dict(RE_ATRIBUTO.findall(m.group(2)))
        id_ = re.search(r"#([\w-]+)", m.group(2))
        atributos["id"] = id_.group(1) if id_ else None
        salida.append((m.group(1), atributos, m.start()))
    return salida


@pytest.mark.parametrize("pagina", PAGINAS, ids=lambda p: p.name)
def test_cada_ejercicio_final_tiene_dos_pistas_tituladas(pagina):
    texto = pagina.read_text(encoding="utf-8")
    cuerpo = seccion(texto, "Ejercicios")
    assert cuerpo is not None, f"{pagina.name}: falta la sección «## Ejercicios»"
    control = texto.find("**Punto de control")
    assert control == -1 or texto.find("## Ejercicios") < control, (
        f"{pagina.name}: «## Ejercicios» va antes del punto de control")

    objetos = [d for d in directivas(cuerpo) if d[0] in {"exercise", "hint", "answer"}]
    ejercicios = [i for i, d in enumerate(objetos) if d[0] == "exercise"]
    assert ejercicios, f"{pagina.name}: «## Ejercicios» no tiene ningún ejercicio"
    for i in ejercicios:
        ej = objetos[i][1]
        siguientes = objetos[i + 1:i + 4]
        familias = [d[0] for d in siguientes]
        assert familias == ["hint", "hint", "answer"], (
            f"{pagina.name}: {ej['id']} va seguido de {familias}, no de pista, pista, respuesta")
        for d in siguientes:
            assert d[1].get("of") == ej["id"], f"{pagina.name}: {d[1]['id']} no es de {ej['id']}"
        assert siguientes[0][1].get("title", "").startswith("Pista 1 · "), siguientes[0][1]
        assert siguientes[1][1].get("title", "").startswith("Pista 2 · "), siguientes[1][1]
        assert siguientes[2][1].get("title", "").startswith("Respuesta · "), siguientes[2][1]
        # El preámbulo literal va entre el ejercicio y su primera pista.
        tramo = cuerpo[objetos[i][2]:siguientes[0][2]]
        assert PREAMBULO in " ".join(tramo.split()), (
            f"{pagina.name}: {ej['id']} no trae el preámbulo literal")


def test_markov_aparece_en_navegacion_en_orden():
    if not (ARTEFACTO / "manifest.json").is_file():
        pytest.skip("No hay artifact/ construido; corre `raya build` primero")
    nav = json.loads((ARTEFACTO / "data/navigation.json").read_text())
    items = {it["id"]: it for it in nav["items"]}
    assert "markov" in items, "la unidad no aparece en la navegación"
    hijos = items["markov"]["children"]
    assert hijos[0] == "markov-que-es-una-cadena", hijos
    assert items["markov-que-es-una-cadena"]["children"] == CLASE_1_EN_ORDEN
