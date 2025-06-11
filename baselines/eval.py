import fire
import json
import polars as pl
from ranx import Qrels, Run, evaluate


def eval(
    result_path: str = './Experiment/00-Baselines/random/seed_42.json',
    leaderboard_path: str = './Experiment/00-Baselines/random/seed_42_leaderboard.csv',
    method_name: str = 'random_seed_42',
):
    with open(result_path, 'r') as fread:
        results = json.load(fread)
    qrels_dict = {}
    run_dict = {}
    for result in results:
        go_id = result['GO_ID']
        qrels_dict[go_id] = result['Biodomain_true']
        run_dict[go_id] = result['Biodomain_pred']
    qrels = Qrels(qrels_dict)
    run = Run(run_dict)
    metrics = evaluate(qrels, run, metrics=['precision@1', 'precision@2', 'recall@1', 'recall@2'])
    metrics['method'] = method_name
    df = pl.from_dicts([metrics])
    print(df)
    df.write_csv(leaderboard_path)


if __name__ == '__main__':
    fire.Fire()