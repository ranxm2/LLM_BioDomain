#!/usr/bin/env python
import argparse
import json
import os
import pandas as pd
from google import genai
from google.genai.types import UploadFileConfig

CHUNK_SIZE = 1000

def parse_args():
    p = argparse.ArgumentParser(description="Submit GO‐term prompts to Gemini Batch Mode")
    p.add_argument("--key_path",         required=True, help="File with your Gemini API key")
    p.add_argument("--df_go_path",       required=True, help="CSV of GO terms + ontology paths")
    p.add_argument("--obo_path",         required=True, help="OBO file (go-basic.obo)")
    p.add_argument("--similarity_path",  required=True, help="Filtered Jaccard similarity CSV")
    p.add_argument("--result_dir",       required=True, help="Where to record outputs")
    p.add_argument("--work_dir",         required=True, help="`cd` here before running")
    p.add_argument("--array_index",      type=int, required=True, help="1‐based SLURM array index")
    p.add_argument("--temperature",      type=float, required=True, help="Sampling temperature")
    return p.parse_args()

def load_api_key(path):
    with open(path) as f:
        return f.read().strip()

def generate_prompts(df_go, obo_path, sim_path):
    # --- REPLACE this stub with your existing prompt‐builder logic ---
    # e.g. loop over df_go rows, grab term, definition via obo, root, similarity, etc.
    prompts = []
    for _, row in df_go.iterrows():
        term = row["node"]
        root = row["root node"]
        prompts.append(
            f"GO term: {term}\nRoot: {root}\n"
            "Assign the top 5 Biodomains."
        )
    return prompts

def write_chunk_jsonl(prompts, temp, start_idx, out_path):
    with open(out_path, "w") as f:
        for local_idx, prompt in enumerate(prompts, 1):
            global_idx = start_idx + local_idx
            entry = {
                "key": f"req-{global_idx}",
                "request": {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": temp}
                }
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return out_path

def main():
    args = parse_args()
    os.chdir(args.work_dir)
    os.makedirs(args.result_dir, exist_ok=True)

    # 1) API key & client
    api_key = load_api_key(args.key_path)
    os.environ["GEMINI_API_KEY"] = api_key
    client = genai.Client(api_key=api_key)

    # 2) Load GO dataframe
    df_go = pd.read_csv(args.df_go_path)

    # 3) Build ALL prompts, then slice out your chunk
    all_prompts = generate_prompts(df_go, args.obo_path, args.similarity_path)
    offset = (args.array_index - 1) * CHUNK_SIZE
    chunk = all_prompts[offset: offset + CHUNK_SIZE]
    if not chunk:
        raise ValueError(f"No prompts for array_index={args.array_index}")

    # 4) Write JSONL for just this chunk
    jsonl_file = os.path.join(args.result_dir, f"batch_{args.array_index}.jsonl")
    write_chunk_jsonl(chunk, args.temperature, start_idx=offset, out_path=jsonl_file)
    print("Wrote batch file:", jsonl_file)

    # 5) Upload via Files API
    uploaded = client.files.upload(
        file=jsonl_file,
        config=UploadFileConfig(
            display_name=os.path.basename(args.result_dir),
            mime_type="application/jsonl"
        )
    )
    print("Uploaded:", uploaded.name)

    # 6) Create the batch job
    batch = client.batches.create(
        model="models/gemini-2.5-flash",
        src=uploaded.name,
        config={"display_name": os.path.basename(args.result_dir)}
    )

    print("Batch job created:", batch.name)
    print("To poll status: client.batches.get(name='{}')".format(batch.name))

if __name__ == "__main__":
    main()
