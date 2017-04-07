#include <stdio.h>
#include "percolar.h"

#define	A		16807
#define M 		2147483647
#define Q		127773
#define R		2836
#define S		260572

void llenar(int *red, int n, float proba, int *semilla)
{
	int i;
	int n2=n*n;
	
	for(i=0;i<n2;i++)
	{
		if (proba<random(semilla)) *(red+i)=0; else *(red+i)=1;
	}
}

void imprimir(int *red, int n)
{
	int i,j,n2;
	
	j=1;
	n2=n*n;
	
	printf("\n");
	for(i=0;i<n2;i++)
	{
		printf("%d",*(red+i));
		if (j==(i+1)/n)
		{
			printf("\n");
			j++;
		}
	}
	printf("\n");
	
}

float random(int *semilla)
{
	int k;
	float x;
	
	k=(*semilla)/Q;
	*semilla=A*(*semilla-k*Q)-R*k;
	if (*semilla<0) *semilla+=M;
	
	x=(*semilla)*(1.0/M);
	
	return x;
}
