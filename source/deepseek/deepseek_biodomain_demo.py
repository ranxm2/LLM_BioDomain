#!/usr/bin/env python3

import pandas as pd
import obonet
import time
from types import SimpleNamespace
args = SimpleNamespace(
    key_path="keys/deepseek_key.txt",
    df_go_path="data/go_root_paths.csv",
    similarity_path="data/go_jaccard_long_filtered.csv",
    obo_path="data/go-basic.obo",
    result_dir="Experiment/Deepseek"
)
# Step 1: Set working directory
git_folder = "/projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder"
os.chdir(git_folder)
print(" Current working directory set to:", os.getcwd())




from openai import OpenAI

# load the api key from an txt file
key_path = args.key_path
with open(key_path, "r") as file:
    api_key = file.read().strip()


client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


response = client.chat.completions.create(
    model='deepseek-reasoner',
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)

print(response.choices[0].message.content)

df_go = pd.read_csv(args.df_go_path)
graph  = obonet.read_obo(args.obo_path)
df_similarity = pd.read_csv(args.similarity_path)

Biodomain_list = ['Mitochondrial Metabolism',
 'Unknown',
 'Oxidative Stress',
 'Proteostasis',
 'Synapse',
 'Structural Stabilization',
 'Vasculature',
 'Immune Response',
 'Endolysosome',
 'Apoptosis',
 'Tau Homeostasis',
 'Metal Binding and Homeostasis',
 'Lipid Metabolism',
 'Autophagy',
 'Cell Cycle',
 'Myelination',
 'RNA Spliceosome',
 'APP Metabolism',
 'Epigenetic',
 'DNA Repair']

go_index=0


domains_str = "\n".join(f"- {d}" for d in Biodomain_list)
def format_pathway(pw: str) -> str:
    return pw.replace('_',' ').title()


for go_index in tqdm(range(len(df_go)), desc="Assigning top-5 Biodomains"):
    go_term = df_go.iloc[go_index]['node']
    go_id = df_go.iloc[go_index]['nodeID']
    go_def = graph.nodes[go_id]
    go_root = df_go.iloc[go_index]['root node']

    go_term = format_pathway(go_term)

    prompt = f"""
You are a biomedical ontology expert.  
Below is a GO term with its definition and full ontology paths.  
From the list of Biodomains, choose the **top 5** labels that best fit this term—ranked most-to-least appropriate.  
**Do not** ever reply “Unknown,” and **do not** return more or fewer than five.  
**List only** the domain names, **without** any numbering, bullets, or additional text.

**Biodomain options:**
{domains_str}

**GO Term:** {go_term}  
**Definition:** {go_def}  
**Root ontology term:** {go_root}

Please respond with exactly 5 items, separated by commas, in descending order of relevance.
"""

    try:
        resp = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=[
                {"role": "system", "content": "You are a biomedical ontology expert. Always return exactly five ranked Biodomains—never 'Unknown'—for any GO term."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0
        )
        bd = resp.choices[0].message.content.strip()
    except Exception as e:
        bd = f"ERROR: {e}"

    df_go.loc[go_index, 'biodomain'] = bd
    print(f"Pathway: {go_term} -> Biodomain: {bd}\n")
    time.sleep(1)
\