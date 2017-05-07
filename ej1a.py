import numpy as np
import matplotlib.pyplot as plt
from percolar import Percolacion as perc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-info', action='store_true', default=False)
parser.add_argument('-lmin', type=int, default=4)
parser.add_argument('-lmax', type=int, default=10)
params = parser.parse_args()

# Punto a)
# Determinar pc buscando la probabilidad que hace percolar la red y
# promediando sobre diferentes realizaciones (semillas)

# Red mas pequeña y mas grande en potencias de 2
lmin = params.lmin
lmax = params.lmax
# Origen de los datos
ruta_datos = './datos'
# Tamaños de las redes utilizadas
Ls = 2**np.arange(lmin, lmax+1)
# Arrays para valores de pc obtenidos y correspondientes desviaciones
pc = np.zeros(len(Ls), dtype=float)
sd = np.zeros(len(Ls), dtype=float)
# Lista de redes
redes = list()
for i, L in enumerate(Ls):
    # Crea la instancia de la red para el tamaño correspondiente de la lista
    # Al hacer esto se recuperan los resultados guardados
    redes.append(perc(L), ruta=ruta_datos)

for i, red in enumerate(redes):
    # Muestra informacion de las redes si fue pedida
    if params.info:
        red.info_pc()
    # Carga los datos para el gráfico pc(L) con barras de error
    pc[i] = red.pc
    sd[i] = red.sd

fig = plt.figure()
kargs = {'xlabel': '$L$',
         'ylabel': '$p_c$',
         'xscale': 'linear',
         'yscale': 'linear',
         'axisbg': 'w',
         'title': 'Obtención de $P_c(L)$ Método 1'}
ax1 = fig.add_subplot(111, **kargs)
ax1.errorbar(Ls, pc, yerr=sd, fmt='--s', label='$<p_c>$')
ax1.legend(loc='lower right')

fig = plt.figure()
kargs = {'xlabel': '$L$',
         'ylabel': '$p_c$',
         'xscale': 'linear',
         'yscale': 'linear',
         'axisbg': 'w',
         'title': 'Dispersión para $p_c(L)$ - Método 1'}
ax2 = fig.add_subplot(111, **kargs)
ax2.plot(Ls, sd, '--s', label='Dispersión $\sigma$')
ax2.legend(loc='upper right')

plt.show()
