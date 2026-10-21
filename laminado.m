function lam = laminado(m, angulos, espesores)
%LAMINADO Define un laminado (capas de arriba hacia abajo, z positiva hacia abajo; Kaw cap. 4).
%   m: lámina (struct) o cell de láminas; angulos y espesores: vectores.
n = numel(angulos);
if isscalar(espesores), espesores = repmat(espesores, 1, n); end
if ~iscell(m), m = repmat({m}, 1, n); end
h = sum(espesores);
lam.z = [-h/2, -h/2 + cumsum(espesores)];
lam.h = h; lam.angulos = angulos; lam.mat = m;
lam.Qb = cell(1, n);
for k = 1:n, lam.Qb{k} = cpo.Qbar(m{k}, angulos(k)); end
end
