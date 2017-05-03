import numpy as np
import matplotlib.pyplot as plt
from percolar import Percolacion as perc

# Detalle del punto b)
# Determina pc ajustando la probabilidad hasta que el promedio de las veces
# que percola sea 0.5 +/- precisión (previamente elegida)

# Número de realizaciones
N = 1000
# Precisión (Distancia aceptada a p=0.5)
precision = 1e-5
# Tamaños de las redes utilizadas
Ls = np.array([4, 8, 16, 32, 64, 128, 256, 512, 1024])
# Lista de pc
pc = list()
# Lista de sd
sd = list()
# Lista de resultados
probs = list()
ps = list()
# Lista de redes
redes3 = list()

for L in Ls:
    redes3.append(perc(L))
    probs.append(list())
    ps.append(list())

for i, red in enumerate(redes3):
    # Setea la red en la probabilidad de los extremos del intervalo
    borde = [0.5, 0.8]
    probabilidad = (borde[1] + borde[0]) / 2
    red.prob = probabilidad

    #Tiene en cuenta las iteraciones realizadas para el dado L y prob
    if red.N < N:
        restantes = int(N - red.N)
        red.iterar_prob_fija(N=restantes, n_threads=8)

    while abs(red.p - 0.5) > precision:
        if red.p >= 0.5:
            borde[1] = probabilidad
        else:
            borde[0] = probabilidad

        probabilidad = (borde[1] + borde[0]) / 2
        if (red.prob != probabilidad):
            red.prob = probabilidad
        else:
            break

        if red.N < N:
            restantes = int(N - red.N)
            red.iterar_prob_fija(N=restantes, n_threads=8)

        probs[i].append(probabilidad)
        ps[i].append(red.p)

    desviacion = abs((probs[i][-3]-probs[i][-2])/2)
    valor_pc = probs[i][-1]

    sd.append(desviacion)
    pc.append(valor_pc)

    kargs = {'xlim': (valor_pc - 10 * desviacion, valor_pc + 10 * desviacion),
             'ylim': (0.5 - 10 * precision, 0.5 + 10 * precision),
             'xlabel': '$p$',
             'ylabel': '$F(p)\,dp$',
             'xscale': 'linear',
             'yscale': 'linear',
             'axisbg': 'w',
             'title': 'Red de tamaño ' + str(Ls[i]) + 'x' + str(Ls[i])}

    fig = plt.figure()
    ax = fig.add_subplot(111, **kargs)
    ax.plot(probs[i], ps[i], 'o', label='$F(p)\,dp$')
    ax.axhline(0.5 + precision)
    ax.axhline(0.5 - precision)
    ax.legend(loc='upper left')

fig = plt.figure()
kargs = {'xlabel': '$L$',
         'ylabel': '$p_c$',
         'xscale': 'linear',
         'yscale': 'linear',
         'axisbg': 'w',
         'title': 'Obtención de $p_c$ - Método alternativo'}
ax = fig.add_subplot(111, **kargs)
ax.errorbar(Ls, pc, yerr=sd, fmt='--s', label='$p_c(L)$')
ax.legend(loc='lower right')

fig = plt.figure()
kargs = {'xlabel': '$L$',
         'ylabel': '$\sigma$',
         'xscale': 'linear',
         'yscale': 'linear',
         'axisbg': 'w',
         'title': 'Dispersión para $p_c(L)$ - Método alternativo'}
ax = fig.add_subplot(111, **kargs)
ax.plot(Ls, sd, '--o', label='Dispersión $\sigma$')
ax.legend(loc='upper right')

plt.show()
