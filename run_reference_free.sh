#!/bin/bash

# With Name only
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/01-Refernce_free/01-Name/biodomain_results_top5_0630.csv \
  --out_json Experiment/01-Refernce_free/01-Name/01-Name-combined.json

python -m baselines.eval eval \
  --result_path './Experiment/01-Refernce_free/01-Name/01-Name-combined.json' \
  --leaderboard_path './Experiment/01-Refernce_free/01-Name/Name_leaderboard.csv' \
  --method_name 'Reference_free_Name' 



# With Name and Structure
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/01-Refernce_free/02-Name_structure/biodomain_results_top5_with_structure_0630.csv \
  --out_json Experiment/01-Refernce_free/02-Name_structure/02-Name_structure-combined.json


python -m baselines.eval eval \
  --result_path './Experiment/01-Refernce_free/02-Name_structure/02-Name_structure-combined.json' \
  --leaderboard_path './Experiment/01-Refernce_free/02-Name_structure/Name_structure_leaderboard.csv' \
  --method_name 'Reference_free_Name_structure'



# With Name and Structure Similarity

python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/01-Refernce_free/03-Name_structure_similarity/biodomain_results_top5_with_similarity_0630.csv \
  --out_json Experiment/01-Refernce_free/03-Name_structure_similarity/03-Name_structure_similarity-combined.json

python -m baselines.eval eval \
  --result_path './Experiment/01-Refernce_free/03-Name_structure_similarity/03-Name_structure_similarity-combined.json' \
  --leaderboard_path './Experiment/01-Refernce_free/03-Name_structure_similarity/Name_structure_similarity_leaderboard.csv' \
  --method_name 'Reference_free_Name_structure_similarity'


# Use the AD as reference