# Prompt de arranque, Fase 1 (vigas de pared delgada)

Contexto: proyecto "Composites", repositorio cpo (GPL, público). La Fase 0 está cerrada: datos con fuente en data/, reproducción de la tesis, Python como referencia y MATLAB espejo cruzado. Lee docs/hoja_de_ruta.md, docs/vv_plan.md y claude/auditoria-tesis-tradeoffs.md del proyecto.

Roles de las fuentes: carpeta "TESIS resumen" = caso base; libros de la carpeta Materiales (Barbero cap. 7 y 10, Gay cap. 12, 15, 16 y 19.10, Niu cap. 7) = ecuaciones y casos de verificación, citando capítulo y página; web = valores admisibles (NCAMP/CMH-17) y ASTM F2245.

Tarea: módulos clt (matriz ABD, esfuerzos por capa con cargas mecánicas), failure (esfuerzo máximo, Tsai-Hill, Tsai-Wu y Hashin con factor de reserva), structures/beam (I, C, Z de pared delgada y sección constante: rigideces, eje neutro, esfuerzos por pared, pandeo local de patín y alma) y loads (V-n según F2245). Verificación mínima: Gay 19.7 y 19.10, ejemplos de Barbero cap. 10 y la viga de Arreola. Entrega: proyecto completo en .zip, texto del workflow, run_fase1.m y pruebas_fase1.m con cruce contra Python, y docs/fase1_reporte.md. Las figuras se referencian como [Imagen: archivo, ubicación].
