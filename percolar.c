#include <stdio.h>
#include <stdlib.h>
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
		if (proba<rnd(semilla)) *(red+i)=0; else *(red+i)=1;
	}

}

int hoshen(int *red, int n)
{
	int i,j,k,n2,s1,s2,frag;
	int *clase;
	
	n2=n*n;
	frag=0;
	clase=(int *)malloc(n*n*sizeof(int));
	
	for (k=0;k<n2;k++) *(clase+k)=frag;
	
	s1=0;
	frag=2;
	
	if (*red) frag=actualizar(red,clase,s1,frag);
	
	for (i=1;i<n;i++)
	{
		if (*(red+i))
		{
			s1=*(red+i-1);
			frag=actualizar(red+i,clase,s1,frag);
		}
	}
	
	for(i=n;i<n*n;i=i+n)
	{
		if (*(red+i))
		{
			s1=*(red+i-n);
			frag=actualizar(red+i,clase,s1,frag);
		}
		
		for (j=1;j<n;j++)
		{
			if (*(red+i+j))
			{
				s1=*(red+i+j-1);
				s2=*(red+i+j-n);
				
				if (s1*s2>0)
				{
					etiqueta_falsa(red+i+j,clase,s1,s2);
				}
				else
				{
					if (s1!=0)
					{		
						frag=actualizar(red+i+j,clase,s1,frag);
					}
					else
					{
						frag=actualizar(red+i+j,clase,s2,frag);
					}
				}
			}
		}
	}
	
	corregir_etiqueta(red,clase,n);	
	free(clase);	
	return 0;
}

int actualizar(int *red, int *clase, int s, int frag)
{
	return 0;
}
void etiqueta_falsa(int *red, int *clase, int s1, int s2)
{

}
void corregir_etiqueta(int *red, int *clase, int n)
{

}
int	percola(int *red, int n)
{
	return 0;
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

float rnd(int *semilla)
{
	int k;
	float x;
	
	k=(*semilla)/Q;
	*semilla=A*(*semilla-k*Q)-R*k;
	if (*semilla<0) *semilla+=M;
	
	x=(*semilla)*(1.0/M);
	
	return x;
}