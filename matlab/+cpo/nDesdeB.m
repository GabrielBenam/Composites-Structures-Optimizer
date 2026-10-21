function n = nDesdeB(b, masa_kg, g, semi_mm)
%NDESDEB Factor de carga implícito en un valor de b [N/mm].
n = b .* pi .* semi_mm ./ (2 .* masa_kg .* g);
end
