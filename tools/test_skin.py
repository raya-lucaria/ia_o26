"""Ata el color de fondo horneado en los generadores a su fuente de verdad.

`#211033` esta hardcodeado en tres lugares (`tools/gen_ilustraciones.py`,
`tools/test_ilustraciones.py`, `tools/test_aceptacion.py`) porque cada uno
necesita el valor literal para hornear o verificar un fondo. Pero la
autoridad real es `tokens.color.surface` en `skins/eva-cyberpunk.yaml`. Si
alguien edita el skin, esas copias se quedan desactualizadas y cada guarda
que las usa se compara contra si misma: veintidos SVG y cuatro PNG quedarian
visualmente rotos (fondo del skin distinto al fondo horneado) sin que
ninguna prueba lo note, porque ninguna prueba mira al skin.

Esta prueba es la unica que sí lee `skins/eva-cyberpunk.yaml` y compara con
el valor que todas las demas asumen. Si falla, el problema no es esta
prueba: es que las copias hardcodeadas ya no coinciden con el skin y hay que
actualizarlas (y regenerar lo que dependa de ellas) antes de comitear.
"""
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
SKIN = RAIZ / "skins/eva-cyberpunk.yaml"

SURFACE_ASUMIDO = "#211033"

# Las paginas HTML autocontenidas de _assets/ copian la paleta del skin en un
# bloque :root, porque se sirven fuera del CSS del sitio y no tienen forma de
# leer sus tokens. Son copias literales mas, y esta prueba existe para que
# ninguna se quede atras en silencio.
PAGINAS_CON_PALETA_COPIADA = sorted(
    (RAIZ / "course").glob("*/_assets/*.html")
)


def test_el_color_surface_del_skin_sigue_siendo_el_asumido_por_los_generadores():
    datos = yaml.safe_load(SKIN.read_text(encoding="utf-8"))
    surface = datos["tokens"]["color"]["surface"]
    assert surface == SURFACE_ASUMIDO, (
        f"tokens.color.surface de {SKIN.name} es {surface!r}, pero "
        f"tools/gen_ilustraciones.py, tools/test_ilustraciones.py y "
        f"tools/test_aceptacion.py siguen asumiendo {SURFACE_ASUMIDO!r} a mano. "
        "Actualiza esas tres copias y regenera los SVG y los PNG horneados "
        "antes de tocar este valor."
    )


def test_las_paginas_html_de_assets_copian_el_surface_vigente():
    """Un HTML de _assets/ con la paleta vieja se publica sin que nada lo note.

    No los vigila test_9 --que solo mira SVG-- ni las guardas de imagenes
    --que filtran por extension y no ven .html--, asi que sin esta prueba una
    edicion del skin dejaria esas paginas sobre un fondo distinto al del resto
    del sitio, y la suite seguiria verde.
    """
    assert PAGINAS_CON_PALETA_COPIADA, "no se encontro ningun HTML en course/*/_assets/"
    sin_paleta = []
    for pagina in PAGINAS_CON_PALETA_COPIADA:
        texto = pagina.read_text(encoding="utf-8")
        if "--surface:" not in texto and "--page:" not in texto:
            continue  # no copia la paleta: no hay nada que atar
        if SURFACE_ASUMIDO not in texto:
            sin_paleta.append(pagina.relative_to(RAIZ))
    assert not sin_paleta, (
        f"estas paginas copian la paleta del skin pero no traen {SURFACE_ASUMIDO}: "
        f"{sin_paleta}. Actualiza su bloque :root al surface vigente."
    )
