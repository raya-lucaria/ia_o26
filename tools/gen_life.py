"""Genera un PNG con cuatro generaciones del Game of Life de Conway."""
from pathlib import Path

from PIL import Image, ImageDraw

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "course/1_introduccion/2_historia_ia/_assets/v13-game-of-life.png"

N, CELDA, MARGEN, PASOS = 28, 12, 16, 4
FONDO, MUERTA, VIVA, REJILLA = "#211033", "#2c1642", "#a8ff5a", "#42164f"


def vecinos(rejilla, x, y):
    return sum(
        rejilla[(y + dy) % N][(x + dx) % N]
        for dy in (-1, 0, 1)
        for dx in (-1, 0, 1)
        if (dx, dy) != (0, 0)
    )


def paso(rejilla):
    return [
        [
            1 if (rejilla[y][x] and vecinos(rejilla, x, y) in (2, 3))
            or (not rejilla[y][x] and vecinos(rejilla, x, y) == 3)
            else 0
            for x in range(N)
        ]
        for y in range(N)
    ]


def main():
    # Nave planeadora mas un bloque estable, para que se vea movimiento y quietud.
    rejilla = [[0] * N for _ in range(N)]
    for x, y in [(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)]:
        rejilla[y + 2][x + 2] = 1
    for x, y in [(0, 0), (1, 0), (0, 1), (1, 1)]:
        rejilla[y + 18][x + 18] = 1

    lado = N * CELDA
    ancho = MARGEN + PASOS * (lado + MARGEN)
    img = Image.new("RGB", (ancho, lado + 2 * MARGEN), FONDO)
    dibujo = ImageDraw.Draw(img)

    for p in range(PASOS):
        ox = MARGEN + p * (lado + MARGEN)
        for y in range(N):
            for x in range(N):
                x0, y0 = ox + x * CELDA, MARGEN + y * CELDA
                dibujo.rectangle(
                    [x0, y0, x0 + CELDA - 1, y0 + CELDA - 1],
                    fill=VIVA if rejilla[y][x] else MUERTA,
                    outline=REJILLA,
                )
        rejilla = paso(rejilla)

    img.save(DESTINO, optimize=True)
    print(f"{DESTINO.name}  {DESTINO.stat().st_size/1000:.0f} KB")


if __name__ == "__main__":
    main()
