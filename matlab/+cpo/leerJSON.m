function s = leerJSON(relativa)
%LEERJSON Lee data/<relativa> como struct.
s = jsondecode(fileread(fullfile(cpo.raiz(), 'data', relativa)));
end
