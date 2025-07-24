#!/usr/bin/env python3

import json
import pandas as pd
from pathlib import Path
import os
import sys
import csv
from pathlib import Path


os.chdir("/projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder")


import pandas as pd

# Load your CSV (update the path if necessary)
df = pd.read_csv('./Experiment_summary/merged_go_biodomain.csv')

# 1. Filter out rows with '_unknown'
df = df[~df['method'].str.contains('_unknown')]

# 2. Define metrics
metrics = ['precision@1', 'precision@2', 'recall@1', 'recall@2']

# 3. Extract model prefix function
def extract_prefix(m):
    if m.startswith('chatgpt_name_AD'):
        return 'chatgpt_name_AD'
    if m.startswith('chatgpt_name_FXS'):
        return 'chatgpt_name_FXS'
    if m.startswith('chatgpt_name_structure_similarity'):
        return 'chatgpt_name_structure_similarity'
    if m.startswith('chatgpt_name_structure'):
        return 'chatgpt_name_structure'
    if m.startswith('chatgpt_name_temperature'):
        return 'chatgpt_name'
    if m.startswith('deepseek_AD'):
        return 'deepseek_AD'
    if m.startswith('deepseek_FXS'):
        return 'deepseek_name_FXS'
    if m.startswith('deepseek_name_structure_similarity'):
        return 'deepseek_name_structure_similarity'
    if m.startswith('deepseek_name_structure'):
        return 'deepseek_name_structure'
    if m.startswith('deepseek_name_temperature'):
        return 'deepseek_name'
    if m.startswith('go_similarity_search'):
        return 'go_similarity_search'
    if m.startswith('graph_traversal'):
        return 'graph_traversal'
    if m.startswith('go_similarity'):
        return 'go_similarity'
    if m.startswith('random_seed'):
        return 'random'
    return m

df['model'] = df['method'].apply(extract_prefix)

# 5. Compute mean and std for each model within each disease
results = []
for source in ['01-AD', '02-FXS']:
    sub = df[df['source'] == source]
    for model in sorted(sub['model'].unique()):
        group = sub[sub['model'] == model][metrics]
        means = group.mean()
        stds  = group.std()
        entry = {
            'source': source,
            'model': model,
        }
        # add mean and std for each metric
        for metric in metrics:
            entry[f'{metric}_mean'] = means[metric]
            entry[f'{metric}_std']  = stds[metric]
        results.append(entry)

# 6. Convert to DataFrame, round to two decimals, and print
results_df = pd.DataFrame(results).round(4)
print(results_df.to_string(index=False))

# save to CSV
results_df.to_csv('./Experiment_summary/summary_metrics.csv', index=False)
     