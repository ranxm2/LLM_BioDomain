#!/bin/bash


cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder
conda activate openai

#----------------------------------------------------------------#
#-------------- Case Study 1: AD in the BioDomain  --------------#
#----------------------------------------------------------------#

# mkdir for the AD case study
mkdir -p Experiment_summary/01-AD

# Baseline model 1: Random Ranker
mkdir -p Experiment_summary/01-AD/random_ranker

# Step 1: Run experiments with different seeds
python -m baselines.random_ranker main --seed 42 \
    --output_dir './Experiment_summary/01-AD/random_ranker'
python -m baselines.random_ranker main --seed 27 \
    --output_dir './Experiment_summary/01-AD/random_ranker'
python -m baselines.random_ranker main --seed 2025 \
    --output_dir './Experiment_summary/01-AD/random_ranker'


# Step 2: Evaluate the results
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/random_ranker/seed_42.json' \
    --leaderboard_path './Experiment_summary/01-AD/random_ranker/seed_42_leaderboard.csv' \
    --method_name 'random_seed_42'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/random_ranker/seed_27.json' \
    --leaderboard_path './Experiment_summary/01-AD/random_ranker/seed_27_leaderboard.csv' \
    --method_name 'random_seed_27'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/random_ranker/seed_2025.json' \
    --leaderboard_path './Experiment_summary/01-AD/random_ranker/seed_2025_leaderboard.csv' \
    --method_name 'random_seed_2025'    

# Baseline model 2: Graph Traversal
mkdir -p Experiment_summary/01-AD/graph_traversal
# Step 1: Run experiments with different seeds
python -m baselines.graph_traversal main --seed 42 \
    --output_dir './Experiment_summary/01-AD/graph_traversal'
python -m baselines.graph_traversal main --seed 27 \
    --output_dir './Experiment_summary/01-AD/graph_traversal'
python -m baselines.graph_traversal main --seed 2025 \
    --output_dir './Experiment_summary/01-AD/graph_traversal'


# Step 2: Evaluate the results
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/graph_traversal/seed_42.json' \
    --leaderboard_path './Experiment_summary/01-AD/graph_traversal/seed_42_leaderboard.csv' \
    --method_name 'graph_traversal_random_seed_42'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/graph_traversal/seed_27.json' \
    --leaderboard_path './Experiment_summary/01-AD/graph_traversal/seed_27_leaderboard.csv' \
    --method_name 'graph_traversal_random_seed_27'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/graph_traversal/seed_2025.json' \
    --leaderboard_path './Experiment_summary/01-AD/graph_traversal/seed_2025_leaderboard.csv' \
    --method_name 'graph_traversal_random_seed_2025'



# Model 3: Go similarity
mkdir -p Experiment_summary/01-AD/go_similarity

SIM_PATH="./data/go_jaccard_long_filtered.csv"
DATA_PATH="./data/AD_Biological_Domain_GO_annotate.csv"
BASE_OUT="./Experiment_summary/01-AD/go_similarity"
TOPK=5

for SEED in 42 27 2025; do
  OUT_DIR="${BASE_OUT}"
  mkdir -p "${OUT_DIR}"

  echo "=== Running go_similarity for seed=${SEED} ==="
  python -m baselines.go_similarity \
    --seed "${SEED}" \
    --output_dir "${OUT_DIR}" \
    --similarity_path "${SIM_PATH}" \
    --dataset_path   "${DATA_PATH}" \
    --topk            "${TOPK}"

  echo "=== Evaluating results for seed=${SEED} ==="
  python -m baselines.eval eval \
    --result_path      "${OUT_DIR}/jaccard_seed_${SEED}.json" \
    --leaderboard_path "${OUT_DIR}/jaccard_seed_${SEED}_leaderboard.csv" \
    --method_name      "go_similarity_random_seed_${SEED}"
done


# Model 4: Go similarity search
mkdir -p Experiment_summary/01-AD/go_similarity_search
SIM_PATH="./data/go_jaccard_long_filtered.csv"
DATA_PATH="./data/AD_Biological_Domain_GO_annotate.csv"
BASE_OUT="./Experiment_summary/01-AD/go_similarity_search"
TOPK=5

for SEED in 42 27 2025; do
  OUT_DIR="${BASE_OUT}"
  mkdir -p "${OUT_DIR}"

  echo "=== Running go_similarity_search for seed=${SEED} ==="
  python -m baselines.go_similarity_search \
    --seed "${SEED}" \
    --output_dir "${OUT_DIR}" \
    --similarity_path "${SIM_PATH}" \
    --dataset_path   "${DATA_PATH}" \
    --topk            "${TOPK}"

  echo "=== Evaluating results for seed=${SEED} ==="
  python -m baselines.eval eval \
    --result_path      "${OUT_DIR}/similarity_expansion_seed_${SEED}.json" \
    --leaderboard_path "${OUT_DIR}/similarity_expansion_seed_${SEED}_leaderboard.csv" \
    --method_name      "go_similarity_search_random_seed_${SEED}"
done



#-----------------------------------------------------------------#
#-------------- Case Study 2: FXS in the BioDomain  --------------#
#-----------------------------------------------------------------#

# mkdir for the FXS case study
mkdir -p Experiment_summary/02-FXS

# Baseline model 1: Random Ranker
mkdir -p Experiment_summary/02-FXS/random_ranker

# Step 1: Run experiments with different seeds
python -m baselines.random_ranker main --seed 42 \
    --output_dir './Experiment_summary/02-FXS/random_ranker' \
    --dataset_path './data/FXS_bidomain_annotation_certain.csv'
python -m baselines.random_ranker main --seed 27 \
    --output_dir './Experiment_summary/02-FXS/random_ranker' \
    --dataset_path './data/FXS_bidomain_annotation_certain.csv'
python -m baselines.random_ranker main --seed 2025 \
    --output_dir './Experiment_summary/02-FXS/random_ranker' \
    --dataset_path './data/FXS_bidomain_annotation_certain.csv'

# Step 2: Evaluate the results
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/random_ranker/seed_42.json' \
    --leaderboard_path './Experiment_summary/02-FXS/random_ranker/seed_42_leaderboard.csv' \
    --method_name 'random_seed_42'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/random_ranker/seed_27.json' \
    --leaderboard_path './Experiment_summary/02-FXS/random_ranker/seed_27_leaderboard.csv' \
    --method_name 'random_seed_27'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/random_ranker/seed_2025.json' \
    --leaderboard_path './Experiment_summary/02-FXS/random_ranker/seed_2025_leaderboard.csv' \
    --method_name 'random_seed_2025'






# Baseline model 2: Graph Traversal
mkdir -p Experiment_summary/02-FXS/graph_traversal

# Step 1: Run experiments with different seeds
python -m baselines.graph_traversal_FXS main --seed 42 \
    --output_dir './Experiment_summary/02-FXS/graph_traversal' \
    --dataset_path './data/FXS_bidomain_annotation_certain.csv'
python -m baselines.graph_traversal_FXS main --seed 27 \
    --output_dir './Experiment_summary/02-FXS/graph_traversal' \
    --dataset_path './data/FXS_bidomain_annotation_certain.csv'
python -m baselines.graph_traversal_FXS main --seed 2025 \
    --output_dir './Experiment_summary/02-FXS/graph_traversal' \
    --dataset_path './data/FXS_bidomain_annotation_certain.csv'

# Step 2: Evaluate the results
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/graph_traversal/seed_42.json' \
    --leaderboard_path './Experiment_summary/02-FXS/graph_traversal/seed_42_leaderboard.csv' \
    --method_name 'graph_traversal_random_seed_42'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/graph_traversal/seed_27.json' \
    --leaderboard_path './Experiment_summary/02-FXS/graph_traversal/seed_27_leaderboard.csv' \
    --method_name 'graph_traversal_random_seed_27'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/graph_traversal/seed_2025.json' \
    --leaderboard_path './Experiment_summary/02-FXS/graph_traversal/seed_2025_leaderboard.csv' \
    --method_name 'graph_traversal_random_seed_2025'


# Model 3: Go similarity
mkdir -p Experiment_summary/02-FXS/go_similarity

SIM_PATH="./data/go_jaccard_long_filtered.csv"
DATA_PATH="./data/FXS_bidomain_annotation_certain.csv"
BASE_OUT="./Experiment_summary/02-FXS/go_similarity"
TOPK=5

for SEED in 42 27 2025; do
  OUT_DIR="${BASE_OUT}"
  mkdir -p "${OUT_DIR}"

  echo "=== Running go_similarity_FXS for seed=${SEED} ==="
  python -m baselines.go_similarity \
    --seed "${SEED}" \
    --output_dir "${OUT_DIR}" \
    --similarity_path "${SIM_PATH}" \
    --dataset_path   "${DATA_PATH}" \
    --topk            "${TOPK}"

  echo "=== Evaluating results for seed=${SEED} ==="
  python -m baselines.eval eval \
    --result_path      "${OUT_DIR}/jaccard_seed_${SEED}.json" \
    --leaderboard_path "${OUT_DIR}/jaccard_seed_${SEED}_leaderboard.csv" \
    --method_name      "go_similarity_random_seed_${SEED}"
done


# Model 4: Go similarity search
mkdir -p Experiment_summary/02-FXS/go_similarity_search
SIM_PATH="./data/go_jaccard_long_filtered.csv"
DATA_PATH="./data/FXS_bidomain_annotation_certain.csv"
BASE_OUT="./Experiment_summary/02-FXS/go_similarity_search"
TOPK=5

for SEED in 42 27 2025; do
  OUT_DIR="${BASE_OUT}"
  mkdir -p "${OUT_DIR}"

  echo "=== Running go_similarity_search_FXS for seed=${SEED} ==="
  python -m baselines.go_similarity_search_FXS \
    --seed "${SEED}" \
    --output_dir "${OUT_DIR}" \
    --similarity_path "${SIM_PATH}" \
    --dataset_path   "${DATA_PATH}" \
    --topk            "${TOPK}"

  echo "=== Evaluating results for seed=${SEED} ==="
  python -m baselines.eval eval \
    --result_path      "${OUT_DIR}/similarity_expansion_seed_${SEED}.json" \
    --leaderboard_path "${OUT_DIR}/similarity_expansion_seed_${SEED}_leaderboard.csv" \
    --method_name      "go_similarity_search_random_seed_${SEED}"
done
