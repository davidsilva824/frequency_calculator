import pandas as pd
import os
import itertools
import numpy as np

# Load Excel
df_excel = pd.read_excel("SUBTLEX-UK.xlsx", sheet_name="Sheet1")
df_excel['Spelling'] = df_excel['Spelling'].str.lower()

# Explicit list of CSV files
csv_files = [
    "regular_singulars.csv",
    "regular_plurals.csv",
    "irregular_singulars.csv",
    "irregular_plurals.csv"
]

# Store Zipf values per group
group_zipfs = {}
results = []

for file in csv_files:
    group_name = file.replace(".csv", "")
    words = pd.read_csv(file, header=None)[0].str.lower()
    matched = df_excel[df_excel['Spelling'].isin(words)]
    group_zipfs[group_name] = matched['LogFreq(Zipf)'].dropna().values
    results.append((group_name, matched['LogFreq(Zipf)'].mean(), matched.shape[0]))

# Display means
results_df = pd.DataFrame(results, columns=["Group", "Mean_Zipf", "Words_Found"])
print(results_df)

# Function to compute Cohen's d
def cohens_d(x, y):
    nx, ny = len(x), len(y)
    pooled_std = np.sqrt(((nx - 1) * np.std(x, ddof=1)**2 + (ny - 1) * np.std(y, ddof=1)**2) / (nx + ny - 2))
    return (np.mean(x) - np.mean(y)) / pooled_std

# Compute selected Cohen's d
print("\nCohen's d values:")
skip = {
    frozenset(['regular_singulars', 'irregular_plurals']),
    frozenset(['regular_plurals', 'irregular_singulars']),
}

for (g1, x), (g2, y) in itertools.combinations(group_zipfs.items(), 2):
    if frozenset([g1, g2]) in skip:
        continue
    d = cohens_d(x, y)
    print(f"{g1} vs {g2}: d = {d:.3f}")

# Singulars vs Plurals
all_singulars = np.concatenate([group_zipfs[g] for g in group_zipfs if "singular" in g])
all_plurals = np.concatenate([group_zipfs[g] for g in group_zipfs if "plural" in g])
d_sing_vs_plur = cohens_d(all_singulars, all_plurals)
print(f"\nAll singulars vs all plurals: d = {d_sing_vs_plur:.3f}")

# Regulars vs Irregulars
all_regulars = np.concatenate([group_zipfs[g] for g in group_zipfs if "regular" in g])
all_irregulars = np.concatenate([group_zipfs[g] for g in group_zipfs if "irregular" in g])
d_reg_vs_irreg = cohens_d(all_regulars, all_irregulars)
print(f"All regulars vs all irregulars: d = {d_reg_vs_irreg:.3f}")