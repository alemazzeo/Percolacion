extern void llenar(int *red,
		   int n,
		   double proba,
		   int *semilla);

extern int hoshen(int *red,
		  int n);

extern int actualizar(int *red,
		      int *clase,
		      int s,
		      int frag);

extern void etiqueta_falsa(int *red,
			   int *clase,
			   int s1,
			   int s2);

extern void corregir_etiqueta(int *red,
			      int *clase,
			      int n);

extern int percola(int *red,
		   int n);

extern int id_percolantes(int *red,
			  int n,
			  int *percolantes);

extern void hist(int *datos,
		 int *resultado,
		 int n);

extern void iterar_prob_fija(int n,
			     int semilla_inicial,
			     double proba,
			     int n_iter,
			     int *p_total,
			     double *spt_total,
			     double *spm_total,
			     double *spmax_total,
			     double *snp_total,
			     double *s0_total,
			     int *np_total,
			     double *fppt_total,
			     double *fppmax_total,
			     int *ns_total);

extern double forzar_percolacion(int n, int semilla,
				 double proba_inicial,
				 int profundidad);

extern void iterar_buscar_pc(int n,
			     int semilla_inicial,
			     int n_iter,
			     int profundidad,
			     double *proba,
			     double *proba2);

extern void reemplazar(int *red,
		       int *clase,
		       int n);

extern void imprimir(int *red,
		     int n);

extern double rnd(int *semilla);
