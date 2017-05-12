import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from percolar import Percolacion as perc
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-N', type=float, default=10000)
parser.add_argument('-prob', type=float, default=0.59335)
parser.add_argument('-pc', type=float, default=0.59276)
params = parser.parse_args()

# Número de realizaciones
N = params.N
# Tamaños de las redes utilizadas
Ls = np.array([32,48,64,96,128,192,256,384,512,640,768,896,1024])
ruta = './datos/dfractal2/'
# Probabilidades estudiada
prob = params.prob
pc = params.pc
probs = np.array([pc, prob])
puntos = len(probs)
# Densidad del cluster percolante
snps = list()
fps = list()
fpps = list()

# Lista de redes
redes = list()
for L in Ls:
    # Crea la instancia de la red para el tamaño correspondiente de la lista.
    # Al hacer esto se recuperan los resultados guardados.
    redes.append(perc(L, ruta=ruta))
    snps.append(np.zeros(puntos))
    fps.append(np.zeros(puntos))
    fpps.append(np.zeros(puntos))

for i, red in enumerate(redes):
    for j, prob in enumerate(probs):
        red.prob = prob
        if red.N < N:
            restantes = int(N - red.N)
            red.iterar_prob_fija(N=restantes, n_threads=8)

        snps[i][j] = red.snp
        fps[i][j] = red.spt
        fpps[i][j] = red.fppt

# Figura: Dimensión fractal

fig1 = plt.figure(figsize=(9,7))
fig1.subplots_adjust(left=0.20)

# Probabilidad crítica

j = 0
y = np.zeros(len(Ls))

for i, L in enumerate(Ls):
    y[i] = fps[i][j]

logx = np.log(Ls[3:])
logy = np.log(y[3:])
plt.plot(logx, logy, 'ok', label='Probabilidad ' + str(probs[j]))
a, b = np.polyfit(logx, logy, 1)
chi2 = np.sum((logy - (a*logx+b))**2)
D = '% 10.3f ' % (a + 2)
#sd = '% 10.3f ' % (chi2**0.5)
etiqueta = '$D=' + D + '$'
plt.plot(logx, logx*a+b, '--k',label=etiqueta)

plt.title(r'Dimensión fractal',
          fontsize=18)
plt.legend(loc='best',fontsize=15)
plt.grid()
plt.tick_params(labelsize=15)
plt.xlabel(r'$log(L)$', fontsize=18)
plt.ylabel(r'$log(\rho)$)', fontsize=18)
plt.show()

# Probabilidad critica + corrimiento

fig2 = plt.figure(figsize=(9,7))
fig2.subplots_adjust(left=0.20)

j = 1
y = np.zeros(len(Ls))

for i, L in enumerate(Ls):
    y[i] = fps[i][j]

logx = np.log(Ls)
logy = np.log(y)
plt.plot(logx, logy, 'ok', label='Probabilidad ' + str(probs[j]))

i1 = 0
i2 = 7

a, b = np.polyfit(logx[i1:i2], logy[i1:i2], 1)
chi2 = np.sum((logy[i1:i2] - (a*logx[i1:i2]+b))**2)
D = '% 10.3f ' % a
#sd = '% 10.3f ' % (chi2**0.5)
etiqueta = '$D-d=' + D + '$'
plt.plot(logx[i1:i2], logx[i1:i2]*a+b, '--k',label=etiqueta)

i1 = 6
i2 = 13

a, b = np.polyfit(logx[i1:i2], logy[i1:i2], 1)
chi2 = np.sum((logy[i1:i2] - (a*logx[i1:i2]+b))**2)
D = '% 10.3f ' % a
#sd = '% 10.3f ' % (chi2**0.5)
etiqueta = '$D-d=' + D + '$'
plt.plot(logx[i1:i2], logx[i1:i2]*a+b, ':k', label=etiqueta)

plt.title(r'Dimensión fractal',
          fontsize=18)
plt.legend(loc='best',fontsize=15)
plt.grid()
plt.tick_params(labelsize=15)
plt.xlabel(r'$log(L)$', fontsize=18)
plt.ylabel(r'$log(\rho)$', fontsize=18)
plt.show()
