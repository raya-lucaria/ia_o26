#!/usr/bin/env bash
# capturas.sh — compuerta 5: capturas a 390x844 y 1280x800 de páginas construidas y SVG.
#
# Uso:
#   capturas.sh SALIDA RUTA [RUTA ...]
#   capturas.sh /tmp/cap juegos/mirar-todo-y-podar/minimax/ course/7_juegos/_assets/jue-t-arbol.svg
#
# RUTA: ruta del sitio construido (artifact/site/<ruta>/index.html), un .svg,
# o un .html de _assets/ con #fragmento opcional. SALIDA va fuera del repo
# (el scratchpad). Construye antes con raya build.
#
# Con playwright instalado delega en capturas.py: página completa, todos los
# <details> abiertos, MathJax terminado, scrollWidth y errores de consola.
# Sin playwright cae a `google-chrome --headless --screenshot`: solo la
# ventana (alto 844 y 800, no la página completa), <details> cerrados y sin
# medir nada; avisa de ello (SIN_PLAYWRIGHT=1 fuerza este modo).
# Después: mira cada PNG (Read de la imagen).
set -uo pipefail

[ $# -lt 2 ] && { sed -n '2,18p' "$0"; exit 2; }
DIR="$(cd "$(dirname "$0")" && pwd)"
RAIZ="$(git -C "$DIR" rev-parse --show-toplevel)" || exit 2
SALIDA="$1"; shift
mkdir -p "$SALIDA"

if [ -z "${SIN_PLAYWRIGHT:-}" ] && python3 -c "import playwright" 2>/dev/null; then
  exec python3 "$DIR/capturas.py" --salida "$SALIDA" "$@"
fi

echo "AVISO: sin playwright; capturas solo de ventana, con <details> cerrados." >&2
CHROME="$(command -v google-chrome || command -v chromium || command -v chromium-browser)" \
  || { echo "no hay Chrome/Chromium" >&2; exit 2; }
falla=0
for ruta in "$@"; do
  base="${ruta%%#*}"; frag=""; [ "$base" != "$ruta" ] && frag="#${ruta#*#}"
  case "$base" in
    /*) f="$base" ;;
    *.svg|*.html) f="$RAIZ/$base" ;;
    *) f="$RAIZ/artifact/site/${base#/}"; f="${f%/}/index.html" ;;
  esac
  [ -f "$f" ] || { echo "NO EXISTE $f"; falla=1; continue; }
  nombre="$(echo "${ruta#course/}" | sed -E 's/[^A-Za-z0-9]+/-/g; s/^-+|-+$//g')"
  for tam in 390,844 1280,800; do
    png="$SALIDA/${nombre}_${tam%%,*}.png"
    "$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
      --force-device-scale-factor=1 --window-size="$tam" \
      --screenshot="$png" "file://$f$frag" >/dev/null 2>&1 \
      && echo "ok  $png" || { echo "MAL $png"; falla=1; }
  done
done
exit $falla
