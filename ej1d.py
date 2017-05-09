import numpy as np
import matplotlib.pyplot as plt
from percolar import Percolacion as perc
from scipy import stats
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-N', type=float, default=1000)
parser.add_argument('-i', type=float, default=0.56)
parser.add_argument('-f', type=float, default=0.61)
parser.add_argument('-p', type=float, default=0.001)
parser.add_argument('-lmin', type=int, default=7)
parser.add_argument('-lmax', type=int, default=7)
parser.add_argument('-tau', type=float, default=2.054945055)
parser.add_argument('-fig', type=int, action='append')
params = parser.parse_args()

# Figuras a mostrar
if params.fig is None:
    figuras = list([True,True])
else:
    figuras = list([False,False])
    for figs in params.fig:
        figuras[figs-1] = True
# Mínimo número de iteraciones aceptado para añadir el punto
N = params.N
# prob inicial y final
p1 = params.i
p2 = params.f
paso = params.p
# Red mas pequeña y mas grande en potencias de 2
lmin = params.lmin
lmax = params.lmax
# Tamaños de las redes utilizadas
Ls = 2**np.arange(lmin,lmax+1)
# Probabilidades estudiadas
probs = np.arange(p1, p2, paso)
puntos = len(probs)
mascara = list()
# Valores obtenidos del ajuste chi cuadrado
chi2 = list()
# Valores de tau
taus = list()
# Distribuciones de fragmentos
nss = list()

# Lista de redes
redes = list()
for L in Ls:
    # Crea la instancia de la red para el tamaño correspondiente de la lista.
    # Al hacer esto se recuperan los resultados guardados.
    redes.append(perc(L))
    mascara.append(np.zeros(puntos, dtype=bool))
    chi2.append(np.zeros(puntos))
    taus.append(np.zeros(puntos))

for i, red in enumerate(redes):
    si = 500
    sf = 1500
    s = np.arange(si,sf)

    for j, prob in enumerate(probs):

        red.prob = prob
        if red.N > N:
            mascara[i][j] = True
            ns = red.ns[si+1:sf+1]
            x = s
            y = ns
            positivos = y > 0

            logx = np.log(x[positivos])
            logy = np.log(y[positivos])
            #plt.plot(logx,logy)

            a, b = np.polyfit(logx, logy, 1)
            taus[i][j] = a
            chi2[i][j] = np.sum((logy - (a * logx + b))**2)
        else:
            mascara[i][j] = False

    #plt.show()

# Figura: Ajuste chi cuadrado

if figuras[0]:

    fig1 = plt.figure(figsize=(9,7))

    for i, red in enumerate(redes):
        tamaño = str(Ls[i]) + 'x' + str(Ls[i])
        plt.plot(probs[mascara[i]], chi2[i][mascara[i]],
                 'o', color='k', label='Red de ' + tamaño)

    plt.title(r'Ajuste $\chi^2$ a la distribución de fragmentos', fontsize=18)
    plt.legend(loc='best', fontsize=15)
    plt.grid()
    plt.tick_params(labelsize=15)
    plt.xlabel('$p$', fontsize=18)
    plt.ylabel(r'$\chi^2$', fontsize=18)
    plt.show()

# Figura: Taus

if figuras[1]:

    fig1 = plt.figure(figsize=(9,7))

    for i, red in enumerate(redes):
        tamaño = str(Ls[i]) + 'x' + str(Ls[i])
        plt.plot(probs[mascara[i]], taus[i][mascara[i]],
                 'o', color='k', label='Red de ' + tamaño)

    plt.title(r'Valores de $\tau$', fontsize=18)
    plt.legend(loc='best', fontsize=15)
    plt.grid()
    plt.tick_params(labelsize=15)
    plt.xlabel('$p$', fontsize=18)
    plt.ylabel(r'$\tau$', fontsize=18)
    plt.show()
