import random
import json

import polars as pl
import fire
from collections import defaultdict
import numpy as np

from .meta_data import AD_BioDomain_GOID_map



# # test
# AD_BioDomain_GOID_map = {
#     'Synapse': 'GO:0045202',
#     'Immune Response': 'GO:0006955',
#     'Mitochondrial Metabolism': None, 
#     'Structural Stabilization': None,
#     'Proteostasis': None,
#     "Lipid Metabolism": 'GO:0006629',
#     'Vasculature': None,
#     'Endolysosome': 'GO:0036019',
#     'Cell Cycle': 'GO:0007049',
#     'Apoptosis': 'GO:0006915',
#     'Oxidative Stress': None,
#     'Myelination': 'GO:0042552',
#     'Metal Binding and Homeostasis': None,
#     'Autophagy': 'GO:0006914',
#     'Epigenetic': None,
#     'APP Metabolism': 'GO:0042982',
#     'DNA Repair': 'GO:0006281',
#     'RNA Spliceosome': None,
#     'Tau Homeostasis': None,
# }
# output_dir = '../Experiment_summary/01-AD/go_similarity'
# similarity_path = '../data/go_jaccard_long_filtered.csv'
# dataset_path = '../data/AD_Biological_Domain_GO_annotate.csv'
# seed = 42
# topk = 5
# expansions_per_node = 10
# max_iterations = 5

def main_expand(
    output_dir: str = './Experiment/02-Expansion/',
    similarity_path: str = './data/go_jaccard_long_filtered.csv',
    dataset_path: str = './data/AD_Biological_Domain_GO_annotate.csv',
    seed: int = 42,
    topk: int = 5,
    expansions_per_node: int = 10,
    max_iterations: int = 5,
):
    random.seed(seed)

    # 1) Build reverse map: GO_ID → Biodomain name
    go_to_domain = {go: bd for bd, go in AD_BioDomain_GOID_map.items() if go}

    # 2) Load and symmetrize Jaccard distances
    sim = pl.read_csv(similarity_path)
    sim_swapped = sim.rename({"GO_ID1":"GO_ID2", "GO_ID2":"GO_ID1"}).select(sim.columns)
    sim_both = pl.concat([sim, sim_swapped], how="vertical_relaxed")

    # 3) Precompute sorted neighbor lists for fast lookup
    #    adjacency[go1] = list of go2 sorted by ascending Jaccard_distance
    sorted_df = sim_both.sort("Jaccard_distance")
    adjacency = defaultdict(list)
    for row in sorted_df.iter_rows(named=True):
        adjacency[row["GO_ID1"]].append(row["GO_ID2"])

    # 4) For each Biodomain seed, do iterative expansion
    domain_members = {}
    for domain, seed_go in AD_BioDomain_GOID_map.items():
        if seed_go is None:
            domain_members[domain] = set()  # no seed to expand
            continue

        members = {seed_go}
        frontier = [seed_go]

        for it in range(max_iterations):
            new_frontier = []
            for go in frontier:
                # take the top-N most similar neighbors
                for neighbor in adjacency.get(go, [])[:expansions_per_node]:
                    if neighbor not in members:
                        members.add(neighbor)
                        new_frontier.append(neighbor)
            if not new_frontier:
                break
            frontier = new_frontier

        domain_members[domain] = members

    # 5) Load true labels and prepare output
    df_true = pl.read_csv(
        dataset_path,
        infer_schema_length=10000
    ).group_by('GO_ID').agg(pl.col('Biodomain').alias('Biodomain_true')).to_dicts()

    # 5. Generate predictions + count hits, with ranked scores for multi‐domain hits
    total = len(df_true)
    hit_count = 0

    results = []
    for rec in df_true:
        go = rec["GO_ID"]
        rec["Biodomain_true"] = {d: 1.0 for d in rec["Biodomain_true"]}

        preds = {}
        # 5.1 Find all domains whose expanded set contains this GO
        hit_domains = [
            domain
            for domain, members in domain_members.items()
            if go in members
        ]

        # 5.2 If we got any real hits, count it once
        if hit_domains:
            hit_count += 1

            # 5.3 Assign decreasing scores: 0.9, 0.7, 0.5, …
            for idx, domain in enumerate(hit_domains):
                score = 0.9 - idx * 0.2
                # floor at 0.1 if you want a minimum
                preds[domain] = round(max(score, 0.1), 2)

        # 5.4 Random‐fill to reach exactly topk predictions
        remaining = [d for d in AD_BioDomain_GOID_map if d not in preds]
        k = topk - len(preds)
        if k > 0:
            fill_scores = list(np.linspace(0.9, 0.1, num=k))
            picks       = random.sample(remaining, k)
            for d, s in zip(picks, fill_scores):
                preds[d] = float(round(s, 2))

        rec["Biodomain_pred"] = preds
        results.append(rec)


    # 6) Print summary and save JSON
    print(f"Expansion‑based hits: {hit_count}/{total} GO terms ({hit_count/total:.1%})")
    for domain, members in domain_members.items():
        print(f" - {domain}: expanded to {len(members)} GO terms")

    with open(f"{output_dir}/similarity_expansion_seed_{seed}.json", "w") as fw:
        json.dump(results, fw, indent=2)

if __name__ == "__main__":
    fire.Fire(main_expand)
