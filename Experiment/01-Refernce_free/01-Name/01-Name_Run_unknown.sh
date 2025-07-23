#!/bin/bash
#SBATCH --job-name=BD_Name
#SBATCH --output=./logs/Unknown_%A_out.txt
#SBATCH --error=./logs/Unknown_%A_err.txt
#SBATCH --array=1
#SBATCH --ntasks=1
#SBATCH --time=20:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --mail-user=ximing.ran@emory.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --partition=day-long-cpu,month-long-cpu,week-long-cpu,largemem,encore,encore-gpu

cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder/Experiment/01-Refernce_free/01-Name

# conda init
conda activate openai

python 01-Name-unknown.py 