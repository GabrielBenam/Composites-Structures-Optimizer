# 0002. Ejemplos resueltos con explicación en LaTeX y política de derechos de autor

Fecha: 2026-10-21. Estado: aceptada.

Contexto: se quiere que la herramienta resuelva los ejemplos de la bibliografía (Gay, Kaw, Barbero, Voyiadjis) y muestre cómo se resolvieron, en un repositorio público.

Decisión:
1. Cada ejemplo es una función que construye una `Derivacion`: planteamiento, pasos con ecuación simbólica, sustitución y resultado, y una tabla de comparación contra el valor publicado. La salida es LaTeX en español; el PDF lo compila GitHub Actions.
2. Los valores publicados se guardan en `data/ejemplos/<bloque>_referencias.json` con libro y página. Python y MATLAB leen ese mismo archivo.
3. No se copia texto, figuras ni soluciones de los libros: los planteamientos se redactan con palabras propias, las figuras se citan como `[Imagen: libro, figura, página]` y la derivación es propia.
4. Si un valor del libro es incorrecto se marca como errata con su justificación; la prueba no se relaja en silencio.
5. MATLAB replica los solucionadores y verifica los mismos resultados numéricos; el documento LaTeX lo genera solo Python.

Consecuencias: cada ejemplo es a la vez material didáctico y prueba de regresión. La tolerancia por defecto es 0.5 %; las tolerancias mayores se justifican en una nota (redondeos del libro).
