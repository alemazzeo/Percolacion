import numpy as np
import matplotlib.pyplot as plt
from percolar import Percolacion as perc
from scipy import stats
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-N', type=float, default=1000)
parser.add_argument('-i', type=float, default=0.5)
parser.add_argument('-f', type=float, default=0.7)
parser.add_argument('-p', type=float, default=0.001)
parser.add_argument('-lmin', type=int, default=6)
parser.add_argument('-lmax', type=int, default=7)
parser.add_argument('-tau', type=float, default=2.054945055)
parser.add_argument('-q', type=float, default=400)
parser.add_argument('-pc', type=float, default=0.5927)
params = parser.parse_args()

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
# Valor teórico de Tau
tau = params.tau
# Valor teórico de pc
pc_teo = params.pc
# Valor estimado de q0
q0 = params.q
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
    mascara.append(np.zeros(puntos, dtype=bool))
    chi2.append(np.zeros(puntos))

for i, red in enumerate(redes):
    si = 50
    sf = int((red._L**2) * 1e-1)
    s = np.arange(si,sf)

    for j, prob in enumerate(probs):

        red.prob = prob
        if red.N > N:
            mascara[i][j] = True
            ns = red.ns[si+1:sf+1]
            x = s
            y = ns/q0
            positivos = y > 0

            logx = np.log(x[positivos])
            logy = np.log(y[positivos])

            chi2[i][j] = np.sum((logy + tau * logx)**2)
        else:
            mascara[i][j] = False

# Figura: Ajuste chi cuadrado

kargs = {'xlabel': '$p$ (prob. nodo ocupado)',
         'ylabel': r'$\chi^2$',
         'xscale': 'linear',
         'yscale': 'linear',
         'axisbg': 'w',
         'title': r'Ajuste $\chi^2$ a la distribución de fragmentos'}

fig = plt.figure()
ax = fig.add_subplot(111, **kargs)

for i, red in enumerate(redes):
    tamaño = str(Ls[i]) + 'x' + str(Ls[i])
    ax.plot(probs[mascara[i]], chi2[i][mascara[i]], label='Red de ' + tamaño)
    ax.legend(loc='best', title='Iteraciones: ' + str(N))

plt.show()
