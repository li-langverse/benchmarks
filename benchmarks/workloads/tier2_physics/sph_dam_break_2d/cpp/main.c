/* sph_dam_break_2d — tier-2 2D dam-break SPH (physics-codegen Arm B cpp). */
#include "sph_dam_kernel.h"
#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {
  li_sph_dam_2d_kernel();
  const double checksum = li_sph_dam_2d_checksum();
  if (argc > 1 && strcmp(argv[1], "--verify") == 0) {
    printf("%.17g\n", checksum);
    return 0;
  }
  (void)checksum;
  return 0;
}
