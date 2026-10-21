function r = fase0()
%FASE0 Reproducción de la tesis y línea base corregida (equivalente a cpo.fase0 en Python).
av = cpo.leerJSON(fullfile('aeronave', 'cessna162.json'));
m = av.mtow_kg; g = av.g; a = av.semi_envergadura_mm; k = av.factor_carga_larguero_tesis;
r.n = [2.5 3.8 6.0];
r.b = cpo.bEliptica(m, g, r.n, a);
r.momentoRaiz_Nm = cpo.momentoRaiz(r.b, a) / 1000;
r.nImplicitoAnsys = cpo.nDesdeB(av.b_usado_en_ansys_N_mm, m, g, a);
r.reaccionEsperada_N = k * cpo.sustentacionSemiala(cpo.bEliptica(m, g, [2.5 3.8], a), a);
r.anchos_mm = [30 50 75 100];
r.fuerzaAplicada_N = cpo.fuerzaAplicadaPorPresion(av.b_usado_en_ansys_N_mm, a, k, av.cuerda_mm, r.anchos_mm);
c = av.costilla;
r.R2_N = cpo.r2Tesis(av.b_usado_en_ansys_N_mm * av.cuerda_mm, c.dist_sustentacion_a_larguero_mm, ...
    c.peso_costilla_N, c.dist_cg_costilla_mm, sum(c.dist_larguero_a_larguero_mm));
r.ahorroNiu = cpo.ahorroNiu(av.pesos_viga_kg.aluminio_zicral, av.pesos_viga_kg.carbono_hm, av.niu_usd_por_kg);

T = cpo.leerTabla(fullfile('tesis', 'tabla18_propiedades.csv'));
r.materiales = T.filas; 
[~, P] = cpo.leerCSV(fullfile(cpo.raiz(), 'data', 'tesis', 'pesos_propiedades.csv'));
metaP = jsondecode(fileread(fullfile(cpo.raiz(), 'data', 'tesis', 'pesos_propiedades.meta.json')));
ex = metaP.pesos_reproduccion_exacta_por_columna_tabla18;
nombres = fieldnames(ex); valores = cellfun(@(f) ex.(f), nombres);
r.pmTesis = cpo.puntajeMaterial(T.valores, T.columnas, nombres, valores);

imp = str2double(P(:, 2)); correcta = P(:, 3);
usa = ~cellfun(@isempty, correcta);
r.faltantes = P(~usa, 1);
wAl = imp(usa) / sum(imp(usa));
r.pmAlineado = cpo.puntajeMaterial(T.valores, T.columnas, correcta(usa), wAl);

pub = cpo.leerTabla(fullfile('tesis', 'publicado_tabla19.csv'));
r.tabla19DifMax = max(abs(r.pmTesis - pub.valores(:, 1)));

C = cpo.leerTabla(fullfile('tesis', 'costos_seer_tabla7.csv'));
r.procesos = C.columnas;
[~, PP] = cpo.leerCSV(fullfile(cpo.raiz(), 'data', 'tesis', 'puntaje_procesos_tabla21.csv'));
pp = str2double(PP(:, 2));
[r.rcm, r.rcp] = cpo.relacionesCosto(r.pmTesis, pp, C.valores);
r.ptTesis = cpo.puntajeTotal(r.rcm, r.rcp);
[rcmA, rcpA] = cpo.relacionesCosto(r.pmAlineado, pp, C.valores);
r.ptAlineado = cpo.puntajeTotal(rcmA, rcpA);
r.ptAlineadoNorm = cpo.puntajeTotal(rcmA, rcpA, true);
r.escalaRcpSobreRcm = mean(r.rcp(:)) / mean(r.rcm(:));
end
