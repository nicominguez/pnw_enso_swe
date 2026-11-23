from pathlib import Path
import json

import pandas as pd
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "ds1.csv"
CONFIG = ROOT / "config" / "station-year_filter.json"

df = pd.read_csv(DATA)
config = json.loads(CONFIG.read_text())
ms, me = int(config["month_range"]["start"]), int(config["month_range"]["end"])
required_months = (me - ms) % 12 + 1

incomplete = (df["n_SWE"] != required_months) | df["SWE"].isna()
percentage = 100 * incomplete.mean()

by_season = (
    df.assign(incomplete=incomplete)
    .groupby("season")
    .agg(
        enso=("enso", "first"),
        discarded=("incomplete", "sum"),
        total=("station_id", "nunique"),
    )
)
by_season["discarded_fraction"] = by_season["discarded"] / by_season["total"]
correlation = spearmanr(
    by_season["enso"], by_season["discarded_fraction"], nan_policy="omit"
)

print(f"complete SWE window: {required_months} months")
print(f"discarded station-seasons: {percentage:.2f}%")
print(f"Spearman rho: {correlation.statistic:.4f}")
print(f"Spearman p-value: {correlation.pvalue:.4g}")
