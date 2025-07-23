#!/bin/bash
set -euo pipefail


chmod +x ./source/deepseek/deepseek_combination.py 


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





# Only use tree to search for the files named "go_biodomain_results.csv"
tree Experiment/DeepSeek/01-Reference_free -P go_biodomain_results.csv -






# ground‑truth annotation files
TRUE_AD_CSV="data/AD_Biological_Domain_GO_annotate.csv"
TRUE_FXS_CSV="data/FXS_Biological_Domain_GO_annotate.csv"
ROOT="Experiment/DeepSeek/01-Reference_free"

find "$ROOT" -type f -name go_biodomain_results.csv | while read -r PRED_CSV; do
  DIR=$(dirname "$PRED_CSV")
  STAGE=$(basename "$(dirname "$DIR")")   # e.g. "01-Name" or "04-AD_temp" or "05-FXS"
  SUB=$(basename "$DIR")                  # e.g. "Temp_0", "Unknown_0"
  
  # choose the correct true_csv
  if [[ "$STAGE" == *FXS* ]]; then
    TRUE_CSV="$TRUE_FXS_CSV"
  else
    TRUE_CSV="$TRUE_AD_CSV"
  fi

  OUT_JSON="$DIR/go_biodomain_results.json"
  LB_CSV="$DIR/go_biodomain_leaderboard.csv"
  METHOD="DeepSeek_${STAGE}_${SUB}"

  echo "=== $STAGE / $SUB → $METHOD ==="

  python -m baselines.convert_biodomain \
    --true_csv "$TRUE_CSV" \
    --pred_csv "$PRED_CSV" \
    --out_json "$OUT_JSON"

  python -m baselines.eval eval \
    --result_path      "$OUT_JSON" \
    --leaderboard_path "$LB_CSV" \
    --method_name      "$METHOD"
done


cd Experiment/DeepSeek/01-Reference_free

# write header from the first file
first=$(find . -type f -name go_biodomain_leaderboard.csv | head -n1)
head -n1 "$first" > merged_go_biodomain_leaderboard.csv

# append all data rows (skip each file’s header)
find . -type f -name go_biodomain_leaderboard.csv \
  -exec awk 'FNR>1' {} + >> merged_go_biodomain_leaderboard.csv

echo "Merged into merged_go_biodomain_leaderboard.csv"
