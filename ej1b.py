import numpy as np
import matplotlib.pyplot as plt
from percolar import Percolacion as perc

# Punto b)
# Calcula la probabilidad de aparición del cluster percolante F(p) dp

# Número de realizaciones
N = 200
# prob inicial y final
p1 = 0.5
p2 = 1.0
# Subdivisiones
puntos = 200
# Tamaños de las redes utilizadas
Ls = np.array([4, 16, 32, 64, 128, 256, 512, 1024])
# Probabilidades estudiadas
probs = np.linspace(p1, p2, puntos)
# Veces que percola / realizaciones
ps = list()
# Fuerzas de percolacion / realizaciones
fps = list()
fpps = list()

# Lista de redes
redes2 = list()
for L in Ls:
    # Crea la instancia de la red para el tamaño correspondiente de la lista.
    # Al hacer esto se recuperan los resultados guardados.
    redes2.append(perc(L))
    ps.append(np.zeros(puntos))
    fps.append(np.zeros(puntos))
    fpps.append(np.zeros(puntos))

for i, red in enumerate(redes2):
    for j, prob in enumerate(probs):
        red.prob = prob
        if red.N < N:
            restantes = int(N - red.N)
            red.iterar_prob_fija(N=restantes, n_threads=8)
        ps[i][j] = red.p
        fps[i][j] = red.spt
        fpps[i][j] = red.fppt

    kargs = {'xlabel': '$p$ (prob. nodo ocupado)',
             'ylabel': 'Probabilidad',
             'xscale': 'linear',
             'yscale': 'linear',
             'axisbg': 'w',
             'title': 'Red de tamaño ' + str(Ls[i]) + 'x' + str(Ls[i])}

    fig = plt.figure()
    ax = fig.add_subplot(111, **kargs)
    ax.plot(probs, ps[i], 'r', label='$F(p)$ Prob. aparición c. percolante')
    ax.plot(probs, fps[i], 'b', label='$P(p)$ (Fuerza del c. percolante)')
    ax.plot(probs, fpps[i], 'g', label='$P(p)/p$')
    ax.axhline(0.5)
    ax.legend(loc='lower right')

plt.show()