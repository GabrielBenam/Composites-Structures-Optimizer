%RUN_FASE0 Ejecutable MATLAB de la Fase 0 (también corre en GNU Octave >= 7).
%   Abrir MATLAB en la carpeta "matlab" del repositorio y ejecutar:  run_fase0
%   Escribe resultados en resultados/fase0_matlab/ y los muestra en consola.
here = fileparts(mfilename('fullpath'));
addpath(here);
r = cpo.fase0();

fprintf('\n=== FASE 0: reproducción de la tesis ===\n');
fprintf('b usado en ANSYS (2.012 N/mm) implica n = %.3f\n', r.nImplicitoAnsys);
fprintf('Reacción esperada en el larguero: n=2.5 -> %.0f N ; n=3.8 -> %.0f N\n', r.reaccionEsperada_N);
for i = 1:numel(r.anchos_mm)
    fprintf('  Fuerza aplicada con patín de %3d mm (error de la tesis): %.0f N\n', r.anchos_mm(i), r.fuerzaAplicada_N(i));
end
fprintf('R2 recalculado: %.2f N (tesis 143.89) | Ahorro Niu: %.1f USD (tesis 1082.37)\n', r.R2_N, r.ahorroNiu);
fprintf('Tabla 19 reproducida, diferencia máx.: %.2e\n', r.tabla19DifMax);

[~, o1] = sort(r.pmTesis, 'descend'); [~, o2] = sort(r.pmAlineado, 'descend');
fprintf('\n%-18s %10s %10s\n', 'Material', 'Tesis', 'Alineado');
for i = 1:numel(r.materiales)
    fprintf('%-18s %10.5f %10.5f\n', r.materiales{i}, r.pmTesis(i), r.pmAlineado(i));
end
fprintf('Primer lugar tesis: %s | alineado: %s\n', r.materiales{o1(1)}, r.materiales{o2(1)});

[mx, ix] = max(r.ptTesis(:)); [ii, jj] = ind2sub(size(r.ptTesis), ix);
fprintf('\nGanador Ec. 11 (tesis): %s + %s (%.4e)\n', r.materiales{ii}, r.procesos{jj}, mx);
[mx, ix] = max(r.ptAlineadoNorm(:)); [ii, jj] = ind2sub(size(r.ptAlineadoNorm), ix);
fprintf('Ganador corregido (alineado + normalizado): %s + %s (%.4f)\n', r.materiales{ii}, r.procesos{jj}, mx);
fprintf('R_c-p / R_c-m promedio: %.2f\n', r.escalaRcpSobreRcm);

out = fullfile(cpo.raiz(), 'resultados', 'fase0_matlab');
if ~exist(out, 'dir'), mkdir(out); end
nombres = {'ptTesis', 'ptAlineado', 'ptAlineadoNorm'};
for k = 1:numel(nombres)
    M = r.(nombres{k});
    fid = fopen(fullfile(out, [nombres{k} '.csv']), 'w');
    fprintf(fid, 'material,%s\n', strjoin(r.procesos, ','));
    for i = 1:size(M, 1)
        fprintf(fid, '%s', r.materiales{i}); fprintf(fid, ',%.6e', M(i, :)); fprintf(fid, '\n');
    end
    fclose(fid);
end
fprintf('\nResultados escritos en %s\n', out);
