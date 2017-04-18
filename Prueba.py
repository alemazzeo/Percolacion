import ctypes as C
import numpy as np
import matplotlib.pyplot as plt
import time
import threading

N = 64
prob = 0.63
semilla = 26572

class Percolacion():

    def __init__(self, N, prob, semilla):

        self.N = N
        self.prob = prob
        self.semilla = C.c_int(semilla)

        self.percolar = C.CDLL('./libpercolar.so')
        self.intp = C.POINTER(C.c_int)

        self.red = np.zeros(self.N**2, dtype=C.c_int)
        self.clase = np.zeros(self.N**2, dtype=C.c_int)

        self.percolantes = np.zeros(self.N**2, dtype=C.c_int)
        self.cant_percolantes = 0
        self.cant_tamaño = np.zeros(self.N**2, dtype=C.c_int)
        self.cant_etiqueta = np.zeros(self.N**2, dtype=C.c_int)

        self.analisis_cluster = False
        self.analisis_percolacion = False
        self.analisis_tamaños = False
        self.analisis_etiquetas = False

    def _colormaps(self, cmap, indice=0, color=(0,0,0)):

        cmaplist = [cmap(i) for i in range(cmap.N)]
        cmaplist[indice] = color
        return cmap.from_list('Red', cmaplist, cmap.N)

    def llenar(self, prob, semilla):

        self.prob = prob
        self.semilla = C.c_int(semilla)
        self.red = np.zeros(self.N**2, dtype=C.c_int)

        self.percolar.llenar(self.red.ctypes.data_as(self.intp), C.c_int(self.N),
                             C.c_float(self.prob), C.byref(self.semilla))

        self.percolar.hoshen(self.red.ctypes.data_as(self.intp), C.c_int(self.N),
                             self.clase.ctypes.data_as(self.intp))

        self.analisis_cluster = True
        self.analisis_percolacion = False
        self.analisis_tamaños = False
        self.analisis_etiquetas = False

    def id_percolantes(self):

        self.cant_percolantes = self.percolar.percola(self.red.ctypes.data_as(self.intp),
                                                      self.percolantes.ctypes.data_as(self.intp),
                                                      C.c_int(self.N))

        self.analisis_percolacion = True

        return self.cant_percolantes > 0

    def contar_etiquetas(self):

        self.percolar.hist(self.red.ctypes.data_as(self.intp),
                           self.cant_etiqueta.ctypes.data_as(self.intp),
                           C.c_int(self.N**2))

        self.analisis_percolacion = True

    def contar_tamaños(self):

        self.percolar.hist(self.cant_etiqueta.ctypes.data_as(self.intp),
                           self.cant_tamaño.ctypes.data_as(self.intp),
                           C.c_int(self.N**2))

        self.analisis_tamaños = True

    def ver_tamaños(self):

        red_auxiliar = np.copy(self.red)
        cant_etiqueta = np.copy(self.cant_etiqueta)
        cant_etiqueta[0] = - np.amax(cant_etiqueta) / 100
        cmap = self._colormaps(plt.cm.rainbow)

        self.percolar.reemplazar(red_auxiliar.ctypes.data_as(self.intp),
                                 cant_etiqueta.ctypes.data_as(self.intp),
                                 C.c_int(self.N))

        matriz = red_auxiliar.reshape(self.N, self.N)
        return plt.matshow(matriz, cmap=cmap)

    def ver_percolantes(self):

        red_auxiliar = np.copy(self.red)
        clase = np.zeros(self.N**2, dtype=C.c_int)
        percolantes = np.trim_zeros(np.copy(self.percolantes))
        for i in percolantes:
            clase[i] = 10

        clase[0] = -10

        cmap = self._colormaps(plt.cm.rainbow)

        self.percolar.reemplazar(red_auxiliar.ctypes.data_as(self.intp),
                                 clase.ctypes.data_as(self.intp),
                                 C.c_int(self.N))

        matriz = red_auxiliar.reshape(self.N, self.N)
        return plt.matshow(matriz, cmap=cmap)

    def ver_red(self):

        red_auxiliar = np.copy(self.red)
        cmap = self._colormaps(plt.cm.rainbow_r)

        matriz = red_auxiliar.reshape(self.N, self.N)
        return plt.matshow(matriz, cmap=cmap)


red = Percolacion(N, prob, semilla)
red2 = Percolacion(N, prob+0.5, semilla)

tiempo_inicial = time.time()

for i in range(27):
    for j in range(10):
        red.llenar(prob, i*1000+j)
        red2.llenar(prob, i*1000+j)
    print (str(i+1) + "000 / 27000", end="\r")

print ("Tiempo secuencial: " + str(time.time() - tiempo_inicial) + " segundos")

tiempo_inicial = time.time()

for i in range(27):
    for j in range(10):
        t1 = threading.Thread(target=red.llenar, args=(prob,i*1000+j))
        t2 = threading.Thread(target=red2.llenar, args=(prob,i*1000+j))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    print (str(i+1) + "000 / 27000", end="\r")


print ("Tiempo paralelo: " + str(time.time() - tiempo_inicial) + " segundos")

red.contar_etiquetas()
red.contar_tamaños()
red.id_percolantes()

red.ver_red()
plt.show()

#plt.plot(mired.cant_tamaño[0:100], "o")
#plt.show()

red.ver_tamaños()
plt.show()

red.ver_percolantes()
plt.show()
