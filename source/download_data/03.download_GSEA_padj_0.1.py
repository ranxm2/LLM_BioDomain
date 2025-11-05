import pandas as pd
import argparse
import os
import obonet
import networkx as nx
import requests
import json

# change the working directory /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder \
os.chdir("/projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder")


# the GSEA data download from the https://www.gsea-msigdb.org/gsea/msigdb/download_file.jsp?filePath=/msigdb/release/2025.1.Hs/c5.all.v2025.1.Hs.json

# Load the JSON file
file_path = "data/c5.all.v2025.1.Hs.json"
with open(file_path, "r") as f:
    c5 = json.load(f)

# Extract exactSource for each gene set
df_exact_source = pd.DataFrame([
    {"pathway": gs, "GOID": info.get("exactSource", "")}
    for gs, info in c5.items()
])


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


# load the   'data/FXS_bidomain_annotation_JX_raw.csv
df_FXS = pd.read_csv("data/D154-GSVA-padj-0.1.csv")
df_FXS = df_FXS[["pathway"]]
df_FXS = df_FXS.merge(df_exact_source, on="pathway", how="left")


#  .to_csv('../../data/go_root_paths.csv', index=False)
df_roots = pd.read_csv("data/go_root_paths.csv")

# merge it to df_FXS
df_FXS =  df_FXS.merge(df_roots, how="left", left_on="GOID", right_on="nodeID")

df_FXS = df_FXS[["pathway", "GOID", "root node","root node ID"]]

# rename the colnames 
df_FXS.columns = ["node", "nodeID", "root node", "root node ID"]

# save the result to csv
df_FXS.to_csv("data/D154-GSVA-padj-0.1-node.csv", index=False)




# load the   'data/FXS_bidomain_annotation_JX_raw.csv
df_FXS = pd.read_csv("data/D56-GSVA-padj-0.1.csv")
df_FXS = df_FXS[["pathway"]]
df_FXS = df_FXS.merge(df_exact_source, on="pathway", how="left")


#  .to_csv('../../data/go_root_paths.csv', index=False)
df_roots = pd.read_csv("data/go_root_paths.csv")

# merge it to df_FXS
df_FXS =  df_FXS.merge(df_roots, how="left", left_on="GOID", right_on="nodeID")

df_FXS = df_FXS[["pathway", "GOID", "root node","root node ID"]]

# rename the colnames 
df_FXS.columns = ["node", "nodeID", "root node", "root node ID"]

# save the result to csv
df_FXS.to_csv("data/D56-GSVA-padj-0.1-node.csv", index=False)






# load the   'data/FXS_bidomain_annotation_JX_raw.csv
df_FXS = pd.read_csv("data/D154-GSVA-padj-0.1_4_samples.csv")
df_FXS = df_FXS[["pathway"]]
df_FXS = df_FXS.merge(df_exact_source, on="pathway", how="left")


#  .to_csv('../../data/go_root_paths.csv', index=False)
df_roots = pd.read_csv("data/go_root_paths.csv")

# merge it to df_FXS
df_FXS =  df_FXS.merge(df_roots, how="left", left_on="GOID", right_on="nodeID")

df_FXS = df_FXS[["pathway", "GOID", "root node","root node ID"]]

# rename the colnames 
df_FXS.columns = ["node", "nodeID", "root node", "root node ID"]

# save the result to csv
df_FXS.to_csv("data/D154-GSVA-padj-0.1_4_samples-node.csv", index=False)


# save to csv file
# df_FXS.to_csv("data/FXS_bidomain_annotation_JX_with_exact_source.csv", index=False)

# path to your downloaded file
obo_path = 'data/go-basic.obo'
graph = obonet.read_obo(obo_path)

# # create a new dataframe with the nodeid and the name of the nodes
df_go_graph = pd.DataFrame(graph.nodes(data=True), columns=['nodeID', 'data'])
df_go_graph['name'] = df_go_graph['data'].apply(lambda x: x.get('name', ''))
df_go_graph['nodeID'] = df_go_graph['nodeID'].astype(str)
df_go_graph = df_go_graph[['nodeID', 'name']]

# # create a new column with the lower case name of the nodes as match_text
# df_go_graph['match_text'] = df_go_graph['name'].str.lower()
# df_go_graph['match_text'] = df_go_graph['match_text'].str.replace(" ", "_")
# df_go_graph['match_text'] = df_go_graph['match_text'].str.replace(",", "")
# df_go_graph['match_text'] = df_go_graph['match_text'].str.replace("'", "")
# df_go_graph['match_text'] = df_go_graph['match_text'].str.replace('"', "")  

# # use missing_exact_source to match with df_go_graph
# missing_exact_source = df_FXS[df_FXS["GOID"].isnull()]
# missing_exact_source['match_text'] = missing_exact_source['Lower_case'].str[5:].str.lower()
# missing_exact_source = missing_exact_source.merge(df_go_graph[['match_text', 'nodeID']], on='match_text', how='left')

# # see how many rows are matched
# matched_rows = missing_exact_source[missing_exact_source['nodeID'].notnull()]
# print(f"Number of matched rows: {len(matched_rows)}")

# # for the unmatched rows, print their result
# unmatched_rows = missing_exact_source[missing_exact_source['nodeID'].isnull()]
# print(f"Number of unmatched rows: {len(unmatched_rows)}")

# check if all the infor are in the graph

df_FXS_order = pd.read_csv("data/FXS_bidomain_annotation_certain.csv")

# check if all the GO_ID in df_FXS_order are in the graph
missing_goid = df_FXS_order[~df_FXS_order['GO_ID'].isin(df_go_graph['nodeID'])]
if not missing_goid.empty:
    print("The following GOIDs are missing in the graph:")
    print(missing_goid['GO_ID'].unique())
else:
    print("All GOIDs in df_FXS_order are present in the graph.")    