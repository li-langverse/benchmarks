/* combustion_passive — tier-2 passive combustion ODE (physics-codegen Arm B cpp). */
#include "combust_kernel.h"
#include <stdio.h>
#include <string.h>

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
