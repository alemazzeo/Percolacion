import numpy as np
import matplotlib.pyplot as plt
from percolar import Percolacion as perc
from scipy import stats
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-N', type=int, default=5000)
parser.add_argument('-i', type=float, default=0.4)
parser.add_argument('-f', type=float, default=0.7)
parser.add_argument('-p', type=float, default=0.001)
parser.add_argument('-lmin', type=int, default=7)
parser.add_argument('-lmax', type=int, default=7)
parser.add_argument('-pc', type=float, default=0.5927)
parser.add_argument('-nsp', type=float, default=0.35)
parser.add_argument('-ventana', type=int, default=5)
params = parser.parse_args()

# Mínimo número de iteraciones aceptado para añadir el punto
N = params.N
# Fraccion ocupada por el cluster percolante
nsp = params.nsp
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
# Pc
pc = params.pc
# Lista de numero de fragmentos de tamaño s
# nss[i][j][k] corresponde a nss[L][prob][s]
nss = list()

# Lista de redes
redes = list()
for i, L in enumerate(Ls):
    # Crea la instancia de la red para el tamaño correspondiente de la lista.
    # Al hacer esto se recuperan los resultados guardados.
    redes.append(perc(L))
    mascara.append(np.zeros(puntos, dtype=bool))

for i, red in enumerate(redes):
    # Menor y mayor fragmento considerado
    smin = 1
    smax = int(nsp * (Ls[i]**2))
    st = smax - smin
    nss.append(np.zeros((len(probs), st)))
    for j, prob in enumerate(probs):
        red.prob = prob
        if red.N >= N:
            mascara[i][j] = True
            nss[i][j] = red.ns[smin:smax]
        else:
            mascara[i][j] = False

for i, L in enumerate(Ls):
    # Menor y mayor fragmento considerado
    smin = 1
    smax = int(nsp * (Ls[i]**2))
    st = smax - smin

    s = np.arange(smin,smax)

    m2 = np.zeros(len(probs))

    for j, prob in enumerate(probs):
        m2[j] = np.sum(nss[i][j] * (s**2))

    m2inv = m2[::-1]
    m2izq = m2[0:np.argmax(m2>np.amax(m2)*0.8)]
    m2der = m2inv[0:np.argmax(m2inv>np.amax(m2)*0.8)]

    probinv = probs[::-1]
    probizq = probs[0:np.argmax(m2>np.amax(m2)*0.8)]
    probder = probinv[0:np.argmax(m2inv>np.amax(m2)*0.8)]

    plt.plot(probizq, m2izq)
    plt.plot(probder, m2der)
    plt.show()
    plt.loglog(probizq, m2izq)
    plt.loglog(probder, m2der)
    plt.show()

    ventana = params.ventana

    pivotes = list()
    rectas = list()

    for j, prob in enumerate(probizq[ventana:-ventana]):
        x = np.log(probizq[j:j+ventana*2])
        y = np.log(m2izq[j:j+ventana*2])
        pivotes.append(np.log(m2izq[j]))
        rectas.append(np.polyfit(x, y, 1)[0])

    for j, prob in enumerate(probder[ventana:-ventana]):
        x = np.log(probder[j:j+ventana*2])
        y = np.log(m2der[j:j+ventana*2])
        pivotes.append(np.log(m2der[j]))
        rectas.append(abs(np.polyfit(x, y, 1)[0]))

    plt.plot(pivotes,rectas, 'o')
    plt.show()
