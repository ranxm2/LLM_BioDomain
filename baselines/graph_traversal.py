"""
A graph traversal algorithm that starts from the GO term (leaf node) and traverses up to the root node.
"""
import random
import json

import polars as pl
import fire
import obonet
import networkx as nx
import numpy as np
from tqdm.auto import tqdm

from .meta_data import AD_BioDomain_GOID_map


def main(
    output_dir: str = './Experiment/00-Baselines/graph_traversal/',
    go_obo_path: str = './data/go-basic.obo',
    seed: int = 42,
    dataset_path: str = './data/AD_Biological_Domain_GO_annotate.csv',
    topk: int = 5,
):
    random.seed(seed)
    AD_BioDomains = list(AD_BioDomain_GOID_map.keys())
    AD_BioDomain_GOID_map_reverse = {
        v: k for k, v in AD_BioDomain_GOID_map.items() if v is not None
    }
    # load full GO Ontology
    graph = obonet.read_obo(go_obo_path)
    print(f'Number of GO terms: {len(graph)}; Number of edges: {graph.number_of_edges()}')
    # load dataset
    df = pl.read_csv(
        dataset_path,
        infer_schema_length=10000
    ).group_by('GO_ID').agg(pl.col('Biodomain').alias('Biodomain_true'))
    df_dicts = df.to_dicts()
    hit_traversal = 0
    obo_missing = 0
    for row in tqdm(df_dicts):
        # assign gold scores: all 1.0
        ground_truth = row['Biodomain_true']
        row['Biodomain_true'] = {p: 1.0 for p in ground_truth}
        # gen predictions
        if row['GO_ID'] in graph:
            descendants: set = nx.descendants(graph, row['GO_ID']) # GO_IDs
            # set score as 1.0
            preds = {AD_BioDomain_GOID_map_reverse[d]: 1.0 for d in descendants if d in AD_BioDomain_GOID_map_reverse}
            if len(preds) > 0:
                hit_traversal += 1
        else:
            preds = {}
            obo_missing += 1
        # remaining predictions are generated randomly
        candidates: list = [d for d in AD_BioDomains if d not in preds]
        sample_k = topk - len(preds)
        random_scores = list(np.linspace(0.9, 0.1, num=sample_k))
        preds_remaining: list = random.sample(candidates, k=sample_k)
        preds.update({p: s for p, s in zip(preds_remaining, random_scores)})
        # add predictions to the row
        row['Biodomain_pred'] = preds
    print(f'Number of hits in traversal: {hit_traversal} out of {len(df_dicts)}')
    print(f'Number of OBO missing GO IDs: {obo_missing} out of {len(df_dicts)}')
    # save the results
    with open(f'{output_dir}/seed_{seed}.json', 'w') as fwrite:
        json.dump(df_dicts, fwrite, indent=2)
    """
    OBO item:
    GO ID: GO:0000001, data: {'name': 'mitochondrion inheritance', 'namespace': 'biological_process', 'def': '"The distribution of mitochondria, including the mitochondrial genome, into daughter cells after mitosis or meiosis, mediated by interactions between mitochondria and the cytoskeleton." [GOC:mcc, PMID:10873824, PMID:11389764]', 'synonym': ['"mitochondrial inheritance" EXACT []'], 'is_a': ['GO:0048308', 'GO:0048311']}
    """



def sanity_check(
    data_path: str = '../data/AD_Biological_Domain_GO_annotate.csv',
):
    data_df = pl.read_csv(
        data_path,
        infer_schema_length=10000
    )
    n_bio_domain = data_df.n_unique(subset='Biodomain')
    n_GO_ID = data_df.n_unique(subset='GO_ID')
    print(f'Number of unique rows: {data_df.height}')
    print(f'Number of unique biological domains: {n_bio_domain}')
    print(f'Number of unique GO IDs: {n_GO_ID}')


if __name__ == '__main__':
    fire.Fire()