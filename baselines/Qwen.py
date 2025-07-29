import random
import json
from typing import List, Literal

import numpy as np
from tqdm.auto import tqdm
import fire
import polars as pl

from .meta_data import AD_BioDomain_GOID_map, FXS_Biodomain_GO_map

def main(
    output_dir: str = './Experiment/00-Baselines/Qwen3-0.6B',
    model_name: str = 'Qwen/Qwen3-0.6B',
    seed: int = 42,
    dataset_path: str = './data/AD_Biological_Domain_GO_annotate.csv',
    topk: int = 5,
    thinking_mode: bool = True,
    biodomain_type: Literal['AD', 'FXS'] = 'AD',
):
    from pybiomedlink.linker import Qwen3PromptLinker
    import torch
    random.seed(seed)
    if biodomain_type == 'FXS':
        bio_domains = list(FXS_Biodomain_GO_map.keys())
    elif biodomain_type == 'AD':
        bio_domains = list(AD_BioDomain_GOID_map.keys())
    else:
        raise ValueError(f'Unknown biodomain type: {biodomain_type}. Choose from "AD" or "FXS".')
    print(f'Using model: {model_name} with biodomain type: {biodomain_type}')
    linker = Qwen3PromptLinker(
        bio_domains, 
        model_name=model_name,
    )
    # TODO: incoporate into the package to speed up
    linker.model.eval()
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
        with torch.inference_mode():
            pred_score_results = linker.predict_aux(
                row['GOterm_Name'],
                topk,
                enable_thinking=thinking_mode,
                )
        # add predictions to the row
        preds = {p: s for p, s in zip(pred_score_results['labels'], pred_scores_template)}
        row['Biodomain_pred'] = preds
        row['_LLM_raw_output'] = pred_score_results
        fwrite.write(json.dumps(row) + '\n')
        fwrite.flush()
    fwrite.close()


def post_process(
    result_path: str = './Experiment/00-Baselines/Qwen3-0.6B-No-Thinking/seed_27.jsonl',
    biodomain_type: Literal['AD', 'FXS'] = 'AD',
    topk: int = 5,
):
    """
    Some returned json may be broken. 
    This is the cleanining function.
    """
    if biodomain_type == 'FXS':
        label_bio_domains = list(FXS_Biodomain_GO_map.keys())
    elif biodomain_type == 'AD':
        label_bio_domains = list(AD_BioDomain_GOID_map.keys())
    else:
        raise ValueError(f'Unknown biodomain type: {biodomain_type}. Choose from "AD" or "FXS".')
    seed = int(result_path.split('/')[-1].split('_')[1].split('.')[0])
    random.seed(seed)
    print(f'biodomain type: {biodomain_type}')
    print(f'Post-processing {result_path}')
    outputs = []
    total_cnt = 0
    error_cnt = 0
    post_cnt = 0
    with open(result_path, 'r') as fread:
        for line in fread:
            total_cnt += 1
            output = json.loads(line.strip())
            if len(output["Biodomain_pred"]) == 0:
                error_cnt += 1
                content = output['_LLM_raw_output']['content']
                if content.startswith("```json"):
                    # 0.6B No Thinking typical output
                    #print(content)
                    post_content = content.lstrip("```json\n").rstrip("\n```")
                    #print(post_content)
                    biodomain_pred = json.loads(post_content)
                    pred_scores_template = list(np.linspace(0.9, 0.1, num=len(biodomain_pred)))
                    output["Biodomain_pred"] = {
                        p: s for p, s in zip(biodomain_pred, pred_scores_template)
                    }
                    post_cnt += 1
                elif content == '[]':
                    # 0.6B Thinking typical output
                    pred_scores_template = list(np.linspace(0.9, 0.1, num=topk))
                    random_pred_biodomain = random.sample(label_bio_domains, k=topk)
                    output["Biodomain_pred"] = {
                        p: s for p, s in zip(random_pred_biodomain, pred_scores_template)
                    }
                    post_cnt += 1
                else:
                    print(f'(not post-processed) Error in line {total_cnt}: {output}')
            outputs.append(output)
    print(f'Total: {total_cnt} | Error: {error_cnt} | Post-processed: {post_cnt}')
    out_path = result_path.replace('.jsonl', '-post.json')
    with open(out_path, 'w') as fwrite:
        json.dump(outputs, fwrite, indent=2)

if __name__ == '__main__':
    fire.Fire()