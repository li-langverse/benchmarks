/* advection_diffusion_2d — tier-2 upwind advection + diffusion (physics-codegen Arm B cpp). */
#include "advdiff_kernel.h"
#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {
  li_advdiff_2d_kernel();
  const double checksum = li_advdiff_2d_checksum();
  if (argc > 1 && strcmp(argv[1], "--verify") == 0) {
    printf("%.17g\n", checksum);
    return 0;
  }
  (void)checksum;
  return 0;
}
