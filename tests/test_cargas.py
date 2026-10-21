"""Verificación del módulo de cargas contra los valores de la tesis y cálculo a mano."""
import math

import pytest

from cpo import cargas as C
from cpo.datos import leer_json

AV = leer_json("aeronave/cessna162.json")
M, G, A = AV["mtow_kg"], AV["g"], AV["semi_envergadura_mm"]


def test_b_publicado_corresponde_a_n_3_8():
    assert C.b_eliptica(M, G, 3.8, A) == pytest.approx(3.059, abs=5e-4)


def test_b_usado_en_ansys_corresponde_a_n_2_5():
    assert C.n_desde_b(2.012, M, G, A) == pytest.approx(2.5, abs=2e-3)


def test_area_elipse_igual_a_sustentacion_semiala():
    b = C.b_eliptica(M, G, 3.8, A)
    assert C.sustentacion_semiala(b, A) == pytest.approx(M * G * 3.8 / 2, rel=1e-12)


def test_integracion_numerica_q_y_momento():
    import numpy as np
    b = 2.0
    x = np.linspace(0, A, 200001)
    q = C.q_eliptica(x, b, A)
    trap = getattr(np, "trapezoid", None) or np.trapz
    assert trap(q, x) == pytest.approx(C.sustentacion_semiala(b, A), rel=1e-5)
    assert trap(q * x, x) == pytest.approx(C.momento_raiz(b, A), rel=1e-5)


def test_fuerza_correcta_si_divisor_igual_a_ancho():
    b = C.b_eliptica(M, G, 2.5, A)
    f = C.fuerza_aplicada_por_presion(b, A, 1.07, 50.0, 50.0)
    assert f == pytest.approx(1.07 * M * G * 2.5 / 2, rel=1e-9)


def test_r2_recalculado_difiere_de_tesis():
    r2 = C.r2_tesis(2263.0, 21.09, 31.09, 180.86, 315.7 + 180.86)
    assert r2 == pytest.approx(107.44, abs=0.05)
    assert abs(r2 - 143.89) > 30


def test_ahorro_niu():
    assert C.ahorro_niu(45.89, 14.68, 110) == pytest.approx(3433.1, abs=0.05)
