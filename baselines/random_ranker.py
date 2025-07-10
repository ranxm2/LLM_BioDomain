import random
import json

import numpy as np
import fire
import polars as pl

from .meta_data import AD_BioDomain_GOID_map


def main(
    output_dir: str = './Experiment/00-Baselines/random/',
    seed: int = 42,
    dataset_path: str = './data/AD_Biological_Domain_GO_annotate.csv',
    topk: int = 5,
):
    random.seed(seed)
    AD_BioDomains = list(AD_BioDomain_GOID_map.keys())
    # load the dataset
    df = pl.read_csv(
        dataset_path,
        infer_schema_length=10000
    ).group_by('GO_ID').agg(pl.col('Biodomain').alias('Biodomain_true'))
    df_dicts = df.to_dicts()
    # create a template for predicted scores
    # [0.9, 0.7, 0.5, 0.3, 0.1] for topk=5
    pred_scores_template = list(np.linspace(0.9, 0.1, num=topk))
    for row in df_dicts:
        # assign gold scores: all 1.0
        ground_truth = row['Biodomain_true']
        row['Biodomain_true'] = {p: 1.0 for p in ground_truth}
        # radonmly predict
        preds: List = random.sample(AD_BioDomains, k=topk)
        row['Biodomain_pred'] = {p: s for p, s in zip(preds, pred_scores_template)}
    # save the results
    with open(f'{output_dir}/seed_{seed}.json', 'w') as fwrite:
        json.dump(df_dicts, fwrite, indent=2)


if __name__ == '__main__':
    fire.Fire()