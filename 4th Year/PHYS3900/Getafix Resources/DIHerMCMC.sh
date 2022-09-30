#!/bin/bash -l
#
#SBATCH --job-name=DIHerMCMC
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=168G  # memory (MB)
#SBATCH --time=15-00:00      # time (D-HH:MM)

module load starry

python "DIHerMCMC.py"
