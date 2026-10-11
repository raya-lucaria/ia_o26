#!/usr/bin/env bash
# generadores_limpios.sh — compuerta 1: correr los generadores y exigir árbol limpio.
#
# Uso:
#   generadores_limpios.sh course/7_juegos                 # detecta los gen_*.py de la unidad
#   generadores_limpios.sh tools/gen_juegos.py tools/gen_traza_web.py
#   generadores_limpios.sh --sin-commit course/7_juegos    # durante el trabajo, antes de comitear
#
# Qué hace:
#   1. Arma la lista de generadores: los .py que se le pasen, o, para cada
#      directorio de unidad, los tools/gen_*.py que nombran su ruta
#      («course/7_juegos») o su constante ASSETS_* de tools/unidades.py.
#      gen_ilustraciones.py NUNCA se corre (cuesta dinero; ver CLAUDE.md).
#   2. Los corre desde la raíz del repo: `python3 tools/gen_x.py`.
#   3. Modo por omisión (estricto, para antes de publicar): falla si
#      `git status --porcelain` muestra cualquier cambio en los _assets/ de
#      las unidades tocadas o en los archivos que cambió la corrida. Lo
#      comiteado tiene que ser lo que el generador produce hoy.
#      Con --sin-commit: solo falla si la corrida CAMBIÓ algo respecto de lo
#      que había en disco (el árbol de trabajo ya es lo que el generador
#      produce); los cambios previos sin comitear se listan, no fallan.
#
# Sale 0 si limpio, 1 si hay cambios, 2 por error de uso o de un generador.
set -uo pipefail

RAIZ="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)" || exit 2
cd "$RAIZ" || exit 2

sin_commit=0
gens=()
unidades=()
for a in "$@"; do
  case "$a" in
    --sin-commit) sin_commit=1 ;;
    -h|--help) sed -n '2,22p' "$0"; exit 0 ;;
    *.py) gens+=("tools/$(basename "$a")") ;;
    *) d="${a%/}"; [ -d "$d" ] || { echo "no existe: $d" >&2; exit 2; }; unidades+=("$d") ;;
  esac
done
[ ${#gens[@]} -eq 0 ] && [ ${#unidades[@]} -eq 0 ] && { sed -n '2,22p' "$0"; exit 2; }

# Detecta los generadores de cada unidad.
for u in "${unidades[@]}"; do
  base="${u#course/}"; base="${base%%/*}"
  consts=$(grep -E "^ASSETS_[A-Z_]+ = RAIZ / \"course/${base}[/\"]" tools/unidades.py \
           | sed -E 's/ =.*//' | paste -sd'|' -)
  for g in tools/gen_*.py; do
    if grep -q "course/${base}\b" "$g" || { [ -n "$consts" ] && grep -Eq "\b(${consts})\b" "$g"; }; then
      gens+=("$g")
    fi
  done
done

# Únicos, y fuera gen_ilustraciones.py.
mapfile -t gens < <(printf '%s\n' "${gens[@]}" | grep -v '/gen_ilustraciones\.py$' | awk '!v[$0]++')
[ ${#gens[@]} -eq 0 ] && { echo "ningún generador para: ${unidades[*]}" >&2; exit 2; }

# Rutas vigiladas: los _assets/ de las unidades (de los args o de los generadores).
vigiladas=()
for u in "${unidades[@]}"; do
  base="${u#course/}"; vigiladas+=("course/${base%%/*}")
done
for g in "${gens[@]}"; do
  for c in $(grep -oE 'ASSETS_[A-Z_]+' "$g" | sort -u); do
    p=$(grep -E "^${c} = RAIZ / \"" tools/unidades.py | sed -E 's/.*"(course\/[^/"]+).*/\1/')
    [ -n "$p" ] && vigiladas+=("$p")
  done
  for p in $(grep -oE 'course/[0-9][A-Za-z0-9_]+' "$g" | sort -u); do vigiladas+=("$p"); done
done
mapfile -t vigiladas < <(printf '%s\n' "${vigiladas[@]}" | awk '!v[$0]++')

huella() {  # hash de cada archivo cambiado o sin seguimiento en las rutas vigiladas
  git status --porcelain --untracked-files=all -- "${vigiladas[@]}" | cut -c4- \
    | while read -r f; do [ -f "$f" ] && echo "$(sha1sum "$f" | cut -c1-40) $f" || echo "borrado $f"; done | sort
}

antes="$(huella)"
for g in "${gens[@]}"; do
  echo "→ python3 $g"
  python3 "$g" > /tmp/gen_limpio.$$ 2>&1 || { cat /tmp/gen_limpio.$$; rm -f /tmp/gen_limpio.$$;
    echo "FALLA: $g terminó con error" >&2; exit 2; }
  tail -n 2 /tmp/gen_limpio.$$ | sed 's/^/    /'
done
rm -f /tmp/gen_limpio.$$
despues="$(huella)"

echo "Vigilado: ${vigiladas[*]}"
if [ "$sin_commit" -eq 1 ]; then
  cambio=$(diff <(echo "$antes") <(echo "$despues") | grep -E '^[<>]' || true)
  [ -n "$antes" ] && { echo "Cambios previos sin comitear (no fallan con --sin-commit):"; echo "$antes" | cut -c42- | sed 's/^/    /'; }
  if [ -n "$cambio" ]; then
    echo "FALLA: la corrida cambió archivos; lo que había en disco no era lo que producen los generadores:"
    echo "$cambio" | sed 's/^/    /'
    exit 1
  fi
  echo "OK: los generadores no cambiaron nada en disco."
  exit 0
fi

sucio=$(git status --porcelain --untracked-files=all -- "${vigiladas[@]}")
if [ -n "$sucio" ]; then
  echo "FALLA: git status no queda limpio tras los generadores:"
  echo "$sucio" | sed 's/^/    /'
  echo "Si el cambio es el que buscabas, revísalo (git diff), comitéalo y vuelve a correr esto."
  exit 1
fi
echo "OK: git status limpio tras ${#gens[@]} generador(es)."
