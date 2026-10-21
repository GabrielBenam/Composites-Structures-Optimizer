function s = ahorroNiu(w0, w1, usd_kg)
%AHORRONIU Ahorro por reducción de peso [USD].
s = (w0 - w1) .* usd_kg;
end
