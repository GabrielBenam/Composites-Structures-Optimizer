"""Cargas sobre la semiala: distribución elíptica de la tesis y diagnósticos.

Convención de la tesis (secc. 6.4.2 y 7.2.1): cuarto de elipse con semieje
``a`` = semienvergadura [mm] y semieje ``b`` = carga por unidad de envergadura
en la raíz [N/mm]. El área del cuarto de elipse iguala la sustentación de una
semiala: m·g·n/2 = π·a·b/4.

Unidades: masa kg, g m/s², longitudes mm, fuerzas N, momentos N·mm.
"""
from __future__ import annotations

import math

import numpy as np


def b_eliptica(masa_kg: float, g: float, n: float, semi_mm: float) -> float:
    """Carga en la raíz q(0) [N/mm] para que la semiala sustente m·g·n/2."""
    return 2.0 * masa_kg * g * n / (math.pi * semi_mm)


def n_desde_b(b_N_mm: float, masa_kg: float, g: float, semi_mm: float) -> float:
    """Inversa de :func:`b_eliptica`: factor de carga implícito en un valor de b."""
    return b_N_mm * math.pi * semi_mm / (2.0 * masa_kg * g)


def q_eliptica(x_mm, b_N_mm: float, semi_mm: float):
    """Carga por unidad de envergadura q(x) [N/mm]; cero fuera de [0, a]."""
    x = np.asarray(x_mm, dtype=float)
    r = np.clip(1.0 - (x / semi_mm) ** 2, 0.0, None)
    return b_N_mm * np.sqrt(r)


def sustentacion_semiala(b_N_mm: float, semi_mm: float) -> float:
    """Integral de q(x) en [0, a] = π·a·b/4 [N]."""
    return math.pi * semi_mm * b_N_mm / 4.0


def momento_raiz(b_N_mm: float, semi_mm: float) -> float:
    """Momento flector en la raíz = ∫ q(x)·x dx = b·a²/3 [N·mm]."""
    return b_N_mm * semi_mm**2 / 3.0


def fraccion_larguero_palanca(d_carga_mm: float, d_largueros_mm: float) -> float:
    """Fracción de la carga que toma el larguero principal por regla de la palanca.

    ``d_carga_mm``: distancia de la resultante al larguero principal, medida
    hacia el larguero secundario (positiva si cae entre ambos).
    ``d_largueros_mm``: distancia entre largueros.
    """
    return 1.0 - d_carga_mm / d_largueros_mm


def r2_tesis(sust_N: float, d_sust_mm: float, peso_costilla_N: float, d_cg_mm: float,
             d_largueros_mm: float) -> float:
    """Reacción en el larguero secundario con la ecuación de momentos de la tesis (secc. 7.2.5)."""
    return (sust_N * d_sust_mm + peso_costilla_N * d_cg_mm) / d_largueros_mm


def fuerza_aplicada_por_presion(b_N_mm: float, semi_mm: float, factor: float,
                                divisor_mm: float, ancho_cara_mm: float) -> float:
    """Fuerza total que recibe la viga si la presión se calculó como
    ``factor·q(x)/divisor`` y se aplicó sobre una cara de ancho ``ancho_cara_mm``.

    Con ``divisor = ancho_cara`` el resultado es factor·L (correcto).
    La tesis usó ``divisor = cuerda`` (1125 mm) sobre la cara del patín.
    """
    return factor * sustentacion_semiala(b_N_mm, semi_mm) * ancho_cara_mm / divisor_mm


def ahorro_niu(peso_original_kg: float, peso_nuevo_kg: float, usd_por_kg: float) -> float:
    """Ahorro por reducción de peso según el criterio que la tesis atribuye a Niu."""
    return (peso_original_kg - peso_nuevo_kg) * usd_por_kg
