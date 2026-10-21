%RUN_BLOQUEA Ejecutable MATLAB del Bloque A (lámina y laminado). También corre en GNU Octave >= 7.
%   Desde la carpeta matlab:  run_bloqueA
here = fileparts(mfilename('fullpath')); addpath(here);
res = cpo.bloqueA();
fprintf('\n=== BLOQUE A: lámina y laminado (MATLAB) ===\n');
casos = unique({res.caso});
for i = 1:numel(casos)
    r = res(strcmp({res.caso}, casos{i}));
    d = max(abs([r.calculado] - [r.libro]) ./ abs([r.libro]));
    estado = 'REVISAR'; if all([r.ok]), estado = 'OK'; end
    fprintf('%-12s %3d comparaciones, dif. máx. %6.3f %%  %s\n', casos{i}, numel(r), 100*d, estado);
end
fprintf('Total: %d de %d dentro de tolerancia\n', sum([res.ok]), numel(res));
