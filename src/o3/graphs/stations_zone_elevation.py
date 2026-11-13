from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
df = pd.read_csv(ROOT / "data" / "ds3.csv")
stations = df[["zone", "station_name", "elevation_m"]].drop_duplicates()
target_elevations = stations["elevation_m"].quantile([0.2, 0.5, 0.8])
selected = []
for target in target_elevations:
    candidate = stations.assign(distance=(stations["elevation_m"] - target).abs())
    candidate = candidate[~candidate["station_name"].isin(selected)]
    selected.append(candidate.sort_values("distance").iloc[0]["station_name"])
selected_stations = stations[stations["station_name"].isin(selected)].sort_values(
    "elevation_m"
)

fig, axis = plt.subplots(figsize=(7, 4.5), constrained_layout=True)
axis.axhspan(630.9, 2816.4, color="tab:green", alpha=0.1, label="Banda común")
axis.axhline(630.9, color="tab:green", linestyle="--", linewidth=1)
axis.axhline(2816.4, color="tab:green", linestyle="--", linewidth=1)
for position, row in enumerate(selected_stations.itertuples()):
    axis.scatter(position, row.elevation_m, s=90, label=row.zone)
    axis.annotate(
        f"{row.station_name}\n{row.elevation_m:.0f} m",
        (position, row.elevation_m),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize="small",
    )
axis.set_xticks(range(len(selected_stations)), ["Baja", "Media", "Alta"])
axis.set_ylabel("Elevación (m)")
axis.set_xlabel("Estación representativa")
axis.legend(title="Zona", fontsize="small")
axis.grid(axis="y", alpha=0.25)
output = ROOT / "images" / "o3" / "stations_zone_elevation.png"
output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(output, dpi=200)
plt.close(fig)
