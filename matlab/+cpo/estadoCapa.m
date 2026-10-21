function s = estadoCapa(lam, k, pos, e0, kap, dT, dC)
%ESTADOCAPA Deformaciones y esfuerzos en 'sup', 'medio' o 'inf' de la capa k.
if nargin < 6, dT = 0; end
if nargin < 7, dC = 0; end
switch pos
    case 'sup', z = lam.z(k);
    case 'medio', z = (lam.z(k) + lam.z(k+1)) / 2;
    otherwise, z = lam.z(k+1);
end
th = lam.angulos(k); m = lam.mat{k};
s.eps = e0(:) + z * kap(:);
libre = cpo.alfaGlobal(m, th, 'a')*dT + cpo.alfaGlobal(m, th, 'b')*dC;
s.sig = lam.Qb{k} * (s.eps - libre);
s.sigLocal = cpo.Tmat(th) * s.sig;
s.epsLocal = diag([1 1 2]) * cpo.Tmat(th) * diag([1 1 0.5]) * s.eps;
end
