import pdbfixer
import sys
import os
from simtk.openmm.app import PDBFile
from simtk.openmm import app
import simtk
import parmed

if len(sys.argv)==3 and os.path.exists(sys.argv[1]):
    inputfilename=sys.argv[1]
    outfilename=sys.argv[2]
else:
    sys.exit("Usage: python pdb2mfj.py input.pdb output.mfj [options]")

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


PDBFile.writeFile(fixer.topology, fixer.positions, open(outfilename, 'w'))

protein = parmed.load_file(outfilename)["!(:HOH,NA,CL)"]  # remove ions and water
forcefield = app.ForceField("amber99sb.xml")

[templates, residues] = forcefield.generateTemplatesForUnmatchedResidues(protein.topology)
# Se the atom types
for template in templates:
    template.overrideLevel=1
    template.name="GLY"
    for atom in template.atoms:
        atom.type = "H" # set the atom types here
    # Register the template with the forcefield.
    forcefield.registerResidueTemplate(template)


protein_system = forcefield.createSystem(protein.topology)
non_bonded_force = [for force in protein_system.getForces() if type(force)==simtk.openmm.openmm.NonbondedForce]
if non_bonded_force:
    for aidx in range(0,non_bonded_force.getNumParticles()):
        charge=non_bondonded_force.getParticleParameters(aidx)[0]._value
        positions=protein.positions[aidx]
        x=positions._value.x
        y=positions._value.y
        z=positions._value.z
else:
    sys.exit("No non bonded forces found. Something went wrong during the system preparation")