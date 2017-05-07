import numpy as np
import matplotlib.pyplot as plt
from percolar import Percolacion as perc
from scipy import stats

# Punto 5
# Halla el coeficiente gamma utilizando los eps que maximizan ns

# Número de realizaciones
N = 20000
# Tamaños de las redes utilizadas
Ls = np.array([16, 32, 64, 128, 256, 512, 1024])
Ls = np.array([128])
# Probabilidades estudiadas
p1 = 0.55
p2 = 0.65
paso = 0.001
probs = np.arange(p1, p2, paso)
# Menor y mayor fragmento considerado
smin = 1
smax = 6000
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
    nss.append(np.zeros((len(probs), st)))

for i, red in enumerate(redes):
    for j, prob in enumerate(probs):
        red.prob = prob
        if red.N < N:
            restantes = int(N - red.N)
            red.iterar_prob_fija(N=restantes, n_threads=8)
        print('L: ' + str(Ls[i]) + ' - p:' + str(prob) + ' '*10,
              end='\r')
        nss[i][j] = red.ns[smin:smax]

s = np.arange(smin,smax)

m2 = np.zeros(len(probs))

for j, prob in enumerate(probs):
    m2[j] = np.sum(nss[0][j] * (s**2))

plt.plot(probs, m2, 'o')
plt.axvline(0.5927)
plt.show()

delta = 2
gammas = np.zeros(len(probs))
epsilons = np.zeros(len(probs))
for j, prob in enumerate(probs[delta:-delta]):
    x = probs[j:j+delta*2]
    y = m2[j:j+delta*2]
    gammas[j] = stats.linregress(np.log(x), np.log(y))[0]
    epsilons[j] = probs[j+delta] - 0.5927

plt.plot(abs(epsilons), abs(gammas), 'o')
plt.show()


