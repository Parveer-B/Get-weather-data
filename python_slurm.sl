#!/bin/bash -l
#SBATCH --job-name=python_running
#SBATCH --account=def-zebtate # adjust this to match the accounting group you are using to submit jobs
#SBATCH --time=7-00:00   # adjust this to match the walltime of your job
#SBATCH --nodes=1      
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1      # adjust this if you are using parallel commands
#SBATCH --mem=4000             # adjust this according to the memory requirement per node you need
#SBATCH --mail-user=parveer.banwait@mail.utoronto.ca # adjust this to match your email address
#SBATCH --mail-type=END

# Choose a version of MATLAB by loading a module:

module load python/3.10

#module load scipy-stack  # Loads scipy, numpy, matplotlib, pandas, etc.
#module load netcdf        # Loads netCDF4 and dependencies

module load mpi4py/3.1.4
source ENV2/bin/activate


pip install mpi4py

# Remove -singleCompThread below if you are using parallel commands:
ARG1=$1

python maineventgen.py 50000 $ARG1