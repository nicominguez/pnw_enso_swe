"""Descriptive association between categorical zone and fixed elevation bands."""

from pathlib import Path

import pandas as pd
from scipy.stats import chi2_contingency


ROOT = Path(__file__).resolve().parents[3]
df = pd.read_csv(ROOT / "data" / "ds3.csv")

stations = df[
    ["zone", "station_name", "elevation_m", "elevation_band"]
].drop_duplicates()
contingency = pd.crosstab(stations["zone"], stations["elevation_band"])
chi2, p_value, degrees_of_freedom, _ = chi2_contingency(contingency)
cramers_v = (
    (chi2 / len(stations))
    / min(contingency.shape[0] - 1, contingency.shape[1] - 1)
) ** 0.5

print(f"stations: {len(stations)}")
print(f"zones: {stations['zone'].nunique()}")
print(f"zone/elevation chi-squared: {chi2:.4f}")
print(f"zone/elevation degrees of freedom: {degrees_of_freedom}")
print(f"zone/elevation p-value: {p_value:.4g}")
print(f"zone/elevation Cramer's V: {cramers_v:.4f}")
print("contingency table:")
print(contingency.to_string())
