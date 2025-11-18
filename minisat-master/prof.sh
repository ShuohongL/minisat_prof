#!/bin/bash
MSATP=./bin/minisat
#$MSATP aim-50-1_6-yes1-4.cnf > run.aim-50-1_6-yes1-4.cnf.out
$MSATP ./inputs/g2-ak128astepbg1btisc.cnf
#gprof $MSATP gmon.out > gprof.aim-50-1_6-yes1-4.cnf.out
gprof $MSATP gmon.out > prof_g2-ak128astepbg1btisc.cnf

#$MSATP ../inputs/mp1-ps_5000_21250_3_0_0.8_0_1.55_8.cnf
#gprof $MSATP gmon.out > prof_mp1-ps_5000.output
