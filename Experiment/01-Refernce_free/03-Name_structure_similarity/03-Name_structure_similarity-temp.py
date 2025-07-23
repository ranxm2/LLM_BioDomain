from openai import OpenAI
import openai
import pandas as pd
import time
from tqdm import tqdm
import obonet
import networkx as nx


import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--temp', type=float, required=True, help='Temperature value for OpenAI API')
args = parser.parse_args()
temperature = args.temp

# load the api key from an txt file
with open("../../../keys/api_keys.txt", "r") as file:
    api_key = file.read().strip()

client = OpenAI(
  api_key=    api_key
)

response = client.responses.create(
  model="gpt-4o-mini",
  input="Tell me a three sentence bedtime story about a unicorn."
)
# only show the response content
print(response.output[0].content[0].text)

# load the GO term from the file
df_go = pd.read_csv("../../../data/go_root_paths.csv")
# add the biodomain column
df_go['biodomain'] = "Unspecified"
# path to your downloaded file

# read the OBO into a directed graph
graph = obonet.read_obo('../../../data/go-basic.obo')


# load the GO term from the file
Biodomain_list = ['Mitochondrial Metabolism',
 'Unknown',
 'Oxidative Stress',
 'Proteostasis',
 'Synapse',
 'Structural Stabilization',
 'Vasculature',
 'Immune Response',
 'Endolysosome',
 'Apoptosis',
 'Tau Homeostasis',
 'Metal Binding and Homeostasis',
 'Lipid Metabolism',
 'Autophagy',
 'Cell Cycle',
 'Myelination',
 'RNA Spliceosome',
 'APP Metabolism',
 'Epigenetic',
 'DNA Repair']

domains_str = "\n".join(f"- {d}" for d in Biodomain_list)
def format_pathway(pw: str) -> str:
    return pw.replace('_',' ').title()

def get_root_paths(go_id):
    """
    Return all simple paths from go_id up to any root term
    (terms with no further parents).
    Each path is a list of GO IDs starting at go_id and ending at a root.
    """
    # find terms with no outgoing edges → these are the “roots”
    roots = [n for n, outdeg in graph.out_degree() if outdeg == 0]

    paths = []
    for r in roots:
        # all_simple_paths follows directed edges in the forward direction
        # i.e. from child→parent
        for p in nx.all_simple_paths(graph, go_id, r):
            paths.append(p)
    return paths

def get_ancestors(go_id):
    """
    Return the set of all ancestor GO IDs (more general terms)
    reachable from go_id by following parent links.
    """
    # Since edges are child→parent, 
    # descendants(graph, go_id) will walk from your term up
    return nx.descendants(graph, go_id)


# load the similarity matrix
df_similarity = pd.read_csv("../../../data/go_jaccard_long_filtered.csv")

df_sim = pd.concat([
    df_similarity.rename(columns={"GO_ID1":"A", "GO_ID2":"B", "Jaccard_distance":"sim"}),
    df_similarity.rename(columns={"GO_ID2":"A", "GO_ID1":"B", "Jaccard_distance":"sim"})
], ignore_index=True).set_index(["A","B"])["sim"]


# ——— 2) Define your AD to GOID map ———
AD_BioDomain_GOID_map = {
    'Synapse': 'GO:0045202',
    'Immune Response': 'GO:0006955',
    'Mitochondrial Metabolism': None,
    'Structural Stabilization': None,
    'Proteostasis': None,
    "Lipid Metabolism": 'GO:0006629',
    'Vasculature': None,
    'Endolysosome': 'GO:0036019',
    'Cell Cycle': 'GO:0007049',
    'Apoptosis': 'GO:0006915',
    'Oxidative Stress': None,
    'Myelination': 'GO:0042552',
    'Metal Binding and Homeostasis': None,
    'Autophagy': 'GO:0006914',
    'Epigenetic': None,
    'APP Metabolism': 'GO:0042982',
    'DNA Repair': 'GO:0006281',
    'RNA Spliceosome': None,
    'Tau Homeostasis': None,
}
import pandas as pd
import time
from tqdm import tqdm

# ——— 1) Load your similarity matrix ———
df_similarity = pd.read_csv("../../../data/go_jaccard_long_filtered.csv")
df_sim = pd.concat([
    df_similarity.rename(columns={"GO_ID1":"A", "GO_ID2":"B", "Jaccard_distance":"sim"}),
    df_similarity.rename(columns={"GO_ID2":"A", "GO_ID1":"B", "Jaccard_distance":"sim"})
], ignore_index=True).set_index(["A","B"])["sim"]

# ——— 2) AD→GO map ———
AD_BioDomain_GOID_map = {
    'Synapse': 'GO:0045202',
    'Immune Response': 'GO:0006955',
    'Mitochondrial Metabolism': None,
    'Structural Stabilization': None,
    'Proteostasis': None,
    "Lipid Metabolism": 'GO:0006629',
    'Vasculature': None,
    'Endolysosome': 'GO:0036019',
    'Cell Cycle': 'GO:0007049',
    'Apoptosis': 'GO:0006915',
    'Oxidative Stress': None,
    'Myelination': 'GO:0042552',
    'Metal Binding and Homeostasis': None,
    'Autophagy': 'GO:0006914',
    'Epigenetic': None,
    'APP Metabolism': 'GO:0042982',
    'DNA Repair': 'GO:0006281',
    'RNA Spliceosome': None,
    'Tau Homeostasis': None,
}


# ——— 3) Loop ———
for idx in tqdm(range(len(df_go)), desc="Assigning top-5 Biodomains"):
# for idx in tqdm(range(10), desc="Assigning top-5 Biodomains testing"):
    go_id   = df_go.at[idx, 'nodeID']
    go_term = format_pathway(df_go.at[idx, 'node'])
    go_def  = graph.nodes[go_id].get('definition', 'No definition available')
    go_root = df_go.at[idx, 'root node']

    # build paths & structure text
    paths = get_root_paths(go_id)
    structure_lines = [" -> ".join(f"{nid} ({graph.nodes[nid]['name']})" for nid in path)
                       for path in paths]
    go_structure_text = "\n".join(structure_lines) or "No structure available"

    # — Similarity to each AD‐Biodomain GOID (fill N/A with 1.0) —
    sim_lines = []
    for domain, bd_goid in AD_BioDomain_GOID_map.items():
        sim = df_sim.get((go_id, bd_goid), 1.0) if bd_goid else 1.0
        # df_go.at[idx, f"sim_to_{domain.replace(' ','_')}"] = sim
        sim_lines.append(f"{domain}: {sim:.3f}")
    sim_text = "\n".join(sim_lines)

    # — Similarity along each path (term→ancestors) —
    path_sim_lines = []
    for path in paths:
        entries = []
        for nid in path:
            sim = df_sim.get((go_id, nid), 1.0)
            name = graph.nodes[nid]['name']
            entries.append(f"{nid} ({name}): {sim:.3f}")
        path_sim_lines.append(" → ".join(entries))
    path_sim_text = "\n\n".join(path_sim_lines) or "No paths available"

    # — Build prompt —
    prompt = f"""
You are a biomedical ontology expert.
Below is a GO term with its definition, full ontology paths, and Jaccard distances.
**Note:** smaller distance ⇒ greater similarity.

**Biodomain options:**
{domains_str}

**GO Term:** {go_term}
**Definition:** {go_def}
**Root ontology term:** {go_root}

**GO Structure (all root paths):**
{go_structure_text}

**Similarity to AD‐Biodomain GOIDs** (missing filled as 1.0):
{sim_text}

**Similarity along each GO path** (term → ancestors):
{path_sim_text}

From the list of Biodomains, choose the **top 5** labels that best fit this term—ranked most-to-least appropriate.
Do **not** reply “Unknown,” and return **exactly five** domain names, **without** numbering or bullets.
Please respond with five comma-separated items only.
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a biomedical ontology expert. "
                        "Always return exactly five ranked Biodomains—never 'Unknown'."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        top5 = resp.choices[0].message.content.strip()
    except Exception as e:
        top5 = f"ERROR: {e}"

    df_go.at[idx, 'biodomain'] = top5
    print(f"[{idx}] {go_term} -> Top-5: {top5}")

    time.sleep(1)

# ——— 4) Save ———
# df_go.to_csv("biodomain_results_top5_with_similarity_demo.csv", index=False)


# ——— 4) Save your enriched DataFrame ———
# df_go.to_csv(f"result/biodomain_results_top5_with_similarity_demo_{temperature}.csv", index=False)
df_go.to_csv(f"result/biodomain_results_top5_with_similarity_{temperature}.csv", index=False)