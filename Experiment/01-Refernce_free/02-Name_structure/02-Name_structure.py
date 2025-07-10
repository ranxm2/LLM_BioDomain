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


# # --- Loop and assign Biodomains

# for go_index in tqdm(range(len(df_go)), desc="Assigning Biodomains testing"):
#     go_term = df_go.iloc[go_index]['node']
#     go_id = df_go.iloc[go_index]['nodeID']
#     go_def = term = graph.nodes[go_id]
#     go_root = df_go.iloc[go_index]['root node']
#     go_term = format_pathway(go_term)

#     go_structure = graph.nodes[go_id].get('structure', 'Unknown')
#     # get all root‐paths
#     paths = get_root_paths(go_id)

#     # turn each path into a “GO:0000000 (Name) -> … -> Root” string
#     structure_lines = []
#     for path in paths:
#         names = [f"{nid} ({graph.nodes[nid]['name']})" for nid in path]
#         structure_lines.append(" -> ".join(names))

#     # join multiple paths with newlines (or use '; ' if you prefer)
#     go_structure_text = "\n".join(structure_lines)



#     prompt = f"""
# You are a biomedical ontology expert.  
# Below is a GO term and its context.  From the list of Biodomains, choose **only** the single best label—or 'Unknown'—that fits this term.

# **Biodomain options:**
# {domains_str}

# **GO Term:** { go_term }  
# **Definition:** {go_def}  
# **Root ontology term:** {go_root} 
# **GO Structure:** {go_structure_text}

# Please respond with exactly one item from the Biodomain list (or 'Unknown').
# """

#     try:
#         resp = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "You are a biomedical ontology expert. Infer only the most appropriate Biodomain or 'unknown'."},
#                 {"role": "user",   "content": prompt}
#             ],
#             temperature=0
#         )
#         bd = resp.choices[0].message.content.strip()
#     except Exception as e:
#         bd = f"ERROR: {e}"

#     df_go.loc[go_index, 'biodomain'] = bd
#     print(f"Pathway: {go_term } -> Biodomain: {bd}\n")
#     time.sleep(1)


# df_go.to_csv("biodomain_results_name_structure_0630.csv", index=False)




# --- Loop and assign top-5 Biodomains
for go_index in tqdm(range(len(df_go)), desc="Assigning top-5 Biodomains"):
    go_term = df_go.iloc[go_index]['node']
    go_id   = df_go.iloc[go_index]['nodeID']
    go_def  = graph.nodes[go_id].get('definition', 'No definition available')
    go_root = df_go.iloc[go_index]['root node']
    go_term = format_pathway(go_term)

    # Build GO structure text from all root paths
    paths = get_root_paths(go_id)
    structure_lines = []
    for path in paths:
        names = [f"{nid} ({graph.nodes[nid]['name']})" for nid in path]
        structure_lines.append(" -> ".join(names))
    go_structure_text = "\n".join(structure_lines) or "No structure available"

    prompt = f"""
You are a biomedical ontology expert.  
Below is a GO term with its definition and full ontology paths.
From the list of Biodomains, choose the **top 5** labels that best fit this term—ranked most-to-least appropriate.  
**Do not** ever reply “Unknown,” and **do not** return more or fewer than five.  
**List only** the domain names, **without** any numbering, bullets, or additional text.

**Biodomain options:**
{domains_str}

**GO Term:** {go_term}  
**Definition:** {go_def}  
**Root ontology term:** {go_root}  
**GO Structure (all root paths):**
{go_structure_text}

Please respond with exactly five items, separated by commas, in descending order of relevance.
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a biomedical ontology expert. "
                        "Always return exactly five ranked Biodomains—never 'Unknown'—for any GO term."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        top5 = resp.choices[0].message.content.strip()
    except Exception as e:
        top5 = f"ERROR: {e}"

    df_go.at[go_index, 'biodomain'] = top5
    print(f"{go_term} -> Top-5 Biodomains: {top5}")

    time.sleep(1)

# Save results
df_go.to_csv("biodomain_results_top5_with_structure_0630.csv", index=False)
# df_go.to_csv("biodomain_results_top5_with_structure_demo.csv", index=False)
