#!/usr/bin/env python3

import os
import time
import argparse
import pandas as pd
import obonet
from openai import OpenAI
from tqdm import tqdm
from google import genai
from google.genai import types

BIODOMAIN_LIST = [
    'Mitochondrial Metabolism', 'Unknown', 'Oxidative Stress', 'Proteostasis',
    'Synapse', 'Structural Stabilization', 'Vasculature', 'Immune Response',
    'Endolysosome', 'Apoptosis', 'Tau Homeostasis', 'Metal Binding and Homeostasis',
    'Lipid Metabolism', 'Autophagy', 'Cell Cycle', 'Myelination',
    'RNA Spliceosome', 'APP Metabolism', 'Epigenetic', 'DNA Repair'
]

domains_str = "\n".join(f"- {d}" for d in BIODOMAIN_LIST)

# chdir(args.working_dir)
working_dir="/projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder"
os.chdir(working_dir)
print("Current working directory set to:", os.getcwd())


# Load the df_go DataFrame
df_go = pd.read_csv("data/go_root_paths.csv")  # Adjust path as needed
go_graph = obonet.read_obo("data/go-basic.obo")  # Adjust path as needed
df_similarity = pd.read_csv("data/go_jaccard_long_filtered.csv")  # Adjust path as needed



def format_pathway(pw: str) -> str:
    return pw.replace('_', ' ').title()






inline_requests_Name = []

for go_index in tqdm(range(len(df_go)), desc="Assigning Biodomains"):
# for go_index in tqdm(range(2), desc="Assigning Biodomains"):

    go_term = df_go.iloc[go_index]['node']
    go_id = df_go.iloc[go_index]['nodeID']
    go_root = df_go.iloc[go_index]['root node']
    go_def = go_graph.nodes[go_id]

    go_term_fmt = format_pathway(go_term)

    prompt = f"""
You are a biomedical ontology expert.  
Below is a GO term with its definition and full ontology paths.  
From the list of Biodomains, choose the **top 5** labels that best fit this term—ranked most-to-least appropriate.  
**Do not** ever reply “Unknown,” and **do not** return more or fewer than five.  
**List only** the domain names, **without** any numbering, bullets, or additional text.

**Biodomain options:**
{domains_str}

**GO Term:** {go_term_fmt}  
**Definition:** {go_def}  
**Root ontology term:** {go_root}

Please respond with exactly 5 items, separated by commas, in descending order of relevance.
"""

    # append a properly structured request dict
    inline_requests_Name.append({
        'contents': [
            {
                'parts': [{'text': prompt}],
                'role': 'user'
            }
        ]
    })






inline_batch_job = client.batches.create(
    model="models/gemini-2.5-flash",
    src=inline_requests_Name,
    config={
        'temperature': 0.0,
        'display_name': "inlined-requests-job-1",
    },
)

print(f"Created batch job: {inline_batch_job.name}")







key_path="keys/gemini_key.txt"

def load_api_key(key_path):
    with open(key_path, "r") as file:
        return file.read().strip()

api_key = load_api_key(key_path)
client = genai.Client(api_key=api_key)

















# Use the name of the job you want to check
# e.g., inline_batch_job.name from the previous step
job_name = "batches/zyz8mvejtdtdoacxg66nn71haxyd0l54l75b"  # (e.g. 'batches/your-batch-id')
batch_job = client.batches.get(name=job_name)

completed_states = set([
    'JOB_STATE_SUCCEEDED',
    'JOB_STATE_FAILED',
    'JOB_STATE_CANCELLED',
])

print(f"Polling status for job: {job_name}")
batch_job = client.batches.get(name=job_name) # Initial get

while batch_job.state.name not in completed_states:
  print(f"Current state: {batch_job.state.name}")
  time.sleep(5) # Wait for 30 seconds before polling again
  batch_job = client.batches.get(name=job_name)

print(f"Job finished with state: {batch_job.state.name}")
if batch_job.state.name == 'JOB_STATE_FAILED':
    print(f"Error: {batch_job.error}")


import json

# Use the name of the job you want to check
# e.g., inline_batch_job.name from the previous step
# job_name = "YOUR_BATCH_JOB_NAME"
batch_job = client.batches.get(name=job_name)

if batch_job.state.name == 'JOB_STATE_SUCCEEDED':

    # If batch job was created with a file
    if batch_job.dest and batch_job.dest.file_name:
        # Results are in a file
        result_file_name = batch_job.dest.file_name
        print(f"Results are in file: {result_file_name}")

        print("Downloading result file content...")
        file_content = client.files.download(file=result_file_name)
        # Process file_content (bytes) as needed
        print(file_content.decode('utf-8'))

    # If batch job was created with inline request
    elif batch_job.dest and batch_job.dest.inlined_responses:
        # Results are inline
        print("Results are inline:")
        for i, inline_response in enumerate(batch_job.dest.inlined_responses):
            print(f"Response {i+1}:")
            if inline_response.response:
                # Accessing response, structure may vary.
                try:
                    print(inline_response.response.text)
                except AttributeError:
                    print(inline_response.response) # Fallback
            elif inline_response.error:
                print(f"Error: {inline_response.error}")
    else:
        print("No results found (neither file nor inline).")
else:
    print(f"Job did not succeed. Final state: {batch_job.state.name}")
    if batch_job.error:
        print(f"Error: {batch_job.error}")