#include "system_includes.h"
#include "mobcal_pgpsq.h"
void mobcal_pgpsq(int n, double *p, double *q) {
  /*
    p <- p .- q 
  */
  int i;
  int padi;
  for (i=0;i<8;i++) {
    p[i] = p[i] - q[i];
  }
}
