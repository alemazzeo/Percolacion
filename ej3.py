import numpy as np
import matplotlib.pyplot as plt
from percolar import Percolacion as perc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-N', type=float, default=1000)
parser.add_argument('-i', type=float, default=0.6)
parser.add_argument('-f', type=float, default=0.7)
parser.add_argument('-p', type=float, default=0.05)
parser.add_argument('-lmin', type=int, default=4)
parser.add_argument('-lmax', type=int, default=100)
parser.add_argument('-tau', type=float, default=2.054945055)
parser.add_argument('-q', type=float, default=400)
parser.add_argument('-pc', type=float, default=0.5927)
params = parser.parse_args()

# Número de realizaciones
N = 27000
# prob inicial y final
p1 = params.i
p2 = params.f
paso = params.p
# Tamaños de las redes utilizadas
Ls = np.arange(4, 100, 1)
# Probabilidades estudiadas
probs = np.arange(p1, p2, paso)
puntos = len(probs)
mascara = list()
# Densidad del cluster percolante
snps = list()
fps = list()
fpps = list()

# Lista de redes
redes = list()
for L in Ls:
    # Crea la instancia de la red para el tamaño correspondiente de la lista.
    # Al hacer esto se recuperan los resultados guardados.
    redes.append(perc(L, ruta='./datos/dfractal/'))
    mascara.append(np.zeros(puntos, dtype=bool))
    snps.append(np.zeros(puntos))
    fps.append(np.zeros(puntos))
    fpps.append(np.zeros(puntos))

for i, red in enumerate(redes):
    for j, prob in enumerate(probs):
        red.prob = prob
        if red.N < N:
            restantes = int(N - red.N)
            red.iterar_prob_fija(N=restantes, n_threads=8)
        snps[i][j] = red.snp
        fps[i][j] = red.spt
        fpps[i][j] = red.fppt

# Figura: Comportamiento de

kargs = {'xlabel': '$L$ (tamaño de la red)',
         'ylabel': r'$\rho(L)$',
         'axisbg': 'w',
         'title': 'Dimensión fractal'}

fig = plt.figure()
ax = fig.add_subplot(111, **kargs)

for j, prob in enumerate(probs):
    y = np.zeros(len(Ls))
    for i, L in enumerate(Ls):
        y[i] = fps[i][j]
    ax.loglog(Ls, y, 'o', label='Probabilidad ' + str(prob))
    ax.legend(loc='lower right', title='Iteraciones: ' + str(N))

plt.show()
