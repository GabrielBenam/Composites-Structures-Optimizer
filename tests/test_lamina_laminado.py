"""Propiedades matemáticas que deben cumplirse para cualquier lámina y laminado."""
import numpy as np
import pytest

from cpo import lamina as LM
from cpo.laminado import Capa, Laminado
from cpo.materiales import kaw

L = kaw("graphite_epoxy")


@pytest.mark.parametrize("th", [0, 15, 30, 45, 60, 75, 90, -30, 123])
def test_qbar_es_inversa_de_sbar_y_simetrica(th):
    Q, S = LM.Qbar(L, th), LM.Sbar(L, th)
    assert np.allclose(Q @ S, np.eye(3), atol=1e-10)
    assert np.allclose(Q, Q.T, rtol=1e-12, atol=1e-3)


@pytest.mark.parametrize("th", [10, 37, 81])
def test_invariantes_reconstruyen_qbar11(th):
    U = LM.invariantes(L)
    t = np.radians(th)
    q11 = U["U1"] + U["U2"] * np.cos(2 * t) + U["U3"] * np.cos(4 * t)
    assert LM.Qbar(L, th)[0, 0] == pytest.approx(q11, rel=1e-12)


def test_laminado_simetrico_tiene_B_nula():
    lam = Laminado([Capa(L, a, 1e-4) for a in (0, 45, -45, 90, 90, -45, 45, 0)])
    assert np.allclose(lam.ABD()[1], 0, atol=1e-6)


def test_laminado_balanceado_sin_acoplamiento_en_plano():
    lam = Laminado([Capa(L, a, 1e-4) for a in (30, -30, -30, 30)])
    A = lam.ABD()[0]
    assert abs(A[0, 2]) < 1e-6 * A[0, 0] and abs(A[1, 2]) < 1e-6 * A[0, 0]


def test_laminado_de_una_capa_reproduce_la_lamina():
    lam = Laminado([Capa(L, 0, 2e-3)])
    c = lam.constantes_en_plano()
    assert c["Ex"] == pytest.approx(L.E1, rel=1e-12) and c["nuxy"] == pytest.approx(L.nu12, rel=1e-12)
