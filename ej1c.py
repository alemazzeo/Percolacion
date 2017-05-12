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
parser.add_argument('-i', type=float, default=0.0)
parser.add_argument('-f', type=float, default=1.0)
parser.add_argument('-p', type=float, default=0.001)
parser.add_argument('-lmin', type=int, default=4)
parser.add_argument('-lmax', type=int, default=10)
parser.add_argument('-fig', type=int, action='append')
params = parser.parse_args()

# Figuras a mostrar
if params.fig is None:
    figuras = list([True,True,True])
else:
    figuras = list([False,False,False])
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
# Valor medio
vmedio = np.zeros(len(Ls))
# Desviacion estandar
sd = np.zeros(len(Ls))
# Mediana
mediana = np.zeros(len(Ls))

# Lista de redes
redes = list()
for L in Ls:
    # Crea la instancia de la red para el tamaño correspondiente de la lista.
    # Al hacer esto se recuperan los resultados guardados.
    redes.append(perc(L))
    mascara.append(np.zeros(puntos, dtype=bool))
    ps.append(np.zeros(puntos))

for i, red in enumerate(redes):
    for j, prob in enumerate(probs):
        red.prob = prob
        if red.N >=N:
            mascara[i][j] = True
            ps[i][j] = red.p
        else:
            mascara[i][j] = False

if figuras[0] or figuras[1]:
    for i, red in enumerate(redes):
        vmedio[i] = 1 - np.trapz(ps[i][mascara[i]], probs[mascara[i]])
        sd2 = 1 - 2 * np.trapz(ps[i][mascara[i]]*probs[mascara[i]], probs[mascara[i]])
        sd[i] = sd2 - vmedio[i]**2

if figuras[0]:

    fig1 = plt.figure(figsize=(9,7))
    fig1.subplots_adjust(left=0.15)

    plt.errorbar(Ls, vmedio, yerr=sd, fmt='--s', color = 'k',
                 label='$<p_c>$')

    plt.title(r'Obtención de $\langle p_c \rangle_L$ mediante $F(p) dp$',
              fontsize=18)
    plt.legend(loc='best',fontsize=15)
    plt.grid()
    plt.tick_params(labelsize=15)
    plt.xlabel('$L$', fontsize=18)
    plt.ylabel(r'$\langle p_c \rangle_L = 1-\int F(p)\,dP$', fontsize=18)
    plt.show()

if figuras[1]:

    fig2 = plt.figure(figsize=(9,7))

    plt.plot(Ls, vmedio,'s', color = 'k', label='$<p_c>$')

    plt.title(r'Dispersión de $\langle p_c \rangle_L$',
              fontsize=18)
    plt.legend(loc='best',fontsize=15)
    plt.grid()
    plt.tick_params(labelsize=15)
    plt.xlabel('$L$', fontsize=18)
    plt.ylabel(r'$1-2\,\int p\,F(p)\,dP$', fontsize=18)
    plt.show()

if figuras[2]:
    for i, red in enumerate(redes):
        mediana[i] = (probs[mascara[i]])[np.argmin(abs(ps[i][mascara[i]]-0.5))]
    print('Mediana: ' + str(np.average(mediana)))
    print('Dispersión: ' + str((np.average(mediana**2)-np.average(mediana)**2)**0.5))
