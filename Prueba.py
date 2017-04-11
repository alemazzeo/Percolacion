import ctypes as C
import numpy as np

N = 124
prob = 0.5
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

		self.percolar.llenar(self.red.ctypes.data_as(self.intp), C.c_int(self.N), 
						C.c_float(self.prob), C.byref(self.semilla))

	def llenar(self, prob, semilla):
		self.prob = prob
		self.semilla = C.c_int(semilla)
		self.red = np.zeros(self.N**2, dtype=C.c_int)

		self.percolar.llenar(self.red.ctypes.data_as(self.intp), C.c_int(self.N), 
						C.c_float(self.prob), C.byref(self.semilla))

	def hoshen(self):
		self.percolar.hoshen(red.ctypes.data_as(self.intp), C.c_int(self.N))

mired = Percolar(N, prob, semilla)
mired.hoshen()
