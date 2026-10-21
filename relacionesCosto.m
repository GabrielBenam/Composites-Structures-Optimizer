function [rcm, rcp] = relacionesCosto(pm, pp, costos)
%RELACIONESCOSTO Ec. 9 y 10: R_c-m y R_c-p (materiales x procesos).
rcm = pm(:) ./ costos;
rcp = pp(:).' ./ costos;
end
