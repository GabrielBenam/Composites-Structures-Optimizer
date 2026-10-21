"""Mecánica de la lámina (capa) ortótropa.

Convenciones (Kaw 2006, cap. 2; equivalentes a Gay cap. 11 con ℓ ≡ 1, t ≡ 2):
- Ejes locales 1-2 (fibra, transversal); ejes globales x-y; θ medido de x a 1.
- Vectores de esfuerzo [σ1, σ2, τ12] y de deformación ingenieril [ε1, ε2, γ12].
- [T] transforma esfuerzos globales a locales; [R] = diag(1, 1, 2) (matriz de Reuter).
- Unidades consistentes elegidas por el usuario (Pa y m, o MPa y mm).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

R = np.diag([1.0, 1.0, 2.0])
R_INV = np.diag([1.0, 1.0, 0.5])


@dataclass(frozen=True)
class Lamina:
    """Propiedades de una lámina unidireccional (o tela balanceada) en ejes locales."""

    E1: float
    E2: float
    nu12: float
    G12: float
    Xt: float = np.nan   # resistencia longitudinal a tensión
    Xc: float = np.nan   # resistencia longitudinal a compresión (magnitud)
    Yt: float = np.nan   # resistencia transversal a tensión
    Yc: float = np.nan   # resistencia transversal a compresión (magnitud)
    S: float = np.nan    # resistencia a cortante en el plano
    a1: float = 0.0      # coeficiente de expansión térmica longitudinal
    a2: float = 0.0      # coeficiente de expansión térmica transversal
    b1: float = 0.0      # coeficiente de expansión por humedad longitudinal
    b2: float = 0.0      # coeficiente de expansión por humedad transversal
    nombre: str = ""

    @property
    def nu21(self) -> float:
        return self.nu12 * self.E2 / self.E1


# ---------------------------------------------------------------- 3D ortótropo
def S_ortotropo_3d(E1, E2, E3, nu12, nu23, nu13, G12, G23, G31) -> np.ndarray:
    """Matriz de flexibilidad 6x6, orden [1, 2, 3, 23, 31, 12] (Kaw ec. 2.69)."""
    S = np.zeros((6, 6))
    S[0, 0], S[1, 1], S[2, 2] = 1 / E1, 1 / E2, 1 / E3
    S[0, 1] = S[1, 0] = -nu12 / E1
    S[0, 2] = S[2, 0] = -nu13 / E1
    S[1, 2] = S[2, 1] = -nu23 / E2
    S[3, 3], S[4, 4], S[5, 5] = 1 / G23, 1 / G31, 1 / G12
    return S


# ------------------------------------------------------------ esfuerzo plano
def S_local(L: Lamina) -> np.ndarray:
    """Flexibilidad reducida [S] (Kaw ec. 2.92)."""
    return np.array([[1 / L.E1, -L.nu12 / L.E1, 0.0],
                     [-L.nu12 / L.E1, 1 / L.E2, 0.0],
                     [0.0, 0.0, 1 / L.G12]])


def Q_local(L: Lamina) -> np.ndarray:
    """Rigidez reducida [Q] (Kaw ec. 2.93; en Gay, E11, E12, E22, E33 a 0°)."""
    d = 1 - L.nu12 * L.nu21
    return np.array([[L.E1 / d, L.nu12 * L.E2 / d, 0.0],
                     [L.nu12 * L.E2 / d, L.E2 / d, 0.0],
                     [0.0, 0.0, L.G12]])


def T(theta_deg: float) -> np.ndarray:
    """Transformación de esfuerzos globales a locales (Kaw ec. 2.94)."""
    t = np.radians(theta_deg)
    c, s = np.cos(t), np.sin(t)
    return np.array([[c * c, s * s, 2 * s * c],
                     [s * s, c * c, -2 * s * c],
                     [-s * c, s * c, c * c - s * s]])


def Qbar(L: Lamina, theta_deg: float) -> np.ndarray:
    """Rigidez reducida transformada [Q̄] = [T]⁻¹[Q][R][T][R]⁻¹ (Kaw ec. 2.103)."""
    Ti = np.linalg.inv(T(theta_deg))
    return Ti @ Q_local(L) @ R @ T(theta_deg) @ R_INV


def Sbar(L: Lamina, theta_deg: float) -> np.ndarray:
    """Flexibilidad reducida transformada [S̄] = [R][T]⁻¹[R]⁻¹[S][T] (Kaw ec. 2.105)."""
    Ti = np.linalg.inv(T(theta_deg))
    return R @ Ti @ R_INV @ S_local(L) @ T(theta_deg)


def esfuerzo_a_local(sig_global, theta_deg):
    return T(theta_deg) @ np.asarray(sig_global, float)


def deformacion_a_local(eps_global, theta_deg):
    """Deformaciones ingenieriles globales -> locales: [R][T][R]⁻¹."""
    return R @ T(theta_deg) @ R_INV @ np.asarray(eps_global, float)


def esfuerzo_a_global(sig_local, theta_deg):
    return np.linalg.inv(T(theta_deg)) @ np.asarray(sig_local, float)


def constantes_angulo(L: Lamina, theta_deg: float) -> dict:
    """Constantes ingenieriles de una lámina en ángulo (Kaw ec. 2.117–2.128)."""
    Sb = Sbar(L, theta_deg)
    return {"Ex": 1 / Sb[0, 0], "nuxy": -Sb[0, 1] / Sb[0, 0], "mx": -Sb[0, 2] * L.E1,
            "Ey": 1 / Sb[1, 1], "my": -Sb[1, 2] * L.E1, "Gxy": 1 / Sb[2, 2]}


def invariantes(L: Lamina) -> dict:
    """Invariantes de rigidez U1..U4 (Kaw ec. 2.138) y de flexibilidad V1..V4 (ec. 2.140)."""
    Q, S = Q_local(L), S_local(L)
    Q11, Q12, Q22, Q66 = Q[0, 0], Q[0, 1], Q[1, 1], Q[2, 2]
    S11, S12, S22, S66 = S[0, 0], S[0, 1], S[1, 1], S[2, 2]
    return {"U1": (3 * Q11 + 3 * Q22 + 2 * Q12 + 4 * Q66) / 8,
            "U2": (Q11 - Q22) / 2,
            "U3": (Q11 + Q22 - 2 * Q12 - 4 * Q66) / 8,
            "U4": (Q11 + Q22 + 6 * Q12 - 4 * Q66) / 8,
            "V1": (3 * S11 + 3 * S22 + 2 * S12 + S66) / 8,
            "V2": (S11 - S22) / 2,
            "V3": (S11 + S22 - 2 * S12 - S66) / 8,
            "V4": (S11 + S22 + 6 * S12 - S66) / 8}


def principales(vx, vy, vxy, ingenieril=False):
    """Valores principales, ángulo principal [°], máximo cortante y su ángulo [°].

    Para deformaciones usar ``ingenieril=True`` (γxy se divide entre 2).
    """
    t = vxy / 2 if ingenieril else vxy
    c, r = (vx + vy) / 2, np.hypot((vx - vy) / 2, t)
    ang_p = 0.5 * np.degrees(np.arctan2(2 * t, vx - vy))
    ang_s = 0.5 * np.degrees(np.arctan(-(vx - vy) / (2 * t)))
    vmax_corte = 2 * r if ingenieril else r
    return c + r, c - r, ang_p, vmax_corte, ang_s


def alfa_global(L: Lamina, theta_deg: float) -> np.ndarray:
    """[αx, αy, αxy] de una lámina en ángulo (Kaw ec. 2.175, con αxy ingenieril)."""
    v = np.linalg.inv(T(theta_deg)) @ np.array([L.a1, L.a2, 0.0])
    return v * np.array([1, 1, 2])


def beta_global(L: Lamina, theta_deg: float) -> np.ndarray:
    v = np.linalg.inv(T(theta_deg)) @ np.array([L.b1, L.b2, 0.0])
    return v * np.array([1, 1, 2])


def deformacion_galga(eps_global, phi_deg):
    """Deformación normal leída por una galga a φ del eje x (Kaw ec. B.15)."""
    ex, ey, gxy = eps_global
    p = np.radians(phi_deg)
    return ex * np.cos(p) ** 2 + ey * np.sin(p) ** 2 + gxy * np.sin(p) * np.cos(p)
