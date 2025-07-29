import random
import json
from typing import List, Literal

import numpy as np
from tqdm.auto import tqdm
import fire
import polars as pl
from pybiomedlink.linker import TransformerEmbLinker

from .meta_data import AD_BioDomain_GOID_map, FXS_Biodomain_GO_map

def main(
    output_dir: str = './Experiment/00-Baselines/SapBERT',
    seed: int = 42,
    dataset_path: str = './data/AD_Biological_Domain_GO_annotate.csv',
    topk: int = 5,
    biodomain_type: Literal['AD', 'FXS'] = 'AD',
):
    random.seed(seed)
    if biodomain_type == 'AD':
        bio_domains = list(AD_BioDomain_GOID_map.keys())
    elif biodomain_type == 'FXS':
        bio_domains = list(FXS_Biodomain_GO_map.keys())
    else:
        raise ValueError(f'Unknown biodomain type: {biodomain_type}')
    linker = TransformerEmbLinker(bio_domains, model_name="cambridgeltl/SapBERT-from-PubMedBERT-fulltext")
    # load the dataset
    df = pl.read_csv(
        dataset_path,
        infer_schema_length=10000
    ).group_by(['GO_ID', 'GOterm_Name']).agg(pl.col('Biodomain').alias('Biodomain_true'))
    df_dicts = df.to_dicts()
    for row in tqdm(df_dicts):
        # assign gold scores: all 1.0
        ground_truth = row['Biodomain_true']
        row['Biodomain_true'] = {p: 1.0 for p in ground_truth}
        # predict
        pred_score_results = linker.predict_aux(row['GOterm_Name'], topk)
        #print(f'Predicted scores for GO term {row["GO_ID"]}, {row["GOterm_Name"]}: {pred_score_results}')
        # add predictions to the row
        preds = {p: s for p, s in zip(pred_score_results['labels'], pred_score_results['scores'])}
        row['Biodomain_pred'] = preds
    # save the results
    with open(f'{output_dir}/seed_{seed}.json', 'w') as fwrite:
        json.dump(df_dicts, fwrite, indent=2)


if __name__ == '__main__':
    fire.Fire()