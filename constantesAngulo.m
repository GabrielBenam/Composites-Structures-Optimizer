function c = constantesAngulo(m, theta)
%CONSTANTESANGULO Constantes ingenieriles de una lámina en ángulo (Kaw ec. 2.117-2.128).
Sb = cpo.Sbar(m, theta);
c.Ex = 1/Sb(1,1); c.nuxy = -Sb(1,2)/Sb(1,1); c.mx = -Sb(1,3)*m.E1;
c.Ey = 1/Sb(2,2); c.my = -Sb(2,3)*m.E1; c.Gxy = 1/Sb(3,3);
end
