import numpy as np
import matplotlib.pyplot as plt
from percolar import Percolacion as perc

# Punto a)
# Determinar pc buscando la probabilidad que hace percolar la red y
# promediando sobre diferentes realizaciones (semillas)

# Número de realizaciones
M = 2000
# Profundidad: veces que se divide el intervalo de busqueda
prof = 16
# Tamaños de las redes utilizadas
Ls = np.array([4, 8, 16, 32, 64, 96, 128, 256, 512, 1024])
# Arrays para valores de pc obtenidos y correspondientes desviaciones
pc = np.zeros(len(Ls), dtype=float)
sd = np.zeros(len(Ls), dtype=float)
# Lista de redes
redes = list()
for L in Ls:
    # Crea la instancia de la red para el tamaño correspondiente de la lista.
    # Al hacer esto se recuperan los resultados guardados.
    redes.append(perc(L))

for i, red in enumerate(redes):
    # Verifica si el estado actual de la red cumple el número de iteraciones.
    # Tiene en cuenta las iteraciones recuperadas.
    if red.M < M:
        restantes = int(M - red.M)
        # Itera hasta alcanzar el objetivo (iteraciones restantes)
        # utilizando múltiples hilos (n_threads).
        red.iterar_buscar_pc(N=restantes, n_threads=8)
        red.info_pc('Se añadieron ' + str(restantes) +
                       ' nuevas iteraciones a la red.')
    else:
        # Si se tienen mas iter. que las requeridas sólo informa resultados.
        red.info_pc()

    # Carga los datos para el gráfico pc(L) con barras de error.
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