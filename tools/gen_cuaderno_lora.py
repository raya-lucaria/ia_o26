"""Arma el notebook 03 de deep learning, «Fine-tuning generativo con LoRA».

Envoltorio de tools/gen_cuaderno_entender_red.py: el mismo formato de
fuentes (un par sNN_<slug>.py + sNN_<slug>.texto.md por sección, aquí en
tools/cuadernos_dl/03_finetuning_lora/) y las mismas opciones. Solo cambian
las rutas, la URL de Colab y el badge; todo lo demás es del generador del
notebook 02.

Uso:
    python3 tools/gen_cuaderno_lora.py                          # el .ipynb, sin salidas
    python3 tools/gen_cuaderno_lora.py --script /tmp/humo.py \\
        --borrador --secciones 1,2,3,5                          # código plano
    python3 tools/gen_cuaderno_lora.py --integrar descarga.ipynb
"""
import importlib.util
import sys
from pathlib import Path

# Una copia PRIVADA del generador del notebook 02, no el módulo importado:
# si reasignáramos los globales de `gen_cuaderno_entender_red`, sus propias
# pruebas leerían las fuentes del 03 al correr en la misma sesión de pytest.
_spec = importlib.util.spec_from_file_location(
    "_gen_cuaderno_lora_base",
    Path(__file__).resolve().parent / "gen_cuaderno_entender_red.py")
g = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(g)

# Las funciones del generador leen estos globales al llamarse, no al
# importarse: reasignarlos en la copia basta.
g.FUENTES = g.RAIZ / "tools" / "cuadernos_dl" / "03_finetuning_lora"
g.RUTA_NB = "course/10_deep_learning/_assets/03_finetuning_lora.ipynb"
g.DESTINO = g.RAIZ / g.RUTA_NB
g.URL_COLAB = ("https://colab.research.google.com/github/raya-lucaria/ia_o26/"
               "blob/main/" + g.RUTA_NB)
g.BADGE = ("[![Abrir en Colab](https://colab.research.google.com/assets/"
           f"colab-badge.svg)]({g.URL_COLAB})")
g.PREAMBULO = g.PREAMBULO.replace("gen_cuaderno_entender_red.py",
                                  "gen_cuaderno_lora.py")
g.__doc__ = __doc__                      # la descripción de --help

FUENTES, RUTA_NB, DESTINO = g.FUENTES, g.RUTA_NB, g.DESTINO
URL_COLAB, BADGE = g.URL_COLAB, g.BADGE
cuaderno, script, serializar = g.cuaderno, g.script, g.serializar
fuente, pares, main = g.fuente, g.pares, g.main

if __name__ == "__main__":
    sys.exit(main())
