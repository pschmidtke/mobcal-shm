import pdbfixer
import sys
import os
from simtk.openmm.app import PDBFile
from simtk.openmm import app
import simtk
import parmed
import time

if len(sys.argv)==3 and os.path.exists(sys.argv[1]):
    inputfilename=sys.argv[1]
    pdboutfilename=sys.argv[2]+".pdb"
    mfjoutfilename=sys.argv[2]+".mfj"
else:
    sys.exit("Usage: python pdb2mfj.py input.pdb outputPrefix [options]")

protonate=1
pH=10.0 #fixed ph to charge the protein



def writeMfjOutput(protein,mfjfilename):
    """Prepare the mobcal input file from a prepared openmm system"""






print("Reading file: "+inputfilename)
fixer=pdbfixer.PDBFixer(inputfilename)
fixer.removeHeterogens(False)
fixer.findMissingResidues()
print("Missing residues: ")
print(fixer.missingResidues)
fixer.findMissingAtoms()

print("Missing atoms: ")
print(fixer.missingAtoms)
if(len(fixer.missingAtoms)):
    print("adding missing atoms")
    fixer.addMissingAtoms()

if protonate:
    print("Protonating at pH: "+str(pH))
    fixer.addMissingHydrogens(pH)

print("Building system")
PDBFile.writeFile(fixer.topology, fixer.positions, open(pdboutfilename, 'w'))

protein = parmed.load_file(pdboutfilename)["!(:HOH,NA,CL)"]  # remove ions and water
forcefield = app.ForceField("amber99sb.xml")

[templates, residues] = forcefield.generateTemplatesForUnmatchedResidues(protein.topology)
# Set the atom types 
# This is a current workaround for unknown residues and missing atoms ... given the crude CCS caclulations, this should not affect a lot the shape of the system
for template in templates:
    template.overrideLevel=1
    template.name="GLY"
    for atom in template.atoms:
        atom.type = "H" # set the atom types here
    # Register the template with the forcefield.
    forcefield.registerResidueTemplate(template)


protein_system = forcefield.createSystem(protein.topology)
non_bonded_force = [force for force in protein_system.getForces() if type(force)==simtk.openmm.openmm.NonbondedForce][0]
atoms=[atom for atom in protein.topology.atoms()]


print("Writing output")
outputhandle=open(mfjoutfilename,"w")
outputhandle.write("""pdb2mfj_output
1
%d
ang                           
calc                          
1.0000\n"""%(len(atoms)))
tc=0.0
tpos=0.0
twrite=0.0
tmass=0.0
if non_bonded_force:
    #TODO: here we are assuming that non bonded force particles are ordered like the atoms in the topology ... this should be double checked first
    #adapt loop over positions to make this faster here
    for idx, pos in enumerate(protein.positions):
    #for aidx in range(0,non_bonded_force.getNumParticles()-31000):
        charge=non_bonded_force.getParticleParameters(idx)[0]._value
        #positions=protein.positions[aidx]
        
        x=pos._value.x
        y=pos._value.y
        z=pos._value.z
        mass=round(atoms[idx].element._mass._value)
        outputhandle.write("%.3f   %.3f   %.3f   %d   %.2f\n"%(x,y,z,mass,charge))

    outputhandle.close()
    print("Result file written to "+mfjoutfilename)
else:
    sys.exit("No non bonded forces found. Something went wrong during the system preparation")