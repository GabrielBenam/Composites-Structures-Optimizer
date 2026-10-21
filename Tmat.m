function T = Tmat(theta)
%TMAT Transformación de esfuerzos globales a locales, theta en grados (Kaw ec. 2.94).
c = cosd(theta); s = sind(theta);
T = [c^2, s^2, 2*s*c; s^2, c^2, -2*s*c; -s*c, s*c, c^2 - s^2];
end
