#!/bin/bash
#SBATCH --job-name=ChatGPT_FXS
#SBATCH --output=../logs/FXS_%A_%a_out.txt
#SBATCH --error=../logs/FXS_%A_%a_err.txt
#SBATCH --array=1-4
#SBATCH --ntasks=1
#SBATCH --time=24:00:00
#SBATCH --mail-user=ximing.ran@emory.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --partition=day-long-cpu,month-long-cpu,week-long-cpu,largemem,encore,encore-gpu



# cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder/source/chatgpt/Run_sh
cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder

# Define temperatures corresponding to array indices
temps=(0.0 0.1 0.5 0.9)
TEMP=${temps[$((SLURM_ARRAY_TASK_ID - 1))]}

# Activate environment
conda activate openai

# Run Python script with temperature as argument
python ./source/chatgpt/chatgpt_biodomain_FXS_temp_v2.py \
  --key_path keys/api_keys.txt \
  --df_go_path data/go_root_paths_FXS.csv \
  --obo_path data/go-basic.obo \
  --similarity_path data/go_jaccard_long_filtered.csv \
  --result_dir Experiment/ChatGPT/03-FXS_v2/Temp_${TEMP} \
  --work_dir /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder \
  --temperature ${TEMP}
