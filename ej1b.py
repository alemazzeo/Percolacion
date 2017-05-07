import numpy as np
import matplotlib.pyplot as plt
from percolar import Percolacion as perc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-', action='store_true', default=False)
parser.add_argument('-i', type=float, default=0.0)
parser.add_argument('-f', type=float, default=1.0)
parser.add_argument('-p', type=float, default=0.01)
parser.add_argument('-lmin', type=int, default=4)
parser.add_argument('-lmax', type=int, default=10)
params = parser.parse_args()

# Punto b)
# Calcula la probabilidad de aparición del cluster percolante F(p) dp

# prob inicial y final
p1 = params.i
p2 = params.f
paso = params.p
pot = params.l
# Tamaños de las redes utilizadas
Ls = 2**np.arange(4,pot+1)
# Probabilidades estudiadas
probs = np.arange(p1, p2, paso)
puntos = len(probs)
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
redes2 = list()
for L in Ls:
    # Crea la instancia de la red para el tamaño correspondiente de la lista.
    # Al hacer esto se recuperan los resultados guardados.
    redes2.append(perc(L))
    ps.append(np.zeros(puntos))
    nps.append(np.zeros(puntos))
    fps.append(np.zeros(puntos))
    fpps.append(np.zeros(puntos))
    spts.append(np.zeros(puntos))
    spms.append(np.zeros(puntos))
    spmaxs.append(np.zeros(puntos))
    snps.append(np.zeros(puntos))
    s0s.append(np.zeros(puntos))

for i, red in enumerate(redes2):
    for j, prob in enumerate(probs):
        red.prob = prob
        ps[i][j] = red.p
        nps[i][j] = red.np
        fps[i][j] = red.spt
        fpps[i][j] = red.fppt
        spts[i][j] = red.spt
        spms[i][j] = red.spm
        spmaxs[i][j] = red.spmax
        snps[i][j] = red.snp
        s0s[i][j] = red.s0

# Figura: Probabilidades de aparición

kargs = {'xlabel': '$p$ (prob. nodo ocupado)',
         'ylabel': '$F(p)\,dp$',
         'xscale': 'linear',
         'yscale': 'linear',
         'axisbg': 'w',
         'title': 'Probabilidad de aparición del cluster percolante'}

fig = plt.figure()
ax = fig.add_subplot(111, **kargs)

for i, red in enumerate(redes2):
    tamaño = str(Ls[i]) + 'x' + str(Ls[i])
    ax.plot(probs, ps[i], label='Red de ' + tamaño)
    ax.axhline(0.5)
    ax.legend(loc='lower right', title='Iteraciones: ' + str(N))

plt.show()

# Figura: Fuerza de percolación

kargs = {'xlabel': '$p$ (prob. nodo ocupado)',
         'ylabel': r'$\frac{Nº\,nodos\,percolantes}{Nº\,nodos}$',
         'xscale': 'linear',
         'yscale': 'linear',
         'axisbg': 'w',
         'title': 'Fuerza de percolación'}

fig = plt.figure()
ax = fig.add_subplot(111, **kargs)

for i, red in enumerate(redes2):
    tamaño = str(Ls[i]) + 'x' + str(Ls[i])
    ax.plot(probs, fps[i], label='Red de ' + tamaño)
    ax.legend(loc='lower right', title='Iteraciones: ' + str(N))

plt.show()

# Figura: Fuerza de percolación / Probabilidad de ocupación

kargs = {'xlabel': '$p$ (prob. nodo ocupado)',
         'ylabel': (r'$\frac{Nº\,nodos\,percolantes}' +
                    '{Nº\,nodos\,ocupados\,no\,percolantes}$'),
         'xscale': 'linear',
         'yscale': 'linear',
         'axisbg': 'w',
         'title': 'Fuerza de percolación / Probabilidad de ocupación'}

fig = plt.figure()
ax = fig.add_subplot(111, **kargs)

for i, red in enumerate(redes2):
    tamaño = str(Ls[i]) + 'x' + str(Ls[i])
    ax.plot(probs, fpps[i], label='Red de ' + tamaño)
    ax.legend(loc='lower right', title='Iteraciones: ' + str(N))

plt.show()

# Figura: Cantidad de clusters percolantes mayor a 1

kargs = {'xlabel': '$p$ (prob. nodo ocupado)',
         'ylabel': (r'$Nº\,clusters\,percolantes\,adicionales$'),
         'xscale': 'linear',
         'yscale': 'linear',
         'axisbg': 'w',
         'title': 'Cantidad de clusters percolantes múltiples'}

fig = plt.figure()
ax = fig.add_subplot(111, **kargs)

for i, red in enumerate(redes2):
    tamaño = str(Ls[i]) + 'x' + str(Ls[i])
    ax.plot(probs, nps[i]-ps[i], label='Red de ' + tamaño)
    ax.legend(loc='lower right', title='Iteraciones: ' + str(N))

plt.show()

# Figura: Nodos ocupados

kargs = {'xlabel': '$p$ (prob. nodo ocupado)',
         'ylabel': (r'$\frac{Nº\,nodos\,no\,percolantes\,ocupados}' +
                    r'{Nº\,nodos}$'),
         'xscale': 'linear',
         'yscale': 'linear',
         'axisbg': 'w',
         'title': 'Nodos no percolantes ocupados'}

fig = plt.figure()
ax = fig.add_subplot(111, **kargs)

for i, red in enumerate(redes2):
    tamaño = str(Ls[i]) + 'x' + str(Ls[i])
    ax.plot(probs, snps[i], label='Red de ' + tamaño)
    ax.legend(loc='lower right', title='Iteraciones: ' + str(N))

plt.show()

# Figura: Derivada de nodos ocupados

kargs = {'xlabel': '$p$ (prob. nodo ocupado)',
         'ylabel': (r'$\frac{d}{dp}\,'+
                    r'\frac{Nº\,nodos\,no\,percolantes\,ocupados}' +
                    r'{Nº\,nodos}$'),
         'xscale': 'linear',
         'yscale': 'linear',
         'axisbg': 'w',
         'title': 'Derivada de nodos no percolantes ocupados'}

fig = plt.figure()
ax = fig.add_subplot(111, **kargs)

for i, red in enumerate(redes2):
    tamaño = str(Ls[i]) + 'x' + str(Ls[i])
    ax.plot(probs[0:-1], np.diff(snps[i],1), label='Red de ' + tamaño)
    ax.legend(loc='lower right', title='Iteraciones: ' + str(N))

plt.show()
