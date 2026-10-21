"""Registro de derivaciones paso a paso y su salida en LaTeX.

Cada ejemplo resuelto crea una ``Derivacion``: un planteamiento redactado con
palabras propias, pasos (texto, ecuación simbólica, sustitución numérica,
resultado) y comparaciones contra el valor publicado en el libro.

Las figuras no se incrustan: se escribe una referencia ``[Imagen: ...]`` que el
autor sustituye en la versión final.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

import numpy as np


# ------------------------------------------------------------------ formato
def num(x: float, cifras: int = 4) -> str:
    """Número en notación LaTeX con ``cifras`` significativas."""
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return r"\text{--}"
    if x == 0:
        return "0"
    if math.isinf(x):
        return r"\infty"
    exp = int(math.floor(math.log10(abs(x))))
    if -3 <= exp <= 4:
        dec = max(cifras - 1 - exp, 0)
        s = f"{x:.{dec}f}"
        return s
    mant = x / 10 ** exp
    return f"{mant:.{cifras - 1}f}\\times10^{{{exp}}}"


def mat(M, cifras: int = 4, escala: float = 1.0) -> str:
    """Matriz o vector como ``bmatrix``. ``escala`` divide los valores (p. ej. 1e9)."""
    M = np.atleast_2d(np.asarray(M, float)).copy()
    if M.shape[0] == 1:
        M = M.T
    M[np.abs(M) < 1e-9 * np.max(np.abs(M))] = 0.0  # ruido numérico de la transformación
    filas = [" & ".join(num(v / escala, cifras) for v in fila) for fila in M]
    return r"\begin{bmatrix}" + r" \\ ".join(filas) + r"\end{bmatrix}"


_SEP = re.compile(r",\\ (?=\[|\\\{|\\?[A-Za-z][A-Za-z0-9]*[_^={])|,\\quad |, (?=[A-Z]_)")


def _empacar(expr: str, ancho: int = 120) -> list[str]:
    """Parte una expresión larga en renglones para ``align*``: separa en comas de alto nivel y
    agrupa segmentos hasta ~``ancho`` caracteres (sin contar matrices)."""
    if len(re.sub(r"\\begin\{bmatrix\}.*?\\end\{bmatrix\}", "M", expr)) <= ancho and expr.count(r"\begin{bmatrix}") <= 1:
        return [expr]
    segs = [q for q in _SEP.split(expr) if q]
    lineas, actual = [], ""
    for sg in segs:
        largo = lambda t: len(re.sub(r"\\begin\{bmatrix\}.*?\\end\{bmatrix\}", "M" * 18, t))
        if actual and (largo(actual) + largo(sg) > ancho or r"\begin{bmatrix}" in sg and r"\begin{bmatrix}" in actual):
            lineas.append(actual)
            actual = sg
        else:
            actual = f"{actual},\\ {sg}" if actual else sg
    if actual:
        lineas.append(actual)
    return lineas


@dataclass
class Comparacion:
    nombre: str          # etiqueta LaTeX de la magnitud
    clave: str           # identificador corto
    calculado: float
    libro: float
    unidad: str = ""
    tol: float = 0.005   # tolerancia relativa
    nota: str = ""       # errata, redondeo del libro, etc.
    errata: bool = False # el valor del libro es incorrecto; se documenta y no se exige coincidencia

    @property
    def dif_rel(self) -> float:
        if self.libro == 0:
            return abs(self.calculado)
        return abs(self.calculado - self.libro) / abs(self.libro)

    @property
    def cumple(self) -> bool:
        return self.errata or self.dif_rel <= self.tol


@dataclass
class Derivacion:
    clave: str
    titulo: str
    fuente: str
    planteamiento: str
    bloques: list = field(default_factory=list)
    comparaciones: list[Comparacion] = field(default_factory=list)

    # --- construcción
    def texto(self, t: str):
        self.bloques.append(("texto", t))

    def imagen(self, referencia: str):
        self.bloques.append(("imagen", referencia))

    def paso(self, descripcion: str, ecuacion: str = "", sustitucion: str = "", resultado: str = ""):
        self.bloques.append(("paso", descripcion, ecuacion, sustitucion, resultado))

    def comparar(self, nombre, clave, calculado, libro, unidad="", tol=0.005, nota="", errata=False):
        self.comparaciones.append(Comparacion(nombre, clave, float(calculado), float(libro),
                                              unidad, tol, nota, errata))

    # --- salida
    def latex(self) -> str:
        out = [f"\\section{{{self.titulo}}}\\label{{ej:{self.clave}}}",
               f"\\textbf{{Fuente:}} {self.fuente}\n",
               f"\\paragraph{{Planteamiento.}} {self.planteamiento}\n",
               "\\paragraph{Solución.}"]
        n = 0
        for b in self.bloques:
            if b[0] == "texto":
                out.append(b[1] + "\n")
            elif b[0] == "imagen":
                out.append(f"\\begin{{center}}\\fbox{{\\parbox{{0.9\\linewidth}}{{\\centering\\small [Imagen: {b[1]}]}}}}\\end{{center}}\n")
            else:
                n += 1
                _, desc, ec, sus, res = b
                out.append(f"\\textit{{Paso {n}.}} {desc}")
                partes = []
                for p in (ec, sus, res):
                    if not p:
                        continue
                    partes += _empacar(p)
                if partes:
                    out.append("\\begin{align*}\n" + " \\\\\n".join(
                        p if p.lstrip().startswith("&") else "&" + p for p in partes) + "\n\\end{align*}")
        if self.comparaciones:
            out.append("\\paragraph{Comparación con el libro.}\n"
                       "\\begin{longtable}{lrrrc}\\toprule Magnitud & Libro & Calculado & Dif. (\\%) & \\\\ "
                       "\\midrule\\endhead")
            for c in self.comparaciones:
                marca = "errata" if c.errata else ("\\checkmark" if c.cumple else "\\textbf{revisar}")
                unidad = ("[$\\mathrm{" + c.unidad + "}$]") if c.unidad else ""
                out.append(f"${c.nombre}$ {unidad} & ${num(c.libro)}$ & "
                           f"${num(c.calculado)}$ & {100 * c.dif_rel:.2f} & {marca} \\\\")
            out.append("\\bottomrule\\end{longtable}")
            notas = [c for c in self.comparaciones if c.nota]
            if notas:
                out.append("\\begin{itemize}\\small")
                out += [f"\\item ${c.nombre}$: {c.nota}" for c in notas]
                out.append("\\end{itemize}")
        return "\n".join(out) + "\n"
