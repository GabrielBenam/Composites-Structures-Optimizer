function F = fuerzaAplicadaPorPresion(b, semi_mm, factor, divisor_mm, ancho_mm)
%FUERZAAPLICADAPORPRESION Fuerza total si p = factor*q/divisor se aplica en una cara de ancho dado.
F = factor .* cpo.sustentacionSemiala(b, semi_mm) .* ancho_mm ./ divisor_mm;
end
