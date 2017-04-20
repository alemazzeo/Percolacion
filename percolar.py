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

        print ('Tamaño de la red: ' + str(self._L))
        print ('Semilla inicial: ' + str(self._semilla_inicial))
        print ('Probabilidad: ' + str(self._prob) + "\n")

    def _correr(self, *args):

        self._percolar.correr(*args)

    def resetear(self):

        self._N = C.c_int(0)
        self._p_total = C.c_int(0)
        self._fp_total = C.c_int(0)
        self._ns_total = np.zeros(self._L**2, dtype=C.c_int)
        self._nsp_total = np.zeros(self._L**2, dtype=C.c_int)

    def iterar(self, N=27000, n_threads=8):

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

        print ("Configurado en " + str(n_threads) + " thread/s simultaneo/s.")
        print ("Iteraciones: " + str(subiter*n_threads))
        print ("Iteraciones por thread: " + str(subiter) + "\n")

        for i in range(n_threads):
            thread.append(threading.Thread(target=self._correr, args=args))

        for t in thread:
            t.start()

        for t in thread:
            t.join()

        print ("Se añadieron " + str(subiter*n_threads) + " iteraciones.")
        print ("Cantidad de iteraciones acumuladas: " + str(self._N.value))

    def ver_resultados(self, imprimir=True):

        N = self._N.value
        ns = self._ns_total / N
        nsp = self._nsp_total / N

        p = self._p_total.value / N
        fp = self._fp_total.value / N

        print ("Número de iteraciones:__" + str(N))
        print ("Percolación:____________" + str(p))
        print ("Fuerza de percolacion:__" + str(fp))

        plt.plot(ns[1:self._L//2])

        plt.show()

red = Percolacion(512, 0.593125)

def rendimiento(n_threads, N=27000):
    print ("Threads: " + str(n_threads))
    tiempo_inicial = time.time()
    red.iterar(N=N, n_threads=n_threads)
    print ("Tiempo transcurrido: " + str(round(time.time() - tiempo_inicial,4))
           + " segundos" + "\n")

#pruebas = (1, 2, 4, 8, 16, 32, 64)
#for i in pruebas:
#   rendimiento(i)

red.iterar(N=27000)
red.ver_resultados()
