function b = bEliptica(masa_kg, g, n, semi_mm)
%BELIPTICA Carga en la raíz q(0) [N/mm] tal que pi*a*b/4 = m*g*n/2.
b = 2 .* masa_kg .* g .* n ./ (pi .* semi_mm);
end
