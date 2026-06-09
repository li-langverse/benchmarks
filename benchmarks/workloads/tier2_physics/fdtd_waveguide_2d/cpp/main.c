/* fdtd_waveguide_2d — tier-2 C oracle entry (physics-codegen Arm B cpp). */
#include <stdio.h>
#include <string.h>

void li_fdtd_waveguide_kernel(void);
double li_fdtd_waveguide_checksum(void);

int main(int argc, char** argv) {
  li_fdtd_waveguide_kernel();
  const double checksum = li_fdtd_waveguide_checksum();
  if (argc > 1 && strcmp(argv[1], "--verify") == 0) {
    printf("%.17g\n", checksum);
    return 0;
  }
  (void)checksum;
  return 0;
}
