from pathlib import Path
import json

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "ds1.csv"
OUT_PATH = ROOT / "data" / "ds2.csv"
CONFIG_PATH = ROOT / "config" / "station-year_filter.json"

df = pd.read_csv(DATA)
config = json.loads(CONFIG_PATH.read_text())

ms, me = int(config["month_range"]["start"]), int(config["month_range"]["end"])
required_swe_months = (me - ms) % 12 + 1

# Retain station-seasons with a complete configured SWE window.
df = df[df["n_SWE"] == required_swe_months].dropna(subset=["SWE", "enso"])

# Retain stations with enough complete seasons.
stations = (
    df.groupby("station_id")["season"]
    .nunique()
    .loc[lambda count: count >= config["minimum_station_seasons"]]
    .index
)
df = df[df["station_id"].isin(stations)].sort_values(["station_id", "season"])

# Keep only fields used by the study.
df = df[["station_name", "huc6", "elevation_m", "SWE", "enso", "season"]]

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT_PATH, index=False)
