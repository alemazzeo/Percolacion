import ctypes as C
import numpy as np

N = 256
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
		self.clase = np.zeros(self.N**2, dtype=C.c_int)

		self.percolar.llenar(self.red.ctypes.data_as(self.intp), C.c_int(self.N), 
						C.c_float(self.prob), C.byref(self.semilla))

	def llenar(self, prob, semilla):
		self.prob = prob
		self.semilla = C.c_int(semilla)
		self.red = np.zeros(self.N**2, dtype=C.c_int)

		self.percolar.llenar(self.red.ctypes.data_as(self.intp), C.c_int(self.N), 
						C.c_float(self.prob), C.byref(self.semilla))

	def hoshen(self):
		self.percolar.hoshen(self.red.ctypes.data_as(self.intp), C.c_int(self.N), 
						self.clase.ctypes.data_as(self.intp))
						
	def imprimir(self):
		for i in self.red:
			print (str(i) + " ")

mired = Percolar(N, prob, semilla)
for i in range(27):
	for j in range(1000):
		mired.llenar(prob, semilla+i)
		mired.hoshen()
	print ("*")
		

