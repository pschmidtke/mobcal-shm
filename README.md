# Mobcal-shm analysis Pipeline
This package includes the mobcal fork, called mobcal-shm and several supplementary utilities allowing to a more straightforward analysis of protein structures especially with mobcal. 

# Using the package
Here you can find the how to use the package with the docker image. 

## Transforming a pdb to a mobcal input file
The scripts directory contains a python script allowing you to convert a PDB file to a mfj file, which is the accepted input format of mobcal. The script prepares the PDB file as well, completing missing atoms, it optionally protonates the structure to a provided pH. Charges are subsequently calculated for the system and written out in the resulting mfj file. 

```
cd scripts;
python pdb2mfj.py examples/1mty.pdb examples/1mty.mfj 
```

# Installation
NB: This is only required if you want to continue development of this package, else, please refer to the docker image of the package to avoid the huzzle of installing & compiling all dependencies. 

## Conda Development environment
Import the conda environment for mobcal using the provided environment file. This is especially required when you want to use the pdb2mfj utility provided in the repo:

`conda env create -f mobcal.yml`

Next activate the environment using 

`conda activate mobcal`

## Compiling mobcal-shm
Now we also need to compile mobcal-shm itself for you environment, unless the provided executable works for you. Simply run the following commands: 
```
cd src;
make
```

# Docker Image
## Building the docker image

`docker build -t mobcalshm .`

## Running the docker image


