function r = raiz()
%RAIZ Carpeta raíz del repositorio (dos niveles arriba de +cpo).
r = fileparts(fileparts(fileparts(mfilename('fullpath'))));
end
