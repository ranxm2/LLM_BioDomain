#!/usr/bin/env python3
import sys
from pathlib import Path
import pandas as pd
import os

os.chdir("/projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder")


# top‑level folder containing your subfolders of leaderboard CSVs
root = Path("Experiment_summary")
out_path = root / "merged_go_biodomain_leaderboard.csv"

# find all files ending with "_leaderboard.csv"
csv_files = sorted(root.rglob("*_leaderboard.csv"))
if not csv_files:
    raise SystemExit(f"No leaderboard CSVs found under {root}/")

# read each, add a "source" column from the first subfolder, and collect
merged_dfs = []
for csv in csv_files:
    
    # e.g. Experiment_summary/01-AD/... → source = "01-AD"
    try:
        source = csv.relative_to(root).parts[0]
    except Exception:
        source = ""
    df = pd.read_csv(csv)
    df["source"] = source
    merged_dfs.append(df)

# concatenate and write out
merged = pd.concat(merged_dfs, ignore_index=True)
merged.to_csv(out_path, index=False)

print(f"Merged {len(csv_files)} leaderboard files into {out_path}")
