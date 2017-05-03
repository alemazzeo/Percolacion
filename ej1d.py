import numpy as np
import matplotlib.pyplot as plt
from percolar import Percolacion as perc
from scipy import stats

# Punto d)
# Calcula la probabilidad de aparición del cluster percolante F(p) dp

# Número de realizaciones
N = 10000
# prob inicial y final
p1 = 0.5
p2 = 0.6
# Subdivisiones
puntos = 10
# Tamaños de las redes utilizadas
Ls = np.array([4, 16, 32, 64, 128, 256, 512, 1024])
Ls = np.array([64, 128])
# Probabilidades estudiadas
probs = np.linspace(p1, p2, puntos)
# Valores obtenidos del ajuste chi cuadrado
chi2 = list()
# Distribuciones de fragmentos
nss = list()

# Lista de redes
redes = list()
for L in Ls:
    # Crea la instancia de la red para el tamaño correspondiente de la lista.
    # Al hacer esto se recuperan los resultados guardados.
    redes.append(perc(L))
    chi2.append(np.zeros(puntos))

for i, red in enumerate(redes):
    for j, prob in enumerate(probs):
        red.prob = prob
        if red.N < N:
            restantes = int(N - red.N)
            red.iterar_prob_fija(N=restantes, n_threads=8)
        logx = np.log(np.arange(2,50))
        logy = np.log(red.ns[3:51])
        plt.plot(logx,logy)

        #a, b = stats.linregress(logx, logy)[0:2]
        logxv = logx[:,np.newaxis]
        a = np.linalg.lstsq(logxv, logy)[0]
        plt.plot(logx, a*logx, '--')

        plt.show()
