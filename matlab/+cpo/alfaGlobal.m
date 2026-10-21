function a = alfaGlobal(m, theta, campo)
%ALFAGLOBAL Coeficientes de expansión globales [ax; ay; axy] (Kaw ec. 2.175).
%   campo = 'a' (térmico) o 'b' (humedad).
if nargin < 3, campo = 'a'; end
v = cpo.Tmat(theta) \ [m.([campo '1']); m.([campo '2']); 0];
a = v .* [1; 1; 2];
end
