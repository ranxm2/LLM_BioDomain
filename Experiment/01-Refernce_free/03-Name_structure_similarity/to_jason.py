import pandas as pd
import json
import random
import numpy as np

# Load CSV
df = pd.read_csv("biodomain_results_top5_0630.csv")

# Set random seed for reproducibility
random.seed(42)

# Define output list
output = []

# Go through each row
for _, row in df.iterrows():
    go_id = row['nodeID']
    
    # Split and clean biodomain labels
    biodomains = [bd.strip() for bd in row['biodomain'].split(',')]
    
    # True label: set each domain to 1.0
    biodomain_true = {bd: 1.0 for bd in biodomains}

    # Get remaining candidates to simulate prediction
    all_domains = sorted(set(biodomains + [
        "APP Metabolism", "Cell Cycle", "Apoptosis", "Vasculature", "Immune Response", 
        "Synapse", "RNA Spliceosome", "Lipid Metabolism", "Metal Binding and Homeostasis", 
        "Endolysosome", "DNA Repair", "Oxidative Stress", "Autophagy", "Proteostasis", 
        "Mitochondrial Metabolism", "Structural Stabilization"
    ]))
    
    candidates = [d for d in all_domains if d not in biodomain_true]
    
    # Randomly sample remaining top-k (simulate prediction)
    sample_k = max(0, 5 - len(biodomain_true))
    pred_random = random.sample(candidates, k=sample_k)
    pred_scores = list(np.linspace(0.9, 0.1, num=sample_k))
    
    biodomain_pred = {bd: 1.0 for bd in biodomain_true}  # known domains get 1.0
    biodomain_pred.update({bd: score for bd, score in zip(pred_random, pred_scores)})
    
    # Append entry
    output.append({
        "GO_ID": go_id,
        "Biodomain_true": biodomain_true,
        "Biodomain_pred": biodomain_pred
    })

# Save to JSON
with open("converted_biodomain_predictions.json", "w") as f:
    json.dump(output, f, indent=2)
