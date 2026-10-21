"""Carga de láminas desde data/materiales con trazabilidad."""
from __future__ import annotations

import csv

from .datos import DATA, leer_meta
from .lamina import Lamina

_CAMPOS = ["E1", "E2", "nu12", "G12", "Xt", "Xc", "Yt", "Yc", "S", "a1", "a2", "b1", "b2"]


def cargar(archivo: str, material: str) -> Lamina:
    ruta = DATA / "materiales" / archivo
    leer_meta(ruta)
    with ruta.open(encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            if fila["material"] == material:
                return Lamina(**{k: float(fila[k]) for k in _CAMPOS}, nombre=material)
    raise KeyError(f"{material} no está en {archivo}")


def kaw(material: str) -> Lamina:
    """Láminas de Kaw (2006), Tabla 2.1, en Pa."""
    return cargar("kaw_tabla2_1.csv", material)


def gay_tela_carbono() -> Lamina:
    """Tela balanceada carbono/epóxica de Gay (2015), Tabla 3.6, en MPa."""
    return cargar("gay_tabla3_6_telas.csv", "carbono_tela_gay")
