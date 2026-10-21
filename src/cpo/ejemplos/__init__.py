"""Ejemplos resueltos de la bibliografía, usados como verificación y como material didáctico.

Cada ejemplo es una función registrada con ``@ejemplo(clave, bloque)`` que devuelve una
``Derivacion``. Los valores publicados se leen de ``data/ejemplos/<bloque>_referencias.json``.
"""
from __future__ import annotations

import json
from functools import lru_cache

from ..datos import DATA
from ..derivacion import Derivacion

REGISTRO: dict[str, dict] = {}


def ejemplo(clave: str, bloque: str, libro: str):
    def deco(fn):
        REGISTRO[clave] = {"fn": fn, "bloque": bloque, "libro": libro}
        return fn
    return deco


@lru_cache(maxsize=None)
def referencias(bloque: str) -> dict:
    return json.loads((DATA / "ejemplos" / f"{bloque}_referencias.json").read_text(encoding="utf-8"))


def ref(bloque: str, clave: str) -> dict:
    return referencias(bloque)[clave]


def nueva(clave: str, bloque: str, titulo: str, planteamiento: str) -> tuple[Derivacion, dict]:
    r = ref(bloque, clave)
    fuente = f"{r['fuente']}, p.~{r['pagina']}."
    return Derivacion(clave, titulo, fuente, planteamiento), r["valores"]


def cargar_todos():
    from . import kaw, gay  # noqa: F401,I001  (registra los ejemplos; Kaw primero)
    return REGISTRO


def resolver(clave: str) -> Derivacion:
    cargar_todos()
    return REGISTRO[clave]["fn"]()
