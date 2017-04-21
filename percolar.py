import ctypes as C
import numpy as np
import matplotlib.pyplot as plt
import time
import threading

class Percolacion():

    def __init__(self, L, prob, semilla_inicial=26572):

        self._L = L
        self._prob = prob
        self._semilla_inicial = semilla_inicial

        self._percolar = C.CDLL('./libpercolar.so')
        self._intp = C.POINTER(C.c_int)

        self._N = C.c_int(0)
        self._p_total = C.c_int(0)
        self._fp_total = C.c_int(0)
        self._ns_total = np.zeros(self._L**2, dtype=C.c_int)
        self._nsp_total = np.zeros(self._L**2, dtype=C.c_int)

        self.N = 0
        self.p = 0
        self.fp = 0
        self.ns = np.zeros(self._L**2)
        self.nsp = np.zeros(self._L**2)

    def info(self):

        print ('Tamaño de la red: ' + str(self._L))
        print ('Semilla inicial: ' + str(self._semilla_inicial))
        print ('Probabilidad: ' + str(self._prob) + "\n")

    def _correr(self, *args):

        self._percolar.correr(*args)

    def resetear(self, prob=-1):

        if prob > 0 and prob < 1:
            self._prob = prob

        self._N = C.c_int(0)
        self._p_total = C.c_int(0)
        self._fp_total = C.c_int(0)
        self._ns_total = np.zeros(self._L**2, dtype=C.c_int)
        self._nsp_total = np.zeros(self._L**2, dtype=C.c_int)

    def iterar(self, N=27000, n_threads=8, info=True):

        subiter = N // n_threads

        args = (C.c_int(self._L),
                C.c_int(self._semilla_inicial),
                C.c_float(self._prob),
                C.c_int(subiter),
                C.byref(self._N),
                C.byref(self._p_total),
                C.byref(self._fp_total),
                self._ns_total.ctypes.data_as(self._intp),
                self._nsp_total.ctypes.data_as(self._intp))

        thread = list()

        if info==True:

            print ("Configurado en " + str(n_threads) + " thread/s simultaneo/s.")
            print ("Iteraciones: " + str(subiter*n_threads))
            print ("Iteraciones por thread: " + str(subiter) + "\n")
            tiempo_inicial = time.time()

        for i in range(n_threads):
            thread.append(threading.Thread(target=self._correr, args=args))

        for t in thread:
            t.start()

        for t in thread:
            t.join()

        self._actualizar()

        if info==True:

            print ("Se añadieron " + str(subiter*n_threads) + " iteraciones.")
            print ("Cantidad de iteraciones acumuladas: " + str(self._N.value))
            print ("Tiempo transcurrido: " + 
                   str(round(time.time() - tiempo_inicial,4)) + " seg\n")

    def _colormaps(self, cmap, indice=0, color=(0,0,0)):

        cmaplist = [cmap(i) for i in range(cmap.N)]
        cmaplist[indice] = color
        return cmap.from_list('Red', cmaplist, cmap.N)

    def ver_red(self, L, prob, semilla=26572):

        red = np.zeros(L**2, dtype=C.c_int)
        s = C.c_int(semilla)

        self._percolar.llenar(red.ctypes.data_as(self._intp), C.c_int(L),
                              C.c_float(prob), 
                              C.byref(s))

        self._percolar.hoshen(red.ctypes.data_as(self._intp), 
                              C.c_int(L))
        
        cmap = self._colormaps(plt.cm.rainbow)
        matriz = red.reshape(L, L)
        matriz[matriz<2] = -10
        plt.matshow(matriz, cmap=cmap)
        plt.show()
            
    def _actualizar(self):

        self.N = self._N.value
        self.ns = self._ns_total / self.N
        self.nsp = self._nsp_total / self.N

        self.p = self._p_total.value / self.N
        self.fp = self._fp_total.value / self.N

    def ver_resultados(self, imprimir=True):

        print ("Número de iteraciones:__" + str(self.N))
        print ("Percolación:____________" + str(self.p))
        print ("Fuerza de percolacion:__" + str(self.fp))

        plt.plot(self.ns[1:self._L//2])

        plt.show()

def buscar_pc_minimo(L, precision, N=1000):
    prob = 0.5
    red_prueba = Percolacion(L, prob)
    denominador = 4

    red_prueba.iterar(N=N, n_threads=8, info=False)

    while (1/denominador > precision):
        print ("p=" + str(red_prueba.p) + ", prob=" + str(prob))
        if red_prueba.p <= 0:
            prob += 1/denominador
        else:
            prob -= 1/denominador

        red_prueba.resetear(prob=prob)
        red_prueba.iterar(N=N, n_threads=8, info=False)
        denominador = denominador * 2

    red_prueba.info()
    red_prueba.ver_red(L, prob, 50)
    red_prueba.ver_resultados()
    return prob

def buscar_pc_medio(L, precision, N=1000):
    prob = 0.5
    red_prueba = Percolacion(L, prob)
    denominador = 4

    red_prueba.iterar(N=N, n_threads=8, info=False)

    while (abs(red_prueba.p -0.5) > precision):
        print ("p=" + str(red_prueba.p) + ", prob=" + str(prob))
        if red_prueba.p <= 0.5:
            prob += 1/denominador
        else:
            prob -= 1/denominador

        red_prueba.resetear(prob=prob)
        red_prueba.iterar(N=N, n_threads=8, info=False)
        denominador = denominador * 2

    red_prueba.info()
    red_prueba.ver_red(L, prob, 50)
    red_prueba.ver_resultados()
    return prob

buscar_pc_minimo(128, 1e-10, N=5000)
buscar_pc_medio(128, 1e-10, N=5000)

red = Percolacion(256, 0.5927)
red.info()

pruebas = (1, 2, 4, 8)
for i in pruebas:
   red.iterar(N=27000, n_threads=i, info=True)

red.ver_resultados()
