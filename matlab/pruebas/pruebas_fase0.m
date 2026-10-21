function pruebas_fase0()
%PRUEBAS_FASE0 Pruebas de la Fase 0 en MATLAB/Octave y cruce contra la implementación Python.
%   Desde la carpeta matlab:  addpath(pwd); addpath('pruebas'); pruebas_fase0
r = cpo.fase0();
assert(abs(cpo.bEliptica(598, 9.81, 3.8, 4639.09) - 3.059) < 5e-4, 'b(n=3.8)');
assert(abs(r.nImplicitoAnsys - 2.5) < 2e-3, 'n implícito 2.5');
assert(abs(r.R2_N - 107.44) < 0.1, 'R2');
assert(abs(r.ahorroNiu - 3433.1) < 0.05, 'Niu');
assert(r.tabla19DifMax < 2e-5, 'Tabla 19');
[~, o] = sort(r.pmAlineado, 'descend');
assert(strcmp(r.materiales{o(1)}, 'Carbon AM') && strcmp(r.materiales{o(end)}, 'Glass'), 'ranking alineado');
assert(r.escalaRcpSobreRcm > 2, 'dominancia de escala');

% Cruce contra Python (si ya se corrió python -m cpo.fase0)
py = fullfile(cpo.raiz(), 'resultados', 'fase0', 'pt_alineado_norm.csv');
if exist(py, 'file')
    [~, celdas] = cpo.leerCSV(py);
    Mpy = str2double(celdas(:, 2:end));
    err = max(abs(Mpy(:) - r.ptAlineadoNorm(:)) ./ abs(Mpy(:)));
    assert(err < 1e-5, sprintf('Python vs MATLAB difieren (%.2e)', err));
    fprintf('Cruce Python vs MATLAB: diferencia relativa máx. %.2e\n', err);
else
    fprintf('Aviso: no hay resultados de Python para cruzar.\n');
end
fprintf('pruebas_fase0: TODAS LAS PRUEBAS PASARON\n');
end
