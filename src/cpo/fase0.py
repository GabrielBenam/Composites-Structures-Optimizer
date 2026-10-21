"""Fase 0: reconstrucción de la tesis y línea base corregida.

Uso:  python -m cpo.fase0      (escribe resultados/fase0/ y docs/fase0_reporte.md)
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from . import cargas as C
from . import decision as D
from .datos import DATA, RAIZ, leer_csv_texto, leer_json, leer_meta, leer_tabla


def calcular() -> dict:
    av = leer_json("aeronave/cessna162.json")
    m, g, a = av["mtow_kg"], av["g"], av["semi_envergadura_mm"]
    r: dict = {"aeronave": av}

    # ---------- Cargas ----------
    r["b_por_n"] = {n: C.b_eliptica(m, g, n, a) for n in (2.5, 3.8, 4.0, 6.0)}
    r["n_implicito_b_ansys"] = C.n_desde_b(av["b_usado_en_ansys_N_mm"], m, g, a)
    r["n_implicito_b_publicado"] = C.n_desde_b(av["b_publicado_N_mm"], m, g, a)
    k = av["factor_carga_larguero_tesis"]
    r["carga_esperada_larguero_N"] = {n: k * C.sustentacion_semiala(C.b_eliptica(m, g, n, a), a)
                                      for n in (2.5, 3.8)}
    r["momento_raiz_Nm"] = {n: C.momento_raiz(C.b_eliptica(m, g, n, a), a) / 1000.0
                            for n in (2.5, 3.8, 6.0)}
    b_ans = av["b_usado_en_ansys_N_mm"]
    r["fuerza_aplicada_si_divide_cuerda_N"] = {
        w: C.fuerza_aplicada_por_presion(b_ans, a, k, av["cuerda_mm"], w) for w in (30, 50, 75, 100)}
    cos = av["costilla"]
    L0 = b_ans * av["cuerda_mm"]  # q(0)·cuerda ≈ 2263 N, valor usado en la tesis (secc. 7.2.5)
    r["R2_recalculado_N"] = C.r2_tesis(L0,
                                       cos["dist_sustentacion_a_larguero_mm"], cos["peso_costilla_N"],
                                       cos["dist_cg_costilla_mm"], sum(cos["dist_larguero_a_larguero_mm"]))
    r["fraccion_palanca"] = C.fraccion_larguero_palanca(cos["dist_sustentacion_a_larguero_mm"],
                                                        sum(cos["dist_larguero_a_larguero_mm"]))
    pv = av["pesos_viga_kg"]
    r["ahorro_niu_usd"] = C.ahorro_niu(pv["aluminio_zicral"], pv["carbono_hm"], av["niu_usd_por_kg"])

    # ---------- Matriz de decisión ----------
    t18 = leer_tabla("tesis/tabla18_propiedades.csv")
    pesos_filas = leer_csv_texto("tesis/pesos_propiedades.csv")
    pesos_exactos = leer_meta(DATA / "tesis/pesos_propiedades.csv")[
        "pesos_reproduccion_exacta_por_columna_tabla18"]
    costos = leer_tabla("tesis/costos_seer_tabla7.csv")
    procs = costos.columnas
    pp_rows = leer_csv_texto("tesis/puntaje_procesos_tabla21.csv")
    p_p = np.array([float(x["puntaje"]) for x in pp_rows])
    assert [x["proceso"] for x in pp_rows] == procs

    mats = t18.filas
    r["materiales"], r["procesos"] = mats, procs

    pm_tesis, celdas = D.puntaje_material(t18.valores, t18.columnas, pesos_exactos)
    pm_desplazado, _ = D.puntaje_material(t18.valores, t18.columnas, D.pesos_como_en_tesis(pesos_filas))
    w_al, faltantes = D.pesos_alineados(pesos_filas)
    pm_alineado, _ = D.puntaje_material(t18.valores, t18.columnas, w_al)
    r.update(pm_tesis=pm_tesis, celdas_tabla19=celdas, pm_desplazado=pm_desplazado,
             pm_alineado=pm_alineado, pesos_alineados=w_al, faltantes=faltantes)
    pub = leer_tabla("tesis/publicado_tabla19.csv").col("total")
    r["tabla19_publicada"] = pub
    r["tabla19_dif_max"] = float(np.max(np.abs(pm_tesis - pub)))

    rcm, rcp = D.relaciones_costo(pm_tesis, p_p, costos.valores)
    pt_tesis = D.puntaje_total(rcm, rcp)
    rcm_a, rcp_a = D.relaciones_costo(pm_alineado, p_p, costos.valores)
    pt_alineado = D.puntaje_total(rcm_a, rcp_a)
    pt_alineado_norm = D.puntaje_total(rcm_a, rcp_a, normalizar=True)
    r.update(rcm=rcm, rcp=rcp, pt_tesis=pt_tesis, pt_alineado=pt_alineado,
             pt_alineado_norm=pt_alineado_norm, costos=costos.valores, p_p=p_p)

    # Dominancia de escalas
    r["dispersion_puntaje_proceso"] = float(p_p.max() / p_p.min() - 1)
    r["dispersion_costo_proceso"] = float(costos.valores.mean(0).max() / costos.valores.mean(0).min() - 1)
    r["dispersion_costo_material_max"] = float(np.max(costos.valores.max(0) / costos.valores.min(0) - 1))
    r["escala_rcp_sobre_rcm"] = float(rcp.mean() / rcm.mean())

    r["mc_freq"] = D.montecarlo_pesos(t18.valores, t18.columnas, w_al, p_p, costos.valores)
    return r


def _tabla_md(encabezado, filas) -> str:
    s = "| " + " | ".join(encabezado) + " |\n|" + "---|" * len(encabezado) + "\n"
    for f in filas:
        s += "| " + " | ".join(str(x) for x in f) + " |\n"
    return s


def escribir(r: dict) -> Path:
    out = RAIZ / "resultados" / "fase0"
    out.mkdir(parents=True, exist_ok=True)
    mats, procs = r["materiales"], r["procesos"]
    for nombre in ("pt_tesis", "pt_alineado", "pt_alineado_norm", "mc_freq"):
        with (out / f"{nombre}.csv").open("w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["material"] + procs)
            for i, mname in enumerate(mats):
                w.writerow([mname] + [f"{v:.6e}" for v in r[nombre][i]])
    with (out / "puntaje_material.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["material", "publicado_tabla19", "reproducido", "alineado_renormalizado"])
        for i, mname in enumerate(mats):
            w.writerow([mname, r["tabla19_publicada"][i], f"{r['pm_tesis'][i]:.5f}",
                        f"{r['pm_alineado'][i]:.5f}"])

    def rk(v):
        return [mats[i] for i in np.argsort(-v)]

    md = ["# Fase 0: reproducción de la tesis y línea base corregida\n",
          "Archivo generado por `python -m cpo.fase0`. No editar a mano.\n",
          "## 1. Cargas\n",
          _tabla_md(["n", "b = q(0) [N/mm]", "M raíz [N·m]"],
                    [[n, f"{r['b_por_n'][n]:.4f}", f"{r['momento_raiz_Nm'].get(n, float('nan')):.0f}"]
                     for n in (2.5, 3.8, 6.0)]),
          f"\nEl valor b = 2.012 N/mm usado en ANSYS implica n = {r['n_implicito_b_ansys']:.3f}; "
          f"el b = 3.059 N/mm publicado implica n = {r['n_implicito_b_publicado']:.3f}.\n",
          "\nCarga total que debería leer la sonda de reacción del larguero aislado (factor 1.07 de la tesis):\n\n",
          _tabla_md(["n", "Reacción esperada [N]"],
                    [[n, f"{v:.0f}"] for n, v in r["carga_esperada_larguero_N"].items()]),
          "\nFuerza realmente aplicada si la presión se calculó dividiendo entre la cuerda (1125 mm) "
          "y se aplicó sobre la cara del patín:\n\n",
          _tabla_md(["Ancho de patín [mm]", "Fuerza aplicada [N]"],
                    [[w, f"{v:.0f}"] for w, v in r["fuerza_aplicada_si_divide_cuerda_N"].items()]),
          f"\nR2 recalculado con la ecuación de momentos de la tesis: {r['R2_recalculado_N']:.2f} N "
          "(la tesis reporta 143.89 N). Con regla de la palanca, si la sustentación cae entre largueros, "
          f"el larguero principal toma {r['fraccion_palanca']:.3f} de la carga, no 1.07.\n",
          f"\nAhorro Niu con los pesos de la Tabla 25: {r['ahorro_niu_usd']:.1f} USD (la tesis reporta 1082.37).\n",
          "\n[Imagen: Tesis actualizada 3.docx, Ilustración 52 — distribución elíptica sobre la viga; "
          "muestra 1913.6 Pa máximos aplicados sobre la cara del patín]\n",
          "\n## 2. Eje de material (Tabla 19)\n",
          f"Diferencia máxima entre la Tabla 19 publicada y la reproducida: {r['tabla19_dif_max']:.2e}.\n\n",
          _tabla_md(["Material", "Publicado", "Reproducido", "Pesos alineados"],
                    [[mats[i], f"{r['tabla19_publicada'][i]:.5f}", f"{r['pm_tesis'][i]:.5f}",
                      f"{r['pm_alineado'][i]:.5f}"] for i in range(len(mats))]),
          f"\nRanking tesis: {', '.join(rk(r['pm_tesis']))}.\n\n"
          f"Ranking con pesos alineados: {', '.join(rk(r['pm_alineado']))}.\n\n"
          "Variables sin columna en la base de datos (peso repartido): "
          + ", ".join(f"{v} ({w:.2%})" for v, w in r["faltantes"]) + ".\n",
          "\n[Imagen: Tesis actualizada 3.docx, Tabla 18 — encabezado de importancias desplazado respecto a las columnas]\n",
          "\n## 3. Dominancia de escalas en la matriz final\n",
          f"Dispersión del puntaje de proceso: {r['dispersion_puntaje_proceso']:.1%}. "
          f"Dispersión del costo entre procesos: {r['dispersion_costo_proceso']:.1%}. "
          f"Variación máxima del costo por cambio de material dentro de un proceso: "
          f"{r['dispersion_costo_material_max']:.2%}. "
          f"R_c-p es {r['escala_rcp_sobre_rcm']:.2f} veces R_c-m en promedio.\n",
          "\n## 4. Ranking material-proceso (top 5)\n"]
    for titulo, clave in (("Tesis (Ec. 11 tal cual)", "pt_tesis"),
                          ("Pesos alineados", "pt_alineado"),
                          ("Pesos alineados y relaciones normalizadas", "pt_alineado_norm")):
        md.append(f"\n{titulo}:\n\n")
        md.append(_tabla_md(["#", "Material", "Proceso", "P_T"],
                            [[k + 1, a, b, f"{c:.4e}"] for k, (a, b, c) in
                             enumerate(D.ranking(r[clave], mats, procs, 5))]))
    f = r["mc_freq"]
    top = D.ranking(f, mats, procs, 5)
    md.append("\n## 5. Robustez (Monte Carlo, 5000 juegos de pesos, Dirichlet concentración 50)\n\n")
    md.append(_tabla_md(["Material", "Proceso", "Frecuencia de primer lugar"],
                        [[a, b, f"{c:.1%}"] for a, b, c in top if c > 0]))
    md.append("\nLimitación: el costo sigue siendo el de SEER para una sola pieza; la Fase 2 lo sustituye "
              "por un modelo con volumen de producción.\n")
    import re
    texto = re.sub(r"^(#+ .*)\n(?!\n)", r"\1\n\n", "".join(md), flags=re.M)
    ruta = RAIZ / "docs" / "fase0_reporte.md"
    ruta.write_text(texto, encoding="utf-8")
    return ruta


def main() -> None:
    r = calcular()
    ruta = escribir(r)
    print(f"Reporte: {ruta}")
    print(f"Tabla 19 dif. máx.: {r['tabla19_dif_max']:.2e}")
    for a, b, c in D.ranking(r["pt_tesis"], r["materiales"], r["procesos"], 3):
        print(f"  tesis   {a:<18} {b:<11} {c:.4e}")
    for a, b, c in D.ranking(r["pt_alineado_norm"], r["materiales"], r["procesos"], 3):
        print(f"  corr.   {a:<18} {b:<11} {c:.4f}")


if __name__ == "__main__":
    main()
