#!/usr/bin/env python3
import os
import re
import pandas as pd
from glob import glob
import argparse

def merge_parts(folder: str, pattern: str="go_biodomain_results_part_*.csv"):
    # find all matching part‑files
    parts = glob(os.path.join(folder, pattern))
    if not parts:
        print(f"[WARN] no files matching {pattern!r} in {folder}")
        return
    # sort by the integer in “part_XX”
    def part_idx(path):
        m = re.search(r"part_(\d+)", path)
        return int(m.group(1)) if m else -1
    parts = sorted(parts, key=part_idx)
    # read & concat
    dfs = [pd.read_csv(p) for p in parts]
    out = pd.concat(dfs, ignore_index=True)
    # write to “go_biodomain_results.csv” (overwrites if exists)
    out_path = os.path.join(folder, "go_biodomain_results.csv")
    out.to_csv(out_path, index=False)
    print(f"Merged {len(parts)} parts → {out_path}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Merge go_biodomain_results_part_*.csv in a folder"
    )
    p.add_argument(
        "folder",
        help="Directory containing go_biodomain_results_part_*.csv"
    )
    args = p.parse_args()
    merge_parts(args.folder)
