"""Genera ilustraciones con gpt-image-2. Nunca personas reales ni personajes protegidos."""
import base64
import io
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image

from unidades import ASSETS_FILOSOFIA, ASSETS_HISTORIA

RAIZ = Path(__file__).resolve().parent.parent
CATALOGO = RAIZ / "tools/ilustraciones.json"
URL = "https://api.openai.com/v1/images/generations"
CALIDAD_JPEG = 85

# tokens.color.surface del skin: el color exacto de la columna de contenido
# de la pagina (medido en pixeles sobre una captura del sitio construido, no
# deducido del CSS). Es distinto del #12061f del margen exterior de pagina,
# que es donde vive la unidad de historia con sus JPEG de fondo oscuro.
FONDO_OBJETIVO = (33, 16, 51)  # #211033

# Tolerancia por canal (distancia maxima, no euclidiana) para decidir que un
# pixel "es" el fondo y hornearlo al color exacto. Se fijo mirando el
# resultado sobre las cuatro imagenes reales (ver informe de la Tarea 8):
# demasiado baja deja un halo del violeta ligeramente distinto que devuelve
# el modelo; demasiado alta empieza a comerse el trazo neon mas tenue.
FONDO_TOLERANCIA = 40


def hornear_fondo(im, tolerancia=FONDO_TOLERANCIA):
    """Reemplaza por el color exacto FONDO_OBJETIVO los pixeles cercanos al
    color de fondo que devolvio el modelo (muestreado en las cuatro esquinas).
    Esto evita el halo que dejaria un fondo transparente: en vez de recortar
    el fondo, lo sustituye por un fondo distinto pero igual de solido, asi que
    los pixeles de antialiasing de la linea (mezcla de neon y fondo) quedan
    casi identicos a como deberian verse."""
    arr = np.asarray(im.convert("RGB"), dtype=np.int16)
    esquinas = np.stack([arr[0, 0], arr[0, -1], arr[-1, 0], arr[-1, -1]])
    color_fondo = np.median(esquinas, axis=0)
    distancia = np.abs(arr - color_fondo).max(axis=2)
    mascara = distancia <= tolerancia
    arr[mascara] = np.array(FONDO_OBJETIVO, dtype=np.int16)
    return Image.fromarray(arr.astype(np.uint8), "RGB")


def clave():
    valor = os.environ.get("OPENAI_API_KEY")
    if not valor:
        raise SystemExit("falta OPENAI_API_KEY: correr 'set -a && . ./.env && set +a'")
    return valor


def receta(nombre, datos):
    """Devuelve (destino, prompt, fondo_plano) segun en que bloque del
    catalogo viva el nombre. Asi la invocacion de siempre sigue funcionando
    igual y el bloque nuevo no necesita una bandera en la linea de comandos."""
    if nombre in datos["ilustraciones"]:
        return (ASSETS_HISTORIA / f"ilus-{nombre}.jpg",
                f'{datos["ilustraciones"][nombre]} {datos["estilo"]}', False)
    if nombre in datos.get("ilustraciones_filosofia", {}):
        return (ASSETS_FILOSOFIA / f"ilus-{nombre}.png",
                f'{datos["ilustraciones_filosofia"][nombre]} {datos["estilo_fondo_plano"]}',
                True)
    raise SystemExit(f"nombre desconocido en el catalogo: {nombre}")


def generar(nombre):
    datos = json.loads(CATALOGO.read_text(encoding="utf-8"))
    destino, prompt, fondo_plano = receta(nombre, datos)
    cuerpo = {"model": "gpt-image-2", "prompt": prompt, "size": datos["tamano"], "n": 1}
    req = urllib.request.Request(
        URL, data=json.dumps(cuerpo).encode(),
        headers={"Authorization": f"Bearer {clave()}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        salida = json.load(r)
    item = salida["data"][0]
    if item.get("b64_json"):
        crudo = base64.b64decode(item["b64_json"])
    else:
        with urllib.request.urlopen(item["url"], timeout=300) as r:
            crudo = r.read()
    destino.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(io.BytesIO(crudo)) as im:
        im = im.convert("RGB")
        if im.width != 1024:
            im = im.resize((1024, round(im.height * 1024 / im.width)), Image.LANCZOS)
        if fondo_plano:
            im = hornear_fondo(im)
            # Cuantizar a paleta (modo P) baja el peso a una fraccion: el
            # fondo horneado es un solo color repetido en la mayoria de los
            # pixeles, que es exactamente el caso donde una paleta gana mas
            # que en modo RGB de color verdadero.
            im = im.quantize(colors=128, method=Image.FASTOCTREE)
            im.save(destino, "PNG", optimize=True)
        else:
            im.save(destino, "JPEG", quality=CALIDAD_JPEG, optimize=True)
    print(f"{destino.name}  ({destino.stat().st_size/1000:.0f} KB)")
    return destino


if __name__ == "__main__":
    nombres = sys.argv[1:]
    if not nombres:
        raise SystemExit("uso: gen_ilustraciones.py <nombre> [nombre ...]")
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(generar, nombres))
