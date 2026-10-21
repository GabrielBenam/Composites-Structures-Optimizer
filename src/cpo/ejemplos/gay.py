"""Ejemplos de Gay (2015), Composite Materials: Design and Applications, 3a ed.

Notación de Gay: ejes de la capa (ℓ, t) ≡ (1, 2); los coeficientes E_ij de Gay son la
rigidez reducida transformada [Q̄]. Unidades: MPa y mm.
"""
from __future__ import annotations

import numpy as np

from .. import falla as F
from .. import lamina as LM
from ..derivacion import mat, num
from ..laminado import A_sobre_h_por_fracciones, Capa, Laminado
from ..materiales import gay_tela_carbono, kaw
from . import ejemplo, nueva

B = "bloqueA"


def _th_tela(sig_local, L):
    """Tsai-Hill de Gay (ec. 14.6) con resistencias según signo; tela balanceada."""
    s1, s2, _ = sig_local
    X = L.Xt if s1 >= 0 else L.Xc
    Y = L.Yt if s2 >= 0 else L.Yc
    return F.indice_tsai_hill(sig_local, X, X, Y, L.S)


@ejemplo("gay_19_10", B, "Gay")
def ej_19_10():
    d, V = nueva("gay_19_10", B, "Gay 19.10: larguero de carbono/epóxica (propiedades y verificación de ruptura)",
                 "Larguero de una superficie de control, de tela balanceada carbono/epóxica ($V_f=45\\%$, capa de 0.24 mm). "
                 "En la zona 1 (patín) actúa $N_x=\\pm435$ N/mm con 9 capas, 67\\% a 0°/90° y 33\\% a ±45°. En la zona 2 "
                 "(alma) actúa $T_{xy}=-30$ N/mm con 5 capas, 40\\% a 0°/90° y 60\\% a ±45°. Se piden las propiedades "
                 "elásticas de ambos laminados y la verificación de ruptura con Tsai-Hill. El pandeo (parte 2b) se "
                 "resuelve en el Bloque D.")
    d.imagen("Gay (2015), figura del enunciado de 19.10, p. 484 — larguero de 2400 mm, alma de 130 mm, patín de 40 mm, zonas 1 y 2")
    L = gay_tela_carbono()
    Q0, Q45 = LM.Qbar(L, 0), LM.Qbar(L, 45)
    d.paso("Rigidez de la tela a 0° y a 45° (en Gay, $E_{ij}^{\\theta}$). Para tela balanceada $E_\\ell=E_t$.",
           r"\bar E_\ell=\frac{E_x}{1-\nu_{xy}^2},\ E^{0}_{12}=\nu\bar E_\ell,\ E^{45}_{11}=\frac{\bar E_\ell+\bar E_t}{4}+\frac{\nu\bar E_\ell+2G}{2},"
           r"\ E^{45}_{12}=\frac{\bar E_\ell+\bar E_t}{4}-\frac{2G-\nu\bar E_\ell}{2},\ E^{45}_{33}=\frac{\bar E_\ell+\bar E_t}{4}-\frac{\nu\bar E_\ell}{2}",
           r"[\bar Q]_{0}=" + mat(Q0, 4) + r",\ [\bar Q]_{45}=" + mat(Q45, 4) + r"\ \mathrm{MPa}")
    res = {}
    for z, fr in (("z1", {0: 0.67, 45: 0.33}), ("z2", {0: 0.40, 45: 0.60})):
        Ah = A_sobre_h_por_fracciones(L, fr)
        Ai = np.linalg.inv(Ah)
        res[z] = (Ah, 1 / Ai[0, 0], -Ai[0, 1] / Ai[0, 0], Ah[2, 2])
        d.paso(f"Zona {z[1]}: mezcla por proporciones de capas ({int(fr[0]*100)}\\% a 0°, {int(fr[45]*100)}\\% a ±45°) "
               "e inversión para obtener las constantes de membrana.",
               r"\tfrac1h[A]=\sum_\theta p_\theta[\bar Q]_\theta,\quad h[A]^{-1}\Rightarrow E_x=E_y,\ \nu_{xy},\ G_{xy}",
               r"\tfrac1h[A]=" + mat(Ah, 4) + rf",\ E_x={num(res[z][1])}\ \mathrm{{MPa}},\ \nu_{{xy}}={num(res[z][2], 3)}")
    # --- 2a, zona 1: compresión del patín
    h1 = 9 * 0.24
    sox = -435 / h1
    Ah1 = res["z1"][0]
    eps1 = np.linalg.inv(Ah1) @ np.array([sox, 0, 0])
    sl0 = LM.T(0) @ (Q0 @ eps1)
    sl45 = LM.T(45) @ (Q45 @ eps1)
    th0, th45 = np.sqrt(_th_tela(sl0, L)), np.sqrt(_th_tela(sl45, L))
    d.paso("Zona 1, patín inferior a compresión: esfuerzo medio y deformaciones de membrana.",
           r"\sigma_{0x}=\frac{N_x}{h}=\frac{-435}{9\times0.24},\quad \{\varepsilon^0\}=h[A]^{-1}\{\sigma_0\}",
           rf"\sigma_{{0x}}={num(sox)}\ \mathrm{{MPa}},\ \{{\varepsilon^0\}}=" + mat(eps1, 4))
    d.paso("Esfuerzos en ejes de la capa y Tsai-Hill (Gay ec. 14.6, con la resistencia de tensión o compresión "
           "según el signo). Las capas 0°/90° fallan primero.",
           r"\Big(\frac{\sigma_\ell}{X}\Big)^2+\Big(\frac{\sigma_t}{Y}\Big)^2-\frac{\sigma_\ell\sigma_t}{X^2}+\Big(\frac{\tau_{\ell t}}{S}\Big)^2=I^2",
           r"\{\sigma\}_{0^\circ}=" + mat(sl0, 4) + r",\ \{\sigma\}_{45^\circ}=" + mat(sl45, 4)
           + rf"\ \mathrm{{MPa}},\ I_{{0}}={num(th0, 3)},\ I_{{45}}={num(th45, 3)},\ \text{{margen}}=\tfrac1{{I_0}}-1={num(100*(1/th0-1), 3)}\%")
    # --- 2a, zona 2: cortante del alma
    tau = -30 / (5 * 0.24)
    g = tau / res["z2"][3]
    eps2 = np.array([0, 0, g])
    s45 = LM.T(45) @ (Q45 @ eps2)
    s0 = LM.T(0) @ (Q0 @ eps2)
    t2_45, t2_0 = np.sqrt(_th_tela(s45, L)), np.sqrt(_th_tela(s0, L))
    d.paso("Zona 2, alma a cortante: el ±45° convierte el cortante en tensión y compresión a lo largo de las fibras, "
           "por eso es la orientación eficiente para almas.",
           r"\tau_{0xy}=\frac{T_{xy}}{h},\ \gamma_{0xy}=\frac{\tau_{0xy}}{G_{xy}},\ \{\sigma\}_{45^\circ}=[T_{45}][\bar Q]_{45}\{0,0,\gamma_{0xy}\}",
           rf"\tau_{{0xy}}={num(tau)}\ \mathrm{{MPa}},\ \gamma_{{0xy}}={num(g)},\ \{{\sigma\}}_{{45^\circ}}=" + mat(s45, 4)
           + rf",\ I_{{45}}={num(t2_45, 3)},\ I_{{0}}={num(t2_0, 3)}")
    for kk, n, v in (("Q11_0", r"\bar Q^{0}_{11}", Q0[0, 0]), ("Q12_0", r"\bar Q^{0}_{12}", Q0[0, 1]), ("Q66_0", r"\bar Q^{0}_{66}", Q0[2, 2]),
                     ("Q11_45", r"\bar Q^{45}_{11}", Q45[0, 0]), ("Q12_45", r"\bar Q^{45}_{12}", Q45[0, 1]), ("Q66_45", r"\bar Q^{45}_{66}", Q45[2, 2])):
        d.comparar(n, kk, v, V[kk], "MPa")
    for z in ("z1", "z2"):
        Ah, Ex, nu, G = res[z]
        d.comparar(rf"A_{{11}}/h\ ({z})", f"{z}_A11", Ah[0, 0], V[f"{z}_A11"], "MPa")
        d.comparar(rf"A_{{12}}/h\ ({z})", f"{z}_A12", Ah[0, 1], V[f"{z}_A12"], "MPa")
        d.comparar(rf"A_{{66}}/h\ ({z})", f"{z}_A66", Ah[2, 2], V[f"{z}_A66"], "MPa")
        d.comparar(rf"E_x\ ({z})", f"{z}_Ex", Ex, V[f"{z}_Ex"], "MPa")
        d.comparar(rf"\nu_{{xy}}\ ({z})", f"{z}_nu", nu, V[f"{z}_nu"], "", 0.03,
                   "El libro redondea a dos cifras." if z == "z1" else "")
    nota_r = "El libro redondea el esfuerzo medio a -202 MPa antes de seguir."
    d.comparar(r"\sigma_{0x}", "z1_sox", sox, V["z1_sox"], "MPa", 0.005, nota_r)
    d.comparar(r"\varepsilon_{0x}", "z1_eox", eps1[0], V["z1_eox"], "", 0.005)
    d.comparar(r"\varepsilon_{0y}", "z1_eoy", eps1[1], V["z1_eoy"], "", 0.03, "El libro usa $\\nu=0.2$ redondeado.")
    d.comparar(r"\sigma_\ell^{0}", "z1_sl0", sl0[0], V["z1_sl0"], "MPa", 0.01)
    d.comparar(r"\sigma_t^{0}", "z1_st0", sl0[1], V["z1_st0"], "MPa", 0.03,
               "El libro arrastra el redondeo $\\nu=0.2$ y $\\varepsilon_{0y}=9\\times10^{-4}$.")
    d.comparar(r"I_{\text{TH}}^{0}\ (z1)", "z1_TH0", th0, V["z1_TH0"], "", 0.02)
    d.comparar(r"I_{\text{TH}}^{45}\ (z1)", "z1_TH45", th45, V["z1_TH45"], "", 0.02)
    d.comparar(r"\tau_{0xy}\ (z2)", "z2_tau", tau, V["z2_tau"], "MPa")
    d.comparar(r"\gamma_{0xy}\ (z2)", "z2_gxy", g, V["z2_gxy"], "", 0.01)
    d.comparar(r"\tau^{45}_{xy}\ (z2)", "z2_t45", (Q45 @ eps2)[2], V["z2_t45"], "MPa", 0.01)
    d.comparar(r"I_{\text{TH}}^{45}\ (z2)", "z2_TH45", t2_45, V["z2_TH45"], "", 0.03)
    d.comparar(r"I_{\text{TH}}^{0}\ (z2)", "z2_TH0", t2_0, V["z2_TH0"], "", 0.07, "El libro da solo una cifra significativa (0.1).")
    return d


@ejemplo("gay_19_14", B, "Gay")
def ej_19_14():
    d, _ = nueva("gay_19_14", B, "Gay 19.14: laminado cuasi-isótropo (fórmulas cerradas contra CLT)",
                 "Laminado simétrico de capas unidireccionales idénticas, 25\\% a 0°, 90°, +45° y −45°. Gay obtiene en forma "
                 "cerrada los módulos de membrana y demuestra que el laminado es isótropo en su plano. Aquí se evalúan "
                 "esas fórmulas con la lámina de grafito/epóxica de Kaw y se comparan contra la CLT numérica de un "
                 "laminado [0/90/45/−45]$_s$; sirve como cruce entre libros.")
    L = kaw("graphite_epoxy")
    Q = LM.Q_local(L)
    El, Et, nuE, G = Q[0, 0], Q[1, 1], Q[0, 1], Q[2, 2]
    A11 = 0.25 * (1.5 * (El + Et) + nuE + 2 * G)
    A12 = 0.25 * (0.5 * (El + Et) + 3 * nuE - 2 * G)
    A33 = 0.25 * (0.5 * (El + Et) - nuE + 2 * G)
    E_f = (A11 ** 2 - A12 ** 2) / A11
    nu_f = A12 / A11
    d.paso("Fórmulas de Gay en términos de $\\bar E_\\ell=Q_{11}$, $\\bar E_t=Q_{22}$, $\\nu_{t\\ell}\\bar E_\\ell=Q_{12}$, $G_{\\ell t}=Q_{66}$.",
           r"\tfrac1hA_{11}=\tfrac14\Big[\tfrac32(\bar E_\ell+\bar E_t)+\nu_{t\ell}\bar E_\ell+2G_{\ell t}\Big],\ "
           r"\tfrac1hA_{12}=\tfrac14\Big[\tfrac12(\bar E_\ell+\bar E_t)+3\nu_{t\ell}\bar E_\ell-2G_{\ell t}\Big],\ "
           r"\tfrac1hA_{33}=\tfrac14\Big[\tfrac12(\bar E_\ell+\bar E_t)-\nu_{t\ell}\bar E_\ell+2G_{\ell t}\Big]",
           rf"E=\frac{{A_{{11}}^2-A_{{12}}^2}}{{hA_{{11}}}}={num(E_f/1e9)}\ \mathrm{{GPa}},\ \nu=\frac{{A_{{12}}}}{{A_{{11}}}}={num(nu_f)},\ G=\tfrac1hA_{{33}}={num(A33/1e9)}\ \mathrm{{GPa}}")
    lam = Laminado([Capa(L, a, 0.125e-3) for a in (0, 90, 45, -45, -45, 45, 90, 0)])
    c = lam.constantes_en_plano()
    d.paso("CLT numérica del laminado [0/90/45/−45]$_s$ con capas de 0.125 mm.", "",
           rf"E_x={num(c['Ex']/1e9)},\ E_y={num(c['Ey']/1e9)},\ G_{{xy}}={num(c['Gxy']/1e9)}\ \mathrm{{GPa}},\ \nu_{{xy}}={num(c['nuxy'])}")
    d.texto("Además se cumple $G=E/[2(1+\\nu)]$, condición de isotropía en el plano.")
    d.comparar(r"E_x\ (\text{CLT vs. Gay})", "E", c["Ex"], E_f, "Pa", 1e-9)
    d.comparar(r"E_y\ (\text{CLT vs. Gay})", "Ey", c["Ey"], E_f, "Pa", 1e-9)
    d.comparar(r"\nu_{xy}\ (\text{CLT vs. Gay})", "nu", c["nuxy"], nu_f, "", 1e-9)
    d.comparar(r"G_{xy}\ (\text{CLT vs. Gay})", "G", c["Gxy"], A33, "Pa", 1e-9)
    d.comparar(r"G\ \text{vs.}\ E/2(1+\nu)", "iso", A33, E_f / (2 * (1 + nu_f)), "Pa", 1e-9)
    return d
