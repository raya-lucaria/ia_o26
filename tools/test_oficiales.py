import re
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
CARDS = RAIZ / "course/1_introduccion/2_historia_ia/_official/cards"

PREFIJO = re.compile(r"^\d+_")


def archivos():
    return sorted(CARDS.glob("*.yaml"))


def tarjetas():
    return [(p, yaml.safe_load(p.read_text(encoding="utf-8"))) for p in archivos()]


def test_hay_al_menos_veinte_tarjetas():
    assert len(archivos()) >= 20, f"solo hay {len(archivos())} tarjetas, se esperaban al menos 20"


def test_cada_tarjeta_tiene_type_card():
    for path, data in tarjetas():
        assert data.get("type") == "card", f"{path.name}: type no es 'card'"


def test_cada_tarjeta_tiene_authority_official():
    for path, data in tarjetas():
        assert data.get("authority") == "official", f"{path.name}: authority no es 'official'"


def test_cada_tarjeta_tiene_anverso_y_reverso_no_vacios():
    for path, data in tarjetas():
        content = data.get("content", {})
        front = content.get("front", "")
        back = content.get("back", "")
        assert isinstance(front, str) and front.strip(), f"{path.name}: front vacio"
        assert isinstance(back, str) and back.strip(), f"{path.name}: back vacio"


def test_ninguna_tarjeta_trae_bloque_scope():
    for path, data in tarjetas():
        assert "scope" not in data, f"{path.name}: no debe traer bloque scope (se infiere del directorio)"


def test_los_id_son_unicos():
    ids = [data.get("id") for _path, data in tarjetas()]
    assert all(ids), "hay una tarjeta sin id"
    assert len(ids) == len(set(ids)), f"hay ids duplicados: {ids}"


def test_los_nombres_de_archivo_llevan_prefijo_numerico():
    for path in archivos():
        assert PREFIJO.match(path.name), f"{path.name}: falta el prefijo numerico de orden"
