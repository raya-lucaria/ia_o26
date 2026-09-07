import json
from pathlib import Path

from PIL import Image

from unidades import (ASSETS_COMPLEJIDAD, ASSETS_COMPUTABILIDAD, ASSETS_FILOSOFIA,
                      ASSETS_HISTORIA, ASSETS_AGENTES)

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = ASSETS_HISTORIA          # el conjunto original no cambia de sitio
CATALOGO = RAIZ / "tools/ilustraciones.json"
CREDITOS = ASSETS / "CREDITOS.md"
CREDITOS_FILOSOFIA = ASSETS_FILOSOFIA / "CREDITOS.md"

# Un PNG con fondo horneado pesa mas que un JPEG al 85: el tope no puede ser
# el mismo. Medidos tras cuantizar a 128 colores, los seis van de 165 a 231 KB
# (el mayor fue 315 KB antes de una regeneracion). El tope queda en 400 KB, un
# escalon arriba del mayor, para que un PNG que se dispare al doble se
# detecte, sin fallar por la variacion normal entre generaciones.
PESO_MAX_PNG = 400_000

# tokens.color.surface del skin: el color exacto de la columna de contenido
# de la pagina, medido en pixeles sobre una captura del sitio construido
# (no deducido del CSS). Las ilustraciones de filosofia hornean su fondo a
# este color en vez de dejarlo transparente.
FONDO_OBJETIVO = (33, 16, 51)

# "nick land" y no "land": "land" sola pega en palabras inocentes (landscape)
# y volveria la guarda inutilizable a fuerza de falsos positivos.
PROHIBIDOS = [
    "turing", "lovelace", "hinton", "astroboy", "atomu", "minsky", "shannon",
    "marx", "deleuze", "guattari", "nick land", "fisher", "barbrook", "cameron",
]


def nombres():
    return list(json.loads(CATALOGO.read_text(encoding="utf-8"))["ilustraciones"])


def test_todas_generadas():
    for nombre in nombres():
        assert (ASSETS / f"ilus-{nombre}.jpg").is_file(), f"falta ilus-{nombre}.jpg"


def test_dimensiones_y_peso():
    for nombre in nombres():
        ruta = ASSETS / f"ilus-{nombre}.jpg"
        with Image.open(ruta) as im:
            assert im.width == 1024, f"{ruta.name} mide {im.width}px de ancho"
        assert ruta.stat().st_size < 400_000, f"{ruta.name} pesa demasiado"


def test_ningun_prompt_pide_persona_real_o_personaje_protegido():
    catalogo = json.loads(CATALOGO.read_text(encoding="utf-8"))
    texto = json.dumps(catalogo, ensure_ascii=False).lower()
    for termino in PROHIBIDOS:
        assert termino not in texto, f"el catalogo menciona '{termino}'"


def test_creditos_marcan_las_generadas():
    creditos = CREDITOS.read_text(encoding="utf-8").lower()
    for nombre in nombres():
        assert f"ilus-{nombre}.jpg" in creditos, f"ilus-{nombre}.jpg sin credito"
    assert "generada" in creditos


def test_no_queda_png_de_ilustracion_huerfano():
    huerfanos = sorted(p.name for p in ASSETS.glob("ilus-*.png"))
    assert not huerfanos, f"PNGs de ilustracion sin reemplazar por jpg: {huerfanos}"


def nombres_filosofia():
    catalogo = json.loads(CATALOGO.read_text(encoding="utf-8"))
    return list(catalogo["ilustraciones_filosofia"])


def test_filosofia_fondo_horneado_al_color_exacto():
    """El fondo no es transparente: es el mismo violeta solido de la columna
    de contenido de la pagina (#211033), horneado en el PNG. Si el modelo
    devuelve un fondo que no se pudo hornear al color exacto -- porque salio
    con gradiente, vineta o textura -- las esquinas no dan (33, 16, 51) y esta
    prueba lo agarra aqui, no en el navegador. Es una prueba mas estricta que
    "hay canal alfa": tambien detecta un horneado al color equivocado."""
    for nombre in nombres_filosofia():
        ruta = ASSETS_FILOSOFIA / f"ilus-{nombre}.png"
        assert ruta.is_file(), f"falta {ruta.name}"
        with Image.open(ruta) as im:
            im = im.convert("RGB")
            esquinas = [
                im.getpixel((0, 0)),
                im.getpixel((im.width - 1, 0)),
                im.getpixel((0, im.height - 1)),
                im.getpixel((im.width - 1, im.height - 1)),
            ]
            assert all(p == FONDO_OBJETIVO for p in esquinas), (
                f"{ruta.name}: las esquinas no son {FONDO_OBJETIVO} exacto ({esquinas})"
            )


def test_filosofia_dimensiones_y_peso():
    for nombre in nombres_filosofia():
        ruta = ASSETS_FILOSOFIA / f"ilus-{nombre}.png"
        with Image.open(ruta) as im:
            assert im.width == 1024, f"{ruta.name} mide {im.width}px de ancho"
        assert ruta.stat().st_size < PESO_MAX_PNG, (
            f"{ruta.name} pesa {ruta.stat().st_size/1000:.0f} KB"
        )


def test_filosofia_acreditadas_como_generadas():
    creditos = CREDITOS_FILOSOFIA.read_text(encoding="utf-8").lower()
    for nombre in nombres_filosofia():
        assert f"ilus-{nombre}.png" in creditos, f"ilus-{nombre}.png sin credito"
    assert "generada" in creditos


# --- Bloque de computabilidad -------------------------------------------------
# Las guardas de arriba leen SOLO su propio bloque del catalogo: nombres() lee
# "ilustraciones" y nombres_filosofia() lee "ilustraciones_filosofia". Un bloque
# nuevo queda cubierto por UNA sola prueba de este archivo --la de prompts
# prohibidos, que serializa el catalogo entero-- y se pierde justamente la mas
# cara: la del fondo horneado, que es la unica que agarra un modelo que devolvio
# gradiente o vineta. Peor, fijar_fondo_en_paleta() de gen_ilustraciones.py se
# rinde EN SILENCIO cuando las esquinas no caen en un solo indice de paleta. Sin
# estas cuatro, la unidad publicaria un fondo desfasado con la suite en verde.

CREDITOS_COMPUTABILIDAD = ASSETS_COMPUTABILIDAD / "CREDITOS.md"


def nombres_computabilidad():
    catalogo = json.loads(CATALOGO.read_text(encoding="utf-8"))
    return list(catalogo.get("ilustraciones_computabilidad", {}))


def test_computabilidad_todas_generadas():
    for nombre in nombres_computabilidad():
        ruta = ASSETS_COMPUTABILIDAD / f"ilus-{nombre}.png"
        assert ruta.is_file(), f"falta {ruta.name}"


def test_computabilidad_fondo_horneado_al_color_exacto():
    for nombre in nombres_computabilidad():
        ruta = ASSETS_COMPUTABILIDAD / f"ilus-{nombre}.png"
        assert ruta.is_file(), f"falta {ruta.name}"
        with Image.open(ruta) as im:
            im = im.convert("RGB")
            esquinas = [
                im.getpixel((0, 0)),
                im.getpixel((im.width - 1, 0)),
                im.getpixel((0, im.height - 1)),
                im.getpixel((im.width - 1, im.height - 1)),
            ]
            assert all(px == FONDO_OBJETIVO for px in esquinas), (
                f"{ruta.name}: las esquinas no son {FONDO_OBJETIVO} exacto ({esquinas})"
            )


def test_computabilidad_dimensiones_y_peso():
    """Tope propio del bloque, mas estricto que PESO_MAX_PNG. El tope global
    del repositorio se retiro, asi que este es el unico numero que impide que
    una ilustracion salga desmesurada sin que nadie lo note."""
    for nombre in nombres_computabilidad():
        ruta = ASSETS_COMPUTABILIDAD / f"ilus-{nombre}.png"
        with Image.open(ruta) as im:
            assert im.width == 1024, f"{ruta.name} mide {im.width}px de ancho"
        assert ruta.stat().st_size < PESO_MAX_PNG, (
            f"{ruta.name} pesa {ruta.stat().st_size/1000:.0f} KB"
        )


def test_computabilidad_acreditadas_como_generadas():
    creditos = CREDITOS_COMPUTABILIDAD.read_text(encoding="utf-8").lower()
    for nombre in nombres_computabilidad():
        assert f"ilus-{nombre}.png" in creditos, f"ilus-{nombre}.png sin credito"
    assert "generada" in creditos


# --- Bloque de complejidad ----------------------------------------------------
# Las mismas cuatro guardas que el bloque de computabilidad, por la misma razon
# que ese comentario explica: cada bloque del catalogo necesita las suyas o se
# queda cubierto solo por la de prompts prohibidos.
#
# Y una quinta, propia de este bloque: es el unico que usa un estilo distinto
# --anime en vez del grabado editorial-- y ese estilo lleva escritas dos
# restricciones (rostro no reconocible, ninguna obra existente) que son la razon
# por la que la unidad puede tener el registro visual que pidio sin copiarle el
# diseño a nadie. Si alguien reescribe el estilo y las quita, la guarda avisa.

CREDITOS_COMPLEJIDAD = ASSETS_COMPLEJIDAD / "CREDITOS.md"


def nombres_complejidad():
    catalogo = json.loads(CATALOGO.read_text(encoding="utf-8"))
    return list(catalogo.get("ilustraciones_complejidad", {}))


def test_complejidad_todas_generadas():
    for nombre in nombres_complejidad():
        ruta = ASSETS_COMPLEJIDAD / f"ilus-{nombre}.png"
        assert ruta.is_file(), f"falta {ruta.name}"


def test_complejidad_fondo_horneado_al_color_exacto():
    for nombre in nombres_complejidad():
        ruta = ASSETS_COMPLEJIDAD / f"ilus-{nombre}.png"
        assert ruta.is_file(), f"falta {ruta.name}"
        with Image.open(ruta) as im:
            im = im.convert("RGB")
            esquinas = [
                im.getpixel((0, 0)),
                im.getpixel((im.width - 1, 0)),
                im.getpixel((0, im.height - 1)),
                im.getpixel((im.width - 1, im.height - 1)),
            ]
            assert all(px == FONDO_OBJETIVO for px in esquinas), (
                f"{ruta.name}: las esquinas no son {FONDO_OBJETIVO} exacto ({esquinas})"
            )


def test_complejidad_dimensiones_y_peso():
    for nombre in nombres_complejidad():
        ruta = ASSETS_COMPLEJIDAD / f"ilus-{nombre}.png"
        with Image.open(ruta) as im:
            assert im.width == 1024, f"{ruta.name} mide {im.width}px de ancho"
        assert ruta.stat().st_size < PESO_MAX_PNG, (
            f"{ruta.name} pesa {ruta.stat().st_size/1000:.0f} KB"
        )


def test_complejidad_acreditadas_como_generadas():
    creditos = CREDITOS_COMPLEJIDAD.read_text(encoding="utf-8").lower()
    for nombre in nombres_complejidad():
        assert f"ilus-{nombre}.png" in creditos, f"ilus-{nombre}.png sin credito"
    assert "generada" in creditos


def test_complejidad_el_estilo_anime_conserva_sus_dos_restricciones():
    """El estilo propio de esta unidad es el unico que pide un registro de una
    tradicion visual concreta (anime de ciencia ficcion), asi que es el unico
    que puede derivar hacia copiar un personaje con dueño. Las dos frases que
    lo impiden viven en el propio prompt y esta guarda las fija."""
    catalogo = json.loads(CATALOGO.read_text(encoding="utf-8"))
    estilo = catalogo["estilo_anime_fondo_plano"].lower()
    assert "rostro nunca visible ni reconocible" in estilo, (
        "el estilo anime perdio la restriccion de rostro no reconocible"
    )
    assert "no basado en ninguna serie ni obra existente" in estilo, (
        "el estilo anime perdio la restriccion de no copiar obra existente"
    )


# --- Bloque de agentes y ambientes ------------------------------------------
# Estas ilustraciones narran decisiones concretas. A diferencia de los PNG con
# fondo plano, se conservan como JPEG editorial de formato ancho; la guarda
# propia fija tanto las tres piezas previstas como las restricciones de diseño
# original que evitan que una referencia pedagógica se vuelva una imitación.

CREDITOS_AGENTES = ASSETS_AGENTES / "CREDITOS.md"


def nombres_agentes():
    catalogo = json.loads(CATALOGO.read_text(encoding="utf-8"))
    return list(catalogo["ilustraciones_agentes_ambientes"])


def test_agentes_todas_generadas():
    for nombre in nombres_agentes():
        ruta = ASSETS_AGENTES / f"ilus-{nombre}.jpg"
        assert ruta.is_file(), f"falta {ruta.name}"


def test_agentes_dimensiones_y_peso():
    for nombre in nombres_agentes():
        ruta = ASSETS_AGENTES / f"ilus-{nombre}.jpg"
        with Image.open(ruta) as im:
            assert im.width == 1024, f"{ruta.name} mide {im.width}px de ancho"
        assert ruta.stat().st_size < 400_000, f"{ruta.name} pesa demasiado"


def test_agentes_acreditadas_como_generadas():
    creditos = CREDITOS_AGENTES.read_text(encoding="utf-8").lower()
    for nombre in nombres_agentes():
        assert f"ilus-{nombre}.jpg" in creditos, f"ilus-{nombre}.jpg sin credito"
    assert "generada" in creditos


def test_agentes_el_estilo_conserva_restricciones_de_originalidad():
    catalogo = json.loads(CATALOGO.read_text(encoding="utf-8"))
    estilo = catalogo["estilo_agentes_ambientes"].lower()
    assert "diseño original" in estilo
    assert "ninguna franquicia" in estilo
    assert "sin texto" in estilo
