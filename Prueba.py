import ctypes as C
import numpy as np

N = 30
prob = 0.5
semilla = 260572

red = np.zeros(N, dtype=C.c_int)

class Percolar():
	def __init__(self, lado, prob, semilla):
		self.N = lado
		self.prob = prob
		self.semilla = semilla
		
		self.percolar = C.CDLL('./libpercolar.so')
		self.intp = C.POINTER(C.c_int)

		self.red = np.zeros(self.N, dtype=C.c_int)

		self.percolar.llenar(self.red.ctypes.data_as(self.intp), C.c_int(len(self.red)), 
						C.c_float(self.proba), C.byref(self.semilla))

	def llenar(self, prob, semilla):
		self.prob = prob
		self.semilla = semilla
		self.red = np.zeros(self.N, dtype=C.c_int)

		self.percolar.llenar(self.red.ctypes.data_as(self.intp), C.c_int(len(self.red)), 
						C.c_float(self.proba), C.byref(self.semilla))

	def hoshen(self):
		self.percolar.hoshen(red.ctypes.data_as(intp), C.c_int(len(red)))

print("E")

mired = Percolar(N, prob, semilla)
mired.llenar(prob, semilla+1)
