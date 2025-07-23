#!/usr/bin/env python3

import os
import time
import argparse
import pandas as pd
import obonet
from openai import OpenAI
from tqdm import tqdm
import networkx as nx

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
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def get_root_paths(go_id, graph):
    """
    Return all simple paths from go_id up to any root term
    (terms with no further parents).
    Each path is a list of GO IDs starting at go_id and ending at a root.
    """
    # find terms with no outgoing edges → these are the “roots”
    roots = [n for n, outdeg in graph.out_degree() if outdeg == 0]

    paths = []
    for r in roots:
        # all_simple_paths follows directed edges in the forward direction
        # i.e. from child→parent
        for p in nx.all_simple_paths(graph, go_id, r):
            paths.append(p)
    return paths


def assign_biodomains(df_go,df_sim, graph, client, result_dir, array_index, batch_size=500, temperature=0.0):
    domains_str = "\n".join(f"- {d}" for d in BIODOMAIN_LIST)

    start_idx = (array_index - 1) * batch_size
    end_idx = min(array_index * batch_size, len(df_go))
    df_subset = df_go.iloc[start_idx:end_idx].copy()
    df_subset.reset_index(drop=True, inplace=True)

    # add the biodomain column
    df_subset['biodomain'] = "Unspecified"

    print(f"Processing array index {array_index}: rows {start_idx} to {end_idx - 1}")

    for go_index in tqdm(range(len(df_subset)), desc=f"Array {array_index}: Assigning Biodomains"):
    # for go_index in tqdm(range(2), desc=f"Array {array_index}: Assigning Biodomains"):
    
        go_term = df_subset.iloc[go_index]['node']
        go_id = df_subset.iloc[go_index]['nodeID']
        go_root = df_subset.iloc[go_index]['root node']
        go_def = graph.nodes[go_id]

        go_term_fmt = format_pathway(go_term)
        
        # Build GO structure text from all root paths
        paths = get_root_paths(go_id, graph)
        structure_lines = []
        for path in paths:
            names = [f"{nid} ({graph.nodes[nid]['name']})" for nid in path]
            structure_lines.append(" -> ".join(names))
        go_structure_text = "\n".join(structure_lines) or "No structure available"

        # — Similarity along each path (term→ancestors) —
        path_sim_lines = []
        for path in paths:
            entries = []
            for nid in path:
                sim = df_sim.get((go_id, nid), 1.0)
                name = graph.nodes[nid]['name']
                entries.append(f"{nid} ({name}): {sim:.3f}")
            path_sim_lines.append(" → ".join(entries))
        path_sim_text = "\n\n".join(path_sim_lines) or "No paths available"



        prompt = f"""
You are a biomedical ontology expert specializing in Fragile X Syndrome (FXS) research, the most common inherited form of intellectual disability and a leading genetic cause of autism spectrum disorders. FXS is caused by CGG repeat expansion in the FMR1 gene, leading to loss of FMRP and resulting in cognitive impairment, behavioral challenges, and synaptic dysfunction. Your task is to classify Gene Ontology (GO) terms in the context of FXS pathology.

Below is a GO term along with its definition and its location in the ontology hierarchy. From the list of Biodomains, select the top five labels that best capture this term's relevance to Fragile X Syndrome, ranking them from most to least appropriate. Provide exactly five domain names only, separated by commas, with no numbering, bullets, or additional text.
**List only** the domain names, **without** any numbering, bullets, or additional text.

**Biodomain options:**
{domains_str}

**GO Term:** {go_term_fmt}  
**Definition:** {go_def}  
**Root ontology term:** {go_root}
**GO Structure (all root paths):**
{go_structure_text}

**Similarity along each GO path** (term -> ancestors):
{path_sim_text}

Please respond with exactly 5 items, separated by commas, in descending order of relevance.
"""

        try:
            resp = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[
                    {"role": "system", "content": "You are a biomedical ontology expert. Always return exactly five ranked Biodomains"},
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
    output_path = os.path.join(result_dir, f"go_biodomain_results_part_{array_index}.csv")
    df_subset.to_csv(output_path, index=False)
    print(f"Saved results to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Assign top-5 Biodomains to GO terms using DeepSeek.")
    parser.add_argument("--key_path", required=True)
    parser.add_argument("--df_go_path", required=True)
    parser.add_argument("--obo_path", required=True)
    parser.add_argument("--similarity_path", required=True)
    parser.add_argument("--result_dir", required=True)
    parser.add_argument("--array_index", type=int, required=True, help="SLURM array index (starting from 1)")
    parser.add_argument("--work_dir", default=None, help="Optional: change to this working directory before running")
    # add the temperature argument
    parser.add_argument("--temperature", type=float, default=0.0, help="Temperature for sampling")


    args = parser.parse_args()

    if args.work_dir:
        os.chdir(args.work_dir)
        print(f"Changed working directory to: {os.getcwd()}")

    start_time = time.time()

    df_go = pd.read_csv(args.df_go_path)
    df_similarity = pd.read_csv(args.similarity_path)
    df_sim = pd.concat([
        df_similarity.rename(columns={"GO_ID1":"A", "GO_ID2":"B", "Jaccard_distance":"sim"}),
        df_similarity.rename(columns={"GO_ID2":"A", "GO_ID1":"B", "Jaccard_distance":"sim"})
    ], ignore_index=True).set_index(["A","B"])["sim"]
    graph = obonet.read_obo(args.obo_path)
    _ = pd.read_csv(args.similarity_path)
    client = load_openai_client(args.key_path)

    assign_biodomains(
        df_go=df_go,
        df_sim=df_sim,
        graph=graph,
        client=client,
        result_dir=args.result_dir,
        array_index=args.array_index,
        batch_size=500,  # Adjust as needed
        temperature=args.temperature
    )

    end_time = time.time()
    elapsed = round(end_time - start_time, 2)

    # Save runtime log
    runtime_log_path = os.path.join(args.result_dir, "runtime_log.csv")
    new_row = pd.DataFrame({
        "array_index": [args.array_index],
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
