#!/bin/bash

cd /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder
conda activate openai

#----------------------------------------------------------------#
#-------------- Case Study 1: AD in the BioDomain  --------------#
#----------------------------------------------------------------#

# LLM model 1: ChatGPT
mkdir -p Experiment_summary/01-AD/chatgpt

# Step 1: Run experiments with different prompts and temperatures
# details are in the .source/chatgpt folder, following code just turns the results into a json file

# Prompt 1: GO term name
### write 5418 annotations to the json file
# Temperature 0.0
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/01-Refernce_free/01-Name/biodomain_results_top5_0630.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_temperature_0.0.json'

# Temperature 0.1
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_0.1.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_temperature_0.1.json'

# Temperature 0.5
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_0.5.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_temperature_0.5.json'

# Temperature 0.9
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_0.9.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_temperature_0.9.json'

# Temperature 0.0 but allow the Unknown GO terms
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_Unknown.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_temperature_0.0_unknown.json'


# Prompt 2: GO term name + GO term structure
### write 5418 annotations to the json file
# Temperature 0.0
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/01-Refernce_free/02-Name_structure/biodomain_results_top5_with_structure_0630.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_temperature_0.0.json'


# Temperature 0.1
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/01-Refernce_free/02-Name_structure/result/biodomain_results_top5_with_structure_0.1.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_temperature_0.1.json'

# Temperature 0.5
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/01-Refernce_free/02-Name_structure/result/biodomain_results_top5_with_structure_0.5.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_temperature_0.5.json'

# Temperature 0.9
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/01-Refernce_free/02-Name_structure/result/biodomain_results_top5_with_structure_0.9.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_temperature_0.9.json'


# Temperature 0.0 but allow the Unknown GO terms
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/01-Refernce_free/02-Name_structure/result/biodomain_results_top5_with_structure_unknown.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_temperature_0.0_unknown.json' 


# Prompt 3: GO term name + GO term structure + GO term similarity
### write 5418 annotations to the json file
# Temperature 0.0
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/01-Refernce_free/03-Name_structure_similarity/biodomain_results_top5_with_similarity_0630.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_similarity_temperature_0.0.json'  

# Temperature 0.1
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/01-Refernce_free/03-Name_structure_similarity/result/biodomain_results_top5_with_similarity_0.1.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_similarity_temperature_0.1.json'

# Temperature 0.5
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/01-Refernce_free/03-Name_structure_similarity/result/biodomain_results_top5_with_similarity_0.5.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_similarity_temperature_0.5.json'
  
# Temperature 0.9
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/01-Refernce_free/03-Name_structure_similarity/result/biodomain_results_top5_with_similarity_0.9.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_similarity_temperature_0.9.json'

# Temperature 0.0 but allow the Unknown GO terms
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/01-Refernce_free/03-Name_structure_similarity/result/biodomain_results_top5_with_similarity_unknown.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_similarity_temperature_0.0_unknown.json'


# Prompt 4: GO term name + AD disease introduction
# Temperature 0.0
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/ChatGPT/02-AD/Temp_0.0/go_biodomain_results_0.0.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_AD_temperature_0.0.json'


# Temperature 0.1
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/ChatGPT/02-AD/Temp_0.1/go_biodomain_results_0.1.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_AD_temperature_0.1.json'

# Temperature 0.5
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/ChatGPT/02-AD/Temp_0.5/go_biodomain_results_0.5.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_AD_temperature_0.5.json'

# Temperature 0.9
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/ChatGPT/02-AD/Temp_0.9/go_biodomain_results_0.9.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_AD_temperature_0.9.json'

# Temperature 0.0 but allow the Unknown GO terms
python -m baselines.convert_biodomain \
  --true_csv './data/AD_Biological_Domain_GO_annotate.csv' \
  --pred_csv './Experiment/ChatGPT/02-AD/Unknown_Temp_0.0/go_biodomain_results_0.0.csv' \
  --out_json './Experiment_summary/01-AD/chatgpt/chatgpt_name_AD_temperature_0.0_unknown.json'


# Step 2: Evaluate the results
## Prompt 1: GO term name
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_temperature_0.0.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_temperature_0.0_leaderboard.csv' \
    --method_name 'chatgpt_name_temperature_0.0'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_temperature_0.1.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_temperature_0.1_leaderboard.csv' \
    --method_name 'chatgpt_name_temperature_0.1'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_temperature_0.5.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_temperature_0.5_leaderboard.csv' \
    --method_name 'chatgpt_name_temperature_0.5'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_temperature_0.9.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_temperature_0.9_leaderboard.csv' \
    --method_name 'chatgpt_name_temperature_0.9'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_temperature_0.0_unknown.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_temperature_0.0_unknown_leaderboard.csv' \
    --method_name 'chatgpt_name_temperature_0.0_unknown'  

## Prompt 2: GO term name + GO term structure
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_temperature_0.0.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_temperature_0.0_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_temperature_0.0'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_temperature_0.1.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_temperature_0.1_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_temperature_0.1'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_temperature_0.5.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_temperature_0.5_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_temperature_0.5'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_temperature_0.9.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_temperature_0.9_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_temperature_0.9'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_temperature_0.0_unknown.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_temperature_0.0_unknown_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_temperature_0.0_unknown'


## Prompt 3: GO term name + GO term structure + GO term similarity
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_similarity_temperature_0.0.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_similarity_temperature_0.0_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_similarity_temperature_0.0'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_similarity_temperature_0.1.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_similarity_temperature_0.1_leaderboard.csv'
    --method_name 'chatgpt_name_structure_similarity_temperature_0.1'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_similarity_temperature_0.5.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_similarity_temperature_0.5_leaderboard.csv'
    --method_name 'chatgpt_name_structure_similarity_temperature_0.5'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_similarity_temperature_0.9.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_similarity_temperature_0.9_leaderboard.csv'
    --method_name 'chatgpt_name_structure_similarity_temperature_0.9'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_similarity_temperature_0.0_unknown.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_structure_similarity_temperature_0.0_unknown_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_similarity_temperature_0.0_unknown' 

## Prompt 4: GO term name + AD disease introduction
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_AD_temperature_0.0.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_AD_temperature_0.0_leaderboard.csv' \
    --method_name 'chatgpt_name_AD_temperature_0.0'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_AD_temperature_0.1.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_AD_temperature_0.1_leaderboard.csv' \
    --method_name 'chatgpt_name_AD_temperature_0.1'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_AD_temperature_0.5.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_AD_temperature_0.5_leaderboard.csv' \
    --method_name 'chatgpt_name_AD_temperature_0.5'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_AD_temperature_0.9.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_AD_temperature_0.9_leaderboard.csv' \
    --method_name 'chatgpt_name_AD_temperature_0.9'
python -m baselines.eval eval \
    --result_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_AD_temperature_0.0_unknown.json' \
    --leaderboard_path './Experiment_summary/01-AD/chatgpt/chatgpt_name_AD_temperature_0.0_unknown_leaderboard.csv' \
    --method_name 'chatgpt_name_AD_temperature_0.0_unknown'

  




#-----------------------------------------------------------------#
#-------------- Case Study 2: FXS in the BioDomain  --------------#
#-----------------------------------------------------------------#
mkdir -p Experiment_summary/02-FXS/chatgpt

# Prompt 1: GO term name
### write 516 annotations to the json file
# Temperature 0.0
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/01-Ref-Free/01-Name/Temp_0.0/go_biodomain_results_0.0.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_temperature_0.0.json'

# Temperature 0.1
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/01-Ref-Free/01-Name/Temp_0.1/go_biodomain_results_0.1.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_temperature_0.1.json'

# Temperature 0.5
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/01-Ref-Free/01-Name/Temp_0.5/go_biodomain_results_0.5.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_temperature_0.5.json'

# Temperature 0.9
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/01-Ref-Free/01-Name/Temp_0.9/go_biodomain_results_0.9.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_temperature_0.9.json'

# Temperature 0.0 but allow the Unknown GO terms
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/01-Ref-Free/01-Name/Unknown_0.0/go_biodomain_results_0.0.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_temperature_0.0_unknown.json'

# Prompt 2: GO term name + GO term structure
### write 516 annotations to the json file
# Temperature 0.0
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/01-Ref-Free/02-Name-OBO/Temp_0.0/go_biodomain_results_0.0.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_temperature_0.0.json'

# Temperature 0.1
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/01-Ref-Free/02-Name-OBO/Temp_0.1/go_biodomain_results_0.1.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_temperature_0.1.json'

# Temperature 0.5
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/01-Ref-Free/02-Name-OBO/Temp_0.5/go_biodomain_results_0.5.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_temperature_0.5.json'    

# Temperature 0.9
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/01-Ref-Free/02-Name-OBO/Temp_0.9/go_biodomain_results_0.9.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_temperature_0.9.json'    

# Temperature 0.0 but allow the Unknown GO terms
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/01-Ref-Free/02-Name-OBO/Unknown_0.0/go_biodomain_results_0.0.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_temperature_0.0_unknown.json'  


# Prompt 3: GO term name + GO term structure + GO term similarity
### write 516 annotations to the json file
# Temperature 0.0
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/01-Ref-Free/03-Name-OBO-Similarity/Temp_0.0/go_biodomain_results_0.0.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_similarity_temperature_0.0.json'

# Temperature 0.1
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/01-Ref-Free/03-Name-OBO-Similarity/Temp_0.1/go_biodomain_results_0.1.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_similarity_temperature_0.1.json'       

# Temperature 0.5
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/01-Ref-Free/03-Name-OBO-Similarity/Temp_0.5/go_biodomain_results_0.5.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_similarity_temperature_0.5.json'

# Temperature 0.9
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/01-Ref-Free/03-Name-OBO-Similarity/Temp_0.9/go_biodomain_results_0.9.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_similarity_temperature_0.9.json'     

# Temperature 0.0 but allow the Unknown GO terms
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/01-Ref-Free/03-Name-OBO-Similarity/Unknown_0.0/go_biodomain_results_0.0.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_similarity_temperature_0.0_unknown.json' 


# Prompt 4: GO term name + FXS disease introduction
# Temperature 0.0
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/03-FXS_v2/Temp_0.0/go_biodomain_results_0.0.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_FXS_temperature_0.0.json'

# Temperature 0.1
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/03-FXS_v2/Temp_0.1/go_biodomain_results_0.1.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_FXS_temperature_0.1.json'

# Temperature 0.5
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/03-FXS_v2/Temp_0.5/go_biodomain_results_0.5.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_FXS_temperature_0.5.json'

# Temperature 0.9
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/03-FXS_v2/Temp_0.9/go_biodomain_results_0.9.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_FXS_temperature_0.9.json' 

# Temperature 0.0 but allow the Unknown GO terms
python -m baselines.convert_biodomain \
  --true_csv './data/FXS_bidomain_annotation_certain.csv' \
  --pred_csv './Experiment/ChatGPT/03-FXS_v2/Unknown_Temp_0.0/go_biodomain_results_0.0.csv' \
  --out_json './Experiment_summary/02-FXS/chatgpt/chatgpt_name_FXS_temperature_0.0_unknown.json'

# Step 2: Evaluate the results
## Prompt 1: GO term name
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_temperature_0.0.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_temperature_0.0_leaderboard.csv' \
    --method_name 'chatgpt_name_temperature_0.0'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_temperature_0.1.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_temperature_0.1_leaderboard.csv' \
    --method_name 'chatgpt_name_temperature_0.1'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_temperature_0.5.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_temperature_0.5_leaderboard.csv' \
    --method_name 'chatgpt_name_temperature_0.5'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_temperature_0.9.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_temperature_0.9_leaderboard.csv' \
    --method_name 'chatgpt_name_temperature_0.9'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_temperature_0.0_unknown.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_temperature_0.0_unknown_leaderboard.csv' \
    --method_name 'chatgpt_name_temperature_0.0_unknown'  

## Prompt 2: GO term name + GO term structure
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_temperature_0.0.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_temperature_0.0_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_temperature_0.0'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_temperature_0.1.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_temperature_0.1_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_temperature_0.1'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_temperature_0.5.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_temperature_0.5_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_temperature_0.5'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_temperature_0.9.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_temperature_0.9_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_temperature_0.9'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_temperature_0.0_unknown.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_temperature_0.0_unknown_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_temperature_0.0_unknown'  

## Prompt 3: GO term name + GO term structure + GO term similarity
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_similarity_temperature_0.0.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_similarity_temperature_0.0_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_similarity_temperature_0.0'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_similarity_temperature_0.1.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_similarity_temperature_0.1_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_similarity_temperature_0.1'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_similarity_temperature_0.5.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_similarity_temperature_0.5_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_similarity_temperature_0.5'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_similarity_temperature_0.9.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_similarity_temperature_0.9_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_similarity_temperature_0.9'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_similarity_temperature_0.0_unknown.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_structure_similarity_temperature_0.0_unknown_leaderboard.csv' \
    --method_name 'chatgpt_name_structure_similarity_temperature_0.0_unknown' 

## Prompt 4: GO term name + FXS disease introduction
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_FXS_temperature_0.0.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_FXS_temperature_0.0_leaderboard.csv' \
    --method_name 'chatgpt_name_FXS_temperature_0.0'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_FXS_temperature_0.1.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_FXS_temperature_0.1_leaderboard.csv' \
    --method_name 'chatgpt_name_FXS_temperature_0.1'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_FXS_temperature_0.5.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_FXS_temperature_0.5_leaderboard.csv' \
    --method_name 'chatgpt_name_FXS_temperature_0.5'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_FXS_temperature_0.9.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_FXS_temperature_0.9_leaderboard.csv' \
    --method_name 'chatgpt_name_FXS_temperature_0.9'
python -m baselines.eval eval \
    --result_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_FXS_temperature_0.0_unknown.json' \
    --leaderboard_path './Experiment_summary/02-FXS/chatgpt/chatgpt_name_FXS_temperature_0.0_unknown_leaderboard.csv' \
    --method_name 'chatgpt_name_FXS_temperature_0.0_unknown'