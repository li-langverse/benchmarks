/* wind_field_bc — tier-2 C oracle entry (physics-codegen Arm B cpp). */
#include <stdio.h>
#include <string.h>

void li_wind_field_kernel(void);
double li_wind_field_checksum(void);

int main(int argc, char** argv) {
  li_wind_field_kernel();
  const double checksum = li_wind_field_checksum();
  if (argc > 1 && strcmp(argv[1], "--verify") == 0) {
    printf("%.17g\n", checksum);
    return 0;
  }
  (void)checksum;
  return 0;
}
