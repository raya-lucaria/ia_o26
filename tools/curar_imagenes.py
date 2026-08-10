"""Extrae, inventaria y recomprime las imagenes del deck heredado."""
import csv
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
PPTX = RAIZ / "legacy/02_historia_del_ai.pptx"
TRABAJO = Path("/tmp/curaduria")
ASSETS = RAIZ / "course/1_introduccion/2_historia_ia/_assets"
INVENTARIO = RAIZ / "tools/imagenes_heredadas.tsv"
ANCHO_MAX = 1400

NS_P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
NS_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def extraer():
    TRABAJO.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(PPTX) as z:
        z.extractall(TRABAJO / "pptx")
    return TRABAJO / "pptx"


def uso_por_imagen(base):
    """Devuelve {imagen: [numeros de diapositiva]} para saber que es plantilla."""
    uso = {}
    for rels in (base / "ppt/slides/_rels").glob("slide*.xml.rels"):
        n = int(re.search(r"slide(\d+)\.xml", rels.name).group(1))
        for rel in ET.parse(rels).getroot():
            if rel.get("TargetMode") == "External":
                continue
            destino = rel.get("Target", "")
            if "media/" in destino:
                uso.setdefault(Path(destino).name, []).append(n)
    return uso


def titulo_de_diapositiva(base, n):
    ruta = base / f"ppt/slides/slide{n}.xml"
    if not ruta.is_file():
        return ""
    textos = [
        t.text.strip()
        for t in ET.parse(ruta).getroot().iter(f"{NS_A}t")
        if t.text and t.text.strip()
    ]
    return textos[0][:60] if textos else ""


def hojas_de_contacto(base, uso):
    """Monta las candidatas en hojas de 12 para revisarlas a ojo."""
    candidatas = sorted(
        img for img, slides in uso.items() if len(slides) <= 3
    )
    salida = TRABAJO / "hojas"
    salida.mkdir(exist_ok=True)
    for i in range(0, len(candidatas), 12):
        lote = candidatas[i : i + 12]
        rutas = [str(base / "ppt/media" / nombre) for nombre in lote]
        subprocess.run(
            ["montage", "-background", "#211033", "-fill", "white", "-pointsize", "14",
             "-label", "%f", *rutas, "-thumbnail", "300x300", "-tile", "4x3",
             "-geometry", "+8+8", str(salida / f"hoja_{i//12:02d}.png")],
            check=True,
        )
    print(f"hojas de contacto en {salida}")
    return candidatas


def recomprimir():
    """Copia y recomprime solo las imagenes marcadas como conservar."""
    base = TRABAJO / "pptx/ppt/media"
    ASSETS.mkdir(parents=True, exist_ok=True)
    with INVENTARIO.open(encoding="utf-8") as f:
        filas = [r for r in csv.DictReader(f, delimiter="\t") if r["decision"] == "conservar"]
    for fila in filas:
        origen = base / fila["origen"]
        destino = ASSETS / fila["destino"]
        with Image.open(origen) as im:
            if im.mode in ("RGBA", "P"):
                im = im.convert("RGBA")
            if im.width > ANCHO_MAX:
                alto = round(im.height * ANCHO_MAX / im.width)
                im = im.resize((ANCHO_MAX, alto), Image.LANCZOS)
            if destino.suffix.lower() in (".jpg", ".jpeg"):
                im.convert("RGB").save(destino, quality=82, optimize=True)
            else:
                im.save(destino, optimize=True)
        print(f"{fila['origen']} -> {destino.name}")
    print(f"{len(filas)} imagenes conservadas")


if __name__ == "__main__":
    base = extraer()
    uso = uso_por_imagen(base)
    plantilla = sorted(img for img, s in uso.items() if len(s) > 3)
    print(f"descartadas por plantilla ({len(plantilla)}): {plantilla}")
    candidatas = hojas_de_contacto(base, uso)
    print(f"candidatas a revisar: {len(candidatas)}")
    for img in candidatas:
        n = uso[img][0]
        print(f"{img}\t{uso[img]}\t{titulo_de_diapositiva(base, n)}")
    recomprimir()
