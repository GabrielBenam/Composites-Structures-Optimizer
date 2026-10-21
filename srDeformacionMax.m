function sr = srDeformacionMax(s, m)
%SRDEFORMACIONMAX Razón de resistencia por deformación máxima (Kaw ec. 2.143).
e = cpo.Slocal(m) * s(:);
sr = min([lim(e(1), m.Xt/m.E1, m.Xc/m.E1), lim(e(2), m.Yt/m.E2, m.Yc/m.E2), ...
          lim(abs(e(3)), m.S/m.G12, m.S/m.G12)]);
end
function r = lim(v, p, n)
if v > 0, r = p/v; elseif v < 0, r = n/(-v); else, r = Inf; end
end
