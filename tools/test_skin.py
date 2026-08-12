"""Ata el color de fondo horneado en los generadores a su fuente de verdad.

`#211033` esta hardcodeado en tres lugares (`tools/gen_ilustraciones.py`,
`tools/test_ilustraciones.py`, `tools/test_aceptacion.py`) porque cada uno
necesita el valor literal para hornear o verificar un fondo. Pero la
autoridad real es `tokens.color.surface` en `skins/eva-cyberpunk.yaml`. Si
alguien edita el skin, esas copias se quedan desactualizadas y cada guarda
que las usa se compara contra si misma: veinte SVG y cuatro PNG quedarian
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
