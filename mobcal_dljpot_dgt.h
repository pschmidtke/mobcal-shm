#ifndef _MOBCAL_DLJPOT_DGT_H_
#define _MOBCAL_DLJPOT_DGT_H_ 1
extern void mobcal_dljpot_dgt(struct mobcal_state_struct *state,
			      double x, double y, double z,
			      double *pot,
			      double *dpotx_p,
			      double *dpoty_p,
			      double *dpotz_p,
			      double *dmax_p);
#endif
