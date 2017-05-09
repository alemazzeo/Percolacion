import numpy as np
import matplotlib.pyplot as plt
from percolar import Percolacion as perc
from scipy import stats

# Punto 5
# Halla el coeficiente gamma utilizando los eps que maximizan ns

# Número de realizaciones
N = 8000
# Tamaños de las redes utilizadas
Ls = np.array([16, 32, 64, 128, 256, 512, 1024])
# Probabilidades estudiadas
p1 = 0.0
p2 = 1.0
paso = 0.01
probs = np.arange(p1, p2, paso)
puntos = len(probs)
# Menor y mayor fragmento considerado
smin = 1
smax = 15
st = smax - smin
# Lista de numero de fragmentos de tamaño s
# nss[i][j][k] corresponde a nss[L][prob][s]
nss = list()

# Lista de redes
redes = list()
for i, L in enumerate(Ls):
    # Crea la instancia de la red para el tamaño correspondiente de la lista.
    # Al hacer esto se recuperan los resultados guardados.
    redes.append(perc(L))
    nss.append(np.zeros((puntos, st)))

for i, red in enumerate(redes):
    for j, prob in enumerate(probs):
        red.prob = prob
        if red.N < N:
            restantes = int(N - red.N)
            red.iterar_prob_fija(N=restantes, n_threads=8)
        nss[i][j] = red.ns[smin:smax]

for i, red in enumerate(redes):
    arg_pmax = np.argmax(nss[i],axis=0)
    pmax = probs[arg_pmax]

    x = np.log(np.arange(smin,smax,1))
    y = np.log(abs(pmax-0.5927))

    plt.plot(x, y)
    a, b = stats.linregress(x,y)[0:2]
    plt.plot(x, a*x + b)

plt.show()
print(a)
