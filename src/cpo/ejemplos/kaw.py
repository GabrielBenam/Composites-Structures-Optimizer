"""Ejemplos de Kaw (2006), Mechanics of Composite Materials, 2a ed., caps. 2, 4 y 5.1.

Planteamientos redactados con palabras propias; los datos y resultados se citan con página.
"""
from __future__ import annotations

import numpy as np

from .. import falla as F
from .. import lamina as LM
from ..derivacion import mat, num
from ..laminado import Capa, Laminado, alabeo
from ..materiales import kaw
from . import ejemplo, nueva

B = "bloqueA"
GE = "Tabla 2.1 de Kaw (grafito/epóxica: $E_1=181$ GPa, $E_2=10.3$ GPa, $\\nu_{12}=0.28$, $G_{12}=7.17$ GPa)"
IDX = {"11": (0, 0), "12": (0, 1), "16": (0, 2), "22": (1, 1), "26": (1, 2), "66": (2, 2),
       "13": (0, 2), "23": (1, 2), "33": (2, 2)}


def _cmp_mat(d, V, simbolo, M, claves, prefijo, unidad="", tol=0.005, notas=None):
    notas = notas or {}
    for k in claves:
        i, j = IDX[k]
        d.comparar(f"{simbolo}_{{{k}}}", prefijo + k, M[i, j], V[prefijo + k], unidad, tol,
                   notas.get(prefijo + k, ""))


# =================================================================== Capítulo 2
@ejemplo("kaw_2_5", B, "Kaw")
def ej_2_5():
    d, V = nueva("kaw_2_5", B, "Kaw 2.5: flexibilidad y rigidez 3D de una lámina ortótropa",
                 "Se pide la matriz de flexibilidad $[S]$ y la de rigidez $[C]$ (6$\\times$6) de una lámina de "
                 "grafito/epóxica tratada como sólido ortótropo, con nueve constantes ingenieriles dadas.")
    p = dict(E1=181e9, E2=10.3e9, E3=10.3e9, nu12=0.28, nu23=0.60, nu13=0.27, G12=7.17e9, G23=3.0e9, G31=7.0e9)
    d.texto("Datos: $E_1=181$, $E_2=E_3=10.3$ GPa; $\\nu_{12}=0.28$, $\\nu_{23}=0.60$, $\\nu_{13}=0.27$; "
            "$G_{12}=7.17$, $G_{23}=3.0$, $G_{31}=7.0$ GPa.")
    S = LM.S_ortotropo_3d(**p)
    C = np.linalg.inv(S)
    d.paso("Los términos de $[S]$ son inversos de módulos o cocientes de Poisson entre módulos "
           "(orden de Voigt 1, 2, 3, 23, 31, 12).",
           r"S_{11}=\frac{1}{E_1},\; S_{12}=-\frac{\nu_{12}}{E_1},\; S_{13}=-\frac{\nu_{13}}{E_1},\;"
           r" S_{23}=-\frac{\nu_{23}}{E_2},\; S_{44}=\frac{1}{G_{23}},\; S_{55}=\frac{1}{G_{31}},\; S_{66}=\frac{1}{G_{12}}",
           r"[S]=" + mat(S, 4, 1e-12) + r"\times10^{-12}\ \mathrm{Pa^{-1}}")
    d.paso("La rigidez es la inversa de la flexibilidad.", r"[C]=[S]^{-1}",
           r"[C]=" + mat(C, 4, 1e9) + r"\ \mathrm{GPa}")
    for k, (i, j) in {"11": (0, 0), "22": (1, 1), "33": (2, 2), "12": (0, 1), "13": (0, 2), "23": (1, 2),
                      "44": (3, 3), "55": (4, 4), "66": (5, 5)}.items():
        d.comparar(f"S_{{{k}}}", "S" + k, S[i, j], V["S" + k], "Pa^{-1}")
    for k, (i, j) in {"11": (0, 0), "12": (0, 1), "13": (0, 2), "22": (1, 1), "23": (1, 2), "33": (2, 2),
                      "44": (3, 3), "55": (4, 4), "66": (5, 5)}.items():
        d.comparar(f"C_{{{k}}}", "C" + k, C[i, j], V["C" + k], "Pa")
    return d


@ejemplo("kaw_2_6", B, "Kaw")
def ej_2_6():
    d, V = nueva("kaw_2_6", B, "Kaw 2.6: lámina unidireccional en esfuerzo plano",
                 "Para una lámina unidireccional de grafito/epóxica se piden la flexibilidad reducida, el "
                 "Poisson menor, la rigidez reducida y las deformaciones locales bajo "
                 "$\\sigma_1=2$, $\\sigma_2=-3$, $\\tau_{12}=4$ MPa.")
    L = kaw("graphite_epoxy")
    d.texto(f"Propiedades: {GE}.")
    S, Q = LM.S_local(L), LM.Q_local(L)
    d.paso("Flexibilidad reducida en ejes del material.",
           r"[S]=\begin{bmatrix}1/E_1 & -\nu_{12}/E_1 & 0\\ -\nu_{12}/E_1 & 1/E_2 & 0\\ 0&0&1/G_{12}\end{bmatrix}",
           r"[S]=" + mat(S, 4, 1e-12) + r"\times10^{-12}\ \mathrm{Pa^{-1}}")
    d.paso("Poisson menor por reciprocidad.", r"\nu_{21}=\nu_{12}\,\frac{E_2}{E_1}",
           rf"\nu_{{21}}=0.28\cdot\frac{{10.3}}{{181}}={num(L.nu21)}")
    d.paso("Rigidez reducida.", r"Q_{11}=\frac{E_1}{1-\nu_{12}\nu_{21}},\ Q_{12}=\frac{\nu_{12}E_2}{1-\nu_{12}\nu_{21}},"
           r"\ Q_{22}=\frac{E_2}{1-\nu_{12}\nu_{21}},\ Q_{66}=G_{12}",
           r"[Q]=" + mat(Q, 4, 1e9) + r"\ \mathrm{GPa}")
    sig = np.array([2e6, -3e6, 4e6])
    eps = S @ sig
    d.paso("Deformaciones locales.", r"\{\varepsilon\}_{12}=[S]\{\sigma\}_{12}",
           r"\{\varepsilon\}_{12}=" + mat(eps * 1e6, 4) + r"\ \mu\mathrm{m/m}")
    for k in ("11", "12", "22", "66"):
        i, j = IDX[k]
        d.comparar(f"S_{{{k}}}", "S" + k, S[i, j], V["S" + k], "Pa^{-1}")
    d.comparar(r"\nu_{21}", "nu21", L.nu21, V["nu21"])
    for k in ("11", "12", "22", "66"):
        i, j = IDX[k]
        d.comparar(f"Q_{{{k}}}", "Q" + k, Q[i, j], V["Q" + k], "Pa",
                   nota="La matriz impresa muestra 7.117 GPa; el texto da 7.17 GPa (errata tipográfica)."
                   if k == "66" else "")
    for n, k, v in zip((r"\varepsilon_1", r"\varepsilon_2", r"\gamma_{12}"), ("e1", "e2", "g12"), eps):
        d.comparar(n, k, v, V[k])
    return d


@ejemplo("kaw_2_7", B, "Kaw")
def ej_2_7():
    d, V = nueva("kaw_2_7", B, "Kaw 2.7: lámina a 60° bajo esfuerzos en el plano",
                 "Una lámina de grafito/epóxica a 60° recibe $\\sigma_x=2$, $\\sigma_y=-3$, $\\tau_{xy}=4$ MPa. "
                 "Se piden $[\\bar S]$, $[\\bar Q]$, deformaciones globales y locales, esfuerzos locales, y "
                 "valores principales de esfuerzo y deformación.")
    d.imagen("Kaw (2006), Figura 2.21, p. 113 — lámina a 60° con los esfuerzos aplicados")
    L, th = kaw("graphite_epoxy"), 60.0
    Sb, Qb, T = LM.Sbar(L, th), LM.Qbar(L, th), LM.T(th)
    d.paso("Matriz de transformación de esfuerzos con $c=\\cos 60^\\circ$, $s=\\sin 60^\\circ$.",
           r"[T]=\begin{bmatrix}c^2 & s^2 & 2sc\\ s^2 & c^2 & -2sc\\ -sc & sc & c^2-s^2\end{bmatrix}",
           r"[T]=" + mat(T, 4))
    d.paso("Flexibilidad y rigidez transformadas.",
           r"[\bar S]=[R][T]^{-1}[R]^{-1}[S][T],\qquad [\bar Q]=[T]^{-1}[Q][R][T][R]^{-1}",
           r"[\bar S]=" + mat(Sb, 4, 1e-12) + r"\times10^{-12}\ \mathrm{Pa^{-1}},\quad [\bar Q]=" + mat(Qb, 4, 1e9) + r"\ \mathrm{GPa}")
    sig = np.array([2e6, -3e6, 4e6])
    eg = Sb @ sig
    el = LM.deformacion_a_local(eg, th)
    sl = T @ sig
    d.paso("Deformaciones globales, locales y esfuerzos locales.",
           r"\{\varepsilon\}_{xy}=[\bar S]\{\sigma\}_{xy},\quad \{\varepsilon\}_{12}=[R][T][R]^{-1}\{\varepsilon\}_{xy},\quad \{\sigma\}_{12}=[T]\{\sigma\}_{xy}",
           r"\{\varepsilon\}_{xy}=" + mat(eg * 1e6, 4) + r"\ \mu\mathrm{m/m},\ \{\varepsilon\}_{12}=" + mat(el * 1e6, 4)
           + r"\ \mu\mathrm{m/m},\ \{\sigma\}_{12}=" + mat(sl / 1e6, 4) + r"\ \mathrm{MPa}")
    smax, smin, thp, tmax, ths = LM.principales(*sig)
    emax, emin, thpe, gmax, thse = LM.principales(*eg, ingenieril=True)
    d.paso("Esfuerzos principales y cortante máximo (círculo de Mohr).",
           r"\sigma_{\max,\min}=\frac{\sigma_x+\sigma_y}{2}\pm\sqrt{\Big(\frac{\sigma_x-\sigma_y}{2}\Big)^2+\tau_{xy}^2},"
           r"\quad \theta_p=\tfrac12\tan^{-1}\frac{2\tau_{xy}}{\sigma_x-\sigma_y}",
           rf"\sigma_{{\max}}={num(smax/1e6)},\ \sigma_{{\min}}={num(smin/1e6)}\ \mathrm{{MPa}},\ \theta_p={num(thp)}^\circ,"
           rf"\ \tau_{{\max}}={num(tmax/1e6)}\ \mathrm{{MPa}},\ \theta_s={num(ths)}^\circ")
    d.paso("Deformaciones principales; los ejes principales de deformación no coinciden con los de esfuerzo "
           "ni con los del material, a diferencia de un material isótropo.",
           r"\varepsilon_{\max,\min}=\frac{\varepsilon_x+\varepsilon_y}{2}\pm\sqrt{\Big(\frac{\varepsilon_x-\varepsilon_y}{2}\Big)^2+\Big(\frac{\gamma_{xy}}{2}\Big)^2}",
           rf"\varepsilon_{{\max}}={num(emax)},\ \varepsilon_{{\min}}={num(emin)},\ \theta_p={num(thpe)}^\circ,"
           rf"\ \gamma_{{\max}}={num(gmax)},\ \theta_s={num(thse)}^\circ")
    _cmp_mat(d, V, r"\bar S", Sb, ("11", "12", "16", "22", "26", "66"), "Sb", "Pa^{-1}")
    _cmp_mat(d, V, r"\bar Q", Qb, ("11", "12", "16", "22", "26", "66"), "Qb", "Pa")
    for n, k, v in zip((r"\varepsilon_x", r"\varepsilon_y", r"\gamma_{xy}", r"\varepsilon_1", r"\varepsilon_2",
                        r"\gamma_{12}", r"\sigma_1", r"\sigma_2", r"\tau_{12}"),
                       ("ex", "ey", "gxy", "e1", "e2", "g12", "s1", "s2", "t12"), (*eg, *el, *sl)):
        d.comparar(n, k, v, V[k])
    for n, k, v in ((r"\sigma_{\max}", "smax", smax), (r"\sigma_{\min}", "smin", smin), (r"\theta_p", "theta_p", thp),
                    (r"\tau_{\max}", "tmax", tmax), (r"\varepsilon_{\max}", "emax", emax),
                    (r"\varepsilon_{\min}", "emin", emin), (r"\theta_{p,\varepsilon}", "theta_pe", thpe),
                    (r"\gamma_{\max}", "gmax", gmax), (r"\theta_{s,\varepsilon}", "theta_se", thse)):
        d.comparar(n, k, v, V[k])
    d.comparar(r"\theta_s", "theta_s", ths, V["theta_s"],
               nota="El signo no es legible en el texto del libro; la ec. 2.110 da un valor negativo.")
    return d


@ejemplo("kaw_2_8", B, "Kaw")
def ej_2_8():
    d, V = nueva("kaw_2_8", B, "Kaw 2.8: lecturas de una roseta de galgas en una lámina a 60°",
                 "La lámina de grafito/epóxica a 60° recibe solo $\\tau_{xy}=2$ MPa. Se piden las deformaciones "
                 "que leerían tres galgas a 0°, 240° y 120° del eje $x$.")
    d.imagen("Kaw (2006), Figura 2.22, p. 119 — roseta de galgas A, B, C sobre la lámina")
    L = kaw("graphite_epoxy")
    eg = LM.Sbar(L, 60) @ np.array([0, 0, 2e6])
    d.paso("Deformaciones globales con la flexibilidad transformada del ejemplo 2.7.",
           r"\{\varepsilon\}_{xy}=[\bar S]\{0,0,\tau_{xy}\}^T", r"\{\varepsilon\}_{xy}=" + mat(eg, 4))
    lect = {k: LM.deformacion_galga(eg, phi) for k, phi in (("eA", 0), ("eB", 240), ("eC", 120))}
    d.paso("Lectura de cada galga a un ángulo $\\varphi$ del eje $x$.",
           r"\varepsilon_\varphi=\varepsilon_x\cos^2\varphi+\varepsilon_y\sin^2\varphi+\gamma_{xy}\sin\varphi\cos\varphi",
           rf"\varepsilon_A={num(lect['eA'])},\ \varepsilon_B={num(lect['eB'])},\ \varepsilon_C={num(lect['eC'])}")
    for n, k, v in zip((r"\varepsilon_x", r"\varepsilon_y", r"\gamma_{xy}"), ("ex", "ey", "gxy"), eg):
        d.comparar(n, k, v, V[k])
    emax = LM.principales(*eg, ingenieril=True)[0]
    nota = (f"Errata probable del libro: el valor impreso supera la deformación principal máxima "
            f"({emax:.3e}), lo que es físicamente imposible; la ecuación B.15 del propio libro da el valor calculado.")
    for k, v in lect.items():
        d.comparar(rf"\varepsilon_{k[1]}", k, v, V[k], nota=nota if k in ("eB", "eC") else "",
                   errata=k in ("eB", "eC"))
    d.texto(f"Comprobación independiente: la deformación principal máxima es ${num(emax)}$, menor que la lectura "
            "impresa para la galga B; por eso se conserva el resultado de la ecuación y se reporta la discrepancia.")
    return d


@ejemplo("kaw_2_9", B, "Kaw")
def ej_2_9():
    d, V = nueva("kaw_2_9", B, "Kaw 2.9: constantes ingenieriles de una lámina a 60°",
                 "Se piden $E_x$, $\\nu_{xy}$, $m_x$, $E_y$, $m_y$ y $G_{xy}$ de la lámina de grafito/epóxica a 60°.")
    L = kaw("graphite_epoxy")
    c = LM.constantes_angulo(L, 60)
    d.paso("Cada constante sale de un término de $[\\bar S]$; $m_x$ y $m_y$ miden el acoplamiento entre "
           "esfuerzo normal y deformación cortante.",
           r"E_x=\frac{1}{\bar S_{11}},\ \nu_{xy}=-\frac{\bar S_{12}}{\bar S_{11}},\ \frac{1}{m_x}=-\frac{1}{\bar S_{16}E_1},"
           r"\ E_y=\frac{1}{\bar S_{22}},\ \frac{1}{m_y}=-\frac{1}{\bar S_{26}E_1},\ G_{xy}=\frac{1}{\bar S_{66}}",
           rf"E_x={num(c['Ex']/1e9)}\ \mathrm{{GPa}},\ \nu_{{xy}}={num(c['nuxy'])},\ m_x={num(c['mx'])},"
           rf"\ E_y={num(c['Ey']/1e9)}\ \mathrm{{GPa}},\ m_y={num(c['my'])},\ G_{{xy}}={num(c['Gxy']/1e9)}\ \mathrm{{GPa}}")
    for n, k in ((r"E_x", "Ex"), (r"\nu_{xy}", "nuxy"), (r"m_x", "mx"), (r"E_y", "Ey"), (r"m_y", "my"), (r"G_{xy}", "Gxy")):
        d.comparar(n, k, c[k], V[k])
    return d


@ejemplo("kaw_2_11", B, "Kaw")
def ej_2_11():
    d, V = nueva("kaw_2_11", B, "Kaw 2.11: invariantes de rigidez y flexibilidad",
                 "Se piden los cuatro invariantes de rigidez $U_i$ y los cuatro de flexibilidad $V_i$ del grafito/epóxica.")
    L = kaw("graphite_epoxy")
    I = LM.invariantes(L)
    d.paso("Invariantes de rigidez: no dependen del ángulo de la lámina.",
           r"U_1=\tfrac18(3Q_{11}+3Q_{22}+2Q_{12}+4Q_{66}),\ U_2=\tfrac12(Q_{11}-Q_{22}),"
           r"\ U_3=\tfrac18(Q_{11}+Q_{22}-2Q_{12}-4Q_{66}),\ U_4=\tfrac18(Q_{11}+Q_{22}+6Q_{12}-4Q_{66})",
           ", ".join(rf"U_{i}={num(I['U'+str(i)]/1e9)}" for i in range(1, 5)) + r"\ \mathrm{GPa}")
    d.paso("Invariantes de flexibilidad.",
           r"V_1=\tfrac18(3S_{11}+3S_{22}+2S_{12}+S_{66}),\ V_2=\tfrac12(S_{11}-S_{22}),"
           r"\ V_3=\tfrac18(S_{11}+S_{22}-2S_{12}-S_{66}),\ V_4=\tfrac18(S_{11}+S_{22}+6S_{12}-S_{66})",
           ", ".join(rf"V_{i}={num(I['V'+str(i)])}" for i in range(1, 5)) + r"\ \mathrm{Pa^{-1}}")
    for k in ("U1", "U2", "U3", "U4", "V1", "V2", "V3", "V4"):
        d.comparar(f"{k[0]}_{k[1]}", k, I[k], V[k])
    return d


def _sig_60_S():
    return LM.T(60) @ np.array([2.0, -3.0, 4.0])


@ejemplo("kaw_2_13", B, "Kaw")
def ej_2_13():
    d, V = nueva("kaw_2_13", B, "Kaw 2.13: criterio de esfuerzo máximo",
                 "Se busca el mayor $S>0$ tal que la lámina a 60° de grafito/epóxica resista "
                 "$\\sigma_x=2S$, $\\sigma_y=-3S$, $\\tau_{xy}=4S$ según el criterio de esfuerzo máximo.")
    L = kaw("graphite_epoxy")
    sl = _sig_60_S()
    sr, modo = F.sr_esfuerzo_maximo(sl, L)
    d.paso("Esfuerzos locales por unidad de $S$.", r"\{\sigma\}_{12}=[T]\{2,-3,4\}^T S",
           r"\{\sigma\}_{12}=" + mat(sl, 4) + "S")
    d.paso("Cada componente se compara con su resistencia según el signo; manda la menor razón.",
           r"S=\min\Big(\frac{X_t \text{ o } X_c}{|\sigma_1|},\frac{Y_t \text{ o } Y_c}{|\sigma_2|},\frac{S_{12}}{|\tau_{12}|}\Big)",
           rf"S={num(sr/1e6)}\ \mathrm{{MPa}}\ \text{{(modo {modo}: cortante en el plano)}}")
    d.comparar("S", "SR", sr, V["SR"], "Pa")
    for n, k, f in ((r"\sigma_x", "sx", 2), (r"\sigma_y", "sy", -3), (r"\tau_{xy}", "txy", 4)):
        d.comparar(n + r"^{\text{falla}}", k, f * sr, V[k], "Pa")
    return d


@ejemplo("kaw_2_14", B, "Kaw")
def ej_2_14():
    d, V = nueva("kaw_2_14", B, "Kaw 2.14 y Tabla 2.3: resistencia a cortante fuera de ejes",
                 "Se pide la resistencia a cortante de láminas de grafito/epóxica a distintos ángulos con el criterio de "
                 "esfuerzo máximo, distinguiendo cortante positivo y negativo.")
    d.imagen("Kaw (2006), Figura 2.31, p. 142 — cortante positivo y negativo sobre una lámina en ángulo")
    L = kaw("graphite_epoxy")
    d.paso("Para cortante puro $\\tau$ los esfuerzos locales son $\\sigma_1=2sc\\,\\tau$, $\\sigma_2=-2sc\\,\\tau$, "
           "$\\tau_{12}=(c^2-s^2)\\tau$. El signo de $\\tau$ decide si la matriz trabaja a tensión o a compresión transversal.",
           r"\tau_{\text{adm}}^{\pm}=\mathrm{SR}\big([T]\{0,0,\pm1\}^T\big)")
    filas = []
    for th in (0, 15, 30, 45, 60, 75, 90):
        p, mp = F.sr_esfuerzo_maximo(LM.T(th) @ [0, 0, 1.0], L)
        n, mn = F.sr_esfuerzo_maximo(LM.T(th) @ [0, 0, -1.0], L)
        filas.append(rf"{th}^\circ: & \ {num(p/1e6)}\ ({mp}) & {num(n/1e6)}\ ({mn})")
        d.comparar(rf"\tau^+_{{{th}}}", f"tau_pos_{th}", p, V[f"tau_pos_{th}"], "Pa")
        d.comparar(rf"\tau^-_{{{th}}}", f"tau_neg_{th}", n, V[f"tau_neg_{th}"], "Pa")
    d.paso("Resultados en MPa (entre paréntesis el modo de falla).", "", " \\\\ &".join(filas))
    return d


@ejemplo("kaw_2_17", B, "Kaw")
def ej_2_17():
    d, V = nueva("kaw_2_17", B, "Kaw 2.17: criterio de deformación máxima",
                 "Mismo estado de esfuerzos que en 2.13, ahora con el criterio de deformación máxima.")
    L = kaw("graphite_epoxy")
    u = F.deformaciones_ultimas(L)
    d.paso("Deformaciones últimas suponiendo respuesta lineal hasta la falla.",
           r"\varepsilon_{1}^{T,C}=\frac{X_{t,c}}{E_1},\ \varepsilon_2^{T,C}=\frac{Y_{t,c}}{E_2},\ \gamma_{12}^{u}=\frac{S_{12}}{G_{12}}",
           ", ".join(rf"{n}={num(u[k])}" for n, k in ((r"\varepsilon_1^T", "e1T"), (r"\varepsilon_1^C", "e1C"),
                                                      (r"\varepsilon_2^T", "e2T"), (r"\varepsilon_2^C", "e2C"), (r"\gamma_{12}^u", "g12"))))
    sr, modo = F.sr_deformacion_maxima(_sig_60_S(), L)
    d.paso("Se comparan las deformaciones locales $[S]\\{\\sigma\\}_{12}$ con sus límites.", "",
           rf"S={num(sr/1e6)}\ \mathrm{{MPa}}\ (\text{{modo {modo}}})")
    for k in ("e1T", "e1C", "e2T", "e2C", "g12"):
        d.comparar(k, k, u[k], V[k])
    d.comparar("S", "SR", sr, V["SR"], "Pa")
    return d


@ejemplo("kaw_2_18", B, "Kaw")
def ej_2_18():
    d, V = nueva("kaw_2_18", B, "Kaw 2.18: criterio de Tsai-Hill y su versión modificada",
                 "Mismo estado de esfuerzos que en 2.13 con Tsai-Hill; después con resistencias elegidas según el signo.")
    L = kaw("graphite_epoxy")
    sl = _sig_60_S()  # esfuerzos locales para S = 1 Pa
    sr, srm = F.sr_tsai_hill(sl, L), F.sr_tsai_hill(sl, L, modificado=True)
    d.paso("Tsai-Hill original usa solo resistencias a tensión.",
           r"\Big(\frac{\sigma_1}{X}\Big)^2-\frac{\sigma_1\sigma_2}{X^2}+\Big(\frac{\sigma_2}{Y}\Big)^2+\Big(\frac{\tau_{12}}{S}\Big)^2=\frac{1}{\mathrm{SR}^2}",
           rf"S={num(sr/1e6)}\ \mathrm{{MPa}}")
    d.paso("La versión modificada toma $X$ y $Y$ de tensión o compresión según el signo de cada esfuerzo; "
           "como $\\sigma_2<0$, usa $Y_c=246$ MPa y el resultado se acerca al de esfuerzo máximo.", "",
           rf"S={num(srm/1e6)}\ \mathrm{{MPa}}")
    d.comparar(r"S_{\text{TH}}", "SR_TH", sr, V["SR_TH"], "Pa")
    d.comparar(r"S_{\text{TH mod}}", "SR_THmod", srm, V["SR_THmod"], "Pa")
    return d


@ejemplo("kaw_2_19", B, "Kaw")
def ej_2_19():
    d, V = nueva("kaw_2_19", B, "Kaw 2.19: criterio de Tsai-Wu",
                 "Mismo estado de esfuerzos que en 2.13 con Tsai-Wu y tres formas de estimar $H_{12}$.")
    L = kaw("graphite_epoxy")
    c = F.coeficientes_tsai_wu(L)
    sl = _sig_60_S()
    d.paso("Coeficientes de resistencia.",
           r"H_1=\frac{1}{X_t}-\frac{1}{X_c},\ H_2=\frac{1}{Y_t}-\frac{1}{Y_c},\ H_{11}=\frac{1}{X_tX_c},\ H_{22}=\frac{1}{Y_tY_c},"
           r"\ H_{66}=\frac{1}{S^2},\ H_{12}=-\tfrac12\sqrt{H_{11}H_{22}}",
           ", ".join(rf"H_{{{k[1:]}}}={num(c[k])}" for k in ("H2", "H11", "H22", "H66", "H12")))
    srs = {k: F.sr_tsai_wu(sl, L, h) for k, h in (("SR_MH", "mises-hencky"), ("SR_TH", "tsai-hill"), ("SR_HOF", "hoffman"))}
    d.paso("Con $\\{\\sigma\\}=\\mathrm{SR}\\{\\sigma\\}_0$ el criterio se vuelve cuadrático en SR.",
           r"a\,\mathrm{SR}^2+b\,\mathrm{SR}=1,\quad a=H_{11}\sigma_1^2+H_{22}\sigma_2^2+H_{66}\tau_{12}^2+2H_{12}\sigma_1\sigma_2,\ b=H_1\sigma_1+H_2\sigma_2",
           rf"S_{{\text{{MH}}}}={num(srs['SR_MH']/1e6)},\ S_{{\text{{TH}}}}={num(srs['SR_TH']/1e6)},\ S_{{\text{{Hoff}}}}={num(srs['SR_HOF']/1e6)}\ \mathrm{{MPa}}")
    for k in ("H2", "H11", "H22", "H66", "H12"):
        d.comparar(f"H_{{{k[1:]}}}", k, c[k], V[k])
    for k, v in srs.items():
        d.comparar(k.replace("_", r"\_"), k, v, V[k], "Pa")
    d.texto("Resumen para este estado de esfuerzos: esfuerzo máximo y deformación máxima dan 16.33 MPa; "
            "Tsai-Hill, 10.94 MPa; Tsai-Hill modificado, 16.06 MPa; Tsai-Wu, 22.39 MPa. La elección del "
            "criterio cambia el margen hasta en un factor de dos, lo que justifica reportar el criterio usado.")
    return d


@ejemplo("kaw_2_20", B, "Kaw")
def ej_2_20():
    d, V = nueva("kaw_2_20", B, "Kaw 2.20: expansión térmica y por humedad de una lámina a 60°",
                 "Para vidrio/epóxica a 60° se piden los coeficientes globales de expansión térmica y por humedad "
                 "y las deformaciones libres con $\\Delta T=-100\\,^\\circ$C y $\\Delta C=0.02$ kg/kg.")
    L = kaw("glass_epoxy")
    a, b = LM.alfa_global(L, 60), LM.beta_global(L, 60)
    d.paso("Los coeficientes se transforman como deformaciones.",
           r"\{\alpha_x,\alpha_y,\alpha_{xy}/2\}^T=[T]^{-1}\{\alpha_1,\alpha_2,0\}^T",
           r"\{\alpha\}_{xy}=" + mat(a * 1e6, 4) + r"\times10^{-6}/^\circ\mathrm{C},\quad \{\beta\}_{xy}=" + mat(b, 4))
    e = a * -100 + b * 0.02
    d.paso("Deformación libre higrotérmica.", r"\{\varepsilon\}=\{\alpha\}\Delta T+\{\beta\}\Delta C",
           r"\{\varepsilon\}=" + mat(e, 4))
    for n, k, v in zip((r"\alpha_x", r"\alpha_y", r"\alpha_{xy}", r"\beta_x", r"\beta_y", r"\beta_{xy}",
                        r"\varepsilon_x", r"\varepsilon_y", r"\gamma_{xy}"),
                       ("ax", "ay", "axy", "bx", "by", "bxy", "ex", "ey", "gxy"), (*a, *b, *e)):
        d.comparar(n, k, v, V[k])
    return d


# =================================================================== Capítulo 4
@ejemplo("kaw_4_1", B, "Kaw")
def ej_4_1():
    d, V = nueva("kaw_4_1", B, "Kaw 4.1: deformaciones en la cara superior de un laminado",
                 "Dadas las deformaciones del plano medio y las curvaturas de un laminado de 0.010 in, se piden las "
                 "deformaciones globales en su cara superior.")
    e0 = np.array([2751e-6, -1331e-6, -1125e-6]); k = np.array([1.965, 0.2385, -1.773])
    e = e0 + (-0.005) * k
    d.paso("Variación lineal de la deformación en el espesor (hipótesis de Kirchhoff); la cara superior está en "
           "$z=-h/2=-0.005$ in.", r"\{\varepsilon\}=\{\varepsilon^0\}+z\{\kappa\}", r"\{\varepsilon\}=" + mat(e * 1e6, 4) + r"\ \mu\mathrm{in/in}")
    for n, kk, v in zip((r"\varepsilon_x", r"\varepsilon_y", r"\gamma_{xy}"), ("ex", "ey", "gxy"), e):
        d.comparar(n, kk, v, V[kk])
    return d


def _lam(angulos, t=0.005, mat_="graphite_epoxy"):
    L = kaw(mat_)
    return Laminado([Capa(L, a, t) for a in angulos])


@ejemplo("kaw_4_2", B, "Kaw")
def ej_4_2():
    d, V = nueva("kaw_4_2", B, "Kaw 4.2: matrices [A], [B] y [D] de un laminado [0/30/-45]",
                 "Laminado de tres capas de grafito/epóxica de 5 mm, orientadas 0°, 30° y −45° de arriba hacia abajo.")
    d.imagen("Kaw (2006), Figura 4.7, p. 332 — espesores y coordenadas z de las capas")
    lam = _lam([0, 30, -45])
    A, Bm, D = lam.ABD()
    d.paso("Coordenadas de las caras de las capas medidas desde el plano medio (positivas hacia abajo).",
           r"h_0=-\tfrac{h}{2},\ h_k=h_{k-1}+t_k", r"h=" + mat(lam.z, 4) + r"\ \mathrm{m}")
    d.paso("Rigidez transformada de cada capa.", r"[\bar Q]_k=[T]^{-1}[Q][R][T][R]^{-1}",
           ",\\ ".join(rf"[\bar Q]_{{{a}^\circ}}=" + mat(lam.Qbar(i), 4, 1e9) for i, a in enumerate((0, 30, -45))) + r"\ \mathrm{GPa}")
    d.paso("Integración por capas.",
           r"A_{ij}=\sum_k \bar Q_{ij,k}(h_k-h_{k-1}),\ B_{ij}=\tfrac12\sum_k \bar Q_{ij,k}(h_k^2-h_{k-1}^2),\ D_{ij}=\tfrac13\sum_k \bar Q_{ij,k}(h_k^3-h_{k-1}^3)",
           r"[A]=" + mat(A, 4) + r"\ \mathrm{Pa\,m},\ [B]=" + mat(Bm, 4) + r"\ \mathrm{Pa\,m^2},\ [D]=" + mat(D, 4) + r"\ \mathrm{Pa\,m^3}")
    ks = ("11", "12", "16", "22", "26", "66")
    _cmp_mat(d, V, "A", A, ks, "A", "Pa\\,m")
    _cmp_mat(d, V, "B", Bm, ks, "B", "Pa\\,m^2",
             notas={"B16": "La matriz impresa en 4.2 muestra -1.972e6; el ejemplo 4.3 usa -1.072e6 (errata)."})
    _cmp_mat(d, V, "D", D, ks, "D", "Pa\\,m^3")
    return d


@ejemplo("kaw_4_3", B, "Kaw")
def ej_4_3():
    d, V = nueva("kaw_4_3", B, "Kaw 4.3: respuesta del laminado [0/30/-45] a $N_x=N_y=1000$ N/m",
                 "Con el laminado del ejemplo 4.2 se piden deformaciones y curvaturas del plano medio, esfuerzos en "
                 "la cara superior de la capa a 30° y la fracción de $N_x$ que toma cada capa.")
    lam = _lam([0, 30, -45])
    e0, k = lam.respuesta(N=(1000, 1000, 0))
    d.paso("Sistema acoplado de seis ecuaciones.",
           r"\begin{Bmatrix}N\\M\end{Bmatrix}=\begin{bmatrix}A&B\\B&D\end{bmatrix}\begin{Bmatrix}\varepsilon^0\\\kappa\end{Bmatrix}",
           r"\{\varepsilon^0\}=" + mat(e0, 4) + r",\quad \{\kappa\}=" + mat(k, 4) + r"\ \mathrm{1/m}")
    s = lam.estado_capa(1, "sup", e0, k)
    d.paso("Cara superior de la capa a 30° ($z=-0.0025$ m): deformación total, esfuerzo global y paso a ejes locales.",
           r"\{\varepsilon\}=\{\varepsilon^0\}+z\{\kappa\},\ \{\sigma\}_{xy}=[\bar Q]\{\varepsilon\},\ \{\sigma\}_{12}=[T]\{\sigma\}_{xy}",
           r"\{\varepsilon\}_{xy}=" + mat(s["eps_global"], 4) + r",\ \{\sigma\}_{xy}=" + mat(s["sig_global"], 4)
           + r",\ \{\varepsilon\}_{12}=" + mat(s["eps_local"], 4) + r",\ \{\sigma\}_{12}=" + mat(s["sig_local"], 4) + r"\ \mathrm{Pa}")
    porc = [lam.estado_capa(i, "medio", e0, k)["sig_global"][0] * lam.capas[i].t for i in range(3)]
    d.paso("Como el esfuerzo varía linealmente dentro de cada capa, su aporte a $N_x$ es el esfuerzo en el plano medio "
           "de la capa por su espesor.", r"N_{x,k}=\sigma_{x,k}^{\text{medio}}\,t_k",
           ",\\ ".join(rf"N_{{x,{a}^\circ}}={num(v)}" for a, v in zip((0, 30, -45), porc)) + r"\ \mathrm{N/m}")
    for n, kk, v in zip((r"\varepsilon^0_x", r"\varepsilon^0_y", r"\gamma^0_{xy}", r"\kappa_x", r"\kappa_y", r"\kappa_{xy}"),
                        ("e0x", "e0y", "g0xy", "kx", "ky", "kxy"), (*e0, *k)):
        d.comparar(n, kk, v, V[kk])
    for tag, vec in (("e", s["eps_global"]), ("s", s["sig_global"])):
        for n, kk, v in zip(("x", "y", "xy"), ("x", "y", "xy"), vec):
            clave = (f"{tag}{kk}_30top" if kk != "xy" else ("gxy_30top" if tag == "e" else "txy_30top"))
            d.comparar((r"\varepsilon_" if tag == "e" else r"\sigma_") + n + r"^{30,\text{sup}}", clave, v, V[clave])
    for n, kk, v in zip((r"\varepsilon_1", r"\varepsilon_2", r"\gamma_{12}", r"\sigma_1", r"\sigma_2", r"\tau_{12}"),
                        ("e1_30top", "e2_30top", "g12_30top", "s1_30top", "s2_30top", "t12_30top"),
                        (*s["eps_local"], *s["sig_local"])):
        d.comparar(n + r"^{30,\text{sup}}", kk, v, V[kk])
    for n, kk, v in zip((r"N_{x,0}", r"N_{x,30}", r"N_{x,-45}"), ("Nx_0", "Nx_30", "Nx_m45"), porc):
        d.comparar(n, kk, v, V[kk], "N/m")
    d.comparar(r"\sigma_1^{-45,\text{sup}}", "s1_m45top", lam.estado_capa(2, "sup", e0, k)["sig_local"][0], V["s1_m45top"])
    d.comparar(r"\sigma_1^{-45,\text{inf}}", "s1_m45bot", lam.estado_capa(2, "inf", e0, k)["sig_local"][0], V["s1_m45bot"])
    return d


@ejemplo("kaw_4_4", B, "Kaw")
def ej_4_4():
    d, V = nueva("kaw_4_4", B, "Kaw 4.4: constantes en el plano y a flexión de un laminado [0/90]$_s$",
                 "Laminado simétrico de tres capas de grafito/epóxica de 5 mm (0°, 90°, 0°).")
    lam = _lam([0, 90, 0])
    A, _, D = lam.ABD()
    cp, cf = lam.constantes_en_plano(), lam.constantes_flexion()
    d.paso("Rigideces del laminado.", "", r"[A]=" + mat(A, 4) + r"\ \mathrm{Pa\,m},\ [D]=" + mat(D, 4) + r"\ \mathrm{Pa\,m^3}")
    d.paso("Constantes en el plano a partir de $[A]^{-1}=[A^*]$.",
           r"E_x=\frac{1}{hA^*_{11}},\ E_y=\frac{1}{hA^*_{22}},\ G_{xy}=\frac{1}{hA^*_{66}},\ \nu_{xy}=-\frac{A^*_{12}}{A^*_{11}}",
           rf"E_x={num(cp['Ex']/1e9)},\ E_y={num(cp['Ey']/1e9)},\ G_{{xy}}={num(cp['Gxy']/1e9)}\ \mathrm{{GPa}},"
           rf"\ \nu_{{xy}}={num(cp['nuxy'])},\ \nu_{{yx}}={num(cp['nuyx'])}")
    d.paso("Constantes a flexión a partir de $[D]^{-1}=[D^*]$; difieren de las del plano porque las capas a 0° "
           "están lejos del plano medio.",
           r"E^f_x=\frac{12}{h^3D^*_{11}},\ E^f_y=\frac{12}{h^3D^*_{22}},\ G^f_{xy}=\frac{12}{h^3D^*_{66}},\ \nu^f_{xy}=-\frac{D^*_{12}}{D^*_{11}}",
           rf"E^f_x={num(cf['Exf']/1e9)},\ E^f_y={num(cf['Eyf']/1e9)},\ G^f_{{xy}}={num(cf['Gxyf']/1e9)}\ \mathrm{{GPa}},"
           rf"\ \nu^f_{{xy}}={num(cf['nuxyf'])},\ \nu^f_{{yx}}={num(cf['nuyxf'])}")
    _cmp_mat(d, V, "A", A, ("11", "12", "22", "66"), "A", "Pa\\,m")
    _cmp_mat(d, V, "D", D, ("11", "12", "22", "66"), "D", "Pa\\,m^3")
    for n, kk in ((r"E_x", "Ex"), (r"E_y", "Ey"), (r"G_{xy}", "Gxy"), (r"\nu_{xy}", "nuxy"), (r"\nu_{yx}", "nuyx")):
        d.comparar(n, kk, cp[kk], V[kk])
    for n, kk in ((r"E^f_x", "Exf"), (r"E^f_y", "Eyf"), (r"G^f_{xy}", "Gxyf"), (r"\nu^f_{xy}", "nuxyf"), (r"\nu^f_{yx}", "nuyxf")):
        d.comparar(n, kk, cf[kk], V[kk])
    return d


@ejemplo("kaw_4_5", B, "Kaw")
def ej_4_5():
    d, V = nueva("kaw_4_5", B, "Kaw 4.5: esfuerzos residuales térmicos en un laminado [0/90]",
                 "Laminado no simétrico de dos capas de grafito/epóxica de 5 mm sometido a $\\Delta T=-75\\,^\\circ$C. "
                 "Se pide el esfuerzo residual en la cara inferior de la capa a 90°.")
    lam = _lam([0, 90])
    NT, MT = lam.cargas_higrotermicas(dT=-75)
    A, Bm, D = lam.ABD()
    d.paso("Fuerzas y momentos térmicos ficticios.",
           r"\{N^T\}=\Delta T\sum_k[\bar Q]_k\{\alpha\}_k(h_k-h_{k-1}),\ \{M^T\}=\tfrac{\Delta T}{2}\sum_k[\bar Q]_k\{\alpha\}_k(h_k^2-h_{k-1}^2)",
           r"\{N^T\}=" + mat(NT, 4) + r"\ \mathrm{N/m},\ \{M^T\}=" + mat(MT, 4) + r"\ \mathrm{N}")
    e0, k = lam.respuesta(dT=-75)
    d.paso("Respuesta del laminado: al no ser simétrico ($[B]\\neq0$), el enfriamiento lo curva.",
           r"\begin{Bmatrix}N^T\\M^T\end{Bmatrix}=\begin{bmatrix}A&B\\B&D\end{bmatrix}\begin{Bmatrix}\varepsilon^0\\\kappa\end{Bmatrix}",
           r"[B]=" + mat(Bm, 4) + r",\ \{\varepsilon^0\}=" + mat(e0, 4) + r",\ \{\kappa\}=" + mat(k, 4) + r"\ \mathrm{1/m}")
    s = lam.estado_capa(1, "inf", e0, k, dT=-75)
    d.paso("En la cara inferior de la capa a 90°, el esfuerzo lo produce la deformación mecánica: total menos libre.",
           r"\{\varepsilon^M\}=\{\varepsilon\}-\{\alpha\}\Delta T,\quad \{\sigma\}=[\bar Q]\{\varepsilon^M\}",
           r"\{\varepsilon\}=" + mat(s["eps_global"], 4) + r",\ \{\varepsilon^M\}=" + mat(s["eps_mecanica"], 4)
           + r",\ \{\sigma\}=" + mat(s["sig_global"] / 1e6, 4) + r"\ \mathrm{MPa}")
    for n, kk, v in ((r"N^T_x", "NTx", NT[0]), (r"N^T_y", "NTy", NT[1]), (r"M^T_x", "MTx", MT[0]), (r"M^T_y", "MTy", MT[1]),
                     ("A_{11}", "A11", A[0, 0]), ("A_{12}", "A12", A[0, 1]), ("A_{66}", "A66", A[2, 2]),
                     ("B_{11}", "B11", Bm[0, 0]), ("B_{22}", "B22", Bm[1, 1]),
                     ("D_{11}", "D11", D[0, 0]), ("D_{12}", "D12", D[0, 1]), ("D_{66}", "D66", D[2, 2]),
                     (r"\varepsilon^0_x", "e0x", e0[0]), (r"\varepsilon^0_y", "e0y", e0[1]),
                     (r"\kappa_x", "kx", k[0]), (r"\kappa_y", "ky", k[1]),
                     (r"\varepsilon_x^{\text{inf}}", "ex_bot", s["eps_global"][0]), (r"\varepsilon_y^{\text{inf}}", "ey_bot", s["eps_global"][1]),
                     (r"\varepsilon^M_x", "emx_bot", s["eps_mecanica"][0]), (r"\varepsilon^M_y", "emy_bot", s["eps_mecanica"][1]),
                     (r"\sigma_x^{\text{inf}}", "sx_bot", s["sig_global"][0]), (r"\sigma_y^{\text{inf}}", "sy_bot", s["sig_global"][1])):
        d.comparar(n, kk, v, V[kk])
    return d


@ejemplo("kaw_4_6", B, "Kaw")
def ej_4_6():
    d, V = nueva("kaw_4_6", B, "Kaw 4.6: coeficientes de expansión de un laminado [0/90]$_s$",
                 "Se piden los coeficientes de expansión térmica y por humedad del laminado del ejemplo 4.4.")
    lam = _lam([0, 90, 0])
    c = lam.coeficientes_expansion()
    d.paso("En un laminado simétrico no hay curvatura; los coeficientes son la deformación del plano medio "
           "por unidad de $\\Delta T$ o de $\\Delta C$.",
           r"\{\alpha\}=[A]^{-1}\{N^T\}_{\Delta T=1},\quad \{\beta\}=[A]^{-1}\{N^C\}_{\Delta C=1}",
           r"\{N^T\}=" + mat(c["NT_unit"], 4) + r",\ \{\alpha\}=" + mat(c["alfa"], 4)
           + r",\ \{N^C\}=" + mat(c["NC_unit"], 4) + r",\ \{\beta\}=" + mat(c["beta"], 4))
    for n, kk, v in ((r"N^T_x", "NTx", c["NT_unit"][0]), (r"N^T_y", "NTy", c["NT_unit"][1]),
                     (r"\alpha_x", "ax", c["alfa"][0]), (r"\alpha_y", "ay", c["alfa"][1]),
                     (r"N^C_x", "NCx", c["NC_unit"][0]), (r"N^C_y", "NCy", c["NC_unit"][1]),
                     (r"\beta_x", "bx", c["beta"][0]), (r"\beta_y", "by", c["beta"][1])):
        d.comparar(n, kk, v, V[kk])
    return d


@ejemplo("kaw_4_7", B, "Kaw")
def ej_4_7():
    d, V = nueva("kaw_4_7", B, "Kaw 4.7: alabeo del laminado [0/90] al enfriarse",
                 "Con las curvaturas del ejemplo 4.5 se pide la deflexión fuera del plano.")
    lam = _lam([0, 90])
    _, k = lam.respuesta(dT=-75)
    cx, cy = alabeo(k, 1.0, 0.0), alabeo(k, 0.0, 1.0)
    d.paso("Integrando $\\kappa_x=-\\partial^2w/\\partial x^2$, $\\kappa_y=-\\partial^2w/\\partial y^2$, "
           "$\\kappa_{xy}=-2\\partial^2w/\\partial x\\partial y$ con $w(0,0)=0$ y pendientes nulas en el origen:",
           r"w=-\tfrac12\left(\kappa_x x^2+\kappa_y y^2+\kappa_{xy}xy\right)",
           rf"w={num(cx)}\,x^2 {'+' if cy >= 0 else '-'} {num(abs(cy))}\,y^2\quad (\mathrm{{m}})")
    d.texto("La superficie resultante es una silla de montar: es el efecto que se evita con laminados simétricos.")
    d.comparar("c_{x^2}", "cx2", cx, V["cx2"], "1/m")
    d.comparar("c_{y^2}", "cy2", cy, V["cy2"], "1/m")
    return d


# =================================================================== Capítulo 5
@ejemplo("kaw_5_1", B, "Kaw")
def ej_5_1():
    d, V = nueva("kaw_5_1", B, "Kaw 5.1: laminado cuasi-isótropo [0/±60]",
                 "Se piden $[A]$, $[B]$ y $[D]$ del laminado de grafito/epóxica [0/60/−60] con capas de 5 mm y se "
                 "verifica en qué sentido se comporta como isótropo.")
    lam = _lam([0, 60, -60])
    A, Bm, D = lam.ABD()
    d.paso("Matrices del laminado.", "", r"[A]=" + mat(A, 4) + r",\ [B]=" + mat(Bm, 4) + r",\ [D]=" + mat(D, 4))
    d.paso("En el plano se cumple la condición de isotropía, pero $[B]\\neq0$ y $[D]$ no es isótropa: "
           "la cuasi-isotropía es solo de membrana.",
           r"A_{11}=A_{22},\ A_{16}=A_{26}=0,\ A_{66}=\frac{A_{11}-A_{12}}{2}",
           rf"\frac{{A_{{11}}-A_{{12}}}}{{2}}={num((A[0,0]-A[0,1])/2)}=A_{{66}}={num(A[2,2])}")
    ks = ("11", "12", "22", "66")
    _cmp_mat(d, V, "A", A, ks, "A", "Pa\\,m")
    _cmp_mat(d, V, "B", Bm, ("11", "12", "16", "22", "26", "66"), "B", "Pa\\,m^2")
    _cmp_mat(d, V, "D", D, ("11", "12", "16", "22", "26", "66"), "D", "Pa\\,m^3")
    return d
