import numpy as np
import matplotlib.pyplot as plt
from percolar import Percolacion as perc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-N', type=int, default=10000)
parser.add_argument('-i', type=float, default=0.0)
parser.add_argument('-f', type=float, default=1.0)
parser.add_argument('-p', type=float, default=0.01)
parser.add_argument('-lmin', type=int, default=4)
parser.add_argument('-lmax', type=int, default=6)
parser.add_argument('-tau', type=float, default=2.054945055)
parser.add_argument('-sigma', type=float, default=0.395604396)
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
# Sigma
sigma = params.sigma
# Tau
tau = params.tau
# Pc
pc_teo = params.pc
# Menor y mayor fragmento considerado
smin = ((Ls**2) * 0.01).astype(int)
smax = ((Ls**2) * 0.12).astype(int) + 1
st = smax - smin
# Lista de numero de fragmentos de tamaño s
# nss[i][j][k] corresponde a nss[L][prob][s]
nss = list()
# Idem anterior para Pc
nss_pc = list()

# Lista de redes
redes = list()
for i, L in enumerate(Ls):
    # Crea la instancia de la red para el tamaño correspondiente de la lista.
    # Al hacer esto se recuperan los resultados guardados.
    redes.append(perc(L))
    mascara.append(np.zeros(puntos, dtype=bool))
    nss.append(np.zeros((puntos, st[i])))
    nss_pc.append(np.zeros(st[i]))

for i, red in enumerate(redes):
    for j, prob in enumerate(probs):

        red.prob = prob
        if red.N >= N:
            mascara[i][j] = True
            nss[i][j] = red.ns[smin[i]:smax[i]]
        else:
            mascara[i][j] = False

    red.prob = pc_teo
    if red.N < N:
        restantes = int(N - red.N)
        red.iterar_prob_fija(N=restantes, n_threads=8)

    nss_pc[i] = red.ns[smin[i]:smax[i]]

zs = list()
fzs = list()
for i, L in enumerate(Ls):
    zs.append(np.zeros(len(probs) * (st[i])))
    fzs.append(np.zeros(len(probs) * (st[i])))

    for j, prob in enumerate(probs):
        epsilon = (prob - pc_teo) / pc_teo

        for k, s in enumerate(np.arange(smin[i],smax[i])):
            z = (s**sigma) * epsilon
            f = nss[i][j][k] / nss_pc[i][k]

            zs[i][j*st[i]+k] = z
            fzs[i][j*st[i]+k] = f

z_stats = list()
fz_stats = list()
for i, L in enumerate(Ls):
    z_stats.append(np.zeros(len(probs)))
    fz_stats.append(np.zeros(len(probs)))

    for j, prob in enumerate(probs):
        z_stats[i][j] = np.median(zs[i][j*st[i]:(j+1)*st[i]])
        fz_stats[i][j] = np.median(fzs[i][j*st[i]:(j+1)*st[i]])

# Figuras: Colapso de datos para cada red

for i, L in enumerate(Ls):
        fig = plt.figure()
        kargs = {'xlabel': '$z$',
                 'ylabel': '$F(z)$',
                 'xscale': 'linear',
                 'yscale': 'linear',
                 'axisbg': 'w',
                 'title': 'Fúncion de scaling - Colapso de datos'}
        ax1 = fig.add_subplot(111, **kargs)
        tamaño = str(Ls[i]) + 'x' + str(Ls[i])
        probabilidad = 'p: ' + str(p1) + ' a ' + str(p2)
        muestras = str(puntos) + ' puntos'
        ax1.semilogy(zs[i], fzs[i], ',', label='$F(z)$ - ' + tamaño)
        ajuste = '$F(z)$ agrupados'
        ax1.semilogy(z_stats[i], fz_stats[i], 'r', label=ajuste)
        ax1.legend(loc='best',
                   title= probabilidad + ' - ' + muestras)
        plt.show()

# Figura: Detalle de zs

i = 0

fig = plt.figure()
kargs = {'xlabel': r'(i,j)',
         'ylabel': r'$z(\varepsilon_i,s_j)$',
         'xscale': 'linear',
         'yscale': 'linear',
         'axisbg': 'w',
         'title': 'Fúncion de scaling - Valores de z'}
ax1 = fig.add_subplot(111, **kargs)
tamaño = str(Ls[i]) + 'x' + str(Ls[i])
probabilidad = 'p: ' + str(p1) + ' a ' + str(p2)
muestras = str(puntos) + ' puntos'
ax1.plot(np.linspace(0,1,len(zs[i])), zs[i], ',',
         label='$z(\varepsilon_i,s_j)$ - ' + tamaño)
ajuste = '$z$ agrupados'
ax1.plot(np.linspace(0,1,len(z_stats[0])), z_stats[0],
         'r', label=ajuste)
ax1.legend(loc='best',
           title= probabilidad + ' - ' + muestras)
plt.show()
