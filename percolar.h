extern void 	llenar(int *red, int n, float proba, int *semilla);
extern int 		hoshen(int *red, int n, int *clase);
extern int 		actualizar(int *red, int *clase, int s, int frag);
extern void 	etiqueta_falsa(int *red, int *clase, int s1, int s2);
extern void		corregir_etiqueta(int *red, int *clase, int n);
extern int		percola(int *red, int n);
extern void 	imprimir(int *red, int n);
extern float 	rnd(int *semilla);
