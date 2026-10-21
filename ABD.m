function [A, B, D] = ABD(lam)
%ABD Matrices de rigidez del laminado (Kaw ec. 4.28).
A = zeros(3); B = zeros(3); D = zeros(3); z = lam.z;
for k = 1:numel(lam.Qb)
    A = A + lam.Qb{k} * (z(k+1) - z(k));
    B = B + lam.Qb{k} * (z(k+1)^2 - z(k)^2) / 2;
    D = D + lam.Qb{k} * (z(k+1)^3 - z(k)^3) / 3;
end
end
