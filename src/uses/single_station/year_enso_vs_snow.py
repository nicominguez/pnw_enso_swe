from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent.parent.parent
df = pd.read_csv(ROOT / "data/04_land_and_ocean_weekly.csv")

df0 = (
    df[df["station_id"] == "USC00049053"]
    .groupby("winter")
    .agg(
        year=("winter", "first"), 
        enso=("nino34", "mean"), 
        snow=("SNOW", "sum")
    )
    .reset_index()
)

colors = df0["enso"].map(lambda x: "red" if x >= 1 else "blue" if x <= -1 else "gray")

fig, ax = plt.subplots()
ax.scatter(df0["year"], df0["snow"], c=colors)
ax.set_xlabel("Year")
ax.set_ylabel("Yearly snowfall")
plt.show()
