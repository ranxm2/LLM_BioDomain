#!/usr/bin/env python3

import os
import time
import argparse
import pandas as pd
import obonet
from openai import OpenAI
from tqdm import tqdm

BIODOMAIN_LIST = [
    'Mitochondrial Metabolism', 'Unknown', 'Oxidative Stress', 'Proteostasis',
    'Synapse', 'Structural Stabilization', 'Vasculature', 'Immune Response',
    'Endolysosome', 'Apoptosis', 'Tau Homeostasis', 'Metal Binding and Homeostasis',
    'Lipid Metabolism', 'Autophagy', 'Cell Cycle', 'Myelination',
    'RNA Spliceosome', 'APP Metabolism', 'Epigenetic', 'DNA Repair'
]

def format_pathway(pw: str) -> str:
    return pw.replace('_', ' ').title()


def load_openai_client(key_path: str) -> OpenAI:
    with open(key_path, "r") as file:
        api_key = file.read().strip()
    return OpenAI(api_key=api_key)


def assign_biodomains(df_go, graph, client, result_dir,  temperature=0.0):
    domains_str = "\n".join(f"- {d}" for d in BIODOMAIN_LIST)

    df_subset = df_go
    df_subset.reset_index(drop=True, inplace=True)

    # add the biodomain column
    df_subset['biodomain'] = "Unspecified"


    for go_index in tqdm(range(len(df_subset)), desc=f"Assigning Biodomains"):
    # for go_index in tqdm(range(2), desc=f"Assigning Biodomains"):
    
        go_term = df_subset.iloc[go_index]['node']
        go_id = df_subset.iloc[go_index]['nodeID']
        go_root = df_subset.iloc[go_index]['root node']
        go_def = graph.nodes[go_id]

        go_term_fmt = format_pathway(go_term)

        prompt = f"""
You are a biomedical ontology expert with a focus on Alzheimer’s disease (AD) research. Alzheimer’s disease is a progressive neurodegenerative disorder marked by cognitive decline, amyloid-beta plaque deposition, and neurofibrillary tangles. Your task is to classify Gene Ontology (GO) terms in the context of AD pathology.

Below is a GO term along with its definition and its location in the ontology hierarchy. From the list of Biodomains, select the top five labels that best capture this term’s relevance to Alzheimer’s disease, ranking them from most to least appropriate. Do not reply “Unknown,” and provide exactly five domain names only, separated by commas, with no numbering, bullets, or additional text.

**Biodomain options:**
{domains_str}

**GO Term:** {go_term_fmt}  
**Definition:** {go_def}  
**Root ontology term:** {go_root}

Please respond with exactly 5 items, separated by commas, in descending order of relevance.
"""

        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a biomedical ontology expert. Always return exactly five ranked Biodomains—never 'Unknown'—for any GO term."},
                    {"role": "user",   "content": prompt}
                ],
                temperature=temperature
            )
            bd = resp.choices[0].message.content.strip()
        except Exception as e:
            bd = f"ERROR: {e}"

        df_subset.loc[go_index, 'biodomain'] = bd
        print(f"GO Term: {go_term_fmt} -> Biodomain: {bd}")
        time.sleep(1)

    os.makedirs(result_dir, exist_ok=True)
    output_path = os.path.join(result_dir, f"go_biodomain_results_{temperature}.csv")
    print(f"Saving results to: {output_path}")
    df_subset.to_csv(output_path, index=False)
    print(f"Saved results to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Assign top-5 Biodomains to GO terms using DeepSeek.")
    parser.add_argument("--key_path", required=True)
    parser.add_argument("--df_go_path", required=True)
    parser.add_argument("--obo_path", required=True)
    parser.add_argument("--similarity_path", required=True)
    parser.add_argument("--result_dir", required=True)
    parser.add_argument("--work_dir", default=None, help="Optional: change to this working directory before running")
    parser.add_argument("--temperature", type=float, default=0.0, help="Temperature for sampling")

    args = parser.parse_args()

    if args.work_dir:
        os.chdir(args.work_dir)
        print(f"Changed working directory to: {os.getcwd()}")

    start_time = time.time()

    df_go = pd.read_csv(args.df_go_path)
    graph = obonet.read_obo(args.obo_path)
    _ = pd.read_csv(args.similarity_path)
    client = load_openai_client(args.key_path)

    assign_biodomains(
        df_go=df_go,
        graph=graph,
        client=client,
        result_dir=args.result_dir,
        temperature=args.temperature
    )

    end_time = time.time()
    elapsed = round(end_time - start_time, 2)

    # Save runtime log
    runtime_log_path = os.path.join(args.result_dir, "runtime_log.csv")
    new_row = pd.DataFrame({
        "seconds_used": [elapsed],
        "timestamp": [time.strftime('%Y-%m-%d %H:%M:%S')],
        "temperature": [args.temperature]
    })

    # Append or create
    if os.path.exists(runtime_log_path):
        runtime_df = pd.read_csv(runtime_log_path)
        runtime_df = pd.concat([runtime_df, new_row], ignore_index=True)
    else:
        runtime_df = new_row

    runtime_df.to_csv(runtime_log_path, index=False)
    print(f"Logged runtime to: {runtime_log_path}")




if __name__ == "__main__":
    main()
