from openai import OpenAI
import openai
import pandas as pd
import time
from tqdm import tqdm
import obonet
import networkx as nx

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





# --- Loop and assign Biodomains
go_index=0
for go_index in tqdm(range(100), desc="Assigning Biodomains testing"):
# for go_index in tqdm(range(len(df_go)), desc="Assigning Biodomains"):
    go_term = df_go.iloc[go_index]['node']
    go_id = df_go.iloc[go_index]['nodeID']
    go_def = term = graph.nodes[go_id]
    go_root = df_go.iloc[go_index]['root node']
    go_term = format_pathway(go_term)
    
    #-----------------------------------
    # get the GO structure
    #-----------------------------------
    paths = get_root_paths(go_id)
    structure_lines = []
    for path in paths:
        names = [f"{nid} ({graph.nodes[nid]['name']})" for nid in path]
        structure_lines.append(" -> ".join(names))

    # join multiple paths with newlines (or use '; ' if you prefer)
    go_structure_text = "\n".join(structure_lines)

    #-----------------------------------
    # get the GO similarity
    #-----------------------------------
    ancestors = get_ancestors(go_id)
    go_ancestors = [go_id] + list(ancestors)
    go_similarities = df_similarity.loc[go_ancestors, go_ancestors].values

    # build the mask
    mask = (
        df_similarity['GO_ID1'].isin( go_ancestors) &
        df_similarity['GO_ID2'].isin( go_ancestors)
    )

    # filter and (if you plan to modify) make a copy to avoid any warnings
    df_filtered = df_similarity.loc[mask].copy()

    # convert the similarity values to a string
    







    prompt = f"""
You are a biomedical ontology expert.  
Below is a GO term and its context.  From the list of Biodomains, choose **only** the single best label—or 'Unknown'—that fits this term.

**Biodomain options:**
{domains_str}

**GO Term:** { go_term }  
**Definition:** {go_def}  
**Root ontology term:** {go_root} 
**GO Structure:** {go_structure_text}

Please respond with exactly one item from the Biodomain list (or 'Unknown').
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a biomedical ontology expert. Infer only the most appropriate Biodomain or 'unknown'."},
                {"role": "user",   "content": prompt}
            ],
            temperature=0
        )
        bd = resp.choices[0].message.content.strip()
    except Exception as e:
        bd = f"ERROR: {e}"

    df_go.loc[go_index, 'biodomain'] = bd
    print(f"Pathway: {go_term } -> Biodomain: {bd}\n")
    time.sleep(1)


df_go.to_csv("biodomain_results_name_structure_0609.csv", index=False)


