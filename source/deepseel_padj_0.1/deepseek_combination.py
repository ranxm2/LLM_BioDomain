import pandas as pd
import glob
import os

# change the working directory
os.chdir("/projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder")


import pandas as pd
import glob
import os

# directories
dirs = {
    "D154": "Experiment/DeepSeek/03-FXS-padj-0.1/D154/Temp_0.0",
    "D56":  "Experiment/DeepSeek/03-FXS-padj-0.1/D56/Temp_0.0",
    "D154_4_samples": "Experiment/DeepSeek/03-FXS-padj-0.1/D154_4_samples/Temp_0.0"
}

for label, d in dirs.items():
    files = glob.glob(f"{d}/go_biodomain_results_part_*.csv")
    df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    
    # save to each folder
    out_file = os.path.join(d, f"combined_go_biodomain_results_{label}.csv")
    df.to_csv(out_file, index=False)
    
    print(f"✅ Saved {out_file}, shape={df.shape}")




import pandas as pd
from pathlib import Path

# === Edit these ===
infile = "Experiment/DeepSeek/03-FXS-padj-0.1/D154/Temp_0.0/combined_go_biodomain_results_D154.csv"
outfile = "Experiment/DeepSeek/03-FXS-padj-0.1/D154/Temp_0.0/combined_go_biodomain_results_D154_wide.csv"

# ==================

df = pd.read_csv(infile)

def split_to_five(val):
    if pd.isna(val):
        parts = []
    else:
        # split by comma and strip spaces
        parts = [p.strip() for p in str(val).split(",") if p.strip() != ""]
    # pad/truncate to length 5
    parts = (parts + [pd.NA]*5)[:5]
    return pd.Series(parts, index=[f"biodomain_{i}" for i in range(1, 6)])

# Apply to create new columns
bd_cols = df["biodomain"].apply(split_to_five)
df_out = pd.concat([df.drop(columns=["biodomain"]), bd_cols], axis=1)

# Save
if outfile is None:
    p = Path(infile)
    outfile = str(p.with_name(p.stem + "_wide.csv"))
df_out.to_csv(outfile, index=False)

print(f"Saved: {outfile}")
print(df_out.head(3))



# now do the same for D56
infile = "Experiment/DeepSeek/03-FXS-padj-0.1/D56/Temp_0.0/combined_go_biodomain_results_D56.csv"
outfile = "Experiment/DeepSeek/03-FXS-padj-0.1/D56/Temp_0.0/combined_go_biodomain_results_D56_wide.csv"

df = pd.read_csv(infile)

def split_to_five(val):
    if pd.isna(val):
        parts = []
    else:
        # split by comma and strip spaces
        parts = [p.strip() for p in str(val).split(",") if p.strip() != ""]
    # pad/truncate to length 5
    parts = (parts + [pd.NA]*5)[:5]
    return pd.Series(parts, index=[f"biodomain_{i}" for i in range(1, 6)])

# Apply to create new columns
bd_cols = df["biodomain"].apply(split_to_five)
df_out = pd.concat([df.drop(columns=["biodomain"]), bd_cols], axis=1)

# Save
if outfile is None:
    p = Path(infile)
    outfile = str(p.with_name(p.stem + "_wide.csv"))
df_out.to_csv(outfile, index=False)

print(f"Saved: {outfile}")
print(df_out.head(3))   



# D154_4_samples

infile = "Experiment/DeepSeek/03-FXS-padj-0.1/D154_4_samples/Temp_0.0/combined_go_biodomain_results_D154_4_samples.csv"
outfile = "Experiment/DeepSeek/03-FXS-padj-0.1/D154_4_samples/Temp_0.0/combined_go_biodomain_results_D154_4_samples_wide.csv"

df = pd.read_csv(infile)

def split_to_five(val):
    if pd.isna(val):
        parts = []
    else:
        # split by comma and strip spaces
        parts = [p.strip() for p in str(val).split(",") if p.strip() != ""]
    # pad/truncate to length 5
    parts = (parts + [pd.NA]*5)[:5]
    return pd.Series(parts, index=[f"biodomain_{i}" for i in range(1, 6)])

# Apply to create new columns
bd_cols = df["biodomain"].apply(split_to_five)
df_out = pd.concat([df.drop(columns=["biodomain"]), bd_cols], axis=1)

# Save
if outfile is None:
    p = Path(infile)
    outfile = str(p.with_name(p.stem + "_wide.csv"))
df_out.to_csv(outfile, index=False)

print(f"Saved: {outfile}")
print(df_out.head(3))   

