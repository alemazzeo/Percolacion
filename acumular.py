import time
import numpy as np
from percolar import Percolacion as perc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-info', action='store_true', default=False)
parser.add_argument('-barrido', action='store_true', default=False)
parser.add_argument('-biseccion', action='store_true', default=False)
parser.add_argument('-N', type=int, default=80)
parser.add_argument('-threads', type=int, default=8)
parser.add_argument('-i', type=float, default=0.0)
parser.add_argument('-f', type=float, default=1.0)
parser.add_argument('-p', type=float, default=0.01)
parser.add_argument('-lmin', type=int, default=3)
parser.add_argument('-lmax', type=int, default=8)
parser.add_argument('-lpaso', type=int, default=0)
params = parser.parse_args()

# Origen de los datos
ruta = './datos/'
# Número de realizaciones
N = params.N
# Número de hilos
threads = params.threads
# prob inicial y final
p1 = params.i
p2 = params.f
paso = params.p
lmin = params.lmin
lmax = params.lmax
lpaso = params.lpaso
# Tamaños de las redes utilizadas
if lpaso==0:
    Ls = 2**np.arange(lmin,lmax+1)
elif lpaso>0:
    Ls = np.arange(lmin, lmax, lpaso)
# Probabilidades estudiadas
probs = np.arange(p1, p2, paso)

# Lista de redes
redes = list()
for i, L in enumerate(Ls):
    # Crea la instancia de la red para el tamaño correspondiente de la lista.
    # Al hacer esto se recuperan los resultados guardados.
    redes.append(perc(L, ruta=ruta))

if params.info:
    for i, red in enumerate(redes):
        red.info_pc()

if params.barrido:
    print('\nBarrido de probabilidades\n')
    t_inicial = time.time()
    t = np.zeros(len(Ls))
    for i, red in enumerate(redes):
        for j, prob in enumerate(probs):
            red.prob = prob
            if red.N < N:
                restantes = int(N - red.N)
                red.iterar_prob_fija(N=restantes, n_threads=threads)
            print(' L: ' + str(Ls[i]) + ' - p: ' + str(prob) +
                  ' '*10, end='\r')

        print('L: ' + str(Ls[i]) + ' - ' +
              str((time.time() - t_inicial) / 60) + ' '*10)

if params.biseccion:
    print('\nMétodo de bisección\n')
    for i, red in enumerate(redes):
        # Modifico la profundidad de búsqueda para no exceder el número de nodos
        if Ls[i]**0.5 < 16:
            red._profundidad = int(Ls[i]**0.5)
        # Verifica si el estado actual de la red cumple el número de iteraciones
        # Tiene en cuenta las iteraciones recuperadas
        if red.M < N:
            restantes = int(N - red.M)
            if restantes > 50:
                fraccion = restantes // 50
                ultimos = restantes - fraccion*49
                # Itera hasta alcanzar el objetivo (iteraciones restantes)
                # utilizando múltiples hilos (n_threads)
                for i in range(49):
                    print('*'*(i+1) + '-'*(50-i), end='\r')

                    red.iterar_buscar_pc(N=fraccion, n_threads=threads)
            else:
                ultimos = restantes

            print(' '*50, end='\r')
            red.iterar_buscar_pc(N=ultimos, n_threads=threads)
            red.iterar_buscar_pc(N=int(N - red.M), n_threads=threads)
            red.info_pc('Se añadieron ' + str(restantes) +
                        ' nuevas iteraciones a la red.')
        else:
            red.info_pc('Sin modificaciones.')
