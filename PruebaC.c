#include <stdio.h>
#include "percolar.h"

#define N		30

int main()
{
	int n=N, red[n*n];
	float proba=0.5;
	int s=260572;

	printf("%f", random(&s));
	printf("%f", random(&s));
	printf("%f", random(&s));
	printf("%f", random(&s));
	llenar(red, n, proba, &s);
	imprimir(red, n);
}
