#!/bin/bash
#SBATCH --job-name=Gemini-N_O
#SBATCH --output=../logs/ref-free-Name-structure-%A_%a_out.txt
#SBATCH --error=../logs/ref-free-Name-structure-%A_%a_err.txt
#SBATCH --array=1-80
#SBATCH --ntasks=1
#SBATCH --time=20:00:00
#SBATCH --mail-user=ximing.ran@emory.edu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --partition=day-long-cpu,month-long-cpu,week-long-cpu,largemem,encore,encore-gpu

# cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder/source/gemini/Run_sh
cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder

conda activate openai

# Define temperatures
temps=(0.0 0.1 0.5 0.9)

# Determine index group: each temp uses 20 array jobs
group_size=20
group_id=$(( (SLURM_ARRAY_TASK_ID - 1) / group_size ))
TEMP=${temps[$group_id]}

# Calculate sub-array index for this temperature
sub_array_index=$(( (SLURM_ARRAY_TASK_ID - 1) % group_size + 1 ))

# Echo the temperature and sub-array index for debugging
echo "Running with TEMP=${TEMP}, sub_array_index=${sub_array_index}"

python ./source/gemini/gemini_biodomain_name_structure_temp.py \
    --key_path keys/gemini_key.txt \
    --df_go_path data/go_root_paths.csv \
    --obo_path data/go-basic.obo \
    --similarity_path data/go_jaccard_long_filtered.csv \
    --result_dir Experiment/Gemini/01-Reference_free/02-Name_structure/Temp_${TEMP} \
    --work_dir /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder \
    --array_index ${sub_array_index} \
    --temperature ${TEMP} \
