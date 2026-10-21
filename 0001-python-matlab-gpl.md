# 0001. Python como referencia, MATLAB como implementación espejo, licencia GPL

Fecha: 2026-10-21. Estado: aceptada.

Contexto: se busca automatizar la metodología, distribuirla abiertamente y conservar una versión ejecutable en MATLAB en cada fase. La tesis original usó MATLAB y Excel, y la Matriz 2 se perdió sin respaldo.

Decisión: Python (numpy; más adelante scipy y pymoo) es la implementación de referencia porque es gratuito, se integra con GitHub Actions y permite compilar ejecutables. Cada fase incluye un paquete MATLAB `+cpo` escrito de forma independiente que lee los mismos `data/` y se cruza contra Python. El repositorio es público y GPL-3.0-or-later; eso permite reutilizar código de Layup Analysis Tool (GPL-3.0) con atribución.

Consecuencias: dos implementaciones exigen más trabajo, pero el cruce entre ellas es una verificación independiente (V2). Para MATLAB solo se usan funciones compatibles con GNU Octave 7, para no depender de toolboxes.
