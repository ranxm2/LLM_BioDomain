#!/bin/bash
#SBATCH --job-name=BD_4_D154
#SBATCH --output=../logs_FXS/D154_4_samples/Name-%A_%a_out.txt
#SBATCH --error=../logs_FXS/D154_4_samples/Name-%A_%a_err.txt
#SBATCH --array=1-90
#SBATCH --ntasks=1
#SBATCH --time=20:00:00
#SBATCH --mail-user=ximing.ran@emory.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --partition=day-long-cpu,month-long-cpu,week-long-cpu,largemem,encore,encore-gpu

# cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder/source/deepseel_padj_0.1/Run_sh_FXS
cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder

conda activate openai

# Define temperatures
temps=(0.0)

# Determine index group: each temp uses 12 array jobs
group_size=90
group_id=$(( (SLURM_ARRAY_TASK_ID - 1) / group_size ))
TEMP=${temps[$group_id]}

# Calculate sub-array index for this temperature
sub_array_index=$(( (SLURM_ARRAY_TASK_ID - 1) % group_size + 1 ))

# Echo the temperature and sub-array index for debugging
echo "Running with TEMP=${TEMP}, sub_array_index=${sub_array_index}"

# Run the Python script
python ./source/deepseek/deepseek_biodomain_name_temp_v2.py \
  --key_path keys/deepseek_key.txt \
  --df_go_path data/D154-GSVA-padj-0.1_4_samples-node.csv \
  --obo_path data/go-basic.obo \
  --similarity_path data/go_jaccard_long_filtered.csv \
  --result_dir Experiment/DeepSeek/03-FXS-padj-0.1/D154_4_samples/Temp_${TEMP} \
  --array_index ${sub_array_index} \
  --work_dir /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder \
  --temperature ${TEMP}