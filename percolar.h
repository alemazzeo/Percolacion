extern void     llenar(int *red, int n, float proba, int *semilla);
extern int      hoshen(int *red, int n);
extern int      actualizar(int *red, int *clase, int s, int frag);
extern void     etiqueta_falsa(int *red, int *clase, int s1, int s2);
extern void     corregir_etiqueta(int *red, int *clase, int n);
extern int      percola(int *red, int n);
extern void     hist(int *datos, int *resultado, int n);
extern void     iterar_prob_fija(int n, int semilla_inicial, float proba,
								 int n_iter, int *p_total, int *fp_total,
								 int *ns_total);
//extern void     iterar_buscar_pc(int n, int semilla_inicial, int n_iter,
//								 int *proba, int *proba2)
extern void     reemplazar(int *red, int *clase, int n);
extern void     imprimir(int *red, int n);
extern float    rnd(int *semilla);
