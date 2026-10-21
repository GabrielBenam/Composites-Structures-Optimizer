function T = leerTabla(relativa)
%LEERTABLA Lee data/<relativa>.csv (primera columna = etiqueta) y exige su .meta.json.
%   T.filas (cell), T.columnas (cell), T.valores (double), T.meta (struct)
ruta = fullfile(cpo.raiz(), 'data', relativa);
rutaMeta = regexprep(ruta, '\.csv$', '.meta.json');
if ~exist(rutaMeta, 'file')
    error('cpo:sinFuente', '%s no tiene .meta.json: todo dato requiere fuente documentada', relativa);
end
T.meta = jsondecode(fileread(rutaMeta));
[enc, celdas] = cpo.leerCSV(ruta);
T.columnas = enc(2:end);
T.filas = celdas(:, 1);
T.valores = str2double(celdas(:, 2:end));
end
