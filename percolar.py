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
        self._doublep = C.POINTER(C.c_double)
        self.__prob = 0
        self._semilla_inicial = 1

        self._p_total = C.c_int(0)
        self._fp_total = C.c_int(0)
        self._ns_total = np.zeros(self._L**2, dtype=C.c_int)
        self._ns2_total = np.zeros(self._L**2, dtype=C.c_int)

        self._profundidad = 16
        self._pcs = 0.0
        self._pcs2 = 0.0
        
        self.M = 0
        self.pc = 0
        self.pc2 = 0
        self.sd = 0
        self.sd2 = 0

        self.N = 0
        self.p = 0
        self.fp = 0
        self.ns = np.zeros(self._L**2)
        self.ns2 = np.zeros(self._L**2)
    
        self._cargar_pc()       

    def info_pc(self, *args):
        self._actualizar()
        print ('Tamaño de la red: ' + str(self._L))
        print ('Pc: ' + str(self.pc) + " +/- " + str(self.sd)) 
        print ('Veces iterada: ' + str(self.M))
        for mensaje in args:
            print (mensaje)
        print('\n', end='')

    def info_prob(self):
        self._actualizar()
        print ('Tamaño de la red: ' + str(self._L))
        print ('Probabilidad: ' + str(self.__prob) + '\n')
        print ('Veces iterada: ' + str(self.N))

    def _iterar_buscar_pc(self, *args):
        self._percolar.iterar_buscar_pc(*args)

    def _iterar_prob_fija(self, *args):
        self._percolar.iterar_prob_fija(*args)

    def iterar_buscar_pc(self, N=27000, n_threads=8, info=False):

        if N<=0:
            return

        subiter = N // n_threads
        iter_actual = self.M
        datos = list()

        for i in range(n_threads):
            datos.append([C.c_double(),
                          C.c_double()])

        thread = list()

        if info==True:
            print ("Configurado en " + str(n_threads) + " thread/s simultaneo/s.")
            print ("Iteraciones: " + str(subiter*n_threads))
            print ("Iteraciones por thread: " + str(subiter) + "\n")
            tiempo_inicial = time.time()

        for i in range(n_threads):
            semilla = self._semilla_inicial + iter_actual + i * subiter
            args = (C.c_int(self._L),
                    C.c_int(int(semilla)),
                    C.c_int(subiter),
                    C.c_int(self._profundidad),
                    C.byref(datos[i][0]),
                    C.byref(datos[i][1]))

            thread.append(threading.Thread(target=self._iterar_buscar_pc, args=args))

        for t in thread:
            t.start()

        for t in thread:
            t.join()

        for i in range(n_threads):
            self.M += subiter
            self._pcs = self._pcs + datos[i][0].value
            self._pcs2 = self._pcs2 + datos[i][1].value

        self._actualizar()
        self._guardar_pc()
        
        if info==True:

            print ("Se añadieron " + str(subiter*n_threads) + " iteraciones.")
            print ("Cantidad de iteraciones acumuladas: " + str(self.M))
            print ("Tiempo transcurrido: " +
                   str(round(time.time() - tiempo_inicial,4)) + " seg\n")

    def iterar_prob_fija(self, N=27000, n_threads=8, info=False):

        if N<=0:
            return

        subiter = N // n_threads
        iter_actual = self.N
        datos = list()

        for i in range(n_threads):
            datos.append([C.c_int(0),
                          C.c_int(0),
                          np.zeros(self._L**2, dtype=C.c_int)])

        thread = list()

        if info==True:

            print ("Configurado en " + str(n_threads) + " thread/s simultaneo/s.")
            print ("Iteraciones: " + str(subiter*n_threads))
            print ("Iteraciones por thread: " + str(subiter) + "\n")
            tiempo_inicial = time.time()

        for i in range(n_threads):
            semilla = self._semilla_inicial + iter_actual + i * subiter
            args = (C.c_int(self._L),
                    C.c_int(semilla),
                    C.c_double(self.__prob),
                    C.c_int(subiter),
                    C.byref(datos[i][0]),
                    C.byref(datos[i][1]),
                    datos[i][2].ctypes.data_as(self._intp))

            thread.append(threading.Thread(target=self._iterar_prob_fija, args=args))

        for t in thread:
            t.start()

        for t in thread:
            t.join()

        for i in range(n_threads):
            self.N += subiter
            self._p_total.value = self._p_total.value + datos[i][0].value
            self._fp_total.value = self._fp_total.value + datos[i][1].value
            self._ns_total = self._ns_total + datos[i][2]

        self._actualizar()
        self._guardar()

        if info==True:

            print ("Se añadieron " + str(subiter*n_threads) + " iteraciones.")
            print ("Cantidad de iteraciones acumuladas: " + str(self.N))
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
                              C.c_double(prob),
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

        if self.M > 0:
            self.pc = self._pcs / self.M
            self.pc2 = self._pcs2 / self.M
            self.sd2 = abs(self.pc2 - self.pc**2)
            self.sd = self.sd2**0.5
        if self.N > 0:
            self.ns = self._ns_total / self.N
            self.p = self._p_total.value / self.N
            self.fp = self._fp_total.value / self.N

    def ver_resultados(self, imprimir=True):

        print ("Número de iteraciones:__" + str(self.N))
        print ("Percolación:____________" + str(self.p))
        print ("Fuerza de percolacion:__" + str(self.fp))

        inicio = 1
        fin = self._L//2
        s = np.arange(inicio, fin)
        ns = self.ns[inicio:fin]
        plt.plot(s, ns, 'o')
        plt.show()

    def _cargar_pc(self):
        os.makedirs(self._ruta + "/" + str(self._L), exist_ok=True)
        archivo = self._ruta + "/" + str(self._L) + "/pc.npy"

        if os.path.isfile(archivo):
            datos = np.load(archivo)
            self.M = datos[0]
            self._pcs = datos[1]
            self._pcs2 = datos[2]

        else:
            self.M = 0
            self._pcs = np.array(0)
            self._pcs2 = np.array(0)

        self._actualizar()

    def _guardar_pc(self):
        os.makedirs(self._ruta + "/" + str(self._L), exist_ok=True)
        archivo = self._ruta + "/" + str(self._L) + "/pc.npy"
        datos = [self.M,
                 self._pcs,
                 self._pcs2]
        np.save(archivo, datos)

    def _cargar(self, prob):
        self.__prob = prob
        os.makedirs(self._ruta + "/" + str(self._L), exist_ok=True)
        archivo = self._ruta + "/" + str(self._L) + "/ " + str(self.__prob) + ".npy"

        if os.path.isfile(archivo):
            datos = np.load(archivo)
            self.N = datos[0][0]
            self._p_total.value  = datos[0][1]
            self._fp_total.value = datos[0][2]
            np.copyto(self._ns_total, datos[1])

        else:
            self.N = 0
            self._p_total.value  = 0
            self._fp_total.value = 0
            np.copyto(self._ns_total, np.zeros(self._L**2, dtype=int))

        self.p = 0
        self.fp = 0
        self.ns = np.zeros(self._L**2)
        
        self._actualizar()

    def _guardar(self):
        os.makedirs(self._ruta + "/" + str(self._L), exist_ok=True)
        archivo = self._ruta + "/" + str(self._L) + "/ " + str(self.__prob) + ".npy"

        datos = [[self.N,
                 self._p_total.value,
                 self._fp_total.value],
                 self._ns_total]

        np.save(archivo, datos)

    def _set_prob(self, prob):
        self._cargar(prob)

    def _get_prob(self):
        return self.__prob

    prob = property (_get_prob, _set_prob)
