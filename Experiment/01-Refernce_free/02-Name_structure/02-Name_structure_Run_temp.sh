#!/bin/bash
#SBATCH --job-name=BD_Name_OBO
#SBATCH --output=./logs/%A_%a_out.txt
#SBATCH --error=./logs/%A_%a_err.txt
#SBATCH --array=1-3
#SBATCH --ntasks=1
#SBATCH --time=20:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --mail-user=ximing.ran@emory.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --partition=day-long-cpu,month-long-cpu,week-long-cpu,largemem,encore,encore-gpu

cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder/Experiment/01-Refernce_free/02-Name_structure
# conda init
conda activate openai

# Define temperatures corresponding to array indices
temps=(0.1 0.5 0.9)
TEMP=${temps[$((SLURM_ARRAY_TASK_ID - 1))]}

python 02-Name_structure-temp.py --temp $TEMP