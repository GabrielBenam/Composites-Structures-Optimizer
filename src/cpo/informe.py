"""Genera el documento LaTeX de ejemplos resueltos de un bloque y un resumen JSON.

Uso:  python -m cpo.informe bloqueA
Salida: docs/ejemplos/<bloque>.tex  y  resultados/<bloque>_comparaciones.json
"""
from __future__ import annotations

import json
import sys

from .datos import RAIZ
from .derivacion import num
from .ejemplos import REGISTRO, cargar_todos, resolver

TITULOS = {"bloqueA": "Bloque A: lámina y laminado"}

PREAMBULO = r"""\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\IfFileExists{lmodern.sty}{\usepackage{lmodern}}{}
\usepackage[spanish,es-noshorthands,es-nodecimaldot]{babel}
\usepackage[margin=2.2cm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{booktabs,longtable}
\usepackage[hidelinks]{hyperref}
\allowdisplaybreaks
\setlength{\parindent}{0pt}
\setlength{\parskip}{4pt}
"""


REEMPLAZOS = {"−": r"\ensuremath{-}", "°": r"\ensuremath{^\circ}", "±": r"\ensuremath{\pm}",
              "ℓ": r"\ensuremath{\ell}", "×": r"\ensuremath{\times}", "μ": r"\ensuremath{\mu}"}


def sanear(texto: str) -> str:
    """Sustituye caracteres Unicode que pdflatex no compone por macros válidas en texto y en modo matemático."""
    for a, b in REEMPLAZOS.items():
        texto = texto.replace(a, b)
    return texto


def generar(bloque: str = "bloqueA"):
    cargar_todos()
    claves = [k for k, v in REGISTRO.items() if v["bloque"] == bloque]
    ders = [resolver(k) for k in claves]
    filas, resumen = [], {}
    for d in ders:
        n = len(d.comparaciones)
        ok = sum(c.cumple for c in d.comparaciones)
        err = sum(c.errata for c in d.comparaciones)
        dmax = max((c.dif_rel for c in d.comparaciones if not c.errata), default=0.0)
        resumen[d.clave] = {"titulo": d.titulo, "comparaciones": n, "cumplen": ok, "erratas": err,
                            "dif_max_rel": dmax,
                            "valores": {c.clave: {"calculado": c.calculado, "libro": c.libro, "cumple": c.cumple,
                                                  "errata": c.errata} for c in d.comparaciones}}
        estado = "completo" if ok == n else "revisar"
        filas.append(f"\\hyperref[ej:{d.clave}]{{{d.titulo.split(':')[0]}}} & {n} & {100*dmax:.2f} & {err} & {estado} \\\\")
    total = sum(r["comparaciones"] for r in resumen.values())
    cumplen = sum(r["cumplen"] for r in resumen.values())
    titulo = TITULOS.get(bloque, bloque)
    tex = [PREAMBULO,
           f"\\title{{Ejemplos resueltos\\\\ {titulo}}}\n\\author{{Proyecto cpo (GPL-3.0)}}\n\\date{{\\today}}",
           "\\begin{document}\\maketitle",
           "\\section*{Cómo leer este documento}",
           "Cada ejemplo reproduce un problema publicado en la bibliografía. El planteamiento está redactado con "
           "palabras propias y cita la página de origen; las figuras se indican como \\textit{[Imagen: libro, figura, "
           "página]} para insertarlas en la versión final. Cada solución muestra la ecuación simbólica, la "
           "sustitución y el resultado, y termina con una tabla que compara el valor del libro contra el calculado por "
           "el programa. Una diferencia mayor que la tolerancia declarada hace fallar las pruebas automáticas del "
           "repositorio. Cuando el valor impreso en el libro es incorrecto se marca como \\textit{errata} y se explica.",
           f"\\paragraph{{Resultado global.}} {cumplen} de {total} comparaciones dentro de tolerancia en {len(ders)} ejemplos.",
           "\\begin{longtable}{lrrrl}\\toprule Ejemplo & Comparaciones & Dif. máx. (\\%) & Erratas & Estado \\\\ "
           "\\midrule\\endhead",
           *filas, "\\bottomrule\\end{longtable}",
           "\\paragraph{Convenciones.} Ejes de la capa 1-2 (en Gay, $\\ell$-$t$); ejes globales $x$-$y$; "
           "$\\theta$ de $x$ hacia 1; deformaciones cortantes ingenieriles; capas numeradas de arriba hacia abajo "
           "con $z$ positiva hacia abajo (Kaw). Las rigideces $E_{ij}$ de Gay equivalen a $\\bar Q_{ij}$.",
           "\\tableofcontents\\clearpage"]
    libro_actual = None
    for k, d in zip(claves, ders):
        libro = REGISTRO[k]["libro"]
        if libro != libro_actual:
            tex.append(f"\\part*{{{libro}}}\\addcontentsline{{toc}}{{part}}{{{libro}}}")
            libro_actual = libro
        tex.append(d.latex())
        tex.append("\\clearpage")
    tex.append("\\end{document}")
    out = RAIZ / "docs" / "ejemplos"
    out.mkdir(parents=True, exist_ok=True)
    ruta_tex = out / f"{bloque}.tex"
    ruta_tex.write_text(sanear("\n".join(tex)), encoding="utf-8")
    res = RAIZ / "resultados"
    res.mkdir(exist_ok=True)
    (res / f"{bloque}_comparaciones.json").write_text(json.dumps(resumen, indent=1, ensure_ascii=False),
                                                      encoding="utf-8")
    return ruta_tex, cumplen, total


def main():
    bloque = sys.argv[1] if len(sys.argv) > 1 else "bloqueA"
    ruta, ok, total = generar(bloque)
    print(f"{ruta}  ({ok}/{total} comparaciones dentro de tolerancia)")
    if ok != total:
        sys.exit(1)


if __name__ == "__main__":
    main()
