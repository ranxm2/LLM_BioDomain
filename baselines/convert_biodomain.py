#!/usr/bin/env python3
"""
Convert a single prediction CSV into JSON using a given truth CSV and output filepath.
"""
import os
import json
import argparse
import pandas as pd

def load_true(true_csv):
    df = pd.read_csv(true_csv, dtype=str)
    # map GO_ID to its single true label
    return {row['GO_ID']: {row['Biodomain'].strip(): 1.0}
            for _, row in df.iterrows()}


def convert(true_map, pred_csv, out_json):
    df = pd.read_csv(pred_csv, dtype=str)
    combined = []
    for _, row in df.iterrows():
        go_id = row.get('nodeID', row.get('GO_ID', ''))
        # skip GO IDs not in true_map
        if go_id not in true_map:
            continue
        labels = [lbl.strip() for lbl in row['biodomain'].split(',')]
        scores = [0.9, 0.7, 0.5, 0.3, 0.1]
        pred_map = {lbl: score for lbl, score in zip(labels, scores)}
        combined.append({
            'GO_ID': go_id,
            'Biodomain_true': true_map[go_id],
            'Biodomain_pred': pred_map,
        })
    # ensure output directory exists
    out_dir = os.path.dirname(out_json) or '.'
    os.makedirs(out_dir, exist_ok=True)
    with open(out_json, 'w') as fout:
        json.dump(combined, fout, indent=2)
    print(f"Wrote {len(combined)} entries to {out_json}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert one biodomain CSV to JSON"
    )
    parser.add_argument('--true_csv', required=True,
                        help='CSV with GO_ID and single true Biodomain label')
    parser.add_argument('--pred_csv', required=True,
                        help='CSV with nodeID and top-5 comma-separated predictions')
    parser.add_argument('--out_json', required=True,
                        help='Output JSON filepath')
    args = parser.parse_args()

    true_map = load_true(args.true_csv)
    convert(true_map, args.pred_csv, args.out_json)

if __name__ == '__main__':
    main()
