import ctypes as C
import numpy as np
import matplotlib.pyplot as plt
import time
import threading
import os

class Percolacion():

    def __init__(self, L, ruta="./datos/"):

        # Tamaño de la red y ruta origen datos
        self._L = L
        self._ruta = ruta

        # Comunicación con C mediante ctypes
        self._percolar = C.CDLL('./libpercolar.so')

        # Punteros usuales
        self._longp = C.POINTER(C.c_long)
        self._doublep = C.POINTER(C.c_double)

        # Parámetros internos de la red
        self.__prob = 0
        self._semilla_inicial = 1
        self._profundidad = 16

        # Contador de iteraciones para probabilidad fija
        self.N = 0
        # Contador de iteraciones para búsqueda de pc por biyección
        self.M = 0

        # Valores acumulados por la función iterar_prob_fija
        self._p_total = C.c_long(0)
        self._spt_total = C.c_double(0.0)
        self._spm_total = C.c_double(0.0)
        self._spmax_total = C.c_double(0.0)
        self._snp_total = C.c_double(0.0)
        self._s0_total = C.c_double(0.0)
        self._np_total = C.c_long(0)
        self._fppt_total = C.c_double(0.0)
        self._fppmax_total = C.c_double(0.0)
        self._ns_total = np.zeros(self._L**2, dtype=C.c_long)

        # Valores acumulador por la función iterar_buscar_pc
        self._pcs = 0.0
        self._pcs2 = 0.0

        # Carga inicial de datos para el tamaño de red dado
        self._cargar_pc()

    # Definición de propiedades de sólo lectura

    @property
    def p(self): return self._p_total.value / self.N

    @property
    def spt(self): return self._spt_total.value / self.N

    @property
    def spm(self): return self._spm_total.value / self.N

    @property
    def spmax(self): return self._spmax_total.value / self.N

    @property
    def snp(self): return self._snp_total.value / self.N

    @property
    def s0(self): return self._s0_total.value / self.N

    @property
    def np(self): return self._np_total.value / self.N

    @property
    def fppt(self): return self._fppt_total.value / self.N

    @property
    def fppmax(self): return self._fppmax_total.value / self.N

    @property
    def ns(self): return np.copy(self._ns_total) / self.N

    @property
    def pc(self): return self._pcs / self.M

    @property
    def sd2(self): return abs((self._pcs2 / self.M) - (self._pcs /self.M)**2)

    @property
    def sd(self): return self.sd2**0.5

    # Definición de la propiedad prob (ver y modificar probabilidad)

    def _set_prob(self, prob):
        # Llama a la función cargar, que recupera información disponible
        self._cargar(prob)
    def _get_prob(self):
        # Devuelve el valor actual de probabilidad fijado
        return self.__prob
    prob = property (_get_prob, _set_prob)



    def info_pc(self, *args):
        '''
        Imprime en pantalla información relevante a la busqueda de pc.
        Los argumentos que recibe se imprimen adicionalmente.
        '''
        print ('Tamaño de la red: ' + str(self._L))
        print ('Pc: ' + str(self.pc) + " +/- " + str(self.sd))
        print ('Veces iterada: ' + str(self.M))
        for mensaje in args:
            print (mensaje)
        print('\n', end='')

    def info_prob(self, *args):
        '''
        Imprime en pantalla información relevante para la prob. configurada.
        Los argumentos que recibe se imprimen adicionalmente.
        '''
        print ('Tamaño de la red: ' + str(self._L))
        print ('Probabilidad: ' + str(self.__prob))
        print ('Veces iterada: ' + str(self.N))
        for mensaje in args:
            print (mensaje)
        print('\n', end='')

    def _iterar_buscar_pc(self, *args):
        ''' Ejecuta una función de C. Utilizada para multihilo. '''
        self._percolar.iterar_buscar_pc(*args)

    def _iterar_prob_fija(self, *args):
        ''' Ejecuta una función de C. Utilizada para multihilo. '''
        self._percolar.iterar_prob_fija(*args)

    def iterar_buscar_pc(self, N=27000, n_threads=8, info=False):

        # Abandona la función si el número de iteraciones es negativo
        if N<=0:
            return

        # Divide la iteraciones requeridas entre los hilos configurados
        subiter = N // n_threads
        # Fija la iteración actual en la última realizada
        iter_actual = self.M

        # Genera una lista con los datos que recibira cada hilo de ejecución
        datos = list()
        for i in range(n_threads):
            datos.append([C.c_double(0.0),
                          C.c_double(0.0)])

        thread = list()

        # Imprime información inicial si se configuro el arg. info a True
        if info==True:
            print ("Configurado en " + str(n_threads) +
                   " thread/s simultaneo/s.")
            print ("Iteraciones: " + str(subiter*n_threads))
            print ("Iteraciones por thread: " + str(subiter) + "\n")
            tiempo_inicial = time.time()

        # Prepara los hilos con los argumentos correspondientes
        for i in range(n_threads):
            semilla = self._semilla_inicial + iter_actual + i * subiter
            args = (C.c_long(self._L),
                    C.c_long(int(semilla)),
                    C.c_long(subiter),
                    C.c_long(self._profundidad),
                    C.byref(datos[i][0]),
                    C.byref(datos[i][1]))

            thread.append(threading.Thread(target=self._iterar_buscar_pc,
                                           args=args))

        # Inicia y une los hilos de ejecución
        for t in thread:
            t.start()
        for t in thread:
            t.join()

        # Recupera la información acumulada de cada proceso y la une
        for i in range(n_threads):
            self.M += subiter
            self._pcs = self._pcs + datos[i][0].value
            self._pcs2 = self._pcs2 + datos[i][1].value

        # Guarda las nuevas iteraciones realizadas
        self._guardar_pc()

        # Imprime información final si se configuro el arg. info a True
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
            datos.append([C.c_long(0),
                          C.c_double(0.0),
                          C.c_double(0.0),
                          C.c_double(0.0),
                          C.c_double(0.0),
                          C.c_double(0.0),
                          C.c_long(0),
                          C.c_double(0.0),
                          C.c_double(0.0),
                          np.zeros(self._L**2, dtype=C.c_long)])

        thread = list()

        if info==True:

            print ("Configurado en " + str(n_threads) +
                   " thread/s simultaneo/s.")
            print ("Iteraciones: " + str(subiter*n_threads))
            print ("Iteraciones por thread: " + str(subiter) + "\n")
            tiempo_inicial = time.time()

        for i in range(n_threads):
            semilla = self._semilla_inicial + iter_actual + i * subiter
            args = (C.c_long(self._L),
                    C.c_long(semilla),
                    C.c_double(self.__prob),
                    C.c_long(subiter),
                    C.byref(datos[i][0]),
                    C.byref(datos[i][1]),
                    C.byref(datos[i][2]),
                    C.byref(datos[i][3]),
                    C.byref(datos[i][4]),
                    C.byref(datos[i][5]),
                    C.byref(datos[i][6]),
                    C.byref(datos[i][7]),
                    C.byref(datos[i][8]),
                    datos[i][9].ctypes.data_as(self._longp))

            thread.append(threading.Thread(target=self._iterar_prob_fija,
                                           args=args))

        for t in thread:
            t.start()

        for t in thread:
            t.join()

        for i in range(n_threads):
            self.N += subiter
            self._p_total.value += datos[i][0].value
            self._spt_total.value += datos[i][1].value
            self._spm_total.value += datos[i][2].value
            self._spmax_total.value += datos[i][3].value
            self._snp_total.value += datos[i][4].value
            self._s0_total.value += datos[i][5].value
            self._np_total.value += datos[i][6].value
            self._fppt_total.value += datos[i][7].value
            self._fppmax_total.value += datos[i][8].value
            self._ns_total = self._ns_total + datos[i][9]

        self._guardar()

        if info==True:

            print ("Se añadieron " + str(subiter*n_threads) + " iteraciones.")
            print ("Cantidad de iteraciones acumuladas: " + str(self.N))
            print ("Tiempo transcurrido: " +
                   str(round(time.time() - tiempo_inicial,4)) + " seg\n")

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
            self._p_total.value = datos[0][1]
            self._spt_total.value = datos[0][2]
            self._spm_total.value = datos[0][3]
            self._spmax_total.value = datos[0][4]
            self._snp_total.value = datos[0][5]
            self._s0_total.value = datos[0][6]
            self._np_total.value = datos[0][7]
            self._fppt_total.value = datos[0][8]
            self._fppmax_total.value = datos[0][9]
            np.copyto(self._ns_total, datos[1])

        else:
            self.N = 0
            self._p_total.value = 0
            self._spt_total.value = 0.0
            self._spm_total.value = 0.0
            self._spmax_total.value = 0.0
            self._snp_total.value = 0.0
            self._s0_total.value = 0.0
            self._np_total.value = 0
            self._fppt_total.value = 0.0
            self._fppmax_total.value = 0.0
            np.copyto(self._ns_total, np.zeros(self._L**2, dtype=C.c_long))

    def _guardar(self):
        os.makedirs(self._ruta + "/" + str(self._L), exist_ok=True)
        archivo = self._ruta + "/" + str(self._L) + "/ " + str(self.__prob) + ".npy"

        datos = [[self.N,
                  self._p_total.value,
                  self._spt_total.value ,
                  self._spm_total.value,
                  self._spmax_total.value,
                  self._snp_total.value,
                  self._s0_total.value,
                  self._np_total.value,
                  self._fppt_total.value,
                  self._fppmax_total.value],
                  self._ns_total]

        np.save(archivo, datos)

#    def _colormaps(self, cmap):
#
#        cmaplist = [cmap(i) for i in range(cmap.N)]
#        cmaplist[0] = (0,0,0)
#        cmaplist[-1] = (1,1,1)
#        return cmap.from_list('Red', cmaplist, cmap.N)
#
#    def ver_red(self, L, prob, semilla=26572):
#
#        red = np.zeros(L**2, dtype=C.c_long)
#        s = C.c_long(semilla)
#
#        self._percolar.llenar(red.ctypes.data_as(self._intp), C.c_long(L),
#                              C.c_double(prob),
#                              C.byref(s))
#
#        self._percolar.hoshen(red.ctypes.data_as(self._intp),
#                              C.c_long(L))
#
#        percolante = self._percolar.percola(red.ctypes.data_as(self._intp),
#                                            C.c_long(L))
#
#        cmap = self._colormaps(plt.cm.rainbow)
#        matriz = red.reshape(L, L)
#        matriz[matriz<2] = -10
#        matriz[matriz==percolante] = np.amax(matriz) * 2
#        print(percolante)
#
#        plt.matshow(matriz, cmap=cmap)
#        plt.show()
