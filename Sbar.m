function Sb = Sbar(m, theta)
%SBAR Flexibilidad reducida transformada (Kaw ec. 2.105).
R = diag([1 1 2]); T = cpo.Tmat(theta);
Sb = R * (T \ (R \ (cpo.Slocal(m) * T)));
end
