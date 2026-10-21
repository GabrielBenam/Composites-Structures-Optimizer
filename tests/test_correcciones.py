"""Efecto de las correcciones de la Fase 0."""
import numpy as np

from cpo import fase0

R = fase0.calcular()


def test_pesos_alineados_suman_uno():
    assert abs(sum(R["pesos_alineados"].values()) - 1) < 1e-12


def test_faltan_modulo_cortante_e_ilss():
    faltan = {v for v, _ in R["faltantes"]}
    assert faltan == {"shear_modulus", "interlaminar_shear_strength"}


def test_vidrio_cae_al_ultimo_lugar_con_pesos_alineados():
    orden = [R["materiales"][i] for i in np.argsort(-R["pm_alineado"])]
    assert orden[0] == "Carbon AM" and orden[-1] == "Glass"


def test_relacion_proceso_domina_por_escala():
    assert R["escala_rcp_sobre_rcm"] > 2


def test_costo_casi_no_distingue_materiales():
    assert R["dispersion_costo_material_max"] < 0.02
