from critdd import Diagram
import pandas as pd

# download example data
exp_result_path = "./Experiment_summary/exp_metrics_CD.csv"
# use all ranking metrics
df = pd.read_csv(exp_result_path)
# Melt the DataFrame
df_long = df.melt(
    id_vars=["dataset", "method"],
    value_vars=["precision@1", "precision@2", "recall@1", "recall@2"],
    var_name="metric",
    value_name="perf"
)
# Create the new dataset column
df_long["dataset"] = df_long["dataset"] + "-" + df_long["metric"]
# Drop the old 'metric' column
df_long = df_long.drop(columns=["metric"])
# Reorder columns if needed
df_long = df_long[["dataset", "perf", "method"]]
df = df_long
df = df.pivot(
    index = "dataset",
    columns = "method",
    values = "perf"
)

# create a CD diagram from the Pandas DataFrame
diagram = Diagram(
    df.to_numpy(),
    treatment_names = df.columns,
    maximize_outcome = True
)

# inspect average ranks and groups of statistically indistinguishable treatments
print(diagram.average_ranks) # the average rank of each treatment
print(diagram.get_groups(alpha=.05, adjustment="holm"))
print(diagram.get_groups(alpha=.05, adjustment="bonferroni"))

# export the diagram to a file
diagram.to_file(
    "./Experiment_summary/prec_at_1.tex",
    alpha = .05,
    adjustment = "holm",
    #adjustment = "bonferroni",
    reverse_x = True,
    axis_options = {"title": ""},
)