import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from percolar import Percolacion as perc
import argparse
from cycler import cycler
plt.rc('lines', linewidth=2)
plt.rc('axes', prop_cycle=(cycler('color', ['0.7','0.6','0.5',
                                            '0.4','0.3','0.2']) +
                           cycler('linestyle', ['--', '-', '--',
                                                '-', '--', '-'])))


parser = argparse.ArgumentParser()
parser.add_argument('-N', type=int, default=1000)
parser.add_argument('-i', type=float, default=0.5)
parser.add_argument('-f', type=float, default=0.8)
parser.add_argument('-p', type=float, default=0.01)
parser.add_argument('-lmin', type=int, default=5)
parser.add_argument('-lmax', type=int, default=10)
parser.add_argument('-fig', type=int, action='append')
params = parser.parse_args()

# Figuras a mostrar
if params.fig is None:
    figuras = list([True,True,True,True,True,True])
else:
    figuras = list([False,False,False,False,False,False])
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
# Veces que percola / realizaciones
ps = list()
# Cantidad de nodos percolantes / realizaciones
nps = list()
# Fuerzas de percolacion / realizaciones
fps = list()
fpps = list()
# Fracciones de percolantes, percolante medio, percolante maximo,
# no percolantes y vacios.
spts = list()
spms = list()
spmaxs = list()
snps = list()
s0s = list()

# Lista de redes
redes = list()
for L in Ls:
    # Crea la instancia de la red para el tamaño correspondiente de la lista.
    # Al hacer esto se recuperan los resultados guardados.
    redes.append(perc(L))
    mascara.append(np.zeros(puntos, dtype=bool))
    ps.append(np.zeros(puntos))
    nps.append(np.zeros(puntos))
    fps.append(np.zeros(puntos))
    fpps.append(np.zeros(puntos))
    spts.append(np.zeros(puntos))
    spms.append(np.zeros(puntos))
    spmaxs.append(np.zeros(puntos))
    snps.append(np.zeros(puntos))
    s0s.append(np.zeros(puntos))

for i, red in enumerate(redes):
    for j, prob in enumerate(probs):
        red.prob = prob
        if red.N >=N:
            mascara[i][j] = True
            ps[i][j] = red.p
            nps[i][j] = red.np
            fps[i][j] = red.spt
            fpps[i][j] = red.fppt
            spts[i][j] = red.spt
            spms[i][j] = red.spm
            spmaxs[i][j] = red.spmax
            snps[i][j] = red.snp
            s0s[i][j] = red.s0
        else:
            mascara[i][j] = False

# Figura: Probabilidades de aparición
if figuras[0]:

    fig1 = plt.figure(figsize=(9,7))

    for i, red in enumerate(redes):
        tamaño = str(Ls[i]) + 'x' + str(Ls[i])
        plt.plot(probs[mascara[i]], ps[i][mascara[i]],
                 label='Red de ' + tamaño)

    plt.title(r'Probabilidad de aparición del cluster percolante', fontsize=18)
    plt.legend(loc='lower right', fontsize=15)
    plt.grid()
    plt.tick_params(labelsize=15)
    plt.xlabel('$p$', fontsize=18)
    plt.ylabel(r'$F(p)\,dp$', fontsize=18)
    plt.show()

# Figura: Fuerza de percolación
if figuras[1]:

    fig2 = plt.figure(figsize=(9,7))

    for i, red in enumerate(redes):
        tamaño = str(Ls[i]) + 'x' + str(Ls[i])
        plt.plot(probs[mascara[i]], fps[i][mascara[i]],
                 label='Red de ' + tamaño)

    plt.title(r'Fuerza de percolación $P(p)$', fontsize=18)
    plt.legend(loc='lower right', fontsize=15)
    plt.grid()
    plt.tick_params(labelsize=15)
    plt.xlabel(r'$p$', fontsize=18)
    plt.ylabel(r'$\frac{Nº\,nodos\,percolantes}{Nº\,nodos}$', fontsize=18)
    plt.show()

# Figura: Fuerza de percolación / Probabilidad de ocupación
if figuras[2]:

    fig3 = plt.figure(figsize=(9,7))

    for i, red in enumerate(redes):
        tamaño = str(Ls[i]) + 'x' + str(Ls[i])
        plt.plot(probs[mascara[i]], fpps[i][mascara[i]],
                 label='Red de ' + tamaño)

    plt.title(r'Fuerza de percolación $P(p)/p$', fontsize=18)
    plt.legend(loc='lower right', fontsize=15)
    plt.grid()
    plt.tick_params(labelsize=15)
    plt.xlabel(r'$p$', fontsize=18)
    plt.ylabel((r'$\frac{Nº\,nodos\,percolantes}' +
                r'{Nº\,nodos\,ocupados\,no\,percolantes}$'), fontsize=18)
    plt.show()

# Figura: Cantidad de clusters percolantes mayor a 1
if figuras[3]:

    fig4 = plt.figure(figsize=(9,7))

    for i, red in enumerate(redes):
        tamaño = str(Ls[i]) + 'x' + str(Ls[i])
        plt.plot(probs[mascara[i]], (nps[i]-ps[i])[mascara[i]],
                 label='Red de ' + tamaño)

    plt.title(r'Cantidad de clusters percolantes múltiples', fontsize=18)
    plt.legend(loc='lower right', fontsize=15)
    plt.grid()
    plt.tick_params(labelsize=15)
    plt.xlabel(r'$p$', fontsize=18)
    plt.ylabel(r'$Nº\,clusters\,perc.\,adicionales$', fontsize=13)
    plt.show()

# Figura: Nodos ocupados
if figuras[4]:

    fig5 = plt.figure(figsize=(9,7))

    for i, red in enumerate(redes):
        tamaño = str(Ls[i]) + 'x' + str(Ls[i])
        plt.plot(probs[mascara[i]], snps[i][mascara[i]],
                 label='Red de ' + tamaño)

    plt.title(r'Nodos no percolantes ocupados', fontsize=18)
    plt.legend(loc='lower right', fontsize=15)
    plt.grid()
    plt.tick_params(labelsize=15)
    plt.xlabel(r'$p$', fontsize=18)
    plt.ylabel(r'$\frac{Nº\,nodos\,no\,percolantes\,ocupados}' +
               r'{Nº\,nodos}$', fontsize=18)
    plt.show()

# Figura: Derivada de nodos ocupados
if figuras[5]:

    fig5 = plt.figure(figsize=(9,7))
    fig5.subplots_adjust(left=0.15)

    for i, red in enumerate(redes):
        tamaño = str(Ls[i]) + 'x' + str(Ls[i])
        plt.plot(probs[mascara[i]][0:-1],
                 np.diff(snps[i][mascara[i]],1),
                 label='Red de ' + tamaño)

    plt.title(r'Derivada de nodos no percolantes ocupados', fontsize=18)
    plt.legend(loc='lower right', fontsize=15)
    plt.grid()
    plt.tick_params(labelsize=15)
    plt.xlabel(r'$p$', fontsize=18)
    plt.ylabel(r'$\frac{d}{dp}\,\left('+
               r'\frac{Nº\,nodos\,no\,percolantes\,ocupados}' +
               r'{Nº\,nodos}\right)$', fontsize=18)
    plt.show()
