function m = cargarLamina(archivo, nombre)
%CARGARLAMINA Lee una lámina de data/materiales/<archivo> (exige .meta.json).
ruta = fullfile(cpo.raiz(), 'data', 'materiales', archivo);
if ~exist(regexprep(ruta, '\.csv$', '.meta.json'), 'file')
    error('cpo:sinFuente', '%s no tiene .meta.json', archivo);
end
[enc, celdas] = cpo.leerCSV(ruta);
fila = find(strcmp(celdas(:, 1), nombre));
if isempty(fila), error('cpo:material', '%s no está en %s', nombre, archivo); end
campos = {'E1','E2','nu12','G12','Xt','Xc','Yt','Yc','S','a1','a2','b1','b2'};
for k = 1:numel(campos)
    m.(campos{k}) = str2double(celdas{fila, strcmp(enc, campos{k})});
end
m.nu21 = m.nu12 * m.E2 / m.E1;
m.nombre = nombre;
end
