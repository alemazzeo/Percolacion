import numpy as np
import matplotlib.pyplot as plt
from percolar import Percolacion as perc

# Punto 4
# Halla la función f(z) con z = s^gamma * (p-pc(L)) / pc(L)

# Número de realizaciones
N = 20000
# sigma
sigma = 0.395604396
# Tau
tau = 2.054945055
# Pc
pc_teo = 0.5926
# prob inicial y final
p1 = 0.5
p2 = 0.7
# Subdivisiones
puntos = 100

# Tamaños de las redes utilizadas
Ls = np.array([16, 32, 64, 128, 256, 512, 1024])
Ls = np.array([64, 128])
# Probabilidades estudiadas
probs = np.linspace(p1, p2, puntos)
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
    nss.append(np.zeros((puntos, st[i])))
    nss_pc.append(np.zeros(st[i]))

for i, red in enumerate(redes):
    for j, prob in enumerate(probs):

        red.prob = prob
        if red.N < N:
            restantes = int(N - red.N)
            red.iterar_prob_fija(N=restantes, n_threads=8)

        nss[i][j] = red.ns[smin[i]:smax[i]]

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
