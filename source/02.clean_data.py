import obonet
import networkx as nx


# -------------------------------------------------------------------------------------------
#                          Load GO Structure
# ------------------------------------------------------------------------------------------


# path to your downloaded file
obo_path = '../data/go-basic.obo'

# read the OBO into a directed graph
graph = obonet.read_obo(obo_path)

# inspect how many terms you loaded
print(f'Loaded {len(graph.nodes())} GO terms')

# example: look up a specific term by its GO ID
go_id =  'GO:0005634'
term = graph.nodes[go_id]
print(f"{go_id}: {term.get('name')}  ({term.get('namespace')})")

def get_ancestors(go_id):
    """
    Return the set of all ancestor GO IDs (more general terms)
    reachable from go_id by following parent links.
    """
    # Since edges are child→parent, 
    # descendants(graph, go_id) will walk from your term up
    return nx.descendants(graph, go_id)

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

# 3. Usage example

my_go = 'GO:0005634'  # e.g. “biological_process”

# a) List all ancestor terms
ancestors = get_ancestors(my_go)
print(f'Found {len(ancestors)} ancestors of {my_go}\n')
for aid in sorted(ancestors):
    name = graph.nodes[aid].get('name', '')
    print(f'  {aid:12s} {name}')

# b) Print every path from your term up to a root
print('\nPaths up to root terms:')
for path in get_root_paths(my_go):
    # join with “→” and annotate each node with its name
    names = [f"{nid} ({graph.nodes[nid]['name']})" for nid in path]
    print('  ' + ' -> '.join(names))



# -------------------------------------------------------------------------------------------
#                          Load GO Annotations
# ------------------------------------------------------------------------------------------

# load the GAF file
import pandas as pd

# 1. Point to your unzipped GAF file
gaf_path = '../data/goa_human.gaf'

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


# 4. Extract just gene symbol and protein ID, drop duplicates

# mapping = (
#     gaf[['DB_Object_Symbol', 'DB_Object_ID','GO_ID']]
#     .dropna()
#     .drop_duplicates()
# )

mapping = (
    gaf[['DB_Object_Symbol', 'DB_Object_ID']]
    .dropna()
    .drop_duplicates()
)

# 5. Group by gene symbol to list all proteins per gene
grouped = mapping.groupby('DB_Object_Symbol')['DB_Object_ID'].apply(list)

# 6. Print out the mapping
for gene_symbol, proteins in grouped.items():
    print(f"{gene_symbol}: {', '.join(proteins)}")




# ------------------------------------------------------------------------------------------
#               check overlap
# ------------------------------------------------------------------------------------------

grapg_nodes = list(graph.nodes())
GAF_nodes = gaf['GO_ID'].dropna().unique().tolist()
print(f"GO terms in graph: {len(grapg_nodes)}")
print(f"GO terms in GAF: {len(GAF_nodes)}")
overlap = set(grapg_nodes) & set(GAF_nodes)
print(f"Overlap: {len(overlap)} terms")


# ------------------------------------------------------------------------------------------
#              Make Annotations for Each GO Term to Root Path
# ------------------------------------------------------------------------------------------

import pandas as pd
import networkx as nx

# 1. Identify the roots in your graph (nodes with no outgoing edges)
roots = [n for n, outdeg in graph.out_degree() if outdeg == 0]

# 2. Build up a list of dicts, one per (node, root) pair
rows = []
for go_id, data in graph.nodes(data=True):
    node_name = data.get('name', '')
    # find which of the roots is an ancestor of go_id (or itself)
    ancestors = nx.descendants(graph, go_id)
    reachable_roots = [r for r in roots if (r in ancestors) or (r == go_id)]
    # in GO you’ll normally get exactly one reachable_root per term
    for root_id in reachable_roots:
        root_name = graph.nodes[root_id].get('name', '')
        rows.append({
            'node':         node_name,
            'nodeID':       go_id,
            'root node':    root_name,
            'root node ID': root_id
        })

# 3. Create the DataFrame
df_roots = pd.DataFrame(rows,
                        columns=['node','nodeID','root node','root node ID'])

# 4. Inspect
print(df_roots.head())

# only keep the overlapping GO terms
df_roots = df_roots[df_roots['nodeID'].isin(GAF_nodes)]
df_roots.shape

# 5. Save to CSV
df_roots.to_csv('../data/go_root_paths.csv', index=False)



# ------------------------------------------------------------------------------------------
#                Calculate Pairwise Jaccard Distances of GO Annotations
# ------------------------------------------------------------------------------------------



import pandas as pd
import numpy as np
from itertools import combinations
from tqdm import tqdm

# 1. Load your un‐gzipped GAF
gaf_path = '../data/goa_human.gaf'
colnames = [
    'DB','DB_Object_ID','DB_Object_Symbol','Qualifier','GO_ID','DB_Reference',
    'Evidence_Code','With_From','Aspect','DB_Object_Name','DB_Object_Synonym',
    'DB_Object_Type','Taxon','Date','Assigned_By','Annotation_Extension',
    'Gene_Product_Form_ID'
]
gaf = pd.read_csv(
    gaf_path,
    sep='\t',
    comment='!',
    header=None,
    names=colnames,
    dtype=str
)

# 2. Map each GO term to the set of proteins annotated to it
go2proteins = gaf.groupby('GO_ID')['DB_Object_ID'].apply(lambda ids: set(ids.dropna()))

# 3. Prepare terms list and Jaccard‐distance DataFrame
terms = go2proteins.index.tolist()
n = len(terms)
jdist = pd.DataFrame(
    np.zeros((n, n)),
    index=terms,
    columns=terms,
    dtype=float
)

# 4. Compute pairwise Jaccard distance with tqdm progress bar
total_pairs = n * (n - 1) // 2
for t1, t2 in tqdm(combinations(terms, 2), total=total_pairs, desc='Computing Jaccard'):
    set1 = go2proteins[t1]
    set2 = go2proteins[t2]
    inter = len(set1 & set2)
    union = len(set1 | set2)
    dist = 1 - (inter / union) if union else 0.0
    jdist.at[t1, t2] = dist
    jdist.at[t2, t1] = dist

# exctra one pair as the sample
jdist.at['GO:0000009', 'GO:0000002']
t1 = 'GO:0000009'  # e.g. "mitochondrion inheritance"
t2 = 'GO:0000002'  # e.g. "mitochondrion organization"



# 5. (Optional) Save or inspect
jdist.to_csv('../data/go_jaccard_distance.csv')
print('Done! Pairwise Jaccard distances saved to go_jaccard_distance.csv')


# #  check with the 1:5 row and 1:5 column
# print(jdist.iloc[:50, :50])

# # plot a heatmap of the Jaccard distances with 1:500 rows and 1:500 columns
# import seaborn as sns
# import matplotlib.pyplot as plt
# plt.figure(figsize=(10, 8))
# plot_matrix = jdist.iloc[:500, :500].copy()
# # remove the values that equal to 1
# plot_matrix[plot_matrix == 1] = np.nan  # set Jaccard distance of 1 to NaN for better visualization
# plt.figure(figsize=(12, 10))

# sns.heatmap(plot_matrix, cmap='viridis', square=True, cbar_kws={'label': 'Jaccard Distance'})        
# plt.title('Pairwise Jaccard Distances of GO Terms')
# plt.tight_layout()


# import pandas as pd
# from itertools import combinations

# # `terms` is your list of GO IDs, and `jdist` is the DataFrame you filled.
# records = []
# for t1, t2 in tqdm(combinations(terms, 2), total=total_pairs, desc='Computing Jaccard'):
#     records.append((t1, t2, jdist.at[t1, t2]))

# # Build the long‐form DataFrame
# df_long = pd.DataFrame(records, columns=['GO_ID1', 'GO_ID2', 'Jaccard_distance'])

# # (Optional) save to CSV
# df_long.to_csv('go_jaccard_long.csv', index=False)

# # Quick peek
# print(df_long.head())


import numpy as np

# Create a boolean mask for the upper triangle (k=1 excludes the diagonal)
mask = np.triu(np.ones(jdist.shape, dtype=bool), k=1)

# Apply the mask, stack the remaining values, and reset the index
df_long = (
    jdist.where(mask)
         .stack()
         .reset_index()
)

# Rename the auto‐generated columns
df_long.columns = ['GO_ID1', 'GO_ID2', 'Jaccard_distance']

# (Optional) save
df_long.to_csv('../data/go_jaccard_long.csv', index=False)

print(df_long.head())



# load the long‐form DataFrame
df_long = pd.read_csv('../data/go_jaccard_long.csv')

# delete the rows where Jaccard_distance is 1
df_long = df_long[df_long['Jaccard_distance'] < 1]

shape = df_long.shape

# save the DataFrame to a new CSV file
df_long.to_csv('../data/go_jaccard_long_filtered.csv', index=False)






# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import MultiLabelBinarizer
# from sklearn.metrics import pairwise_distances
# from tqdm import tqdm

# # 1. Reload GAF → go2proteins mapping (as before)
# gaf_path = '../data/goa_human.gaf'
# colnames = [
#     'DB','DB_Object_ID','DB_Object_Symbol','Qualifier','GO_ID','DB_Reference',
#     'Evidence_Code','With_From','Aspect','DB_Object_Name','DB_Object_Synonym',
#     'DB_Object_Type','Taxon','Date','Assigned_By','Annotation_Extension',
#     'Gene_Product_Form_ID'
# ]
# gaf = pd.read_csv(
#     gaf_path, sep='\t', comment='!', header=None,
#     names=colnames, dtype=str
# )
# go2proteins = gaf.groupby('GO_ID')['DB_Object_ID'].apply(lambda ids: set(ids.dropna()))
# terms = go2proteins.index.tolist()

# # 2. Binarize into sparse matrix, then to dense boolean
# mlb = MultiLabelBinarizer(sparse_output=True)
# X_sparse = mlb.fit_transform(go2proteins.values)
# X_bool = X_sparse.astype(bool).toarray()   # shape: (n_terms, n_proteins)

# # 3. Prepare output DataFrame
# n = X_bool.shape[0]
# jdist = pd.DataFrame(
#     np.zeros((n, n), dtype=float),
#     index=terms,
#     columns=terms
# )

# # 4. Choose a block size (tweak based on your RAM; e.g. 200–1000)
# block_size = 500

# # 5. Compute in blocks
# for start in tqdm(range(0, n, block_size)):
#     stop = min(start + block_size, n)
#     # distances between rows [start:stop] and all rows
#     D_block = pairwise_distances(
#         X_bool[start:stop],
#         X_bool,
#         metric='jaccard',
#         n_jobs=-1
#     )
#     # Assign into the big matrix
#     jdist.iloc[start:stop, :] = D_block

# # 6. (Optional) Save or inspect
# jdist.to_csv('../data/go_jaccard_distance_blockwise.csv')
# print("Done — block‐wise Jaccard matrix saved.")









# #-------------------------------------------------------------------------------------------
# # ----------------------------  Fast Jaccard Distance Matrix Calculatio     ----------------
# # ------------------------------------------------------------------------------------------



# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import MultiLabelBinarizer

# # 1) Reload GAF → go2proteins (as you already have)
# gaf_path = '../data/goa_human.gaf'
# colnames = [
#     'DB','DB_Object_ID','DB_Object_Symbol','Qualifier','GO_ID','DB_Reference',
#     'Evidence_Code','With_From','Aspect','DB_Object_Name','DB_Object_Synonym',
#     'DB_Object_Type','Taxon','Date','Assigned_By','Annotation_Extension',
#     'Gene_Product_Form_ID'
# ]
# gaf = pd.read_csv(
#     gaf_path, sep='\t', comment='!', header=None,
#     names=colnames, dtype=str
# )
# go2proteins = gaf.groupby('GO_ID')['DB_Object_ID'].apply(lambda ids: set(ids.dropna()))
# terms = go2proteins.index.tolist()

# # 2) Binarize to boolean matrix
# mlb = MultiLabelBinarizer(sparse_output=True)
# X_sparse = mlb.fit_transform(go2proteins.values)   # sparse (n_terms × n_proteins)
# X_bool   = X_sparse.astype(bool).toarray()         # dense bool matrix

# # 3) Compute all pairwise |A∩B| with a single mat‐mul
# X_int = X_bool.astype(int)         # now 0/1 ints
# inter = np.dot(X_int, X_int.T)   # shape (n_terms, n_terms)

# # 4) Get |A| and |B|, broadcast to build |A∪B|
# sizes = X_int.sum(axis=1)          # array of length n_terms
# union = sizes[:, None] + sizes[None, :] - inter

# # 5) Jaccard similarity and distance
# #    J = |A∩B| / |A∪B|     →  D = 1 − J
# j_sim  = inter / union
# j_sim[union == 0] = 0.0           # avoid NaNs when union==0
# j_dist = 1.0 - j_sim

# # 6) Wrap in a DataFrame
# jdist_df = pd.DataFrame(j_dist, index=terms, columns=terms)

# # Optional: zero the diagonal (distance of a term to itself)
# np.fill_diagonal(jdist_df.values, 0.0)

# # Save or inspect
# jdist_df.to_csv('go_jaccard_distance_matrix.csv')
# print("Done—Jaccard distance matrix saved.")
