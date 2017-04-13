import ctypes as C
import numpy as np
import matplotlib.pyplot as plt

N = 64
prob = 0.63
semilla = 26572

red = np.zeros(N, dtype=C.c_int)

class Percolar():
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

        self.percolar.llenar(self.red.ctypes.data_as(self.intp), C.c_int(self.N),
                             C.c_float(self.prob), C.byref(self.semilla))

    def llenar(self, prob, semilla):
        self.prob = prob
        self.semilla = C.c_int(semilla)
        self.red = np.zeros(self.N**2, dtype=C.c_int)

        self.percolar.llenar(self.red.ctypes.data_as(self.intp), C.c_int(self.N),
                             C.c_float(self.prob), C.byref(self.semilla))

        self.percolar.hoshen(self.red.ctypes.data_as(self.intp), C.c_int(self.N),
                             self.clase.ctypes.data_as(self.intp))

    def id_percolantes(self):
        self.cant_percolantes = self.percolar.percola(self.red.ctypes.data_as(self.intp),
                                                      self.percolantes.ctypes.data_as(self.intp),
                                                      C.c_int(self.N))
        return self.cant_percolantes > 0

    def contar_etiquetas(self):
        self.percolar.hist(self.red.ctypes.data_as(self.intp),
                           self.cant_etiqueta.ctypes.data_as(self.intp),
                           C.c_int(self.N**2))

    def contar_tamaños(self):
        self.percolar.hist(self.cant_etiqueta.ctypes.data_as(self.intp),
                           self.cant_tamaño.ctypes.data_as(self.intp),
                           C.c_int(self.N**2))

    def ver_tamaños(self):

        red_auxiliar = np.copy(self.red)

        self.percolar.reemplazar(red_auxiliar.ctypes.data_as(self.intp),
                                 self.cant_etiqueta.ctypes.data_as(self.intp),
                                 C.c_int(self.N))

        matriz = red_auxiliar.reshape(self.N, self.N)
        return plt.matshow(matriz, cmap=plt.cm.hot_r)


    def ver_red(self):
        matriz = self.red.reshape(self.N, self.N)
        matriz[matriz < 2] = np.amax(matriz)
        return plt.matshow(matriz, cmap=plt.cm.hot_r)

mired = Percolar(N, prob, semilla)

for i in range(27):
    for j in range(1000):
        mired.llenar(prob, semilla+i)
    print (i+1, "/ 27", end="\r")

mired.ver_red()
plt.show()
mired.contar_etiquetas()
mired.contar_tamaños()
plt.plot(mired.cant_tamaño[0:100], "o")
plt.show()
mired.ver_tamaños()
plt.show()
