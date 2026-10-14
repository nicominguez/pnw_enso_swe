from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent.parent
STATION = "USC00355174"

df = pd.read_csv(ROOT / "data/04_land_and_ocean_weekly.csv")

winters = (
    df[df["station_id"] == STATION]
    .groupby("winter")
    .agg(snow=("SNOW", "sum"), enso=("nino34", "mean"))
    .reset_index()
)

ax = plt.figure().add_subplot(projection="3d")
ax.scatter(winters["enso"], winters["winter"], winters["snow"])
ax.set_xlabel("Niño 3.4 (Nov-Mar mean, °C)")
ax.set_ylabel("Winter (start year)")
ax.set_zlabel("Snowfall (mm)")

print(winters.shape)
plt.show()