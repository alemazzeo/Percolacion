import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from percolar import Percolacion as perc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-info', action='store_true', default=False)
parser.add_argument('-lmin', type=int, default=2)
parser.add_argument('-lmax', type=int, default=10)
parser.add_argument('-fig', type=int, action='append')
params = parser.parse_args()

# Figuras a mostrar
if params.fig is None:
    figuras = list([True,True,True,True])
else:
    figuras = list([False,False,False,False])
    for figs in params.fig:
        figuras[figs-1] = True
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
    redes.append(perc(L, ruta=ruta_datos))

for i, red in enumerate(redes):
    # Muestra informacion de las redes si fue pedida
    if params.info:
        red.info_pc()
    # Carga los datos para el gráfico pc(L) con barras de error
    pc[i] = red.pc
    sd[i] = red.sd

if figuras[0]:
    fig1 = plt.figure(figsize=(9,7))

    plt.errorbar(Ls, pc, yerr=sd, fmt='--s', color = 'k',
                 capsize=3, label='$<p_c>$')

    plt.title(r'Obtención de $\langle p_c \rangle_L$ por biyección',
              fontsize=18)
    plt.legend(loc='best',fontsize=15)
    plt.grid()
    plt.tick_params(labelsize=15)
    plt.xlabel('$L$', fontsize=18)
    plt.ylabel(r'$\langle p_c \rangle_L$', fontsize=18)
    plt.show()

if figuras[1]:
    fig2 = plt.figure(figsize=(9,7))
    logx = np.log(Ls)
    logy = np.log(sd)
    plt.plot(logx, logy, 's', color='k',
             label='Dispersión $\sigma$')
    a, b = np.polyfit(logx, logy, 1)
    plt.plot(logx, a*logx+b,
               label=r'$\nu = ' + str(round(-1/a,3)) + '$')

    plt.title(r'Dispersión para $\langle p_c \rangle_L$ por biyección',
              fontsize=18)
    plt.legend(loc='best',fontsize=15)
    plt.grid()
    plt.tick_params(labelsize=15)
    plt.xlabel(r'$L$', fontsize=18)
    plt.ylabel(r'$\langle p_c \rangle_L$', fontsize=18)
    plt.show()

if figuras[2]:
    fig3 = plt.figure(figsize=(9,7))
    logx = np.log(Ls[:])
    logy = np.log(abs(pc[:] - 0.5927))
    plt.plot(logx, logy, 's', color='k',
             label='Dispersión $\sigma$')
    a, b = np.polyfit(logx, logy, 1)
    plt.plot(logx, a*logx+b,
             label=r'$\nu = ' + str(round(-1/a,3)) + '$')
    plt.plot(logx, -(3/4)*logx - 5,
             label=)

    plt.title(r'$\langle p_c \rangle_L$ en función de $\sigma$',
              fontsize=18)
    plt.legend(loc='best',fontsize=15)
    plt.grid()
    plt.tick_params(labelsize=15)
    plt.xlabel(r'$\sigma$', fontsize=18)
    plt.ylabel(r'$\langle p_c \rangle_L$', fontsize=18)
    plt.show()
