"""Teoría clásica de laminados (CLT).

Convenciones (Kaw 2006, cap. 4): capas numeradas de arriba (k = 1) hacia abajo;
z medida desde el plano medio y positiva hacia abajo; h_0 = −h/2 en la cara superior.
Esfuerzos resultantes N [fuerza/longitud] y M [fuerza·longitud/longitud].
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .lamina import Lamina, Qbar, T, alfa_global, beta_global, deformacion_a_local


@dataclass
class Capa:
    lamina: Lamina
    theta: float
    t: float


@dataclass
class Laminado:
    capas: list[Capa]
    z: np.ndarray = field(init=False)

    def __post_init__(self):
        espesores = np.array([c.t for c in self.capas])
        h = espesores.sum()
        self.z = np.concatenate([[-h / 2], -h / 2 + np.cumsum(espesores)])

    @property
    def h(self) -> float:
        return float(self.z[-1] - self.z[0])

    def Qbar(self, k: int) -> np.ndarray:
        c = self.capas[k]
        return Qbar(c.lamina, c.theta)

    def ABD(self):
        A = np.zeros((3, 3)); B = np.zeros((3, 3)); D = np.zeros((3, 3))
        for k in range(len(self.capas)):
            Q = self.Qbar(k)
            z0, z1 = self.z[k], self.z[k + 1]
            A += Q * (z1 - z0)
            B += Q * (z1 ** 2 - z0 ** 2) / 2
            D += Q * (z1 ** 3 - z0 ** 3) / 3
        return A, B, D

    def matriz_6x6(self) -> np.ndarray:
        A, B, D = self.ABD()
        return np.block([[A, B], [B, D]])

    def cargas_higrotermicas(self, dT: float = 0.0, dC: float = 0.0):
        """Fuerzas y momentos ficticios térmicos y de humedad (Kaw ec. 4.64–4.67)."""
        N = np.zeros(3); M = np.zeros(3)
        for k, c in enumerate(self.capas):
            Q = self.Qbar(k)
            e = alfa_global(c.lamina, c.theta) * dT + beta_global(c.lamina, c.theta) * dC
            z0, z1 = self.z[k], self.z[k + 1]
            N += Q @ e * (z1 - z0)
            M += Q @ e * (z1 ** 2 - z0 ** 2) / 2
        return N, M

    def respuesta(self, N=(0, 0, 0), M=(0, 0, 0), dT: float = 0.0, dC: float = 0.0):
        """Deformaciones del plano medio ε⁰ y curvaturas κ (Kaw ec. 4.29 y 4.68)."""
        NT, MT = self.cargas_higrotermicas(dT, dC)
        F = np.concatenate([np.asarray(N, float) + NT, np.asarray(M, float) + MT])
        x = np.linalg.solve(self.matriz_6x6(), F)
        return x[:3], x[3:]

    def estado_capa(self, k: int, posicion: str, eps0, kappa, dT=0.0, dC=0.0) -> dict:
        """Deformaciones y esfuerzos globales y locales en 'sup', 'medio' o 'inf' de la capa k."""
        z = {"sup": self.z[k], "medio": (self.z[k] + self.z[k + 1]) / 2, "inf": self.z[k + 1]}[posicion]
        c = self.capas[k]
        eps = np.asarray(eps0) + z * np.asarray(kappa)
        libre = alfa_global(c.lamina, c.theta) * dT + beta_global(c.lamina, c.theta) * dC
        sig = self.Qbar(k) @ (eps - libre)
        return {"z": z, "eps_global": eps, "sig_global": sig,
                "eps_local": deformacion_a_local(eps, c.theta),
                "sig_local": T(c.theta) @ sig, "eps_mecanica": eps - libre}

    def constantes_en_plano(self) -> dict:
        """Constantes ingenieriles en el plano de un laminado simétrico (Kaw ec. 4.35–4.45)."""
        As = np.linalg.inv(self.ABD()[0])
        h = self.h
        return {"Ex": 1 / (h * As[0, 0]), "Ey": 1 / (h * As[1, 1]), "Gxy": 1 / (h * As[2, 2]),
                "nuxy": -As[0, 1] / As[0, 0], "nuyx": -As[0, 1] / As[1, 1], "A_inv": As}

    def constantes_flexion(self) -> dict:
        """Constantes ingenieriles a flexión de un laminado simétrico (Kaw ec. 4.46–4.53)."""
        Ds = np.linalg.inv(self.ABD()[2])
        h3 = self.h ** 3
        return {"Exf": 12 / (h3 * Ds[0, 0]), "Eyf": 12 / (h3 * Ds[1, 1]), "Gxyf": 12 / (h3 * Ds[2, 2]),
                "nuxyf": -Ds[0, 1] / Ds[0, 0], "nuyxf": -Ds[0, 1] / Ds[1, 1], "D_inv": Ds}

    def coeficientes_expansion(self) -> dict:
        """α y β del laminado simétrico: [A]⁻¹ N^T(ΔT=1) y [A]⁻¹ N^C(ΔC=1) (Kaw ec. 4.72–4.73)."""
        As = np.linalg.inv(self.ABD()[0])
        NT, _ = self.cargas_higrotermicas(dT=1.0)
        NC, _ = self.cargas_higrotermicas(dC=1.0)
        return {"alfa": As @ NT, "beta": As @ NC, "NT_unit": NT, "NC_unit": NC}


def alabeo(kappa, x, y):
    """Deflexión fuera del plano por curvatura uniforme, relativa a (0,0) (Kaw ec. 4.82)."""
    kx, ky, kxy = kappa
    return -(kx * x ** 2 + ky * y ** 2 + kxy * x * y) / 2


def A_sobre_h_por_fracciones(lamina: Lamina, fracciones: dict) -> np.ndarray:
    """(1/h)[A] de un laminado definido por proporciones de capas por orientación (Gay ec. 12.8)."""
    total = sum(fracciones.values())
    return sum(Qbar(lamina, th) * f / total for th, f in fracciones.items())
