import numpy as np
import matplotlib.pyplot as plt
from percolar import Percolacion as perc


# Punto 3)
# Calcula la densidad

# Número de realizaciones
N = 27000
# prob inicial y final
p1 = 0.5627
p2 = 0.6227
# Subdivisiones
puntos = 13
# Tamaños de las redes utilizadas
Ls = np.arange(16, 368, 16)
# Probabilidades estudiadas
probs = np.linspace(p1, p2, puntos)
# Densidad del cluster percolante
snps = list()
fps = list()
fpps = list()

# Lista de redes
redes = list()
for L in Ls:
    # Crea la instancia de la red para el tamaño correspondiente de la lista.
    # Al hacer esto se recuperan los resultados guardados.
    redes.append(perc(L))
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
    ax.loglog(Ls, y, label='Probabilidad ' + str(prob))
#    ax.legend(loc='lower right', title='Iteraciones: ' + str(N))

plt.show()
