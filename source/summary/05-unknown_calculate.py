#!/usr/bin/env python3

import json
import pandas as pd
from pathlib import Path
import os
import sys
import csv
from pathlib import Path


os.chdir("/projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder")


# directories to scan
BASE_DIR = Path("Experiment_summary")
DATASETS = ["01-AD", "02-FXS"]

# prepare output CSV
OUT_CSV = Path("./Experiment_summary/unknown_by_rank_summary.csv")
fields = [
    "dataset",
    "file",
    "total_go_terms",
    "unknown_top1",
    "unknown_top2",
    "unknown_top3",
    "unknown_top4",
    "unknown_top5",
]
with OUT_CSV.open("w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()

    # walk through JSON files
    for dataset in DATASETS:
        for js in (BASE_DIR / dataset).rglob("*.json"):
            data = json.loads(js.read_text())
            total = len(data)

            # counters for Unknown at each of the top 5 positions
            unknown_counts = {f"unknown_top{i}": 0 for i in range(1, 6)}

            # for each GO term entry, sort preds by score desc and check top 5
            for entry in data:
                preds = entry.get("Biodomain_pred", {})
                # list of (domain,score) sorted highest→lowest
                sorted_preds = sorted(preds.items(), key=lambda x: x[1], reverse=True)
                for i in range(5):
                    if i < len(sorted_preds) and sorted_preds[i][0] == "Unknown":
                        unknown_counts[f"unknown_top{i+1}"] += 1

            # extract the file name without the directory and derived .json extension
            js = js.relative_to(BASE_DIR / dataset).with_suffix("")
            js = js.name

            # write row
            row = {
                "dataset": dataset,
                "file": str(js),
                "total_go_terms": total,
                **unknown_counts
            }
            writer.writerow(row)

print(f"Wrote summary to {OUT_CSV}")
