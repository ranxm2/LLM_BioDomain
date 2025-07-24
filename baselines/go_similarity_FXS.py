import random
import json

import polars as pl
import numpy as np
import fire

from .meta_data import FXS_BioDomain_GOID_map



def main_jaccard(
    output_dir: str = './Experiment_summary/01-AD/go_similarity',
    similarity_path: str = './data/go_jaccard_long_filtered.csv',
    dataset_path: str = './data/AD_Biological_Domain_GO_annotate.csv',
    seed: int = 42,
    topk: int = 5,
):
    random.seed(seed)

    # Reverse‐map GO_ID → Biodomain
    go_to_domain = {
        go_id: domain
        for domain, go_id in FXS_BioDomain_GOID_map.items()
        if go_id is not None
    }
    all_domains = list(FXS_BioDomain_GOID_map.keys())

    # 1) Load true annotations lazily and group by GO_ID
    df_true = pl.read_csv(
        dataset_path,
        infer_schema_length=10000
    ).group_by('GO_ID').agg(pl.col('Biodomain').alias('Biodomain_true'))

    # 2) Load and symmetrize Jaccard distances (same as before)
    sim = pl.read_csv(similarity_path)
    sim_swapped = sim.rename({"GO_ID1":"GO_ID2","GO_ID2":"GO_ID1"})
    sim_swapped = sim_swapped.select(sim.columns)
    sim_both = pl.concat([sim, sim_swapped])

    # 3) Sort by ascending distance, then take the first row for each GO_ID1
    nearest = (
        sim_both
        .sort("Jaccard_distance")
        .unique(subset="GO_ID1", keep="first")    # keeps the first row per GO_ID1
        .select(["GO_ID1","GO_ID2"])
    )

    # 4) Build your dict
    nn_map = {row["GO_ID1"]: row["GO_ID2"] for row in nearest.to_dicts()}

    # 5) Build predictions
    total = len(df_true)
    hit_count = 0

    results = []
    for rec in df_true.to_dicts():
        go = rec["GO_ID"]
        rec["Biodomain_true"] = {d:1.0 for d in rec["Biodomain_true"]}

        preds = {}
        if go in nn_map and nn_map[go] in go_to_domain:
            preds[go_to_domain[nn_map[go]]] = 1.0
            hit_count += 1

        # random‑fill up to topk
        rem = [d for d in all_domains if d not in preds]
        k = topk - len(preds)
        if k>0:
            scores = list(np.linspace(0.9,0.1,num=k))
            picks = random.sample(rem,k)
            for d,s in zip(picks,scores):
                preds[d] = float(s)

        rec["Biodomain_pred"] = preds
        results.append(rec)

    # -----------------------------
    # 6. Print summary and dump JSON
    # -----------------------------
    print(f"Nearest‑neighbor hits: {hit_count} / {total} GO terms "
          f"({hit_count/total:.1%})")
    print(f"Fallback to random fill: {total - hit_count} terms")

    # 4) Save
    with open(f"{output_dir}/jaccard_seed_{seed}.json","w") as fw:
        json.dump(results, fw, indent=2)

if __name__=="__main__":
    fire.Fire(main_jaccard)
