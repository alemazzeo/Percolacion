# Percolacion
Primera práctica de Física Computacional 2017-1c

## percolar.c
Contiene las funciones necesarias para llenar la red, identificar los fragmentos,
detectar percolación y realizar conteos.
Se implementaron ademas funciones de trabajo iterativo independientes que pueden ser 
llamadas por diferentes hilos de ejecución.

#### Nota: La función llenar requiere un parámetro final semilla de tipo *int que apunte a la semilla inicial con que se llena la red.

## makefile
Contiene las instrucciones de compilación para generar la librería de uso compartido
libpercolar.so basada en percolar.c.

## percolar.py
Contiene la clase Percolacion. Encapsula las funciones de percolar.c facilitando el uso
de las mismas. Para iteraciones repetidas, utiliza multiples hilos de ejecución entregando
en partes iguales el trabajo requerido a cada uno de ellos.

## Archivos en desuso
Archivos tales como PruebaC.c, correr.c o prueba.py que pueden ser encontrados en algunas ramas del
repositorio corresponden a pruebas sencillas de funcionamiento o rendimiento utilizadas únicamente 
para rastrear problemas al compilar nuevas características.
