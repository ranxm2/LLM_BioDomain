#!/usr/bin/env python3

import json
import pandas as pd
from pathlib import Path
import os
import sys
import csv
from pathlib import Path


os.chdir("/projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder")


# load /Experiment/DeepSeek/02-FXS/01-Name/Temp_0.9/go_biodomain_results.csv

df = pd.read_csv("./Experiment/DeepSeek/02-FXS/01-Name/Temp_0.9/go_biodomain_results.csv")

# exctra the first biodomain for each GO term
# n   labels = [lbl.strip() for lbl in row['biodomain'].split(',')]
df['biodomain'] = df['biodomain'].apply(lambda x: x.split(',')[0] if isinstance(x, str) else '')
# save the dataframe to a new csv file
output_file = Path("./Experiment/DeepSeek/02-FXS/01-Name/Temp_0.9/go_biodomain_results_first_DeepSeek_Name_temp_0.9.csv")
df.to_csv(output_file, index=False)

# load the FXS df wen/JX/02-AI-BioDomain/git_folder/data/FXS_bidomain_annotation_certain.csv

fxs_df = pd.read_csv("./data/FXS_bidomain_annotation_certain.csv")

def format_pathway(pw: str) -> str:
    return pw.replace('_', ' ').title()

fxs_df['GOterm_Name'] = fxs_df['GOterm_Name'].apply(format_pathway)

# save the dataframe to a new csv file
output_fxs_file = Path("./data/FXS_bidomain_annotation_certain_formatted.csv")
fxs_df.to_csv(output_fxs_file, index=False)