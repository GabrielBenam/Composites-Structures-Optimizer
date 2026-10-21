function res = bloqueA()
%BLOQUEA Recalcula en MATLAB los ejemplos del Bloque A y los compara contra el libro.
%   res: struct array con campos caso, clave, calculado, libro, tol, ok.
ref = jsondecode(fileread(fullfile(cpo.raiz(), 'data', 'ejemplos', 'bloqueA_referencias.json')));
res = struct('caso', {}, 'clave', {}, 'calculado', {}, 'libro', {}, 'tol', {}, 'ok', {});
GE = cpo.cargarLamina('kaw_tabla2_1.csv', 'graphite_epoxy');
VE = cpo.cargarLamina('kaw_tabla2_1.csv', 'glass_epoxy');
ij = struct('k11',[1 1],'k12',[1 2],'k16',[1 3],'k22',[2 2],'k26',[2 3],'k66',[3 3]);

    function chk(caso, clave, calc, tol)
        if nargin < 4, tol = 0.005; end
        lib = ref.(caso).valores.(clave);
        dif = abs(calc - lib) / max(abs(lib), realmin);
        res(end+1) = struct('caso', caso, 'clave', clave, 'calculado', calc, 'libro', lib, ...
                            'tol', tol, 'ok', dif <= tol); %#ok<AGROW>
    end
    function chkMat(caso, pref, M, claves)
        for q = 1:numel(claves)
            p = ij.(['k' claves{q}]);
            chk(caso, [pref claves{q}], M(p(1), p(2)));
        end
    end

% --- Kaw 2.6
S = cpo.Slocal(GE); Q = cpo.Qlocal(GE); e = S * [2e6; -3e6; 4e6];
chk('kaw_2_6','S11',S(1,1)); chk('kaw_2_6','S12',S(1,2)); chk('kaw_2_6','S22',S(2,2)); chk('kaw_2_6','S66',S(3,3));
chk('kaw_2_6','nu21',GE.nu21); chk('kaw_2_6','Q11',Q(1,1)); chk('kaw_2_6','Q12',Q(1,2));
chk('kaw_2_6','Q22',Q(2,2)); chk('kaw_2_6','Q66',Q(3,3));
chk('kaw_2_6','e1',e(1)); chk('kaw_2_6','e2',e(2)); chk('kaw_2_6','g12',e(3));
% --- Kaw 2.7
Sb = cpo.Sbar(GE, 60); Qb = cpo.Qbar(GE, 60); sig = [2e6; -3e6; 4e6];
chkMat('kaw_2_7', 'Sb', Sb, {'11','12','16','22','26','66'});
chkMat('kaw_2_7', 'Qb', Qb, {'11','12','16','22','26','66'});
eg = Sb * sig; sl = cpo.Tmat(60) * sig;
chk('kaw_2_7','ex',eg(1)); chk('kaw_2_7','ey',eg(2)); chk('kaw_2_7','gxy',eg(3));
chk('kaw_2_7','s1',sl(1)); chk('kaw_2_7','s2',sl(2)); chk('kaw_2_7','t12',sl(3));
% --- Kaw 2.9
c = cpo.constantesAngulo(GE, 60);
for f = {'Ex','nuxy','mx','Ey','my','Gxy'}, chk('kaw_2_9', f{1}, c.(f{1})); end
% --- Kaw 2.11
I = cpo.invariantes(GE);
for q = 1:4, chk('kaw_2_11', sprintf('U%d', q), I.U(q)); chk('kaw_2_11', sprintf('V%d', q), I.V(q)); end
% --- Kaw 2.13, 2.17, 2.18, 2.19 (estado sigma = [2 -3 4] S)
s60 = cpo.Tmat(60) * [2; -3; 4];
chk('kaw_2_13','SR',cpo.srEsfuerzoMax(s60, GE));
chk('kaw_2_17','SR',cpo.srDeformacionMax(s60, GE));
chk('kaw_2_18','SR_TH',cpo.srTsaiHill(s60, GE)); chk('kaw_2_18','SR_THmod',cpo.srTsaiHill(s60, GE, true));
chk('kaw_2_19','SR_MH',cpo.srTsaiWu(s60, GE)); chk('kaw_2_19','SR_TH',cpo.srTsaiWu(s60, GE, 'tsai-hill'));
chk('kaw_2_19','SR_HOF',cpo.srTsaiWu(s60, GE, 'hoffman'));
% --- Kaw 2.14 (Tabla 2.3)
for th = [0 15 30 45 60 75 90]
    chk('kaw_2_14', sprintf('tau_pos_%d', th), cpo.srEsfuerzoMax(cpo.Tmat(th)*[0;0;1], GE));
    chk('kaw_2_14', sprintf('tau_neg_%d', th), cpo.srEsfuerzoMax(cpo.Tmat(th)*[0;0;-1], GE));
end
% --- Kaw 2.20
a = cpo.alfaGlobal(VE, 60, 'a'); b = cpo.alfaGlobal(VE, 60, 'b'); ee = a*(-100) + b*0.02;
chk('kaw_2_20','ax',a(1)); chk('kaw_2_20','ay',a(2)); chk('kaw_2_20','axy',a(3));
chk('kaw_2_20','bx',b(1)); chk('kaw_2_20','by',b(2)); chk('kaw_2_20','bxy',b(3));
chk('kaw_2_20','ex',ee(1)); chk('kaw_2_20','ey',ee(2)); chk('kaw_2_20','gxy',ee(3));
% --- Kaw 4.2 y 4.3
lam = cpo.laminado(GE, [0 30 -45], 0.005); [A, B, D] = cpo.ABD(lam);
ks = {'11','12','16','22','26','66'};
chkMat('kaw_4_2','A',A,ks); chkMat('kaw_4_2','B',B,ks); chkMat('kaw_4_2','D',D,ks);
[e0, k] = cpo.respuesta(lam, [1000;1000;0]);
nm = {'e0x','e0y','g0xy'}; for q = 1:3, chk('kaw_4_3', nm{q}, e0(q)); end
nm = {'kx','ky','kxy'};    for q = 1:3, chk('kaw_4_3', nm{q}, k(q)); end
s = cpo.estadoCapa(lam, 2, 'sup', e0, k);
chk('kaw_4_3','sx_30top',s.sig(1)); chk('kaw_4_3','sy_30top',s.sig(2)); chk('kaw_4_3','txy_30top',s.sig(3));
chk('kaw_4_3','s1_30top',s.sigLocal(1)); chk('kaw_4_3','s2_30top',s.sigLocal(2)); chk('kaw_4_3','t12_30top',s.sigLocal(3));
% --- Kaw 4.4
lam = cpo.laminado(GE, [0 90 0], 0.005); [A, ~, D] = cpo.ABD(lam); Ai = inv(A); Di = inv(D); h = lam.h;
chk('kaw_4_4','Ex',1/(h*Ai(1,1))); chk('kaw_4_4','Ey',1/(h*Ai(2,2))); chk('kaw_4_4','Gxy',1/(h*Ai(3,3)));
chk('kaw_4_4','nuxy',-Ai(1,2)/Ai(1,1)); chk('kaw_4_4','Exf',12/(h^3*Di(1,1))); chk('kaw_4_4','Eyf',12/(h^3*Di(2,2)));
chk('kaw_4_4','nuxyf',-Di(1,2)/Di(1,1));
% --- Kaw 4.5
lam = cpo.laminado(GE, [0 90], 0.005);
[e0, k] = cpo.respuesta(lam, [0;0;0], [0;0;0], -75, 0);
chk('kaw_4_5','e0x',e0(1)); chk('kaw_4_5','kx',k(1)); chk('kaw_4_5','ky',k(2));
s = cpo.estadoCapa(lam, 2, 'inf', e0, k, -75, 0);
chk('kaw_4_5','sx_bot',s.sig(1)); chk('kaw_4_5','sy_bot',s.sig(2));
% --- Kaw 4.6
lam = cpo.laminado(GE, [0 90 0], 0.005); [A, ~, ~] = cpo.ABD(lam);
NT = cpo.cargasHigrotermicas(lam, 1, 0); NC = cpo.cargasHigrotermicas(lam, 0, 1);
al = A \ NT; be = A \ NC;
chk('kaw_4_6','ax',al(1)); chk('kaw_4_6','ay',al(2)); chk('kaw_4_6','bx',be(1)); chk('kaw_4_6','by',be(2));
% --- Kaw 5.1
lam = cpo.laminado(GE, [0 60 -60], 0.005); [A, B, D] = cpo.ABD(lam);
chkMat('kaw_5_1','A',A,{'11','12','22','66'}); chkMat('kaw_5_1','B',B,ks); chkMat('kaw_5_1','D',D,ks);
% --- Gay 19.10 (tela carbono, MPa)
TC = cpo.cargarLamina('gay_tabla3_6_telas.csv', 'carbono_tela_gay');
Q0 = cpo.Qbar(TC, 0); Q45 = cpo.Qbar(TC, 45);
z1 = 0.67*Q0 + 0.33*Q45; z2 = 0.40*Q0 + 0.60*Q45;
chk('gay_19_10','z1_A11',z1(1,1)); chk('gay_19_10','z1_A12',z1(1,2)); chk('gay_19_10','z1_A66',z1(3,3));
chk('gay_19_10','z2_A11',z2(1,1)); chk('gay_19_10','z2_A12',z2(1,2)); chk('gay_19_10','z2_A66',z2(3,3));
i1 = inv(z1); i2 = inv(z2);
chk('gay_19_10','z1_Ex',1/i1(1,1)); chk('gay_19_10','z2_Ex',1/i2(1,1));
end
