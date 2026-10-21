"""Lectura de datos con trazabilidad.

Regla del proyecto: todo dato numérico vive en ``data/`` y cada archivo
CSV tiene un ``.meta.json`` hermano con la fuente, las unidades, la base
estadística y los problemas conocidos. Este módulo se niega a cargar un
CSV sin su archivo de metadatos.
"""
from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"


@dataclass
class Tabla:
    """Tabla numérica con etiquetas de filas/columnas y metadatos de fuente."""

    filas: list[str]
    columnas: list[str]
    valores: np.ndarray
    meta: dict = field(default_factory=dict)

    def col(self, nombre: str) -> np.ndarray:
        return self.valores[:, self.columnas.index(nombre)]

    def fila(self, nombre: str) -> np.ndarray:
        return self.valores[self.filas.index(nombre), :]


def leer_meta(ruta_csv: Path) -> dict:
    ruta_meta = ruta_csv.with_suffix(".meta.json")
    if not ruta_meta.exists():
        raise FileNotFoundError(
            f"{ruta_csv.name} no tiene {ruta_meta.name}: todo dato requiere fuente documentada"
        )
    return json.loads(ruta_meta.read_text(encoding="utf-8"))


def leer_tabla(relativa: str, columnas_texto: int = 1) -> Tabla:
    """Lee un CSV cuya primera columna es la etiqueta de fila."""
    ruta = DATA / relativa
    meta = leer_meta(ruta)
    with ruta.open(encoding="utf-8") as f:
        lector = csv.reader(f)
        encabezado = next(lector)
        filas, valores = [], []
        for r in lector:
            if not r:
                continue
            filas.append(r[0])
            valores.append([float(v) for v in r[columnas_texto:]])
    return Tabla(filas, encabezado[columnas_texto:], np.array(valores, dtype=float), meta)


def leer_csv_texto(relativa: str) -> list[dict]:
    """Lee un CSV mixto (texto y números) como lista de diccionarios."""
    ruta = DATA / relativa
    leer_meta(ruta)
    with ruta.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def leer_json(relativa: str) -> dict:
    return json.loads((DATA / relativa).read_text(encoding="utf-8"))
