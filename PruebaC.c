#include <stdio.h>
#include "percolar.h"

#define N		30

int main()
{
	int n=N, red[n*n];
	float proba=0.5;
	int s=260572;

	llenar(red, n, proba, &s);
	imprimir(red, n);
}
