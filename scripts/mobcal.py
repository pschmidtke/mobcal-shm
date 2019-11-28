import os
import sys
import tempfile
from shutil import copy2


if len(sys.argv)!=3:
    sys.exit("Usage: python mobcal.py input.mfj #threads")

inputfilename=sys.argv[1]
ncpus=int(sys.argv[2])




mobcalTemplate="""
parameters.in
atomtype_parameters.in
%s
%s
"""%(sys.argv[1],"output.txt")

parametersTemplate="""
I2 5013489
ITN 10
INP 8
IMP 128
IP 0
IT 0
IGS 0
IM2 0 
IM4 0
IU1 0
IU2 0
IU3 0
IV  0
BUFFER_GAS 14
TEMP 300.0
USE_MT 0
NUM_THREADS %d
"""%(ncpus)


tmpdirname= tempfile.mkdtemp(dir="../tmp")
print(tmpdirname)
copy2(inputfilename,tmpdirname)
copy2("../parameters/atomtype_parameters.in",tmpdirname)
with open(tmpdirname+"/parameters.in", "w") as pfile:
    pfile.write(parametersTemplate)
with open(tmpdirname+"/mobcal.in", "w") as mfile:
    mfile.write(mobcalTemplate)

    