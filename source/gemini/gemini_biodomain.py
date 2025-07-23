# import argparse
# from google import genai

# def load_api_key(key_path):
#     with open(key_path, "r") as file:
#         return file.read().strip()

# def main(args=None):
#     parser = argparse.ArgumentParser(description="Run Gemini biodomain model.")
#     parser.add_argument("--key_path", type=str, default="../../keys/gemini_key.txt", help="Path to Gemini API key")
#     parser.add_argument("--result_dir", type=str, default="inout", help="Directory to store results")
#     args = parser.parse_args(args)

#     api_key = load_api_key(args.key_path)

#     client = genai.Client(api_key=api_key)

#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents="Explain how AI works in a few words"
#     )

#     print("Response:")
#     print(response.text)

#     # Save result to file in the specified directory
#     output_path = f"{args.result_dir}/gemini_response.txt"
#     with open(output_path, "w") as f:
#         f.write(response.text)
#     print(f"\nSaved to: {output_path}")

# if __name__ == "__main__":
#     main()

from types import SimpleNamespace
args = SimpleNamespace(
    key_path="keys/gemini_key.txt",
    df_go_path="data/go_root_paths.csv",
    obo_path="data/go-basic.obo",
    result_dir="Experiment/Gemini"
)
# Step 1: Set working directory
git_folder = "/projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder"
os.chdir(git_folder)
print(" Current working directory set to:", os.getcwd())

import argparse
import pandas as pd
import obonet
from google import genai
# from openai import OpenAI

# Define the list of biodomains
BIODOMAIN_LIST = [
    'Mitochondrial Metabolism', 'Unknown', 'Oxidative Stress', 'Proteostasis',
    'Synapse', 'Structural Stabilization', 'Vasculature', 'Immune Response',
    'Endolysosome', 'Apoptosis', 'Tau Homeostasis', 'Metal Binding and Homeostasis',
    'Lipid Metabolism', 'Autophagy', 'Cell Cycle', 'Myelination',
    'RNA Spliceosome', 'APP Metabolism', 'Epigenetic', 'DNA Repair'
]

def format_pathway(pw: str) -> str:
    return pw.replace('_', ' ').title()

def load_api_key(key_path):
    with open(key_path, "r") as file:
        return file.read().strip()

def main(args=None):
    parser = argparse.ArgumentParser(description="Run Gemini Biodomain Mapping")
    parser.add_argument("--key_path", type=str, default="keys/gemini_key.txt", help="Path to OpenAI API key")
    parser.add_argument("--df_go_path", type=str, default="data/go_root_paths.csv", help="Path to GO term CSV")
    parser.add_argument("--obo_path", type=str, default="data/go-basic.obo", help="Path to GO OBO file")
    parser.add_argument("--result_dir", type=str, default="Experiment/Gemini", help="Directory to store results")
    args = parser.parse_args(args)

    # Load API key
    api_key = load_api_key(args.key_path)

    client = genai.Client(api_key=api_key)

    # Example request (placeholder — replace with real application logic)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Explain how AI works in a few words"
    )

    print("Example API response:")
    print(response.output[0].content[0].text)

    # Load GO term data
    df_go = pd.read_csv(args.df_go_path)
    df_go['biodomain'] = "Unspecified"

    # Load GO OBO graph
    graph = obonet.read_obo(args.obo_path)

    print(f"\nLoaded {len(df_go)} GO terms from: {args.df_go_path}")
    print(f"Loaded GO ontology graph with {graph.number_of_nodes()} nodes.")

    print("\nBiodomain list:")
    for d in BIODOMAIN_LIST:
        print(f"- {d}")

    # TODO: Add biodomain assignment logic here using 

if __name__ == "__main__":
    main()


from tqdm import tqdm
import os
import time
from pydantic import BaseModel
from typing import List
class BiodomainResponse(BaseModel):
    biodomains: List[str]

# Join biodomains as a string
domains_str = "\n".join(f"- {d}" for d in BIODOMAIN_LIST)

# Loop through GO terms
for go_index in tqdm(range(len(df_go)), desc="Assigning top-5 Biodomains"):
    go_term = df_go.iloc[go_index]['node']
    go_id = df_go.iloc[go_index]['nodeID']
    go_def = graph.nodes[go_id].get('def', 'No definition available')
    go_root = df_go.iloc[go_index]['root node']

    go_term_formatted = format_pathway(go_term)

    prompt = f"""
You are a biomedical ontology expert.  
Below is a GO term with its definition and full ontology paths.  
From the list of Biodomains, choose the **top 5** labels that best fit this term—ranked most-to-least appropriate.  
**List only** the domain names, **without** any numbering, bullets, or additional text.

**Biodomain options:**
{domains_str}

**GO Term:** {go_term_formatted}  
**Definition:** {go_def}  
**Root ontology term:** {go_root}

Please respond with exactly 5 items, separated by commas, in descending order of relevance.
"""

    try:
        response = client.models.generate_content(
             model="gemini-2.5-flash",
            contents=[{"role": "user", "parts": [prompt]}],
            config={
                "temperature": 0,
                "response_mime_type": "application/json",
                "response_schema": BiodomainResponse,
            }
        )
        bd = response.text.strip()
    except Exception as e:
        bd = f"ERROR: {e}"

    df_go.loc[go_index, 'biodomain'] = bd
    print(f"\nPathway: {go_term_formatted} -> Biodomain: {bd}\n")
    time.sleep(1)

# Ensure result directory exists
os.makedirs(args.result_dir, exist_ok=True)

# Save output
output_path = os.path.join(args.result_dir, "biodomain_results_top5_Gemini.csv")
df_go.to_csv(output_path, index=False)
print(f"\n✅ Results saved to {output_path}")
