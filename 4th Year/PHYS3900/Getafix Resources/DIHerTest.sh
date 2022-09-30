#!/bin/bash -l
#
#SBATCH --job-name=DIHerTest
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=20G  # memory (MB)
#SBATCH --time=0-00:45      # time (D-HH:MM)

module load starry

# source activate StarryEnv

python "DIHerTestScript.py"
