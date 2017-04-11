#include <stdio.h>
#include "percolar.h"

#define N		64

int main()
{
	int n=N, red[n*n];
	float proba=0.5;
	int s=260572;

	llenar(red, n, proba, &s);
	imprimir(red, n);
	hoshen(red, n);
	imprimir(red, n);
}
