"""Descriptive association between zone and station elevation."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
df = pd.read_csv(ROOT / "data" / "ds3.csv")
stations = df[["zone", "station_name", "elevation_m"]].drop_duplicates()
groups = stations.groupby("zone")["elevation_m"]
grand_mean = stations["elevation_m"].mean()
ss_total = ((stations["elevation_m"] - grand_mean) ** 2).sum()
ss_between = sum(
    len(values) * (values.mean() - grand_mean) ** 2
    for _, values in groups
)
n = len(stations)
k = stations["zone"].nunique()
eta2 = ss_between / ss_total
adjusted_eta2 = 1 - (1 - eta2) * (n - 1) / (n - k)

print(f"stations: {n}")
print(f"zones: {k}")
print(f"zone/elevation eta2 adjusted: {adjusted_eta2:.4f}")
print(f"zone/elevation eta2: {eta2:.4f}")
print(f"within-zone elevation SD: {groups.std().mean():.2f} m")
