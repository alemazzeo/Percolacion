#include <stdio.h>
#include "percolar.h"

#define N		124

int main()
{
	int n=N, red[n*n];
	float proba=0.5;
	int s=260572;
	int i=0,j=0;

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
	//imprimir(red, n);
}
