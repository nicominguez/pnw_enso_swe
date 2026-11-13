from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
DS2 = ROOT / "data" / "ds2.csv"
DS3 = ROOT / "data" / "ds3.csv"


def eta_squared_adjusted(data):
    stations = data[["station_name", "huc6", "elevation_m"]].drop_duplicates()
    grand_mean = stations["elevation_m"].mean()
    groups = stations.groupby("huc6")["elevation_m"]
    ss_between = sum(len(group) * (group.mean() - grand_mean) ** 2 for _, group in groups)
    ss_total = ((stations["elevation_m"] - grand_mean) ** 2).sum()
    n, groups_count = len(stations), stations["huc6"].nunique()
    eta_squared = ss_between / ss_total
    return 1 - (1 - eta_squared) * (n - 1) / (n - groups_count)


before = pd.read_csv(DS2)
after = pd.read_csv(DS3)
print(f"Before: {before['station_name'].nunique()} stations, adjusted eta2 = {eta_squared_adjusted(before):.4f}")
print(f"After: {after['station_name'].nunique()} stations, adjusted eta2 = {eta_squared_adjusted(after):.4f}")
