function S = Slocal(m)
%SLOCAL Flexibilidad reducida [S] de la lámina (Kaw ec. 2.92).
S = [1/m.E1, -m.nu12/m.E1, 0; -m.nu12/m.E1, 1/m.E2, 0; 0, 0, 1/m.G12];
end
