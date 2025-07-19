import random
import json
from typing import List

import numpy as np
from tqdm.auto import tqdm
import fire
import polars as pl
from pybiomedlink.linker import Qwen3PromptLinker

from .meta_data import AD_BioDomain_GOID_map

def main(
    output_dir: str = './Experiment/00-Baselines/Qwen3-0.6B',
    model_name: str = 'Qwen/Qwen3-0.6B',
    seed: int = 42,
    dataset_path: str = './data/AD_Biological_Domain_GO_annotate.csv',
    topk: int = 5,
):
    random.seed(seed)
    AD_BioDomains = list(AD_BioDomain_GOID_map.keys())
    linker = Qwen3PromptLinker(
        AD_BioDomains, 
        model_name=model_name,
    )
    # load the dataset
    df = pl.read_csv(
        dataset_path,
        infer_schema_length=10000
    ).group_by(['GO_ID', 'GOterm_Name']).agg(pl.col('Biodomain').alias('Biodomain_true'))
    df_dicts = df.to_dicts()
    pred_scores_template = list(np.linspace(0.9, 0.1, num=topk))

    fwrite = open(f'{output_dir}/seed_{seed}.jsonl', 'w') # write every line since LLM may fail
    for row in tqdm(df_dicts):
        # assign gold scores: all 1.0
        ground_truth = row['Biodomain_true']
        row['Biodomain_true'] = {p: 1.0 for p in ground_truth}
        # predict
        pred_score_results = linker.predict_aux(row['GOterm_Name'], topk)
        # add predictions to the row
        preds = {p: s for p, s in zip(pred_score_results['labels'], pred_scores_template)}
        row['Biodomain_pred'] = preds
        row['_LLM_raw_output'] = pred_score_results
        fwrite.write(json.dumps(row) + '\n')
        fwrite.flush()
    fwrite.close()


if __name__ == '__main__':
    fire.Fire()