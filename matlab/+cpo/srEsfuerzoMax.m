function sr = srEsfuerzoMax(s, m)
%SRESFUERZOMAX Razón de resistencia por esfuerzo máximo, s = [s1 s2 t12] locales.
sr = min([lim(s(1), m.Xt, m.Xc), lim(s(2), m.Yt, m.Yc), lim(abs(s(3)), m.S, m.S)]);
end
function r = lim(v, p, n)
if v > 0, r = p/v; elseif v < 0, r = n/(-v); else, r = Inf; end
end
