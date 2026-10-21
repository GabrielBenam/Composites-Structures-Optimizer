function [encabezado, celdas] = leerCSV(ruta)
%LEERCSV Lector CSV mínimo compatible con MATLAB y Octave (sin comillas anidadas).
fid = fopen(ruta, 'r', 'n', 'UTF-8');
if fid < 0, error('cpo:archivo', 'No se pudo abrir %s', ruta); end
limpiar = onCleanup(@() fclose(fid));
encabezado = strsplit(strtrim(fgetl(fid)), ',', 'CollapseDelimiters', false);
celdas = {};
while true
    linea = fgetl(fid);
    if ~ischar(linea), break; end
    linea = strtrim(linea);
    if isempty(linea), continue; end
    celdas(end+1, :) = strsplit(linea, ',', 'CollapseDelimiters', false); %#ok<AGROW>
end
end
