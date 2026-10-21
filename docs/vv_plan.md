# Plan de verificación y validación (V&V)

Verificar es comprobar que el código resuelve bien las ecuaciones. Validar es comprobar que esas ecuaciones representan bien la realidad. Como el proyecto es teórico (sin ensayos propios), la validación se apoya en datos experimentales publicados.

| Nivel | Qué se compara | Criterio de aceptación |
|---|---|---|
| V0 Regresión | Código contra tablas publicadas de la tesis | Tabla 19 con diferencia < 2e-5; Tablas 22 y 23 con < 0.2 % |
| V1 Analítica | Módulos contra solución cerrada (integrales, ejemplos resueltos de Gay, Barbero, Vasiliev) | < 1 % |
| V2 Cruzada | Python contra MATLAB (implementaciones independientes) | < 1e-5 relativo |
| V3 Herramientas | Contra Layup Analysis Tool y ANSYS ACP R2 en los mismos laminados | < 2 % en ABD; < 5 % en esfuerzos de capa |
| V4 Caso de referencia | Viga de Arreola (analítica y FEM); Gay 19.10 | < 5–10 % en flecha y esfuerzos |
| V5 Validación con datos publicados | Ensayos de vigas I compuestas en la literatura (p. ej., Zhou y Hood, 2006) | Dentro de la dispersión experimental reportada |
| V6 Decisión | Estabilidad del ranking (Monte Carlo sobre pesos, costos y volumen); comparación TOPSIS contra suma ponderada | Se reporta la frecuencia de primer lugar; un ganador por debajo del 60 % se declara no concluyente |

Estado: V0 y V2 cumplidos para cargas y matriz de decisión (Fase 0). V1 y V2 en curso para lámina y laminado (Bloque A): 267 comparaciones contra Kaw y Gay dentro de tolerancia; 144 de ellas recalculadas en MATLAB, con diferencia contra Python del orden de 1e-15.
