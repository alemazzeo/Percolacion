import ctypes as C
import numpy as np
import matplotlib.pyplot as plt
import time
import threading
import os

class Percolacion():

    def __init__(self, L, ruta="./datos/"):

        self._L = L
        self._ruta = ruta

        self._percolar = C.CDLL('./libpercolar.so')
        self._intp = C.POINTER(C.c_int)

        self._prob = 0
        self._semilla_inicial = 1

        self._N = C.c_int(0)
        self._p_total = C.c_int(0)
        self._fp_total = C.c_int(0)
        self._ns_total = np.zeros(self._L**2, dtype=C.c_int)
        self._ns2_total = np.zeros(self._L**2, dtype=C.c_int)

        self.p = 0
        self.fp = 0
        self.ns = np.zeros(self._L**2)
        self.ns2 = np.zeros(self._L**2)

    def info(self):

        print ('Tamaño de la red: ' + str(self._L))
        print ('Semilla inicial: ' + str(self._semilla_inicial))
        print ('Probabilidad: ' + str(self._prob) + "\n")

    def _correr(self, *args):

        self._percolar.correr(*args)

    def iterar(self, N=27000, n_threads=8, info=True):

        if N<=0:
            return

        subiter = N // n_threads

        iter_actual = self._N.value
        datos = list()

        for i in range(n_threads):
            datos.append([C.c_int(0),
                          C.c_int(0),
                          C.c_int(0),
                          np.zeros(self._L**2, dtype=C.c_int),
                          np.zeros(self._L**2, dtype=C.c_int)])

        thread = list()

        if info==True:

            print ("Configurado en " + str(n_threads) + " thread/s simultaneo/s.")
            print ("Iteraciones: " + str(subiter*n_threads))
            print ("Iteraciones por thread: " + str(subiter) + "\n")
            tiempo_inicial = time.time()

        for i in range(n_threads):
            semilla = self._semilla_inicial + iter_actual + n_threads * subiter
            args = (C.c_int(self._L),
                    C.c_int(semilla),
                    C.c_float(self._prob),
                    C.c_int(subiter),
                    C.byref(datos[i][0]),
                    C.byref(datos[i][1]),
                    C.byref(datos[i][2]),
                    datos[i][3].ctypes.data_as(self._intp),
                    datos[i][4].ctypes.data_as(self._intp))

            thread.append(threading.Thread(target=self._correr, args=args))

        for t in thread:
            t.start()

        for t in thread:
            t.join()

        for i in range(n_threads):
            self._N.value = self._N.value + datos[i][0].value
            self._p_total.value = self._p_total.value + datos[i][1].value
            self._fp_total.value = self._fp_total.value + datos[i][2].value
            self._ns_total = self._ns_total + datos[i][3]
            self._ns2_total = self._ns2_total + datos[i][4]

        self._actualizar()
        self._guardar()

        if info==True:

            print ("Se añadieron " + str(subiter*n_threads) + " iteraciones.")
            print ("Cantidad de iteraciones acumuladas: " + str(self._N.value))
            print ("Tiempo transcurrido: " +
                   str(round(time.time() - tiempo_inicial,4)) + " seg\n")

    def _colormaps(self, cmap):

        cmaplist = [cmap(i) for i in range(cmap.N)]
        cmaplist[0] = (0,0,0)
        cmaplist[-1] = (1,1,1)
        return cmap.from_list('Red', cmaplist, cmap.N)

    def ver_red(self, L, prob, semilla=26572):

        red = np.zeros(L**2, dtype=C.c_int)
        s = C.c_int(semilla)

        self._percolar.llenar(red.ctypes.data_as(self._intp), C.c_int(L),
                              C.c_float(prob),
                              C.byref(s))

        self._percolar.hoshen(red.ctypes.data_as(self._intp),
                              C.c_int(L))

        percolante = self._percolar.percola(red.ctypes.data_as(self._intp),
                                            C.c_int(L))

        cmap = self._colormaps(plt.cm.rainbow)
        matriz = red.reshape(L, L)
        matriz[matriz<2] = -10
        matriz[matriz==percolante] = np.amax(matriz) * 2
        print(percolante)

        plt.matshow(matriz, cmap=cmap)
        plt.show()

    def _actualizar(self):

        self.N = self._N.value
        self.ns = self._ns_total / self.N
        self.ns2 = self._ns2_total / self.N

        self.p = self._p_total.value / self.N
        self.fp = self._fp_total.value / self.N

    def ver_resultados(self, imprimir=True):

        print ("Número de iteraciones:__" + str(self.N))
        print ("Percolación:____________" + str(self.p))
        print ("Fuerza de percolacion:__" + str(self.fp))

        plt.plot(self.ns[1:self._L//2])

        plt.show()

    def _cargar(self, prob):
        self._prob = prob
        os.makedirs(self._ruta + "/" + str(self._L), exist_ok=True)
        archivo = self._ruta + "/" + str(self._L) + "/ " + str(self._prob) + ".npy"
        if os.path.isfile(archivo):
            datos = np.load(archivo)
            self._N.value = datos[0][0]
            self._p_total.value  = datos[0][1]
            self._fp_total.value = datos[0][2]
            np.copyto(self._ns_total, datos[1][0])
            np.copyto(self._ns2_total, datos[1][1])
        else:
            self._N.value = 0
            self._p_total.value  = 0
            self._fp_total.value = 0
            np.copyto(self._ns_total, np.zeros(self._L**2, dtype=int))
            np.copyto(self._ns2_total, np.zeros(self._L**2, dtype=int))

        self.p = 0
        self.fp = 0
        self.ns = np.zeros(self._L**2)
        self.ns2 = np.zeros(self._L**2)


    def _guardar(self):
        os.makedirs(self._ruta + "/" + str(self._L), exist_ok=True)
        archivo = self._ruta + "/" + str(self._L) + "/ " + str(self._prob) + ".npy"
        datos = [[self._N.value,
                 self._p_total.value,
                 self._fp_total.value],
                 self._ns_total,
                 self._ns2_total]

        np.save(archivo, datos)

    def _set_prob(self, prob):
        self._cargar(prob)

    def _get_prob(self):
        return self.prob

    prob = property (_get_prob, _set_prob)


def buscar_pc_medio(L, precision, N=1000):
    prob = 0.5
    red_prueba = Percolacion(L)
    red_prueba.prob = prob
    denominador = 4

    red_prueba.iterar(N=N, n_threads=8, info=False)

    while (abs(red_prueba.p -0.5) > precision):
        print ("p=" + str(red_prueba.p) + ", prob=" + str(prob))
        print (red_prueba._N)
        print (red_prueba._p_total)
        if red_prueba.p <= 0.5:
            prob += 1/denominador
        else:
            prob -= 1/denominador

        red_prueba.prob = prob
        red_prueba.iterar(N=N, n_threads=8, info=False)
        denominador = denominador * 2

    red_prueba.info()
    red_prueba.ver_red(L, prob, 500)
    red_prueba.ver_resultados()
    return prob

buscar_pc_medio(128, 1e-10, N=27000)

#red = Percolacion(32)
#red.prob = 0.5927
#red.info()
#red.iterar(N=27000, n_threads=8, info=True)
#red.ver_resultados()
