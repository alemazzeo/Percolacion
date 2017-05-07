#include <stdio.h>
#include <stdlib.h>
#include "percolar.h"

#define A    16807
#define M    2147483647
#define Q    127773
#define R    2836
#define S    260572

void llenar(long *red, long n, double proba, long *semilla)
{
    long i;
    long n2=n*n;

    for(i=0;i<n2;i++)
    {
        if (proba<rnd(semilla)) *(red+i)=0; else *(red+i)=1;
    }

}

long hoshen(long *red, long n)
{
    long i,j,k,n2,s1,s2,frag, *clase;

    n2=n*n;
    frag=0;

    clase = (long *) malloc(n*n*sizeof(long));

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

long actualizar(long *red, long *clase, long s, long frag)
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
void etiqueta_falsa(long *red, long *clase, long s1, long s2)
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
void corregir_etiqueta(long *red, long *clase, long n)
{
    long i,j;

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

long percola(long *red, long n)
{
    long i, j, s=0;

    for (i=0;i<n;i++)
    {
        if (*(red+i) > s)
        {
			s = *(red+i);
            j = 0;
			for (j=0;j<n;j++)
			{
				if (*(red+(n*(n-1)+j)) == s)
				{
					return 1;
				}
			}
        }
    }
    return 0;
}

long id_percolantes(long *red, long n, long *percolantes)
{
    long i, j, s=0, cantidad=0;

    for (i=0; i<n; i++)
    {
        if (*(red+i) > s)
        {
            s = *(red+i);
            j = 0;
            for (j=0; j<n; j++)
            {
                if (*(red+(n*(n-1)+j)) == s)
                {
                    *(percolantes + cantidad) = s;
                    cantidad++;
					break;
                }
            }
        }
    }

    return cantidad;
}

void hist(long *datos, long *resultado, long n)
{
    long i, s;

    for (i=0; i<n; i++)
    {
        s = *(datos+i);
        *(resultado + s) +=1;
    }
}

void iterar_prob_fija(long n,
					  long semilla_inicial,
					  double proba,
                      long n_iter,
					  long *p_total,
                      double *spt_total,
                      double *spm_total,
                      double *spmax_total,
                      double *snp_total,
                      double *s0_total,
                      long *np_total,
					  double *fppt_total,
					  double *fppmax_total,
                      long *ns_total)
{
    long i, j, n2=n*n, s, cantidad;
    double sp, s0, spt, spmax;
    long *red, *semilla, *n_etiqueta, *percolantes;

    red = (long *) malloc(n*n*sizeof(long));
    n_etiqueta = (long *) malloc(n*n*sizeof(long));
    percolantes = (long *) malloc(n*sizeof(long));

    s = semilla_inicial;
    semilla = &s;

    for (i=0; i<n_iter; i++)
    {
        s = semilla_inicial + i;
        llenar(red, n, proba, semilla);
        hoshen(red, n);

        cantidad = id_percolantes(red, n, percolantes);

        for (j=0; j<n2; j++)
        {
            *(n_etiqueta+j) = 0;
        }

        hist(red, n_etiqueta, n2);

		s0 = *(n_etiqueta);
		spt = 0;
		spmax = 0;

		for (j=0; j<cantidad; j++)
		{
			sp = *(n_etiqueta + (*(percolantes+j)));
			spt += sp;
			if (spmax < sp) spmax = sp;
		}

        if (cantidad > 0)
        {
            (*p_total)++;
			(*spt_total) += spt / n2;
			(*spm_total) += (spt / cantidad) / n2;
			(*spmax_total) += spmax / n2;
			(*fppt_total) += spt / (n2 - s0);
			(*fppmax_total) += spmax / (n2 - s0);
		}

		(*snp_total) += (n2 - spt - s0) / n2;
		(*s0_total) += s0 / n2;
		(*np_total) += cantidad;

        hist(n_etiqueta+2, ns_total, n2-2);

    }

    free(red);
    free(n_etiqueta);
    free(percolantes);

}

void reemplazar(long *red, long *clase, long n)
{
    long i, n2=n*n;

    for (i=0; i<n2; i++)
    {
        *(red+i) = clase[*(red+i)];
    }
}

void imprimir(long *red, long n)
{
    long i,j,n2;

    j=1;
    n2=n*n;

    printf("\n");

    for(i=0;i<n2;i++)
    {
        printf("%li03 ", *(red+i));
        if (j==(i+1)/n)
        {
            printf("\n");
            j++;
        }
    }
    printf("\n");

}

double rnd(long *semilla)
{
    long k;
    double x;

    k=(*semilla)/Q;
    *semilla=A*(*semilla-k*Q)-R*k;
    if (*semilla<0) *semilla+=M;

    x=(*semilla)*(1.0/M);

    return x;
}

double forzar_percolacion(long n, long semilla, double proba_inicial,
						  long profundidad)
{
	long i, denominador=4;
	long *red, s;
	double proba;

	proba = proba_inicial;

	red = (long *) malloc (n*n*sizeof(long));

	for (i=0; i<profundidad;i++)
	{
		s = semilla;
		llenar(red, n, proba, &s);
		hoshen(red, n);
		if (percola(red,n) > 0)
		{
			proba = proba - 1.0/denominador;
		}
		else
		{
			proba = proba + 1.0/denominador;
		}
		denominador = denominador * 2;
	}
	free(red);
	return proba;
}


void iterar_buscar_pc(long n, long semilla_inicial, long n_iter,
					  long profundidad, double *proba, double *proba2)
{
    long i, s;
	double pc;

    s = semilla_inicial;

    for (i=0; i<n_iter; i++)
    {
        s = semilla_inicial + i;
        pc = forzar_percolacion(n, s, 0.5, profundidad);
        (*(proba)) += pc;
        (*(proba2)) += pc * pc;
    }
}
