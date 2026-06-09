/* heat_equation_2d — tier-2 explicit 2D heat equation (physics-codegen Arm B cpp). */
#include "heat_kernel.h"
#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {
  li_heat_2d_kernel();
  const double checksum = li_heat_2d_checksum();
  if (argc > 1 && strcmp(argv[1], "--verify") == 0) {
    printf("%.17g\n", checksum);
    return 0;
  }
  (void)checksum;
  return 0;
}
