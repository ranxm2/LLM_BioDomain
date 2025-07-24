#!/bin/bash

cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder
conda activate openai
set -euo pipefail


chmod +x ./source/deepseek/deepseek_combination.py 

#----------------------------------------------------------------#
#-------------- Case Study 1: AD in the BioDomain  --------------#
#----------------------------------------------------------------#

BASE="Experiment/DeepSeek/01-Reference_free"
# for each sub‐stage (01-Name, 02-Name_structure, …)
for STAGE in "$BASE"/*; do
  [ -d "$STAGE" ] || continue

  # for each Temp_* or Unknown_* folder
  for F in "$STAGE"/*; do
    [ -d "$F" ] || continue
    echo "=== Merging in $F ==="
    ./source/deepseek/deepseek_combination.py "$F"
  done
done


# LLM model 2: DeepSeek
mkdir -p Experiment_summary/01-AD/deepseek



TRUE_CSV="./data/AD_Biological_Domain_GO_annotate.csv"
BASE_PRED_DIR="./Experiment/DeepSeek/01-Reference_free"
SUMMARY_DIR="./Experiment_summary/01-AD/deepseek"
mkdir -p "${SUMMARY_DIR}"

declare -A PROMPTS=(
  ["01-Name"]="deepseek_name"
  ["02-Name_structure"]="deepseek_name_structure"
  ["03-Name_structure_similarity"]="deepseek_name_structure_similarity"
  ["04-AD_temp"]="deepseek_AD_temp"
)

TEMPS=("0" "0.1" "0.5" "0.9")

get_temp_dir(){
  local dir="$1" t="$2"
  if [[ "$t" == "0" ]]; then
    if [[ "$dir" == "01-Name" || "$dir" == "02-Name_structure" ]]; then
      echo "Temp_0"
    else
      echo "Temp_0.0"
    fi
  else
    echo "Temp_${t}"
  fi
}

get_unknown_dir(){
  local dir="$1"
  if [[ "$dir" == "01-Name" || "$dir" == "02-Name_structure" ]]; then
    echo "Unknown_0"
  else
    echo "Unknown_Temp_0.0"
  fi
}

# 1) convert → JSON
for DIR in "${!PROMPTS[@]}"; do
  PREFIX="${PROMPTS[$DIR]}"

  for T in "${TEMPS[@]}"; do
    SUBDIR=$(get_temp_dir "$DIR" "$T")
    # force the output-label to be "0.0" when T is "0"
    LABEL="${T}"
    [[ "$T" == "0" ]] && LABEL="0.0"

    PRED_CSV="${BASE_PRED_DIR}/${DIR}/${SUBDIR}/go_biodomain_results.csv"
    OUT_JSON="${SUMMARY_DIR}/${PREFIX}_temperature_${LABEL}.json"

    echo "[convert] ${DIR} @ Temp ${T} → summary uses ${LABEL}"
    python -m baselines.convert_biodomain \
      --true_csv "${TRUE_CSV}" \
      --pred_csv "${PRED_CSV}" \
      --out_json "${OUT_JSON}"
  done

  UNKNOWN_SUB=$(get_unknown_dir "$DIR")
  PRED_CSV="${BASE_PRED_DIR}/${DIR}/${UNKNOWN_SUB}/go_biodomain_results.csv"
  OUT_JSON="${SUMMARY_DIR}/${PREFIX}_temperature_0.0_unknown.json"

  echo "[convert] ${DIR} @ Unknown → summary uses 0.0_unknown"
  python -m baselines.convert_biodomain \
    --true_csv "${TRUE_CSV}" \
    --pred_csv "${PRED_CSV}" \
    --out_json "${OUT_JSON}"
done

# 2) eval → leaderboard CSVs

echo "=== Evaluating all DeepSeek methods for AD ==="
set -euo pipefail

SUMMARY_DIR="./Experiment_summary/01-AD/deepseek"

echo "=== Evaluating all DeepSeek methods for AD (auto) ==="
for RESULT_JSON in "${SUMMARY_DIR}"/*.json; do
  BASENAME=$(basename "${RESULT_JSON}" .json)
  LB_CSV="${SUMMARY_DIR}/${BASENAME}_leaderboard.csv"

  echo "[eval] ${BASENAME}"
  python -m baselines.eval eval \
    --result_path "${RESULT_JSON}" \
    --leaderboard_path "${LB_CSV}" \
    --method_name "${BASENAME}"
done



#-----------------------------------------------------------------#
#-------------- Case Study 2: FXS in the BioDomain  --------------#
#-----------------------------------------------------------------#
# LLM model 2: DeepSeek
mkdir -p Experiment_summary/02-FXS/deepseek

# Now Loop through the results and convert them to JSON and CSV
BASE="./Experiment/DeepSeek/02-FXS"
for STAGE in "$BASE"/*; do
  [ -d "$STAGE" ] || continue

  # for each Temp_* or Unknown_* folder
  for F in "$STAGE"/*; do
    [ -d "$F" ] || continue
    echo "=== Merging in $F ==="
    ./source/deepseek/deepseek_combination.py "$F"
  done
done


#!/usr/bin/env bash

cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder
conda activate openai


#!/usr/bin/env bash
set -euo pipefail

#── Config ──────────────────────────────────────────────────────#
TRUE_CSV="./data/FXS_bidomain_annotation_certain.csv"
BASE_PRED_DIR="./Experiment/DeepSeek/02-FXS"
SUMMARY_DIR="./Experiment_summary/02-FXS/deepseek"

mkdir -p "${SUMMARY_DIR}"

# map prompt‑dirs to method_name prefixes
declare -A PREFIXES=(
  ["01-Name"]="deepseek_name"
  ["02-Name_structure"]="deepseek_name_structure"
  ["03-Name_structure_similarity"]="deepseek_name_structure_similarity"
  ["04-FXS"]="deepseek_FXS"
)

#── 1) convert all go_biodomain_results.csv → JSON ────────────────#
for PROMPT in "${!PREFIXES[@]}"; do
  PREFIX="${PREFIXES[$PROMPT]}"
  for SUB in "${BASE_PRED_DIR}/${PROMPT}"/*; do
    SUBDIR=$(basename "$SUB")

    # determine label: Temp_* → use the suffix; Unknown_* → "0.0_unknown"
    if [[ "$SUBDIR" == Temp_* ]]; then
      LABEL="${SUBDIR#Temp_}"
    else
      LABEL="0.0_unknown"
    fi

    PRED_CSV="${BASE_PRED_DIR}/${PROMPT}/${SUBDIR}/go_biodomain_results.csv"
    OUT_JSON="${SUMMARY_DIR}/${PREFIX}_temperature_${LABEL}.json"

    echo "[convert] ${PROMPT} / ${SUBDIR} → ${LABEL}"
    python -m baselines.convert_biodomain \
      --true_csv "${TRUE_CSV}" \
      --pred_csv "${PRED_CSV}" \
      --out_json "${OUT_JSON}"
  done
done

#── 2) evaluate every JSON → leaderboard.csv ───────────────────────#
echo
echo "=== Evaluating all DeepSeek FXS methods ==="
for RESULT_JSON in "${SUMMARY_DIR}"/*.json; do
  BASENAME=$(basename "$RESULT_JSON" .json)
  LB_CSV="${SUMMARY_DIR}/${BASENAME}_leaderboard.csv"

  echo "[eval] ${BASENAME}"
  python -m baselines.eval eval \
    --result_path "${RESULT_JSON}" \
    --leaderboard_path "${LB_CSV}" \
    --method_name "${BASENAME}"
done
