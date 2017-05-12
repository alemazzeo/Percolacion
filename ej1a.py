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
    figuras = list([True,True,False,True])
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
Ls = np.array([4,8,16,32,64,80,88,96,104,112,120,128,136,144,152,160,192,224,256,512,1024])
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
    plt.plot(logx, a*logx+b, 'k',
               label=r'$\nu = ' + str(round(-1/a,3)) + '$')

    plt.title(r'Dispersión para $\langle p_c \rangle_L$ por biyección',
              fontsize=18)
    plt.legend(loc='best',fontsize=15)
    plt.grid()
    plt.tick_params(labelsize=15)
    plt.xlabel(r'$log(L)$', fontsize=18)
    plt.ylabel(r'$log(\sigma)$', fontsize=18)
    plt.show()

if figuras[2]:
    fig3 = plt.figure(figsize=(9,7))
    logx = np.log(Ls[5:17])
    logy = np.log(abs(pc[5:17] - 0.5927))
    plt.plot(logx, logy, 's', color='k',
             label='Dispersión $\sigma$')
    a, b = np.polyfit(logx, logy, 1)
    plt.plot(logx, a*logx+b,
             label=r'$\nu = ' + str(round(-1/a,3)) + '$')
    plt.plot(logx, -(3/4)*logx - 5,
             label=r'$\nu = 4/3$')

    plt.title(r'$\langle p_c \rangle_L$ en función de $\sigma$',
              fontsize=18)
    plt.legend(loc='best',fontsize=15)
    plt.grid()
    plt.tick_params(labelsize=15)
    plt.xlabel(r'$\sigma$', fontsize=18)
    plt.ylabel(r'$\langle p_c \rangle_L$', fontsize=18)
    plt.show()

if figuras[3]:
    fig4 = plt.figure(figsize=(9,7))
    fig4.subplots_adjust(left=0.20)
    x = sd[4:-2]
    y = pc[4:-2]
    x0 = np.linspace(0,np.amax(x)+0.001)

    a, b = np.polyfit(x, y, 1)
    plt.plot(x, y, 's', color='k', label='Dispersión $\sigma$')
    chi2 = np.sum((y - (a*x+b))**2)
    pcinf = '% 10.5f ' % b
    sdinf = '% 10.5f ' % (chi2**0.5)
    etiqueta = '$p_c(\infty)=' + pcinf + '\pm '+ sdinf + '$'
    plt.plot(x0, a*x0 + b, '--', color='0.3',label=etiqueta)
    plt.title(r'$\langle p_c \rangle_L$ en función de $\sigma$',
              fontsize=18)
    plt.legend(loc='best',fontsize=15)
    plt.grid()
    plt.tick_params(labelsize=15)
    plt.xlabel(r'$\sigma$', fontsize=18)
    plt.ylabel(r'$\langle p_c \rangle_L$', fontsize=18)
    plt.show()
