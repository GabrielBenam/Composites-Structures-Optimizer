# Metodología (documento vivo)

Convención de figuras: este documento no incrusta imágenes. Donde va una figura aparece una referencia entre corchetes con su origen, por ejemplo `[Imagen: Tesis actualizada 3.docx, Ilustración 26]`, y el autor la inserta en la versión final.

## 1. Origen

La metodología parte de la tesis "Propuesta de metodología tradeoffs aplicada a elementos estructurales de ultraligero entrenador en materiales compuestos" (Benítez y Pérez, Universidad Aeronáutica en Querétaro, 2024) y del artículo homónimo presentado en el 1er Congreso INAE (2024).

[Imagen: Tesis actualizada 3.docx, Ilustración 26 — diagrama de flujo de la metodología original]

## 2. Formulación original (reproducida en la Fase 0)

1. Cargas: distribución elíptica de sustentación sobre la semiala, m·g·n/2 = π·a·b/4, con a = semienvergadura y b = carga por unidad de envergadura en la raíz.
2. Modos de falla: frecuencia media de aparición de cada modo por capa (tesis 7.3.2), convertida en importancia de propiedades mecánicas.
3. Eje de material: suma ponderada de propiedades normalizadas por suma (Ec. 5).
4. Eje de proceso: QFD con benchmark cualitativo de 1 a 5 (Ec. 6 y 7).
5. Eje de costo: SEER-MFG para una pieza (Tabla 7).
6. Puntaje final: P_T = (R_c-p + R_c-m)/2 con R = puntaje/costo (Ec. 9 a 11).

[Imagen: Tesis actualizada 3.docx, Ilustración 68 — superficie material-proceso-costo]

## 3. Hallazgos de la reproducción

Ver `docs/fase0_reporte.md`, que se genera automáticamente. En resumen:

1. La carga usada en ANSYS corresponde a n = 2.5, no a 3.8.
2. En la viga aislada, la carga por unidad de envergadura se dividió entre la cuerda y se aplicó sobre la cara del patín, de modo que la viga recibe solo una fracción de la carga.
3. Las importancias se aplicaron a columnas desplazadas. Con la alineación correcta, el carbono de alto módulo queda claramente primero y el vidrio pasa a último.
4. R_c-p es unas 2.4 veces R_c-m. El costo de SEER para una pieza casi no distingue materiales (variación menor a 1.5 %), así que el proceso ganador lo decide el herramental.

[Imagen: Tesis actualizada 3.docx, Ilustración 52 — presión aplicada sobre la viga]
[Imagen: Tesis actualizada 3.docx, Tabla 18 — encabezado de importancias]

## 4. Formulación objetivo (Fases 1 a 3)

Diseño preliminar como optimización con restricciones y después decisión multicriterio sobre el frente de Pareto:

- Variables: material (lámina con valores admisibles), secuencia de apilado por región, proceso.
- Objetivos: masa y costo a volumen N.
- Restricciones: factor de reserva ≥ 1.5 por modo de falla tras los factores de reducción, pandeo, reglas de diseño (simetría, balance, regla del 10 %, ±45° en las capas exteriores) y factibilidad del proceso.
- Decisión: TOPSIS sobre el frente, con robustez medida por Monte Carlo.

## 5. Pendientes que debe aportar el autor

- Ancho real del patín y sección de la viga de aluminio de referencia (plano o CAD).
- Lectura de la sonda de reacción en el modelo de ANSYS de la tesis.
