
# How do multidimensional poverty rates change over time across countries, 
# and how do rural–urban and gender differences shape these poverty patterns?

import os
print("Running:", os.path.abspath(__file__))

import pandas as pd
import numpy as np

# ---------------------------------------------------
# 1. Load dataset
# ---------------------------------------------------
df = pd.read_csv(
    "Proportion of population living in multidimensional poverty (%).csv",
    engine="python",
    on_bad_lines="skip"
)

# ---------------------------------------------------
# 2. Remove junk "Unnamed" columns
# ---------------------------------------------------
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# ---------------------------------------------------
# 3. Standardize column names
# ---------------------------------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

# ---------------------------------------------------
# 4. Rename geoareaname → country
# ---------------------------------------------------
if "geoareaname" in df.columns:
    df = df.rename(columns={"geoareaname": "country"})

# ---------------------------------------------------
# 5. Clean categorical fields
# ---------------------------------------------------
df["country"] = df["country"].astype(str).str.strip().str.title()
df["age"] = df["age"].astype(str).str.strip().str.upper()
df["location"] = df["location"].astype(str).str.strip().str.upper()
df["sex"] = df["sex"].astype(str).str.strip().str.upper()

# Fill missing units & observation status
df["units"] = df["units"].fillna("PERCENT")
df["observation_status"] = df["observation_status"].fillna("UNKNOWN")

# ---------------------------------------------------
# 6. Identify year columns (2014–2024)
# ---------------------------------------------------
year_cols = [col for col in df.columns if col.isdigit()]

# Convert to numeric
for col in year_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------------------------------------------------
# 7. Fill missing numeric values by country mean
# ---------------------------------------------------
df[year_cols] = df.groupby("country")[year_cols].transform(
    lambda x: x.fillna(x.mean())
)

# ---------------------------------------------------
# 8. Remove impossible values (0–100%)
# ---------------------------------------------------
for col in year_cols:
    df = df[df[col].between(0, 100, inclusive="both")]

# ---------------------------------------------------
# 9. Remove duplicates
# ---------------------------------------------------
df = df.drop_duplicates()

# ---------------------------------------------------
# 10. Save cleaned dataset
# ---------------------------------------------------
df.to_csv("poverty_cleaned.csv", index=False)
print("Saved cleaned dataset as poverty_cleaned.csv")
print("Saved to:", os.path.abspath("poverty_cleaned.csv"))