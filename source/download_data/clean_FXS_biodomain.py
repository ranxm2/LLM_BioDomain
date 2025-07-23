

import pandas as pd
import argparse
import os
import obonet
import networkx as nx
import requests

# change the working directory /projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder \
os.chdir("/projects/compbio/users/xran2/wen/JX/02-AI-BioDomain/git_folder")


import os
import requests
import zipfile

# Direct download URL for MSigDB v2025.1 Hs zip
download_url = (
    "https://data.broadinstitute.org/gsea-msigdb/msigdb/"
    "release/2025.1.Hs/"
    "msigdb_v2025.1.Hs_files_to_download_locally.zip"
)
output_zip = "data/msigdb_v2025.1.Hs_files_to_download_locally.zip"
extract_dir = "data/msigdb_v2025.1.Hs_files_to_download_locally"

# Ensure the data directory exists
os.makedirs(os.path.dirname(output_zip), exist_ok=True)

# 1. Verify the URL is accessible and looks like a ZIP
head = requests.head(download_url, allow_redirects=True)
if head.status_code != 200:
    raise RuntimeError(f"Failed to access URL (status {head.status_code})")
content_type = head.headers.get('Content-Type', '')
if 'zip' not in content_type.lower():
    print(f"Warning: Content-Type is {content_type}. Proceeding with download...")

# 2. Download with streaming
with requests.get(download_url, stream=True) as r:
    r.raise_for_status()
    with open(output_zip, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
print(f"Download complete: {output_zip}")

# 3. Unzip the downloaded file
with zipfile.ZipFile(output_zip, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)
print(f"Extraction complete to directory: {extract_dir}")








# load the   'data/FXS_bidomain_annotation_JX_raw.csv
df_FXS = pd.read_csv("data/FXS_bidomain_annotation_JX_raw.csv")

# delect the first 5 characters of the lower_Case column
df_FXS['match_text'] = df_FXS['Lower_case'].str[5:]


df_go = pd.read_csv("data/go_root_paths.csv")
# turnt he node column to lower case
df_go['match_text'] = df_go['node'].str.lower()
df_go['match_text'] = df_go['match_text'].str.replace(" ", "_")

# only keep the matched rows in the df_go
df_go_matched = df_go[df_go['match_text'].isin(df_FXS['match_text'])]

# find out those are nor in the df_go
df_FXS_not_in_go = df_FXS[~df_FXS['match_text'].isin(df_go['match_text'])]








# path to your downloaded file
obo_path = 'data/go-basic.obo'

# read the OBO into a directed graph
graph = obonet.read_obo(obo_path)

# check if the 'GO:0046102' is in the graph
if 'GO:0046102' in graph.nodes:
    print("GO:0046102 is in the graph")


# 1. Point to your unzipped GAF file
gaf_path = 'data/goa_human.gaf'

# 2. Define the 17 GAF v2 column names
colnames = [
    'DB',
    'DB_Object_ID',
    'DB_Object_Symbol',
    'Qualifier',
    'GO_ID',
    'DB_Reference',
    'Evidence_Code',
    'With_From',
    'Aspect',
    'DB_Object_Name',
    'DB_Object_Synonym',
    'DB_Object_Type',
    'Taxon',
    'Date',
    'Assigned_By',
    'Annotation_Extension',
    'Gene_Product_Form_ID'
]

# 3. Read the file, skipping comment lines ('!' at start)
gaf = pd.read_csv(
    gaf_path,
    sep='\t',
    comment='!',
    header=None,
    names=colnames,
    dtype=str
)
# show the table of DB_Object_Type
print(gaf['DB_Object_Type'].value_counts())

# check if the 'GO:0046102' is in the gaf
if 'GO:0046102' in gaf['GO_ID'].values:
    print("GO:0046102 is in the gaf")

# check the 	ADA gene in the gag
gaf_ada = gaf[gaf['DB_Object_Symbol'] == 'ADA']



# Now check if all the item in df_FXS are in the graph, it should be the name of the nodes
graph_nodes_name = [data.get('name', '') for node, data in graph.nodes(data=True)]
# turn it into lower case and replace spaces with underscores
graph_nodes_name = [name.lower().replace(" ", "_") for name in graph_nodes_name]
# replace the - with _
graph_nodes_name = [name.replace("-", "_") for name in graph_nodes_name]
# delete the "'" with ""
graph_nodes_name = [name.replace("'", "") for name in graph_nodes_name]
# delete the , with ""
graph_nodes_name = [name.replace(",", "") for name in graph_nodes_name]

#chcek if the inosine_metabolic_process is in the graph_nodes_name
if 'inosine_metabolic_process' in graph_nodes_name:
    print("inosine_metabolic_process is in the graph_nodes_name")


df_FXS_graph = df_FXS[df_FXS['match_text'].isin(graph_nodes_name)]


# check if the inosine_metabolic_process is in df_FXS_graph
if 'inosine_metabolic_process' in df_FXS_graph['match_text'].values:
    print("inosine_metabolic_process is in the df_FXS_graph")

# check the name of GO:0006458 for the graph
if 'GO:0006458' in graph.nodes:
    print("GO:0006458 is in the graph")
    print(graph.nodes['GO:0006458'].get('name', 'No name found'))
    # turn it to lower case and replace spaces with underscores
    go_0006458_name = graph.nodes['GO:0006458'].get('name', '').lower().replace(" ", "_")
    print(f"GO:0006458 name: {go_0006458_name}")
    # turn the "-" to "_" 
    go_0006458_name = go_0006458_name.replace("-", "_")
    print(f"GO:0006458 name after replace: {go_0006458_name}")
    # now remove the "' " with ""
    go_0006458_name = go_0006458_name.replace("'", "")
    print(f"GO:0006458 name after remove: {go_0006458_name}")



# find out those are not in the graph
df_FXS_not_in_graph = df_FXS[~df_FXS['match_text'].isin(graph_nodes_name)]