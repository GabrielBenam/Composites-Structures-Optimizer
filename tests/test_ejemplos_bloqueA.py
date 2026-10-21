"""Cada ejemplo resuelto del Bloque A debe coincidir con el libro dentro de su tolerancia."""
import pytest

from cpo.ejemplos import REGISTRO, cargar_todos, resolver

cargar_todos()
CLAVES = [k for k, v in REGISTRO.items() if v["bloque"] == "bloqueA"]


@pytest.mark.parametrize("clave", CLAVES)
def test_ejemplo(clave):
    d = resolver(clave)
    fallas = [f"{c.clave}: calc={c.calculado:.6g} libro={c.libro:.6g} ({100*c.dif_rel:.2f} %)"
              for c in d.comparaciones if not c.cumple]
    assert not fallas, "\n".join(fallas)


def test_hay_al_menos_20_ejemplos():
    assert len(CLAVES) >= 20


def test_latex_compila_sin_caracteres_problematicos():
    from cpo.informe import sanear
    tex = sanear("".join(resolver(k).latex() for k in CLAVES))
    for c in "−°±ℓ×μ":
        assert c not in tex
