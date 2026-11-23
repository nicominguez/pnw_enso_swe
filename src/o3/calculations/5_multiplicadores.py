from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.formula.api import ols


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "ds3.csv"
OUT = ROOT / "data" / "multipliers_by_zone_elevation.csv"

df = pd.read_csv(DATA)
df["zone"] = df["zone"].astype(str)
model = ols(
    "SWE_log1p ~ season + C(zone) + elevation_within_zone + ENSO "
    "+ ENSO:C(zone) + ENSO:elevation_within_zone",
    data=df,
).fit()

stations = df[["zone", "station_name", "elevation_within_zone"]].drop_duplicates()
zone_stats = stations.groupby("zone")["elevation_within_zone"].agg(["mean", "std"])
zones = sorted(df["zone"].astype(str).unique())
bands = [
    ("baja", -3.0, -1.0, -2.0),
    ("media", -1.0, 1.0, 0.0),
    ("alta", 1.0, 3.0, 2.0),
]
grid = pd.DataFrame(
    [
        (
            zone,
            label,
            zone_stats.loc[zone, "mean"] + lower * zone_stats.loc[zone, "std"],
            zone_stats.loc[zone, "mean"] + upper * zone_stats.loc[zone, "std"],
            (
                0.0
                if midpoint == 0.0
                else zone_stats.loc[zone, "mean"] + midpoint * zone_stats.loc[zone, "std"]
            ),
            midpoint,
        )
        for zone in zones
        for label, lower, upper, midpoint in bands
    ],
    columns=[
        "zone",
        "elevation_band",
        "elevation_lower_m",
        "elevation_upper_m",
        "elevation_midpoint_m",
        "elevation_midpoint_sd",
    ],
)
grid["season"] = df["season"].median()
grid["ENSO"] = 0.0
baseline = model.predict(
    grid.rename(columns={"elevation_midpoint_m": "elevation_within_zone"})
)
grid["ENSO"] = 1.0
plus_one_degree = model.predict(
    grid.rename(columns={"elevation_midpoint_m": "elevation_within_zone"})
)
grid["multiplier"] = np.exp(plus_one_degree.to_numpy() - baseline.to_numpy())
grid = grid[
    [
        "zone",
        "elevation_band",
        "elevation_lower_m",
        "elevation_upper_m",
        "elevation_midpoint_m",
        "elevation_midpoint_sd",
        "multiplier",
    ]
]
OUT.parent.mkdir(parents=True, exist_ok=True)
grid.to_csv(OUT, index=False)

representative_zones = [zones[0], zones[-1]]
compact = grid[grid["zone"].isin(representative_zones)]
print("representative zones: " + ", ".join(representative_zones))
print(compact.to_string(index=False))
print(f"complete grid written to {OUT}")
