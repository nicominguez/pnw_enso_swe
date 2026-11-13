from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.formula.api import ols


ROOT = Path(__file__).resolve().parents[3]
DS2 = ROOT / "data" / "ds2.csv"
DS3 = ROOT / "data" / "ds3.csv"

before = pd.read_csv(DS2)
df = pd.read_csv(DS3)
stations = df[["station_name", "zone", "elevation_m"]].drop_duplicates()
band_min = stations["elevation_m"].min()
band_max = stations["elevation_m"].max()
all_zones = set(before["huc6"])
retained_zones = set(df["zone"])

print(f"elevation band: [{band_min:.1f}, {band_max:.1f}] m")
print(f"discarded zones: {len(all_zones - retained_zones)}")

betas = []
for station, group in df.groupby("station_name"):
    design = np.column_stack(
        [np.ones(len(group)), group["ENSO"], group["season"] - group["season"].mean()]
    )
    beta = np.linalg.lstsq(design, group["SWE_log1p"], rcond=None)[0][1]
    betas.append(
        {
            "station_name": station,
            "elevation_m": group["elevation_m"].iloc[0],
            "beta": beta,
        }
    )
betas = pd.DataFrame(betas)
if len(betas) >= 3:
    quadratic = ols(
        "beta ~ elevation_m + I(elevation_m ** 2)", data=betas
    ).fit()
    curvature = quadratic.params["I(elevation_m ** 2)"]
    p_value = quadratic.pvalues["I(elevation_m ** 2)"]
    pattern = (
        "curva cuadrática cóncava"
        if curvature < 0 and p_value < 0.05
        else "sin evidencia suficiente de una campana"
    )
    print(f"quadratic term p-value: {p_value:.4g}")
else:
    pattern = "insuficientes estaciones para evaluar una campana"
print(f"beta-elevation pattern: {pattern}")
