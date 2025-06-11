"""
A graph traversal algorithm that starts from the GO term (leaf node) and traverses up to the root node.
"""
import polars as pl
import fire
import obonet
import networkx as nx


def main(
    go_obo_path: str = '../data/go-basic.obo',
):
    graph = obonet.read_obo(go_obo_path)
    print(f'Number of GO terms: {len(graph)}; Number of edges: {graph.number_of_edges()}')
    result = nx.descendants(graph, 'GO:0006955')
    print(f'Number of descendants of GO:0006955: {len(result)}')
    """
    GO ID: GO:0000001, data: {'name': 'mitochondrion inheritance', 'namespace': 'biological_process', 'def': '"The distribution of mitochondria, including the mitochondrial genome, into daughter cells after mitosis or meiosis, mediated by interactions between mitochondria and the cytoskeleton." [GOC:mcc, PMID:10873824, PMID:11389764]', 'synonym': ['"mitochondrial inheritance" EXACT []'], 'is_a': ['GO:0048308', 'GO:0048311']}
    """
    for id_ in result:
        name = graph.nodes[id_]['name']
        print(f'GO ID: {id_}, Name: {name}')



def sanity_check(
    data_path: str = '../data/AD_Biological_Domain_GO_annotate.csv',
):
    data_df = pl.read_csv(
        data_path,
        infer_schema_length=10000
    )
    n_bio_domain = data_df.n_unique(subset='Biodomain')
    n_GO_ID = data_df.n_unique(subset='GO_ID')
    print(f'Number of unique rows: {data_df.height}')
    print(f'Number of unique biological domains: {n_bio_domain}')
    print(f'Number of unique GO IDs: {n_GO_ID}')


if __name__ == '__main__':
    fire.Fire()