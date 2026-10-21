function Qb = Qbar(m, theta)
%QBAR Rigidez reducida transformada (Kaw ec. 2.103).
R = diag([1 1 2]); T = cpo.Tmat(theta);
Qb = (T \ cpo.Qlocal(m)) * R * T / R;
end
