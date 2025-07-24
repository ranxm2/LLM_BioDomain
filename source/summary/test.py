# change the working directory to the source folder
import os
import sys
import pandas as pd

os.chdir("/projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder")

# check current working directory
print("Current working directory:", os.getcwd())


df_AD = pd.read_csv('data/AD_Biological_Domain_GO_annotate.csv')
df_chatgpt = pd.read_csv('Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_0.5.csv')

# check the overlap of the GO terms
overlap = set(df_AD['GO_ID']).intersection(set(df_chatgpt['nodeID']))
print("Number of overlapping GO terms:", len(overlap))

# keep the overlapping GO terms in the df_AD and save it
df_AD_filtered = df_AD[df_AD['GO_ID'].isin(overlap)]
df_AD_filtered.to_csv('data/AD_Biological_Domain_GO_annotate_filtered.csv', index=False)


# do this for the FXS
df_FXS = pd.read_csv('data/FXS_bidomain_annotation_certain.csv')
df_chatgpt = pd.read_csv('Experiment/01-Refernce_free/01-Name/result/biodomain_results_top5_0.5.csv')

# check the overlap of the GO terms
overlap = set(df_FXS['GO_ID']).intersection(set(df_chatgpt['nodeID']))
print("Number of overlapping GO terms:", len(overlap))

# keep the overlapping GO terms in the df_FXS and save it
df_FXS_filtered = df_FXS[df_FXS['GO_ID'].isin(overlap)]
df_FXS_filtered.to_csv('data/FXS_bidomain_annotation_certain_filtered.csv', index=False)
