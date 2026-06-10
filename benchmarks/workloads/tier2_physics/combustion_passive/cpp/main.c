/* combustion_passive — tier-2 C oracle entry (physics-codegen Arm B cpp). */
#include <stdio.h>
#include <string.h>

void li_combustion_passive_kernel(void);
double li_combustion_passive_checksum(void);

int main(int argc, char** argv) {
  li_combustion_passive_kernel();
  const double checksum = li_combustion_passive_checksum();
  if (argc > 1 && strcmp(argv[1], "--verify") == 0) {
    printf("%.17g\n", checksum);
    return 0;
  }
  (void)checksum;
  return 0;
}
