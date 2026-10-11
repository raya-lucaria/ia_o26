#!/usr/bin/env bash
# en_vivo.sh — compuerta 8: después del merge y del deploy, el sitio publicado.
#
# Uso:
#   en_vivo.sh RUTA [RUTA ...]
#   en_vivo.sh --comparar juegos/ juegos/mirar-todo-y-podar/minimax/
#
# RUTA es la ruta del sitio, la misma que en artifact/site/ («juegos/notacion/»).
# Por cada una:
#   1. GET https://rayalucaria.org/ia_o26/<RUTA> → tiene que dar 200.
#   2. Cada recurso de la unidad que la página usa (src/href a
#      _raya/assets/_source/…: SVG, traza .html, .ipynb) → 200.
#   3. Cada enlace «Abrir en Colab» de la página: el badge responde 200 y el
#      notebook existe en main (raw.githubusercontent.com → 200 y nbformat).
#      OJO: colab.research.google.com responde 200 aunque el archivo no
#      exista, así que lo que se comprueba es la copia en GitHub. El badge
#      solo funciona tras el merge a main.
#   4. Con --comparar: la página publicada es byte a byte la de
#      artifact/site/<RUTA>/index.html (el build es determinista; constrúyelo
#      desde main ya mergeado), y el notebook de main es el del repo local.
# El CDN guarda hasta 10 min (cache-control: max-age=600): si recién
# desplegó y falla 2 o 4, espera y repite antes de concluir.
# Sale 0 si todo está bien, 1 si algo falla.
set -uo pipefail

BASE="https://rayalucaria.org/ia_o26/"
RAW="https://raw.githubusercontent.com/"
RAIZ="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)" || exit 2
comparar=0
rutas=()
for a in "$@"; do
  case "$a" in
    --comparar) comparar=1 ;;
    -h|--help) sed -n '2,24p' "$0"; exit 0 ;;
    *) rutas+=("${a#/}") ;;
  esac
done
[ ${#rutas[@]} -eq 0 ] && { sed -n '2,24p' "$0"; exit 2; }

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
falla=0
codigo() { curl -sL -o "${2:-/dev/null}" -w '%{http_code}' --max-time 30 "$1"; }
mal() { echo "  MAL $*"; falla=1; }

for r in "${rutas[@]}"; do
  url="$BASE$r"
  c=$(codigo "$url" "$TMP/p.html")
  [ "$c" = 200 ] && echo "ok  $c $url" || { mal "$c $url"; continue; }

  # 2. recursos de la unidad (rutas relativas resueltas contra la página)
  dir="$url"; [ "${dir%/}" = "$dir" ] && dir="${dir%/*}/"
  grep -oE '(src|href)="[^"#?]*_raya/assets/_source/[^"#?]*' "$TMP/p.html" | sed -E 's/^(src|href)="//' \
    | sort -u > "$TMP/rec"
  n=0
  while read -r rel; do
    abs=$(python3 -c 'import sys,urllib.parse as u; print(u.urljoin(sys.argv[1], sys.argv[2]))' "$dir" "$rel")
    c=$(codigo "$abs"); n=$((n+1))
    [ "$c" = 200 ] || mal "$c recurso $abs"
  done < "$TMP/rec"
  echo "    $n recurso(s) de la unidad revisados"

  # 3. Colab
  grep -oE 'https://colab\.research\.google\.com/github/[^")[:space:]]+\.ipynb' "$TMP/p.html" | sort -u > "$TMP/colab"
  grep -q 'colab-badge.svg' "$TMP/p.html" && { c=$(codigo "https://colab.research.google.com/assets/colab-badge.svg");
    [ "$c" = 200 ] || mal "$c badge de Colab"; }
  while read -r col; do
    gh="${col#https://colab.research.google.com/github/}"          # owner/repo/blob/main/ruta
    raw="$RAW$(echo "$gh" | sed -E 's#^([^/]+/[^/]+)/blob/#\1/#')"
    c=$(codigo "$raw" "$TMP/nb.ipynb")
    if [ "$c" = 200 ] && python3 -c 'import json,sys; assert json.load(open(sys.argv[1]))["nbformat"]==4' "$TMP/nb.ipynb" 2>/dev/null; then
      echo "    ok  Colab → ${gh#*/blob/}"
      if [ "$comparar" -eq 1 ]; then
        loc="$RAIZ/${gh#*/blob/*/}"
        cmp -s "$TMP/nb.ipynb" "$loc" && echo "    ok  notebook de main = $loc" || mal "el notebook de main difiere de $loc"
      fi
    else
      mal "$c Colab sin notebook en main: $raw"
    fi
  done < "$TMP/colab"

  # 4. publicada = construida
  if [ "$comparar" -eq 1 ]; then
    loc="$RAIZ/artifact/site/${r%/}/index.html"
    if [ ! -f "$loc" ]; then mal "no construida $loc (raya build)"
    elif cmp -s "$TMP/p.html" "$loc"; then echo "    ok  idéntica a $loc"
    else mal "difiere de $loc ($(diff <(tr '>' '\n' <"$TMP/p.html") <(tr '>' '\n' <"$loc") | grep -c '^[<>]') renglones)"; fi
  fi
done
[ $falla -eq 0 ] && echo "OK: ${#rutas[@]} página(s) en vivo." || echo "FALLA en vivo."
exit $falla
