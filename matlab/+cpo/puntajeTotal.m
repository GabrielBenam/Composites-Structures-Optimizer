function pt = puntajeTotal(rcm, rcp, normalizar, pesoMaterial)
%PUNTAJETOTAL Ec. 11. normalizar=true divide cada relación entre su máximo.
if nargin < 3, normalizar = false; end
if nargin < 4, pesoMaterial = 0.5; end
if normalizar
    rcm = rcm ./ max(rcm(:));
    rcp = rcp ./ max(rcp(:));
end
pt = pesoMaterial .* rcm + (1 - pesoMaterial) .* rcp;
end
