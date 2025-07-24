#!/usr/bin/env bash
cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder
conda activate openai


set -euo pipefail

#──────────────────────────────────────────────────────────────────────────────#
# Merge all CSVs under Experiment_summary into one, adding a "source" column
# indicating the top‐level folder (e.g. 01-AD or 02-FXS) each row came from.
# Output: Experiment_summary/merged_go_biodomain_leaderboard.csv
#──────────────────────────────────────────────────────────────────────────────#

OUT="Experiment_summary/merged_go_biodomain_leaderboard.csv"
# Remove any existing merged file
rm -f "$OUT"

# Find all CSVs under Experiment_summary, excluding the merged output itself
mapfile -t CSV_FILES < <(
  find Experiment_summary -type f -name '*.csv' \
    ! -path "$OUT" | sort
)

if [ ${#CSV_FILES[@]} -eq 0 ]; then
  echo "No CSV files found under Experiment_summary/"
  exit 1
fi

first=1
for FILE in "${CSV_FILES[@]}"; do
  # Determine top‑level folder (e.g. "01-AD" or "02-FXS")
  # Path layout: Experiment_summary/<TOP>/<...>.csv
  TOP=$(echo "$FILE" | cut -d/ -f2)

  if [ $first -eq 1 ]; then
    # Write header + new column name
    head -n1 "$FILE" | awk -F, -v OFS=, '{ print $0, "source" }' > "$OUT"
    first=0
  fi

  # Append data rows with the source column
  tail -n +2 "$FILE" | awk -F, -v OFS=, -v src="$TOP" '{ print $0, src }' >> "$OUT"
done

echo "Merged ${#CSV_FILES[@]} files into $OUT"
