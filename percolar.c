#include <stdio.h>
#include <stdlib.h>
#include "percolar.h"

#define A    16807
#define M    2147483647
#define Q    127773
#define R    2836
#define S    260572

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
    int i,j,k,n2,s1,s2,frag, *clase;

    n2=n*n;
    frag=0;

    clase = (int *) malloc(n*n*sizeof(int));

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
    reemplazar(red,clase,n);
    free(clase);
    return 0;
}

int actualizar(int *red, int *clase, int s, int frag)
{
    if (s==0)
    {
        *red = frag;
        *(clase+frag) = frag;
        return frag+1;
    }
    else
    {
        *red = s;
        return frag;
    }

}
void etiqueta_falsa(int *red, int *clase, int s1, int s2)
{
    while (clase[s1]<0)
    {
        s1 = -clase[s1];
    }

    while (clase[s2]<0)
    {
        s2 = -clase[s2];
    }

    if (s1<s2)
    {
        clase[s2] = -s1;
        clase[s1] = s1;
        *red = s1;
    }
    else
    {
        clase[s1] = -s2;
        clase[s2] = s2;
        *red = s2;
    }

}
void corregir_etiqueta(int *red, int *clase, int n)
{
    int i,j;

    i=2;
    while (clase[i] != 0)
    {
        j=i;
        while(clase[j]<0)
        {
            j = -clase[j];
        }
        clase[i] = clase[j];
        i++;
    }
}

int percola(int *red, int n)
{
    int i, j, s=0, actual=0, cantidad=0, mayor=0;
    int *percolantes;

    percolantes = (int *) malloc(n*sizeof(int));

    for (i=0;i<n;i++)
    {
        if (*(red+i) > actual)
        {
            s = *(red+i);
            j = 0;
            while (actual < s && j<n)
            {
                if (*(red+(n*(n-1)+j)) == s)
                {
                    *(percolantes + cantidad) = s;
                    cantidad++;
                    actual = s;
                }
                j++;
            }
        }
    }

    for (i=0; i<cantidad; i++)
    {
        if (*(percolantes+i) > mayor)
            mayor = *(percolantes+i);
    }

    free(percolantes);

    return mayor;
}

void hist(int *datos, int *resultado, int n)
{
    int i, s;

    for (i=0; i<n; i++)
    {
        s = *(datos+i);
        *(resultado + s) +=1;
    }
}

void iterar_prob_fija(int n, int semilla_inicial, float proba,
					  int n_iter, int *p_total, int *fp_total,
					  int *ns_total)
{
    int i, j, n2=n*n, percolante, s;
    int *red, *semilla, *n_etiqueta, *ns;

    red = (int *) malloc(n*n*sizeof(int));
    n_etiqueta = (int *) malloc(n*n*sizeof(int));
	ns = (int *) malloc(n*n*sizeof(int));

    s = semilla_inicial;
    semilla = &s;

    for (i=0; i<n_iter; i++)
    {
        s = semilla_inicial + i;
        llenar(red, n, proba, semilla);
        hoshen(red, n);

        percolante = percola(red, n);


		for (j=0; j<n2; j++)
		{
			*(n_etiqueta+j) = 0;
			*(ns+j) = 0;
		}

        hist(red, n_etiqueta, n2);

        if (percolante > 0)
        {
            (*p_total)++;
            (*fp_total) += (*(n_etiqueta+percolante)) / (n2 - (*n_etiqueta));
        }

        hist(n_etiqueta+2, ns_total, n2-2);

    }

    free(red);
    free(n_etiqueta);

}

void reemplazar(int *red, int *clase, int n)
{
    int i, n2=n*n;

    for (i=0; i<n2; i++)
    {
        *(red+i) = clase[*(red+i)];
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
        printf("%03d ", *(red+i));
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
/*
float forzar_percolacion(int n, int semilla, float proba_inicial,
						 int profundidad)
{
	int i, n2=n*n, denominador=2;
	int *red, *s;
	float proba;

	proba = proba_inicial;

	*s = semilla;

	red = (int *) malloc (n*n*sizeof(int));

	for (i=0; i<profundidad;i++)
	{
		llenar(red, n, proba, s);
		hoshen(red, n);
		if (percola(red,n))
		{
			proba -= 1/denominador;
		}
		else
		{
			proba += 1/denominador;
		}
		denominador = denominador * 2;
	}

	return proba;
}


float buscar_pc(int n, int semilla_inicial, int n_iter,
				int *proba, int *proba2)
{
    int i, j, n2=n*n, percolante, s;
    int *red, *semilla, *n_etiqueta, *ns;

    red = (int *) malloc(n*n*sizeof(int));
    n_etiqueta = (int *) malloc(n*n*sizeof(int));
	ns = (int *) malloc(n*n*sizeof(int));

    s = semilla_inicial;
    semilla = &s;

    for (i=0; i<n_iter; i++)
    {
        s = semilla_inicial + i);
        (*iteraciones)++;
        llenar(red, n, proba, semilla);
        hoshen(red, n);

        percolante = percola(red, n);


		for (j=0; j<n2; j++)
		{
			*(n_etiqueta+j) = 0;
			*(ns+j) = 0;
		}

        hist(red, n_etiqueta, n2);

        if (percolante > 0)
        {
            (*p_total)++;
            (*fp_total) += (*(n_etiqueta+percolante)) / (n2 - (*n_etiqueta));
        }

        hist(n_etiqueta+2, ns, n2-2);

		for (j=0; j<n2; j++)
		{
			*(ns_total+j) += *(ns+j);
			*(ns2_total+j) += (*(ns+j)) * (*(ns+j));
		}

    }

    free(red);
    free(n_etiqueta);

}

*/
