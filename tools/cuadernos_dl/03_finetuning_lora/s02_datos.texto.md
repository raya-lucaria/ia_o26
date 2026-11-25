### celda: s02-intro

## 02 · Datos: caras de anime

- **Qué vamos a enseñarle al modelo:** el estilo «cara de anime». Las caras vienen de la colección *moeimouto*, compilada en el dataset `ComputerVisionAnimeProject/AnimeFaceColorization` (CC-BY-4.0).
- Cada carpeta `reference/NNN_<personaje>` tiene ≈ 64 caras de 252 px. Elegimos personajes y caras con semilla; el resto de las carpetas no se usa.
- Todas las caras llevan el mismo caption, `"an anime face"`.

| Paso | Qué hace | Por qué |
|---|---|---|
| Manifiesto | lista exacta de archivos, elegidos con semilla | misma muestra en cada corrida |
| Deduplicar | hash de la cara reducida a 16×16 | una cara repetida en train y test premia memorizar |
| Partir | 80 % train, 10 % validation, 10 % test **dentro de cada personaje** | los tres conjuntos ven los mismos personajes |
| Reescalar | 252 → 512 px, bicúbico | SD 1.5 trabaja a 512 px |

- **Ojo con el reescalado:** agrandar 252 → 512 suaviza los bordes. El modelo también aprende ese suavizado.
- Validation sirve para elegir. Test se usa **una sola vez**, en el cierre.

### celda: s02-tira-explica

- Ocho caras reales de train, reducidas a 128 px. Es la única vez que el notebook muestra caras reales; el resto son generadas.
- `CONTROL` son 16 caras de train. En la sección de memorización entrenamos con ellas muchos pasos a propósito.
