from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent.parent
BINS = [500, 1000, 1500, 2000]

df = pd.read_csv(ROOT / "data/04_land_and_ocean_weekly.csv")

df0 = df.copy()
df0["band"] = pd.cut(df0["elevation_m"], BINS)

df1 = (
    df0.
    groupby(["winter", "band"])
    .agg(
        n_stations=("station_id", "nunique"),
        enso=("nino34", "mean"),
        snow=("SNOW", "mean"), 
    )
    .reset_index()
)

print(df1.to_string())

fig, ax = plt.subplots()
for band, g in df1.groupby("band", observed=True):
    ax.scatter(g["enso"], g["snow"], label=str(band))
ax.set_xlabel("Niño 3.4")
ax.set_ylabel("Snow")
ax.legend(title="Elevation (m)")
plt.show()