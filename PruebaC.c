#include <stdio.h>
#include <stdlib.h>
#include "percolar.h"

#define N		16

int main()
{
	int n=N, *red, *clase;
	float proba=0.65;
	int s=260572;
	int i=0,j=0;

	red = (int *)malloc(n*n*sizeof(int));

	for (i=0;i<27;i++)
	{
		for (j=0;j<1000;j++)
		{
			llenar(red, n, proba, &s);
			hoshen(red, n);
		}
		printf("*");
		fflush(stdout);
	}
	imprimir(red, n);
	i = percola(red, n);
	printf("%d", i);


}
