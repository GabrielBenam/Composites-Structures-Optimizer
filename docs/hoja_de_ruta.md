# Hoja de ruta

Cada fase cierra con tres entregables: código Python con pruebas, el equivalente MATLAB (`matlab/run_faseN.m` y `matlab/pruebas/pruebas_faseN.m`, que también cruza resultados contra Python) y un reporte en `docs/`. La fase no se da por terminada si alguna prueba falla.

## Fase 0. Reconstrucción de la tesis (esta versión)

Datos con fuente, reproducción de la Tabla 19 y de las Tablas 22 y 23, diagnóstico de cargas y línea base corregida. Ver `docs/fase0_reporte.md`.

## Fase 1. Vigas de pared delgada (alcance inicial)

Larguero I, C y Z de sección constante bajo flexión y cortante. Comprende la teoría clásica de laminados (matriz ABD) por pared, la rigidez de la sección de pared delgada, los esfuerzos por capa, los criterios de falla con factor de reserva (esfuerzo máximo, Tsai-Hill, Tsai-Wu y Hashin), el pandeo local de patín y alma, y las cargas según ASTM F2245 con el diagrama V-n.

Bibliografía base: Barbero, cap. 10 (10.1 Preliminary Design, 10.2 Thin-Walled Beams); Gay, cap. 15 (flexión de vigas de sección arbitraria) y cap. 16 (torsión); Gay, cap. 12 (placas laminadas delgadas); Barbero, cap. 7 (falla de lámina, primera y última capa); Niu, cap. 7 (Laminate Design Practices, incluye Preliminary Sizing).

Casos de verificación:
- Gay 19.10, "Carbon/Epoxy Wing Spar". Es el caso más cercano al larguero de la tesis.
- Gay 19.7, falla de primera capa.
- Gay 19.2, procedimiento de un programa de cálculo de laminados.
- Ejemplos resueltos de Barbero, cap. 10.
- Tesis de Arreola Santillana (IPN, 2020): viga de sección variable con solución analítica y FEM.
- Layup Analysis Tool y ANSYS ACP R2 (estudiantil) sobre los mismos laminados.

Fase 1b: sección variable y caídas de capa (Arreola; Niu cap. 7).

## Fases siguientes: estructuras propuestas según la bibliografía

El orden sigue la pirámide de ensayos por bloques (building block approach): cada estructura reutiliza los módulos ya verificados.

1. **Paneles y revestimientos.** Placas laminadas a flexión y pandeo bajo compresión y cortante en el plano. Barbero 11.1 Plate Bending y 11.2 Plate Buckling; Gay cap. 12 y cap. 17 (placas gruesas); Vasiliev (placas). Verificación: ejemplos de pandeo de Barbero cap. 11 y el benchmark de apilado de Le Riche y Haftka (paneles a pandeo con algoritmo genético).
2. **Paneles sándwich** (revestimientos, superficies de control). Gay cap. 4 (flexión simplificada, pandeo global y arrugamiento de pieles), 18.1 y 19.1; Niu cap. 4 (manufactura de sándwich). Verificación: Gay 18.1, viga sándwich simplemente apoyada.
3. **Paneles rigidizados** (revestimiento con larguerillos). Barbero 11.3 Stiffened Panels; Gay 7.1.9.2 Rib-Stiffened Panels; Niu cap. 7 Preliminary Sizing.
4. **Almas a cortante y costillas.** Pandeo por cortante del alma, costillas planas con aligeramientos. Niu cap. 7; Barbero cap. 11 (pandeo a cortante).
5. **Cajón de torsión monocelda y bicelda** (larguero más revestimientos). Gay cap. 16 (torsión, centro de torsión, acoplamiento flexión-torsión); Barbero 10.2 (secciones cerradas); es el trabajo futuro que propone Arreola.
6. **Tubos y columnas** (montantes, puntales, tren de aterrizaje tipo ballesta). Barbero 13.5 Beam-Column; Gay 5.4.5.4 Laminated Tubes y 18.4 Drive Shaft. Permite evaluar devanado filamentario donde sí aplica.
7. **Uniones atornilladas y adheridas** (raíz del larguero, herrajes). Gay cap. 6 (factor de reducción por agujero, modos de falla de uniones, adhesivos); Niu cap. 5 (Joining). Su análisis es indispensable para un larguero real.

Fuera de alcance por ahora: recipientes a presión y cascarones de revolución (Barbero cap. 12; Gay 18.9). No son estructura primaria de un ultraligero.

## Capas transversales a todas las fases

- **Manufactura** (Fase 2): reglas de factibilidad por proceso como restricciones. Fuentes: Barbero cap. 3; Campbell; Niu cap. 4; ASM Handbook Vol. 21.
- **Costo** (Fase 2): material, horas de trabajo y herramental amortizado con curva de aprendizaje (nota técnica de SEER-H), con el volumen de producción como parámetro.
- **Optimización y decisión** (Fase 3): NSGA-II sobre material, apilado y proceso, y después TOPSIS con Monte Carlo sobre el frente de Pareto.
- **Valores admisibles**: sustituir las propiedades de libro por valores con base estadística (B-basis; NCAMP y CMH-17) con factores de reducción por ambiente y daño (Barbero 1.5; Niu cap. 7).
