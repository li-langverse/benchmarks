/* wave_equation_1d — tier-2 C oracle entry (physics-codegen Arm B cpp). */
#include "../common/wave_core.h"
#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {
  li_wave_1d_kernel();
  const double checksum = li_wave_1d_checksum();
  if (argc > 1 && strcmp(argv[1], "--verify") == 0) {
    printf("%.17g\n", checksum);
    return 0;
  }
  (void)checksum;
  return 0;
}
