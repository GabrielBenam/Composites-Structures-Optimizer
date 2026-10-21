function [N, M] = cargasHigrotermicas(lam, dT, dC)
%CARGASHIGROTERMICAS Fuerzas y momentos ficticios (Kaw ec. 4.64-4.67).
N = zeros(3,1); M = zeros(3,1); z = lam.z;
for k = 1:numel(lam.Qb)
    e = cpo.alfaGlobal(lam.mat{k}, lam.angulos(k), 'a')*dT + cpo.alfaGlobal(lam.mat{k}, lam.angulos(k), 'b')*dC;
    N = N + lam.Qb{k} * e * (z(k+1) - z(k));
    M = M + lam.Qb{k} * e * (z(k+1)^2 - z(k)^2) / 2;
end
end
