"""Rutas de _assets por unidad y lectura de CREDITOS.md.

Las guardas de imagenes nacieron escritas contra la unica unidad que existia
(historia de la IA). Al aparecer la unidad de filosofia con figuras propias,
esas rutas dejaron de ser una constante y pasaron a ser un mapa: este modulo
es la unica fuente de ese mapa, para que agregar una unidad sea agregar una
linea aqui y no editar cuatro archivos de pruebas.
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ASSETS_HISTORIA = RAIZ / "course/1_introduccion/2_historia_ia/_assets"
ASSETS_FILOSOFIA = RAIZ / "course/2_filosofia_ia/_assets"
ASSETS_COMPUTABILIDAD = RAIZ / "course/3_computabilidad/_assets"

ASSETS_POR_UNIDAD = {
    "historia": ASSETS_HISTORIA,
    "filosofia": ASSETS_FILOSOFIA,
    "computabilidad": ASSETS_COMPUTABILIDAD,
}

CELDA_NOMBRE = 0
CELDA_ORIGEN = 2
CELDA_LICENCIA = 3


def filas_de_creditos(assets: Path) -> dict:
    """Parsea las filas de datos de la tabla de CREDITOS.md: {archivo: [celdas]}."""
    lineas = (assets / "CREDITOS.md").read_text(encoding="utf-8").splitlines()
    filas = {}
    for linea in lineas:
        if not linea.startswith("|"):
            continue
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if len(celdas) < 4:
            continue
        if set(celdas[0]) <= {"-", " "}:  # fila separadora |---|---|---|---|
            continue
        nombre = celdas[CELDA_NOMBRE].strip("`")
        if nombre == "Archivo":  # fila de encabezado
            continue
        filas[nombre] = celdas
    return filas
