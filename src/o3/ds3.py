from pathlib import Path
import json

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "ds2.csv"
OUT_PATH = ROOT / "data" / "ds3.csv"
CONFIG_PATH = ROOT / "config" / "station-year_filter.json"

df = pd.read_csv(DATA, dtype={"station_name": str, "huc6": str})
config = json.loads(CONFIG_PATH.read_text())

df["station_key"] = (
    df["station_name"].fillna("")
    + "|"
    + df["huc6"].fillna("")
    + "|"
    + df["elevation_m"].astype(str)
)
station_columns = ["station_key", "station_name", "huc6", "elevation_m"]
stations = df[station_columns].drop_duplicates("station_key")
stations = stations[
    stations["elevation_m"].between(
        config["elevation_m"]["min"], config["elevation_m"]["max"]
    )
]

# Use HUC6 as the explicitly selected proxy for the paper's nominal zone.
df["zone"] = df["huc6"]
zone_counts = stations.groupby("huc6")["station_key"].nunique()
retained_zones = zone_counts[zone_counts >= 3].index
stations = stations[stations["huc6"].isin(retained_zones)]
if stations.empty:
    raise ValueError("No HUC6 proxy zone has at least three stations.")

df = df[df["station_key"].isin(stations["station_key"])].copy()
df["SWE_log1p"] = np.log1p(df["SWE"])
df["ENSO"] = df["enso"]

stations = stations.copy()
zone_means = stations.groupby("huc6")["elevation_m"].transform("mean")
stations["elevation_within_zone"] = stations["elevation_m"] - zone_means
df = df.drop(columns=["elevation_within_zone"], errors="ignore").merge(
    stations[["station_key", "elevation_within_zone"]],
    on="station_key",
    how="inner",
)

df = df.drop(columns=["station_key"]).sort_values(
    ["huc6", "elevation_m", "station_name", "season"]
)
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT_PATH, index=False)
