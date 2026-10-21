function [total, celdas] = puntajeMaterial(props, columnas, nombresPeso, valoresPeso)
%PUNTAJEMATERIAL Suma ponderada normalizada por suma (Ec. 5 de la tesis).
%   La columna 'density' entra como 1/valor (menor es mejor).
celdas = zeros(size(props));
for k = 1:numel(nombresPeso)
    j = find(strcmp(columnas, nombresPeso{k}));
    if isempty(j) || valoresPeso(k) == 0, continue; end
    x = props(:, j);
    if strcmp(nombresPeso{k}, 'density'), x = 1 ./ x; end
    celdas(:, j) = x ./ sum(x) .* valoresPeso(k);
end
total = sum(celdas, 2);
end
