function Q = Qlocal(m)
%QLOCAL Rigidez reducida [Q] de la lámina (Kaw ec. 2.93).
d = 1 - m.nu12 * m.nu21;
Q = [m.E1/d, m.nu12*m.E2/d, 0; m.nu12*m.E2/d, m.E2/d, 0; 0, 0, m.G12];
end
