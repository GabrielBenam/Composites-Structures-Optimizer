# cpo: diseño preliminar de estructuras aeronáuticas en materiales compuestos

Herramienta abierta (GPL-3.0) para dimensionar y optimizar de forma preliminar estructuras aeronáuticas básicas en materiales compuestos, con la selección de material, apilado y proceso de manufactura justificada por costo y desempeño. Nace de la tesis de Benítez y Pérez (UNAQ, 2024) y la corrige y formaliza.

Estado: **Fase 0** cerrada y **Bloque A** (lámina y laminado) en curso: 22 ejemplos de Kaw y Gay resueltos y verificados contra el libro (267 comparaciones), con explicación paso a paso en LaTeX. Hoja de ruta en `docs/hoja_de_ruta.md`.

## Uso rápido

Python (3.10 o superior):

    pip install -e ".[dev]"
    pytest -q
    python -m cpo.fase0        # genera docs/fase0_reporte.md y resultados/fase0/
    python -m cpo.informe bloqueA   # genera docs/ejemplos/bloqueA.tex (compilar con pdflatex o latexmk)

MATLAB (o GNU Octave 7 o superior), desde la carpeta `matlab`:

    run_fase0
    run_bloqueA
    addpath('pruebas'); pruebas_fase0; pruebas_bloqueA   % incluyen el cruce contra Python

## Reglas del proyecto

1. Todo dato numérico vive en `data/`. Cada CSV va acompañado de un `.meta.json` con fuente, unidades, base estadística y problemas conocidos; el código no carga un CSV sin él.
2. Cada módulo se verifica contra un caso con resultado conocido antes de usarse en un caso de estudio (`docs/vv_plan.md`).
3. Python es la implementación de referencia. MATLAB es una implementación independiente que se cruza contra Python en cada fase.
4. No se suben libros ni PDFs con derechos de autor: solo citas (`docs/referencias.bib`) con capítulo y página.
5. Las figuras se referencian como `[Imagen: archivo, ubicación]` y el autor las inserta.
6. Los ejemplos de libros se redactan con palabras propias y citan página; los valores publicados viven en `data/ejemplos/` y las erratas de los libros se documentan, no se ocultan.

## Estructura

    data/        datos con fuente (tesis, aeronave, materiales)
    src/cpo/     paquete Python
    tests/       pruebas de verificación y regresión
    matlab/      paquete +cpo, ejecutable run_faseN.m y pruebas
    docs/        metodología, hoja de ruta, plan V&V, decisiones, reportes
    .github/     integración continua (Python y MATLAB)

## Licencia

GPL-3.0-or-later. Ver `LICENSE`.
