from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.formula.api import ols


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "ds3.csv"

df = pd.read_csv(DATA)
model = ols(
    "SWE_log1p ~ season + C(zone) + C(elevation_tercile) + ENSO "
    "+ ENSO:C(zone) + ENSO:C(elevation_tercile)",
    data=df,
).fit()

grid = df[["zone", "elevation_tercile"]].drop_duplicates().copy()
grid["season"] = df["season"].median()
grid["ENSO"] = 0.0
baseline = model.predict(grid)
grid["ENSO"] = 1.0
plus_one_sd = model.predict(grid)
grid["multiplier"] = np.exp(plus_one_sd.to_numpy() - baseline.to_numpy())

print(grid[["zone", "elevation_tercile", "multiplier"]].to_string(index=False))
