# Fase 0: reproducción de la tesis y línea base corregida

Archivo generado por `python -m cpo.fase0`. No editar a mano.
## 1. Cargas

| n | b = q(0) [N/mm] | M raíz [N·m] |
|---|---|---|
| 2.5 | 2.0126 | 14438 |
| 3.8 | 3.0592 | 21945 |
| 6.0 | 4.8302 | 34651 |

El valor b = 2.012 N/mm usado en ANSYS implica n = 2.499; el b = 3.059 N/mm publicado implica n = 3.800.

Carga total que debería leer la sonda de reacción del larguero aislado (factor 1.07 de la tesis):

| n | Reacción esperada [N] |
|---|---|
| 2.5 | 7846 |
| 3.8 | 11926 |

Fuerza realmente aplicada si la presión se calculó dividiendo entre la cuerda (1125 mm) y se aplicó sobre la cara del patín:

| Ancho de patín [mm] | Fuerza aplicada [N] |
|---|---|
| 30 | 209 |
| 50 | 349 |
| 75 | 523 |
| 100 | 697 |

R2 recalculado con la ecuación de momentos de la tesis: 107.46 N (la tesis reporta 143.89 N). Con regla de la palanca, si la sustentación cae entre largueros, el larguero principal toma 0.958 de la carga, no 1.07.

Ahorro Niu con los pesos de la Tabla 25: 3433.1 USD (la tesis reporta 1082.37).

[Imagen: Tesis actualizada 3.docx, Ilustración 52 — distribución elíptica sobre la viga; muestra 1913.6 Pa máximos aplicados sobre la cara del patín]

## 2. Eje de material (Tabla 19)

Diferencia máxima entre la Tabla 19 publicada y la reproducida: 8.14e-06.

| Material | Publicado | Reproducido | Pesos alineados |
|---|---|---|---|
| Carbon AM | 0.09636 | 0.09636 | 0.14633 |
| Carbon MM | 0.06755 | 0.06755 | 0.07919 |
| Glass | 0.08798 | 0.08797 | 0.04769 |
| Kevlar | 0.07722 | 0.07722 | 0.05768 |
| Borum | 0.09737 | 0.09737 | 0.11220 |
| C-C-C-K-K-C-C-C | 0.07228 | 0.07228 | 0.06828 |
| K-K-C-C-C-C-K-K | 0.08666 | 0.08667 | 0.10182 |
| C-C-G-G-G-G-C-C | 0.07753 | 0.07753 | 0.06309 |
| G-G-C-C-C-C-G-G | 0.09197 | 0.09197 | 0.09671 |
| G-G-K-K-K-K-G-G | 0.08196 | 0.08196 | 0.05173 |
| C-C-C-B-B-C-C-C | 0.08223 | 0.08223 | 0.09534 |
| G-G-B-B-B-B-G-G | 0.09268 | 0.09267 | 0.07994 |

Ranking tesis: Borum, Carbon AM, G-G-B-B-B-B-G-G, G-G-C-C-C-C-G-G, Glass, K-K-C-C-C-C-K-K, C-C-C-B-B-C-C-C, G-G-K-K-K-K-G-G, C-C-G-G-G-G-C-C, Kevlar, C-C-C-K-K-C-C-C, Carbon MM.

Ranking con pesos alineados: Carbon AM, Borum, K-K-C-C-C-C-K-K, G-G-C-C-C-C-G-G, C-C-C-B-B-C-C-C, G-G-B-B-B-B-G-G, Carbon MM, C-C-C-K-K-C-C-C, C-C-G-G-G-G-C-C, Kevlar, G-G-K-K-K-K-G-G, Glass.

Variables sin columna en la base de datos (peso repartido): shear_modulus (30.46%), interlaminar_shear_strength (3.30%).

[Imagen: Tesis actualizada 3.docx, Tabla 18 — encabezado de importancias desplazado respecto a las columnas]

## 3. Dominancia de escalas en la matriz final

Dispersión del puntaje de proceso: 16.6%. Dispersión del costo entre procesos: 54.0%. Variación máxima del costo por cambio de material dentro de un proceso: 1.42%. R_c-p es 2.36 veces R_c-m en promedio.

## 4. Ranking material-proceso (top 5)

Tesis (Ec. 11 tal cual):

| # | Material | Proceso | P_T |
|---|---|---|---|
| 1 | Carbon AM | pultrusion | 3.0941e-07 |
| 2 | Borum | pultrusion | 3.0748e-07 |
| 3 | G-G-C-C-C-C-G-G | pultrusion | 3.0602e-07 |
| 4 | G-G-B-B-B-B-G-G | pultrusion | 3.0528e-07 |
| 5 | Glass | pultrusion | 3.0218e-07 |

Pesos alineados:

| # | Material | Proceso | P_T |
|---|---|---|---|
| 1 | Carbon AM | pultrusion | 3.6051e-07 |
| 2 | Borum | pultrusion | 3.2250e-07 |
| 3 | Carbon AM | contacto | 3.1793e-07 |
| 4 | K-K-C-C-C-C-K-K | pultrusion | 3.1492e-07 |
| 5 | G-G-C-C-C-C-G-G | pultrusion | 3.1089e-07 |

Pesos alineados y relaciones normalizadas:

| # | Material | Proceso | P_T |
|---|---|---|---|
| 1 | Carbon AM | pultrusion | 9.9776e-01 |
| 2 | Carbon AM | contacto | 8.9116e-01 |
| 3 | Borum | pultrusion | 8.7273e-01 |
| 4 | K-K-C-C-C-C-K-K | pultrusion | 8.4549e-01 |
| 5 | G-G-C-C-C-C-G-G | pultrusion | 8.3120e-01 |

## 5. Robustez (Monte Carlo, 5000 juegos de pesos, Dirichlet concentración 50)

| Material | Proceso | Frecuencia de primer lugar |
|---|---|---|
| Carbon AM | pultrusion | 100.0% |

Limitación: el costo sigue siendo el de SEER para una sola pieza; la Fase 2 lo sustituye por un modelo con volumen de producción.
