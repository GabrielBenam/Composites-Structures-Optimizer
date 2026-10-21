function q = qEliptica(x_mm, b, semi_mm)
%QELIPTICA Carga por unidad de envergadura q(x) [N/mm].
q = b .* sqrt(max(1 - (x_mm ./ semi_mm).^2, 0));
end
