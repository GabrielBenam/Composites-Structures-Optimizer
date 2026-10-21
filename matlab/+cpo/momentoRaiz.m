function M = momentoRaiz(b, semi_mm)
%MOMENTORAIZ Momento flector en la raíz b*a^2/3 [N*mm].
M = b .* semi_mm.^2 ./ 3;
end
