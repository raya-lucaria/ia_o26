"""Pruebas de la caja de herramientas del notebook 02 (§1–3).

Arman con el generador el script de las secciones 1–3, le agregan unas líneas
que ejercitan la caja y lo corren en un subproceso con RAPIDO=1 (CPU, datos
recortados). Se saltan si no hay torch o si MNIST no está descargado
(MNIST_DIR, o ~/.cache/mnist_torchvision por omisión).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
GENERADOR = RAIZ / "tools" / "gen_cuaderno_entender_red.py"
MNIST_DIR = Path(os.environ.get(
    "MNIST_DIR", Path.home() / ".cache" / "mnist_torchvision"))

pytest.importorskip("torch")
pytest.importorskip("torchvision")
if not (MNIST_DIR / "MNIST" / "raw").is_dir():
    pytest.skip(f"MNIST no está en {MNIST_DIR}", allow_module_level=True)

SONDA = r'''
import json as _json
_r = {}
# 1) Reejecutar entrenar con el mismo ID deja una sola fila.
for _ in range(2):
    entrenar(Config(id="prueba-repetida", seccion=99, epochs=1,
                    idx_train=subconjunto(300), datos="prueba"))
_t = tabla_maestra()
_r["filas_repetida"] = int((_t["id"] == "prueba-repetida").sum())
_r["corridas_repetida"] = sum(k == "prueba-repetida" for k in CORRIDAS)
# 2) SGD con lr = 5 en una red sin activaciones (identidad, dos ocultas)
#    llega a inf/nan en pocos pasos; curvas no lanza (lineal y log).
#    Con ReLU la loss se dispara pero las neuronas mueren y vuelve a ser finita.
_c = entrenar(Config(id="prueba-diverge", seccion=99, optimizer="sgd", lr=5.0,
                     capas=[784, 128, 128, 10], activacion="identidad",
                     datos="prueba"))
_r["divergio"] = bool(_c.divergio)
_r["paso_no_finito"] = _c.paso_no_finito
_r["pasos"] = int(_c.historial["pasos"].iloc[-1])
curvas([_c]); curvas([_c], metrica="acc"); curvas([_c], log=True)
rejilla([_c, CORRIDAS["prueba-repetida"]])
plt.close("all")
# 3) subconjunto estratificado y determinista.
_i = subconjunto(1000)
_r["por_digito"] = torch.bincount(DATOS["01"]["train"][1].cpu()[_i],
                                  minlength=10).tolist()
_r["determinista"] = bool(torch.equal(_i, subconjunto(1000)))
_r["distinta_semilla"] = not torch.equal(_i, subconjunto(1000, semilla=1))
# 4) adam_l2 y adamw no aplican decay a sesgos (ni a parámetros de BN).
_m = construir_red([784, 32, 10], batch_norm=True)
_sesgos = {id(p) for p in _m.parameters() if p.ndim <= 1}
for _opt in ("adam_l2", "adamw"):
    _o = crear_optimizer(Config(id="x", seccion=99, optimizer=_opt,
                                weight_decay=0.01), _m)
    _r[_opt] = all(id(p) not in _sesgos
                   for g in _o.param_groups if g["weight_decay"] > 0
                   for p in g["params"])
    _r[_opt + "_decay_pesos"] = any(g["weight_decay"] > 0
                                    for g in _o.param_groups)
print("RESULTADO_CAJA " + _json.dumps(_r))
'''


def _entorno(**extra):
    env = dict(os.environ, MPLBACKEND="Agg", MNIST_DIR=str(MNIST_DIR))
    env.update(extra)
    return env


def _script(tmp_path, secciones):
    ruta = tmp_path / f"caja_{secciones.replace(',', '_')}.py"
    subprocess.run([sys.executable, str(GENERADOR), "--script", str(ruta),
                    "--borrador", "--secciones", secciones],
                   check=True, cwd=RAIZ, capture_output=True, text=True)
    return ruta


@pytest.fixture(scope="module")
def resultado(tmp_path_factory):
    ruta = _script(tmp_path_factory.mktemp("caja"), "1,2,3")
    ruta.write_text(ruta.read_text() + "\n" + SONDA)
    corrida = subprocess.run([sys.executable, str(ruta)], cwd=RAIZ,
                             env=_entorno(RAPIDO="1"), capture_output=True,
                             text=True, timeout=600)
    assert corrida.returncode == 0, corrida.stderr[-3000:]
    linea = [l for l in corrida.stdout.splitlines()
             if l.startswith("RESULTADO_CAJA ")][-1]
    return json.loads(linea.removeprefix("RESULTADO_CAJA "))


def test_mismo_id_deja_una_sola_fila(resultado):
    assert resultado["filas_repetida"] == 1
    assert resultado["corridas_repetida"] == 1


def test_sgd_lr_5_sin_activacion_diverge_y_curvas_no_lanza(resultado):
    assert resultado["divergio"] is True
    assert resultado["paso_no_finito"] is not None
    assert 1 <= resultado["paso_no_finito"] <= resultado["pasos"]


def test_subconjunto_estratificado_y_determinista(resultado):
    assert all(99 <= c <= 101 for c in resultado["por_digito"])
    assert sum(resultado["por_digito"]) == 1000
    assert resultado["determinista"]
    assert resultado["distinta_semilla"]


def test_adam_l2_y_adamw_sin_decay_en_sesgos(resultado):
    for opt in ("adam_l2", "adamw"):
        assert resultado[opt], f"{opt} aplica decay a un sesgo"
        assert resultado[opt + "_decay_pesos"], f"{opt} no aplica decay a pesos"


def test_sin_gpu_activa_rapido(tmp_path):
    ruta = _script(tmp_path, "1")
    env = _entorno(CUDA_VISIBLE_DEVICES="")
    env.pop("RAPIDO", None)
    corrida = subprocess.run([sys.executable, str(ruta)], cwd=RAIZ, env=env,
                             capture_output=True, text=True, timeout=300)
    assert corrida.returncode == 0, corrida.stderr[-3000:]
    assert "RAPIDO = True" in corrida.stdout
    assert "NO TIENE GPU" in corrida.stdout
