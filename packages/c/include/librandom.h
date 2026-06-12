#ifndef LIBRANDOMIZER_H
#define LIBRANDOMIZER_H

#ifdef __cplusplus
extern "C" {
#endif

int librandom_random_int(int min, int max, int *out);
int librandom_random_float(double min, double max, double *out);
int librandom_random_char(char min, char max, char *out);

int random_int(void);
int random_int_range(int min, int max);
double random_float(void);
double random_float_range(double min, double max);
char random_char(void);
char random_char_range(char min, char max);

#ifdef __cplusplus
}
#endif

#endif
