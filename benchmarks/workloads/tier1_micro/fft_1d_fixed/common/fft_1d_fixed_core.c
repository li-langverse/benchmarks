#include "fft_1d_fixed_core.h"
#include <math.h>
#include <stdint.h>
#include <stdio.h>

#ifdef LI_BENCH_FFTW
#include <fftw3.h>
enum { N = 4096, REPS = 64 };
#else
enum { N = 1024, REPS = 2 };
#endif

static double g_checksum;

static void init_signal(double *re) {
  for (int n = 0; n < N; ++n) {
    re[n] = cos(0.007 * (double)n) + 0.25 * sin(0.019 * (double)n);
  }
}

#ifdef LI_BENCH_FFTW
__attribute__((noinline)) void li_fft_1d_fixed_kernel(void) {
  static fftw_plan plan;
  static double *in = NULL;
  static double *out = NULL;
  static int ready = 0;
  if (!ready) {
    in = fftw_alloc_real((size_t)N);
    out = fftw_alloc_real((size_t)N);
    init_signal(in);
    plan = fftw_plan_r2r_1d(N, in, out, FFTW_R2HC, FFTW_MEASURE);
    ready = 1;
  }
  for (int rep = 0; rep < REPS; ++rep) {
    fftw_execute(plan);
  }
  double acc = 0.0;
  for (int k = 0; k < N; ++k) {
    acc += out[k];
  }
  g_checksum = acc;
}
#else
__attribute__((noinline)) void li_fft_1d_fixed_kernel(void) {
  double re[N], out_re[N];
  init_signal(re);
  for (int rep = 0; rep < REPS; ++rep) {
    for (int k = 0; k < N; ++k) {
      double sum = 0.0;
      for (int n = 0; n < N; ++n) {
        const double ang = -2.0 * 3.141592653589793 * (double)k * (double)n / (double)N;
        sum += re[n] * cos(ang);
      }
      out_re[k] = sum;
    }
    for (int k = 0; k < N; ++k) {
      re[k] = out_re[k];
    }
  }
  double acc = 0.0;
  for (int k = 0; k < N; ++k) {
    acc += re[k];
  }
  g_checksum = acc;
}
#endif

int li_fft_1d_fixed_n(void) { return N; }

double li_fft_1d_fixed_checksum(void) { return g_checksum; }
