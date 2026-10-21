function pruebas_bloqueA()
%PRUEBAS_BLOQUEA Verifica el Bloque A en MATLAB contra el libro y contra los resultados de Python.
%   Desde la carpeta matlab:  addpath(pwd); addpath('pruebas'); pruebas_bloqueA
res = cpo.bloqueA();
malos = res(~[res.ok]);
for i = 1:numel(malos)
    fprintf('FALLA %s.%s: calc=%g libro=%g\n', malos(i).caso, malos(i).clave, malos(i).calculado, malos(i).libro);
end
assert(isempty(malos), 'Hay comparaciones fuera de tolerancia contra el libro');
fprintf('Contra el libro: %d comparaciones OK\n', numel(res));
py = fullfile(cpo.raiz(), 'resultados', 'bloqueA_comparaciones.json');
if exist(py, 'file')
    P = jsondecode(fileread(py)); n = 0; emax = 0;
    for i = 1:numel(res)
        caso = res(i).caso; clave = res(i).clave;
        if isfield(P, caso) && isfield(P.(caso).valores, clave)
            vp = P.(caso).valores.(clave).calculado;
            e = abs(vp - res(i).calculado) / max(abs(vp), realmin);
            emax = max(emax, e); n = n + 1;
        end
    end
    assert(emax < 1e-6, sprintf('Python y MATLAB difieren (%.2e)', emax));
    fprintf('Cruce Python vs MATLAB: %d valores, diferencia relativa máx. %.2e\n', n, emax);
else
    fprintf('Aviso: no hay resultados de Python para cruzar (corre python -m cpo.informe bloqueA).\n');
end
fprintf('pruebas_bloqueA: TODAS LAS PRUEBAS PASARON\n');
end
