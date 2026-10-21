function sr = srTsaiHill(s, m, modificado)
%SRTSAIHILL Tsai-Hill (Kaw ec. 2.150-2.151). modificado = true usa resistencias según el signo.
if nargin < 3, modificado = false; end
if modificado
    X1 = m.Xt; if s(1) < 0, X1 = m.Xc; end
    X2 = m.Xt; if s(2) < 0, X2 = m.Xc; end
    Y = m.Yt;  if s(2) < 0, Y = m.Yc; end
else
    X1 = m.Xt; X2 = m.Xt; Y = m.Yt;
end
I = (s(1)/X1)^2 - s(1)*s(2)/X2^2 + (s(2)/Y)^2 + (s(3)/m.S)^2;
sr = 1/sqrt(I);
end
