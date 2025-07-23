#!/bin/bash
#SBATCH --job-name=BD_Name
#SBATCH --output=../logs/ref-free-Name-unknown-%A_%a_out.txt
#SBATCH --error=../logs/ref-free-Name-unknown-%A_%a_err.txt
#SBATCH --array=1-20
#SBATCH --ntasks=1
#SBATCH --time=20:00:00
#SBATCH --mail-user=ximing.ran@emory.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --partition=day-long-cpu,month-long-cpu,week-long-cpu,largemem,encore,encore-gpu

# cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder/source/deepseek/Run_sh
cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder

conda activate openai

python ./source/deepseek/deepseek_biodomain_name_unknown.py \
 --key_path keys/deepseek_key.txt \
  --df_go_path data/go_root_paths.csv \
  --obo_path data/go-basic.obo \
  --similarity_path data/go_jaccard_long_filtered.csv \
  --result_dir Experiment/DeepSeek/01-Reference_free/01-Name/Unknown_0 \
  --array_index ${SLURM_ARRAY_TASK_ID} \
  --work_dir /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder
