"""Matriz material-proceso-costo de la tesis: reproducción y versiones corregidas.

Ecuaciones de la tesis (numeración del paper INAE 2024):
  P.RM  = a_p · I_p / Σ p           (Ec. 5)   puntaje relativo por propiedad
  P_m   = Σ P.RM                     (tesis 7.4.3)
  R_c-m = P_m / C_p                  (Ec. 9)
  R_c-p = P_p / C_p                  (Ec. 10)
  P_T   = (R_c-p + R_c-m) / 2        (Ec. 11)

Las propiedades "menor es mejor" (densidad) entran como 1/valor, que es lo
que hace la Tabla 19 publicada.
"""
from __future__ import annotations

import numpy as np

MENOR_ES_MEJOR = {"density"}


def normalizar_por_suma(columna: np.ndarray, menor_es_mejor: bool) -> np.ndarray:
    x = 1.0 / columna if menor_es_mejor else columna
    return x / x.sum()


def puntaje_material(props: np.ndarray, columnas: list[str], pesos: dict[str, float]):
    """Suma ponderada por columnas.

    ``pesos`` mapea nombre de columna -> peso. Devuelve (total, matriz de celdas).
    Columnas sin peso aportan cero.
    """
    celdas = np.zeros_like(props, dtype=float)
    for j, c in enumerate(columnas):
        w = pesos.get(c, 0.0)
        if w:
            celdas[:, j] = normalizar_por_suma(props[:, j], c in MENOR_ES_MEJOR) * w
    return celdas.sum(axis=1), celdas


def pesos_como_en_tesis(filas_pesos: list[dict]) -> dict[str, float]:
    """Aplica cada importancia a la columna donde la tesis la aplicó (desplazada)."""
    return {f["columna_donde_se_aplico_en_tesis"]: float(f["importancia"]) for f in filas_pesos}


def pesos_alineados(filas_pesos: list[dict], renormalizar: bool = True):
    """Aplica cada importancia a su propiedad correcta.

    Las variables sin columna en la base de datos se reportan y, si
    ``renormalizar``, su peso se reparte proporcionalmente.
    """
    pesos, faltantes = {}, []
    for f in filas_pesos:
        col = f["columna_correcta_en_tabla18"]
        if col:
            pesos[col] = float(f["importancia"])
        else:
            faltantes.append((f["variable"], float(f["importancia"])))
    if renormalizar:
        s = sum(pesos.values())
        pesos = {k: v / s for k, v in pesos.items()}
    return pesos, faltantes


def relaciones_costo(p_m: np.ndarray, p_p: np.ndarray, costos: np.ndarray):
    """R_c-m (materiales x procesos), R_c-p (materiales x procesos)."""
    rcm = p_m[:, None] / costos
    rcp = p_p[None, :] / costos
    return rcm, rcp


def puntaje_total(rcm: np.ndarray, rcp: np.ndarray, normalizar: bool = False,
                  peso_material: float = 0.5) -> np.ndarray:
    """Ec. 11. Con ``normalizar=True`` cada relación se divide entre su máximo
    antes de promediar (corrige la dominancia por escala)."""
    if normalizar:
        rcm = rcm / rcm.max()
        rcp = rcp / rcp.max()
    return peso_material * rcm + (1.0 - peso_material) * rcp


def ranking(pt: np.ndarray, materiales: list[str], procesos: list[str], top: int | None = None):
    idx = np.dstack(np.unravel_index(np.argsort(-pt, axis=None), pt.shape))[0]
    out = [(materiales[i], procesos[j], float(pt[i, j])) for i, j in idx]
    return out[:top] if top else out


def montecarlo_pesos(props, columnas, pesos_nominales: dict[str, float], p_p, costos,
                     n: int = 5000, concentracion: float = 50.0, normalizar: bool = True,
                     semilla: int = 2026):
    """Frecuencia con la que gana cada combinación material-proceso cuando los
    pesos de propiedades varían alrededor del nominal (Dirichlet).

    ``concentracion`` alta = poca dispersión. Devuelve matriz de frecuencias.
    """
    rng = np.random.default_rng(semilla)
    claves = list(pesos_nominales)
    alfa = np.array([pesos_nominales[k] for k in claves]) * concentracion
    alfa = np.clip(alfa, 1e-3, None)
    gana = np.zeros(costos.shape)
    for _ in range(n):
        w = dict(zip(claves, rng.dirichlet(alfa)))
        p_m, _ = puntaje_material(props, columnas, w)
        rcm, rcp = relaciones_costo(p_m, p_p, costos)
        pt = puntaje_total(rcm, rcp, normalizar=normalizar)
        i, j = np.unravel_index(np.argmax(pt), pt.shape)
        gana[i, j] += 1
    return gana / n
