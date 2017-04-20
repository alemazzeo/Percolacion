libpercolar.so: percolar.c
	gcc -Wall -c -fPIC percolar.c
	gcc -shared percolar.o -o libpercolar.so

clean:
	rm -f percolar.o libpercolar.so
