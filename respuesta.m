function [e0, k] = respuesta(lam, N, M, dT, dC)
%RESPUESTA Deformaciones del plano medio y curvaturas (Kaw ec. 4.29 y 4.68).
if nargin < 3 || isempty(M), M = [0;0;0]; end
if nargin < 4, dT = 0; end
if nargin < 5, dC = 0; end
[A, B, D] = cpo.ABD(lam);
[NT, MT] = cpo.cargasHigrotermicas(lam, dT, dC);
x = [A B; B D] \ [N(:) + NT; M(:) + MT];
e0 = x(1:3); k = x(4:6);
end
