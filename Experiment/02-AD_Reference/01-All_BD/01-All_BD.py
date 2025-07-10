from openai import OpenAI
import pandas as pd
import time
from tqdm import tqdm
import re
import obonet
import networkx as nx

# ─── 0) Init OpenAI client ───
with open("../../../keys/api_keys.txt", "r") as f:
    api_key = f.read().strip()
client = OpenAI(api_key=api_key)

# ─── 1) Load & clean AD reference ───
ref = pd.read_csv("../../../data/BioDomain_AD_Ref.csv")[['pathway','Biodomain']]
ref_cleaned = (
    ref
    .dropna(subset=['pathway','Biodomain'])
    .query("Biodomain.str.lower() != 'none'", engine='python')
)
# drop any pathways mapping to multiple domains
dup = ref_cleaned['pathway'][ref_cleaned['pathway'].duplicated(keep=False)]
ref_cleaned = ref_cleaned[~ref_cleaned['pathway'].isin(dup)]

def normalize_pathway(p: str) -> str:
    p = re.sub(r'^GO[_]?BP[_]?', '', p)
    return p.replace('_',' ').lower().strip()

ref_cleaned['norm'] = ref_cleaned['pathway'].map(normalize_pathway)

# ─── 2) Build a full AD→Biodomain reference block ───
#   e.g. "- Negative Regulation Of Transcription By Rna Polymerase Ii: Epigenetic"
grouped = (
    ref_cleaned
    .groupby('Biodomain')['norm']
    .apply(lambda terms: sorted(set(terms)))
    .to_dict()
)

ref_context = "\n".join(
    f"- {biodomain}: {', '.join([t.title() for t in go_terms])}"
    for biodomain, go_terms in grouped.items()
)


# ─── 3) Load GO terms ───
df_go = pd.read_csv("../../../data/biodomain_results_0429.csv")
df_go['biodomain_top5'] = ""

# ─── 4) Prepare Biodomain options (exclude “Unknown”) ───
Biodomain_list = [
    'Mitochondrial Metabolism','Oxidative Stress','Proteostasis',
    'Synapse','Structural Stabilization','Vasculature','Immune Response',
    'Endolysosome','Apoptosis','Tau Homeostasis',
    'Metal Binding and Homeostasis','Lipid Metabolism','Autophagy',
    'Cell Cycle','Myelination','RNA Spliceosome','APP Metabolism',
    'Epigenetic','DNA Repair'
]
domains_str = "\n".join(f"- {d}" for d in Biodomain_list)

def format_pathway_title(pw: str) -> str:
    return pw.replace('_',' ').title()



# ─── 6) Loop & prompt for top-5 ───
for idx in tqdm(range(len(df_go))):
    raw = df_go.at[idx, 'pathway']
    # DELETE THE FIRST 5 CHARACTERS
    raw = raw[5:] 
    go_term = format_pathway_title(raw)


    prompt = f"""
You are a biomedical ontology expert.

Here is our AD→GOID reference (compact):
{ref_context}

Now, below is a new GO term.  From the list of Biodomains, choose the **top 5** labels that best fit this term—ranked most→least appropriate.
**Never** reply “Unknown,” and **do not** include numbering, bullets, or any extra text—just the five names, comma-separated.


**Biodomain options:**
{domains_str}

**GO Term:** {go_term}
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role":"system",
                    "content":"You are a biomedical ontology expert. Always return exactly five ranked Biodomains—never 'Unknown'."
                },
                {"role":"user","content":prompt}
            ],
            temperature=0
        )
        top5 = resp.choices[0].message.content.strip()
    except Exception as e:
        top5 = f"ERROR: {e}"

    df_go.at[idx, 'biodomain_top5'] = top5
    print(f"[{idx}] {go_term} → {top5}")
    time.sleep(1)

# ─── 7) Save results ───
df_go.to_csv("biodomain_results_top5_with_AD_ref_0630.csv", index=False)
