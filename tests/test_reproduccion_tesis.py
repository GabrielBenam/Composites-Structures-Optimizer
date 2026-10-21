"""Prueba de regresión: el código debe reproducir las tablas publicadas de la tesis."""
import numpy as np
import pytest

from cpo import fase0

R = fase0.calcular()
IDX = {m: i for i, m in enumerate(R["materiales"])}
JDX = {p: j for j, p in enumerate(R["procesos"])}


def test_tabla19_reproducida():
    assert R["tabla19_dif_max"] < 2e-5


def test_tablas_22_23_reproducidas():
    from cpo.datos import leer_csv_texto
    for fila in leer_csv_texto("tesis/publicado_tablas22_23.csv"):
        i = IDX[fila["material"]]
        mat = R["rcm"] if fila["relacion"] == "rcm" else R["rcp"]
        for p, j in JDX.items():
            assert mat[i, j] == pytest.approx(float(fila[p]), rel=2e-3), (fila["material"], p)


def test_ganador_de_la_tesis():
    i, j = np.unravel_index(np.argmax(R["pt_tesis"]), R["pt_tesis"].shape)
    assert (R["materiales"][i], R["procesos"][j]) == ("Carbon AM", "pultrusion")


def test_empate_tecnico_carbono_boro_en_pultrusion():
    j = JDX["pultrusion"]
    a, b = R["pt_tesis"][IDX["Carbon AM"], j], R["pt_tesis"][IDX["Borum"], j]
    assert abs(a - b) / a < 0.01
