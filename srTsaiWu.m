function sr = srTsaiWu(s, m, h12)
%SRTSAIWU Tsai-Wu (Kaw ec. 2.152). h12: 'mises-hencky' (defecto), 'tsai-hill', 'hoffman' o número.
if nargin < 3, h12 = 'mises-hencky'; end
H1 = 1/m.Xt - 1/m.Xc; H2 = 1/m.Yt - 1/m.Yc;
H11 = 1/(m.Xt*m.Xc); H22 = 1/(m.Yt*m.Yc); H66 = 1/m.S^2;
if isnumeric(h12), H12 = h12;
elseif strcmp(h12, 'mises-hencky'), H12 = -0.5*sqrt(H11*H22);
elseif strcmp(h12, 'tsai-hill'), H12 = -1/(2*m.Xt^2);
else, H12 = -1/(2*m.Xt*m.Xc);
end
a = H11*s(1)^2 + H22*s(2)^2 + H66*s(3)^2 + 2*H12*s(1)*s(2);
b = H1*s(1) + H2*s(2);
sr = (-b + sqrt(b^2 + 4*a)) / (2*a);
end
