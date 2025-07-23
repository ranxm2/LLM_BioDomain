#!/bin/bash
#SBATCH --job-name=DS_FXS_temp_v2
#SBATCH --output=../logs_FXS/04-FXS/FXS-temp-%A_%a_out.txt
#SBATCH --error=../logs_FXS/04-FXS/FXS-temp-%A_%a_err.txt
#SBATCH --array=1-48
#SBATCH --ntasks=1
#SBATCH --time=20:00:00
#SBATCH --mail-user=ximing.ran@emory.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --partition=day-long-cpu,month-long-cpu,week-long-cpu,largemem,encore,encore-gpu

# cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder/source/deepseek/Run_sh
cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder

conda activate openai

# Define temperatures
temps=(0.0 0.1 0.5 0.9)

# Determine index group: each temp uses 20 array jobs
group_size=12
group_id=$(( (SLURM_ARRAY_TASK_ID - 1) / group_size ))
TEMP=${temps[$group_id]}

# Calculate sub-array index for this temperature
sub_array_index=$(( (SLURM_ARRAY_TASK_ID - 1) % group_size + 1 ))

# Echo the temperature and sub-array index for debugging
echo "Running with TEMP=${TEMP}, sub_array_index=${sub_array_index}"


python ./source/deepseek/deepseek_biodomain_FXS_temp_v2.py \
  --key_path keys/deepseek_key.txt \
  --df_go_path data/go_root_paths_FXS.csv \
  --obo_path data/go-basic.obo \
  --similarity_path data/go_jaccard_long_filtered.csv \
  --result_dir Experiment/DeepSeek/02-FXS/04-FXS/Temp_${TEMP} \
  --array_index ${sub_array_index} \
  --work_dir /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder \
  --temperature ${TEMP}