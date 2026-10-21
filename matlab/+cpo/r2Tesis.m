function R2 = r2Tesis(sust_N, d_sust_mm, peso_cost_N, d_cg_mm, d_larg_mm)
%R2TESIS Reacción en el larguero secundario con la ecuación de momentos de la tesis (7.2.5).
R2 = (sust_N .* d_sust_mm + peso_cost_N .* d_cg_mm) ./ d_larg_mm;
end
