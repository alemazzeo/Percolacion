#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 15:55:56 2017

@author: alejandro
"""
import numpy as np
import matplotlib.pyplot as plt
from percolar import Percolacion as perc

#%% Problema 1: Determinación de pc

#%% Punto a)
# Determinar pc buscando la probabilidad que hace percolar la red y
# promediando sobre diferentes realizaciones (semillas)

# Número de realizaciones
M = 8000
# Profundidad: veces que se divide el intervalo de busqueda
prof = 16
# Tamaños de las redes utilizadas
Ls = np.array([4, 8, 16, 32, 64, 96, 128, 256, 512, 1024])
# Arrays para valores de pc obtenidos y correspondientes desviaciones
pc = np.zeros(len(Ls), dtype=float)
sd = np.zeros(len(Ls), dtype=float)
# Lista de redes
redes = list()
for L in Ls:
    # Crea la instancia de la red para el tamaño correspondiente de la lista.
    # Al hacer esto se recuperan los resultados guardados.
    redes.append(perc(L))

for i, red in enumerate(redes):
    # Verifica si el estado actual de la red cumple el número de iteraciones.
    # Tiene en cuenta las iteraciones recuperadas.
    if red.M < M:
        restantes = int(M - red.M)
        # Itera hasta alcanzar el objetivo (iteraciones restantes)
        # utilizando múltiples hilos (n_threads).
        red.iterar_buscar_pc(N=restantes, n_threads=8)
        red.info_pc('Se añadieron ' + str(restantes) +
                       ' nuevas iteraciones a la red.')
    else:
        # Si se tienen mas iter. que las requeridas sólo informa resultados.
        red.info_pc()

    # Carga los datos para el gráfico pc(L) con barras de error.
    pc[i] = red.pc
    sd[i] = red.sd

fig = plt.figure()
kargs = {'xlabel': '$L$',
         'ylabel': '$p_c$',
         'xscale': 'linear',
         'yscale': 'linear',
         'axisbg': 'w',
         'title': 'Obtención de $P_c(L)$ Método 1'}
ax1 = fig.add_subplot(111, **kargs)
ax1.errorbar(Ls, pc, yerr=sd, fmt='--s', label='$<p_c>$')
ax1.legend(loc='lower right')

fig = plt.figure()
kargs = {'xlabel': '$L$',
         'ylabel': '$p_c$',
         'xscale': 'linear',
         'yscale': 'linear',
         'axisbg': 'w',
         'title': 'Dispersión para $p_c(L)$ - Método 1'}
ax2 = fig.add_subplot(111, **kargs)
ax2.plot(Ls, sd, '--s', label='Dispersión $\sigma$')
ax2.legend(loc='upper right')

#plt.show()

#%% Punto b)
# Calcula la probabilidad de aparición del cluster percolante F(p) dp

# Número de realizaciones
N = 200
# prob inicial y final
p1 = 0.5
p2 = 1.0
# Subdivisiones
puntos = 100
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

#plt.show()


#%% Detalle del punto b)
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
