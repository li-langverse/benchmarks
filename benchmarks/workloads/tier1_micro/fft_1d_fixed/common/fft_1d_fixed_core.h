#pragma once

#ifdef __cplusplus
extern "C" {
#endif

/* N=4096 when built with -DLI_BENCH_FFTW (FFTW oracle); else N=1024 naive DFT. */
int li_fft_1d_fixed_n(void);
void li_fft_1d_fixed_kernel(void);
double li_fft_1d_fixed_checksum(void);

#ifdef __cplusplus
}
#endif
