"""Descarga fotografias de Wikimedia Commons con su autor y licencia."""
import csv
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image

from unidades import ASSETS_POR_UNIDAD

RAIZ = Path(__file__).resolve().parent.parent
LISTA = RAIZ / "tools/commons.tsv"
API = "https://commons.wikimedia.org/w/api.php"
AGENTE = "ia-o26-curso/1.0 (material educativo ITAM)"
ANCHO = 1400


def metadatos(titulo):
    params = {
        "action": "query", "format": "json", "prop": "imageinfo",
        "iiprop": "url|extmetadata", "iiurlwidth": str(ANCHO),
        "titles": titulo,
    }
    req = urllib.request.Request(
        f"{API}?{urllib.parse.urlencode(params)}", headers={"User-Agent": AGENTE}
    )
    for intento in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                datos = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and intento < 4:
                time.sleep(15 * (intento + 1))
                continue
            raise
    paginas = datos["query"]["pages"]
    info = next(iter(paginas.values())).get("imageinfo")
    if not info:
        raise SystemExit(f"NO EXISTE en Commons: {titulo}")
    meta = info[0].get("extmetadata", {})
    return {
        "url": info[0].get("thumburl") or info[0]["url"],
        "autor": meta.get("Artist", {}).get("value", "desconocido"),
        "licencia": meta.get("LicenseShortName", {}).get("value", "sin declarar"),
        "descripcion_commons": titulo,
    }


def limpiar_html(texto):
    import re
    return re.sub(r"<[^>]+>", "", texto).strip()


def descargar_con_reintento(url, destino, intentos=5):
    req = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    for intento in range(intentos):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                destino.write_bytes(r.read())
            return
        except urllib.error.HTTPError as e:
            if e.code == 429 and intento < intentos - 1:
                time.sleep(30 * (intento + 1))
                continue
            raise


def main():
    for assets in ASSETS_POR_UNIDAD.values():
        assets.mkdir(parents=True, exist_ok=True)
    creditos = []
    with LISTA.open(encoding="utf-8") as f:
        for fila in csv.DictReader(f, delimiter="\t"):
            assets = ASSETS_POR_UNIDAD[fila["unidad"]]
            destino = assets / fila["destino"]
            meta = metadatos(fila["pagina_commons"])
            time.sleep(3)
            if not destino.is_file():
                descargar_con_reintento(meta["url"], destino)
                with Image.open(destino) as im:
                    im = im.convert("RGB")
                    if im.width > ANCHO:
                        alto = round(im.height * ANCHO / im.width)
                        im = im.resize((ANCHO, alto), Image.LANCZOS)
                    im.save(destino, quality=82, optimize=True)
                time.sleep(8)
            creditos.append((
                fila["unidad"],
                f'| `{fila["destino"]}` | {fila["descripcion"]} | '
                f'{limpiar_html(meta["autor"])} — Wikimedia Commons | '
                f'{limpiar_html(meta["licencia"])} |',
            ))
            print(f'{fila["destino"]}  <-  {meta["licencia"]}')
    print("\nFilas para CREDITOS.md (agrupadas por unidad):")
    for unidad in ASSETS_POR_UNIDAD:
        propias = [c for u, c in creditos if u == unidad]
        if propias:
            print(f"\n## {unidad}\n" + "\n".join(propias))


if __name__ == "__main__":
    main()
