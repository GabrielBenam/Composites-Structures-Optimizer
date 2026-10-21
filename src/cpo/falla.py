"""Criterios de falla de una lámina expresados como razón de resistencia (SR).

SR = carga máxima aplicable / carga aplicada (Kaw ec. 2.142). Factor de reserva
RF = SR. Margen de seguridad MS = SR − 1. El índice de falla de los criterios
cuadráticos es IF = 1/SR².

Todas las funciones reciben esfuerzos locales [σ1, σ2, τ12] y resistencias en
magnitud (Xc, Yc positivas).
"""
from __future__ import annotations

import math

import numpy as np

from .lamina import Lamina, S_local


def _sr_lineal(valor, limite_pos, limite_neg):
    if valor > 0:
        return limite_pos / valor
    if valor < 0:
        return limite_neg / -valor
    return math.inf


def sr_esfuerzo_maximo(sig_local, L: Lamina) -> tuple[float, str]:
    """Esfuerzo máximo (Kaw ec. 2.141). Devuelve (SR, modo)."""
    s1, s2, t12 = sig_local
    candidatos = {"1T" if s1 > 0 else "1C": _sr_lineal(s1, L.Xt, L.Xc),
                  "2T" if s2 > 0 else "2C": _sr_lineal(s2, L.Yt, L.Yc),
                  "S": _sr_lineal(abs(t12), L.S, L.S)}
    modo = min(candidatos, key=candidatos.get)
    return candidatos[modo], modo


def deformaciones_ultimas(L: Lamina) -> dict:
    """Deformaciones últimas supuestas lineales hasta la falla (Kaw ej. 2.17)."""
    return {"e1T": L.Xt / L.E1, "e1C": L.Xc / L.E1, "e2T": L.Yt / L.E2,
            "e2C": L.Yc / L.E2, "g12": L.S / L.G12}


def sr_deformacion_maxima(sig_local, L: Lamina) -> tuple[float, str]:
    """Deformación máxima (Kaw ec. 2.143) a partir de los esfuerzos locales."""
    e1, e2, g12 = S_local(L) @ np.asarray(sig_local, float)
    u = deformaciones_ultimas(L)
    candidatos = {"1T" if e1 > 0 else "1C": _sr_lineal(e1, u["e1T"], u["e1C"]),
                  "2T" if e2 > 0 else "2C": _sr_lineal(e2, u["e2T"], u["e2C"]),
                  "S": _sr_lineal(abs(g12), u["g12"], u["g12"])}
    modo = min(candidatos, key=candidatos.get)
    return candidatos[modo], modo


def indice_tsai_hill(sig_local, X1, X2, Y, S) -> float:
    """(σ1/X1)² − σ1σ2/X2² + (σ2/Y)² + (τ12/S)² (Kaw ec. 2.150–2.151; Gay ec. 14.6)."""
    s1, s2, t = sig_local
    return (s1 / X1) ** 2 - s1 * s2 / X2 ** 2 + (s2 / Y) ** 2 + (t / S) ** 2


def sr_tsai_hill(sig_local, L: Lamina, modificado: bool = False) -> float:
    """Tsai-Hill. Original: X = Xt, Y = Yt. Modificado: resistencias según el signo."""
    s1, s2, _ = sig_local
    if modificado:
        X1 = L.Xt if s1 > 0 else L.Xc
        X2 = L.Xt if s2 > 0 else L.Xc
        Y = L.Yt if s2 > 0 else L.Yc
    else:
        X1 = X2 = L.Xt
        Y = L.Yt
    return 1 / math.sqrt(indice_tsai_hill(sig_local, X1, X2, Y, L.S))


def coeficientes_tsai_wu(L: Lamina, H12: str | float = "mises-hencky") -> dict:
    """Coeficientes de Tsai-Wu (Kaw ec. 2.155–2.171)."""
    c = {"H1": 1 / L.Xt - 1 / L.Xc, "H2": 1 / L.Yt - 1 / L.Yc, "H6": 0.0,
         "H11": 1 / (L.Xt * L.Xc), "H22": 1 / (L.Yt * L.Yc), "H66": 1 / L.S ** 2}
    if isinstance(H12, (int, float)):
        c["H12"] = float(H12)
    elif H12 == "mises-hencky":
        c["H12"] = -0.5 * math.sqrt(c["H11"] * c["H22"])
    elif H12 == "tsai-hill":
        c["H12"] = -1 / (2 * L.Xt ** 2)
    elif H12 == "hoffman":
        c["H12"] = -1 / (2 * L.Xt * L.Xc)
    else:
        raise ValueError(H12)
    return c


def sr_tsai_wu(sig_local, L: Lamina, H12: str | float = "mises-hencky") -> float:
    """Tsai-Wu: resuelve a·SR² + b·SR = 1 (Kaw ec. 2.152)."""
    c = coeficientes_tsai_wu(L, H12)
    s1, s2, t = sig_local
    a = c["H11"] * s1 ** 2 + c["H22"] * s2 ** 2 + c["H66"] * t ** 2 + 2 * c["H12"] * s1 * s2
    b = c["H1"] * s1 + c["H2"] * s2 + c["H6"] * t
    return (-b + math.sqrt(b * b + 4 * a)) / (2 * a)
