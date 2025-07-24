#!/bin/bash
cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder
# Check result on AD data

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


# With Name only, allowing Unknown GO terms
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_Unknown.csv \
  --out_json Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_Unknown.json


python -m baselines.eval eval \
  --result_path './Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_Unknown.json' \
  --leaderboard_path './Experiment/01-Refernce_free/01-Name/Name_leaderboard_Unknown.csv' \
  --method_name 'Reference_free_Name' 

# With Name only, temp 0.1
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_0.1.csv \
  --out_json Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_0.1.json


python -m baselines.eval eval \
  --result_path './Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_0.1.json' \
  --leaderboard_path './Experiment/01-Refernce_free/01-Name/Name_leaderboard_0.1.csv' \
  --method_name 'Reference_free_Name_0.1'

# With Name only, temp 0.5
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_0.5.csv \
  --out_json Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_0.5.json

python -m baselines.eval eval \
  --result_path './Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_0.5.json' \
  --leaderboard_path './Experiment/01-Refernce_free/01-Name/Name_leaderboard_0.5.csv' \
  --method_name 'Reference_free_Name_0.5'


# With Name only, temp 0.9
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_0.9.csv \
  --out_json Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_0.9.json

python -m baselines.eval eval \
  --result_path './Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_0.9.json' \
  --leaderboard_path './Experiment/01-Refernce_free/01-Name/Name_leaderboard_0.9.csv' \
  --method_name 'Reference_free_Name_0.9'




# With Name and Structure, allowing Unknown GO terms
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/01-Refernce_free/02-Name_structure/result/biodomain_results_top5_with_structure_unknown.csv \
  --out_json Experiment/01-Refernce_free/02-Name_structure/result/biodomain_results_top5_with_structure_unknown.json

python -m baselines.eval eval \
  --result_path './Experiment/01-Refernce_free/02-Name_structure/result/biodomain_results_top5_with_structure_unknown.json' \
  --leaderboard_path './Experiment/01-Refernce_free/02-Name_structure/result/Name_structure_leaderboard_Unknown.csv' \
  --method_name 'Reference_free_Name_structure'

# With Name and Structure, temp 0.1
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/01-Refernce_free/02-Name_structure/result/biodomain_results_top5_with_structure_0.1.csv \
  --out_json Experiment/01-Refernce_free/02-Name_structure/result/biodomain_results_top5_with_structure_0.1.json  

python -m baselines.eval eval \
  --result_path './Experiment/01-Refernce_free/02-Name_structure/result/biodomain_results_top5_with_structure_0.1.json' \
  --leaderboard_path './Experiment/01-Refernce_free/02-Name_structure/result/Name_structure_leaderboard_0.1.csv' \
  --method_name 'Reference_free_Name_structure_0.1'

  # With Name and Structure, temp 0.5
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/01-Refernce_free/02-Name_structure/result/biodomain_results_top5_with_structure_0.5.csv \
  --out_json Experiment/01-Refernce_free/02-Name_structure/result/biodomain_results_top5_with_structure_0.5.json

python -m baselines.eval eval \
  --result_path './Experiment/01-Refernce_free/02-Name_structure/result/biodomain_results_top5_with_structure_0.5.json' \
  --leaderboard_path './Experiment/01-Refernce_free/02-Name_structure/result/Name_structure_leaderboard_0.5.csv' \
  --method_name 'Reference_free_Name_structure_0.5'

  # With Name and Structure, temp 0.9
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/01-Refernce_free/02-Name_structure/result/biodomain_results_top5_with_structure_0.9.csv \
  --out_json Experiment/01-Refernce_free/02-Name_structure/result/biodomain_results_top5_with_structure_0.9.json  

python -m baselines.eval eval \
  --result_path './Experiment/01-Refernce_free/02-Name_structure/result/biodomain_results_top5_with_structure_0.9.json' \
  --leaderboard_path './Experiment/01-Refernce_free/02-Name_structure/result/Name_structure_leaderboard_0.9.csv' \
  --method_name 'Reference_free_Name_structure_0.9'


  # With Name and Structure Similarity, allowing Unknown GO terms
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/01-Refernce_free/03-Name_structure_similarity/result/biodomain_results_top5_with_similarity_unknown.csv \
  --out_json Experiment/01-Refernce_free/03-Name_structure_similarity/result/biodomain_results_top5_with_similarity_unknown.json  

python -m baselines.eval eval \
  --result_path './Experiment/01-Refernce_free/03-Name_structure_similarity/result/biodomain_results_top5_with_similarity_unknown.json' \
  --leaderboard_path './Experiment/01-Refernce_free/03-Name_structure_similarity/result/Name_structure_similarity_leaderboard_Unknown.csv' \
  --method_name 'Reference_free_Name_structure_similarity'



# With Name and Structure Similarity, temp 0.1
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/01-Refernce_free/03-Name_structure_similarity/result/biodomain_results_top5_with_similarity_0.1.csv \
  --out_json Experiment/01-Refernce_free/03-Name_structure_similarity/result/biodomain_results_top5_with_similarity_0.1.json

python -m baselines.eval eval \
  --result_path './Experiment/01-Refernce_free/03-Name_structure_similarity/result/biodomain_results_top5_with_similarity_0.1.json' \
  --leaderboard_path './Experiment/01-Refernce_free/03-Name_structure_similarity/result/Name_structure_similarity_leaderboard_0.1.csv' \
  --method_name 'Reference_free_Name_structure_similarity_0.1'



# With Name and Structure Similarity, temp 0.5
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/01-Refernce_free/03-Name_structure_similarity/result/biodomain_results_top5_with_similarity_0.5.csv \
  --out_json Experiment/01-Refernce_free/03-Name_structure_similarity/result/biodomain_results_top5_with_similarity_0.5.json
python -m baselines.eval eval \
  --result_path './Experiment/01-Refernce_free/03-Name_structure_similarity/result/biodomain_results_top5_with_similarity_0.5.json' \
  --leaderboard_path './Experiment/01-Refernce_free/03-Name_structure_similarity/result/Name_structure_similarity_leaderboard_0.5.csv' \
  --method_name 'Reference_free_Name_structure_similarity_0.5'

# With Name and Structure Similarity, temp 0.9
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/01-Refernce_free/03-Name_structure_similarity/result/biodomain_results_top5_with_similarity_0.9.csv \
  --out_json Experiment/01-Refernce_free/03-Name_structure_similarity/result/biodomain_results_top5_with_similarity_0.9.json
python -m baselines.eval eval \
  --result_path './Experiment/01-Refernce_free/03-Name_structure_similarity/result/biodomain_results_top5_with_similarity_0.9.json' \
  --leaderboard_path './Experiment/01-Refernce_free/03-Name_structure_similarity/result/Name_structure_similarity_leaderboard_0.9.csv' \
  --method_name 'Reference_free_Name_structure_similarity_0.9'



  # Now do for the AD data in Experiment/ChatGPT/02-AD/Temp_0.0/go_biodomain_results_0.0.csv 
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/ChatGPT/02-AD/Temp_0.0/go_biodomain_results_0.0.csv \
  --out_json Experiment/ChatGPT/02-AD/Temp_0.0/go_biodomain_results_0.0.json
python -m baselines.eval eval \
  --result_path './Experiment/ChatGPT/02-AD/Temp_0.0/go_biodomain_results_0.0.json' \
  --leaderboard_path './Experiment/ChatGPT/02-AD/Temp_0.0/go_biodomain_leaderboard_0.0.csv' \
  --method_name 'ChatGPT_AD_0.0'

# Temp 0.1
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/ChatGPT/02-AD/Temp_0.1/go_biodomain_results_0.1.csv \
  --out_json Experiment/ChatGPT/02-AD/Temp_0.1/go_biodomain_results_0.1.json
python -m baselines.eval eval \
  --result_path './Experiment/ChatGPT/02-AD/Temp_0.1/go_biodomain_results_0.1.json' \
  --leaderboard_path './Experiment/ChatGPT/02-AD/Temp_0.1/go_biodomain_leaderboard_0.1.csv' \
  --method_name 'ChatGPT_AD_0.1'

# Temp 0.5
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/ChatGPT/02-AD/Temp_0.5/go_biodomain_results_0.5.csv \
  --out_json Experiment/ChatGPT/02-AD/Temp_0.5/go_biodomain_results_0.5.json
python -m baselines.eval eval \
  --result_path './Experiment/ChatGPT/02-AD/Temp_0.5/go_biodomain_results_0.5.json' \
  --leaderboard_path './Experiment/ChatGPT/02-AD/Temp_0.5/go_biodomain_leaderboard_0.5.csv' \
  --method_name 'ChatGPT_AD_0.5'  

# Temp 0.9
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/ChatGPT/02-AD/Temp_0.9/go_biodomain_results_0.9.csv \
  --out_json Experiment/ChatGPT/02-AD/Temp_0.9/go_biodomain_results_0.9.json
python -m baselines.eval eval \
  --result_path './Experiment/ChatGPT/02-AD/Temp_0.9/go_biodomain_results_0.9.json' \
  --leaderboard_path './Experiment/ChatGPT/02-AD/Temp_0.9/go_biodomain_leaderboard_0.9.csv' \
  --method_name 'ChatGPT_AD_0.9'


# All with Unknown GO terms
python -m baselines.convert_biodomain \
  --true_csv data/AD_Biological_Domain_GO_annotate.csv \
  --pred_csv Experiment/ChatGPT/02-AD/Unknown_Temp_0.0/go_biodomain_results_0.0.csv \
  --out_json Experiment/ChatGPT/02-AD/Unknown_Temp_0.0/go_biodomain_results_0.0.json
python -m baselines.eval eval \
  --result_path './Experiment/ChatGPT/02-AD/Unknown_Temp_0.0/go_biodomain_results_0.0.json' \
  --leaderboard_path './Experiment/ChatGPT/02-AD/Unknown_Temp_0.0/go_biodomain_leaderboard_0.0.csv' \
  --method_name 'ChatGPT_AD_Unknown_0.0'

  