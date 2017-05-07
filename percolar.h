extern void llenar(long *red,
		   long n,
		   double proba,
		   long *semilla);

extern long hoshen(long *red,
		  long n);

extern long actualizar(long *red,
		      long *clase,
		      long s,
		      long frag);

extern void etiqueta_falsa(long *red,
			   long *clase,
			   long s1,
			   long s2);

extern void corregir_etiqueta(long *red,
			      long *clase,
			      long n);

extern long percola(long *red,
		   long n);

extern long id_percolantes(long *red,
			  long n,
			  long *percolantes);

extern void hist(long *datos,
		 long *resultado,
		 long n);

extern void iterar_prob_fija(long n,
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
			     long *ns_total);

extern double forzar_percolacion(long n, long semilla,
				 double proba_inicial,
				 long profundidad);

extern void iterar_buscar_pc(long n,
			     long semilla_inicial,
			     long n_iter,
			     long profundidad,
			     double *proba,
			     double *proba2);

extern void reemplazar(long *red,
		       long *clase,
		       long n);

extern void imprimir(long *red,
		     long n);

extern double rnd(long *semilla);
