from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
df = pd.read_csv(ROOT / "data" / "ds3.csv")
betas = []
for station, group in df.groupby("station_name"):
    design = np.column_stack(
        [np.ones(len(group)), group["ENSO"], group["season"] - group["season"].mean()]
    )
    beta = np.linalg.lstsq(design, group["SWE_log1p"], rcond=None)[0][1]
    betas.append(
        {
            "station_name": station,
            "zone": group["zone"].iloc[0],
            "elevation_m": group["elevation_m"].iloc[0],
            "beta": beta,
        }
    )
betas = pd.DataFrame(betas)
targets = betas["elevation_m"].quantile([0.2, 0.5, 0.8])
selected = []
for target in targets:
    candidate = betas.assign(distance=(betas["elevation_m"] - target).abs())
    candidate = candidate[~candidate["station_name"].isin(selected)]
    selected.append(candidate.sort_values("distance").iloc[0]["station_name"])
selected = betas[betas["station_name"].isin(selected)].sort_values("elevation_m")
colors = dict(zip(selected["zone"].unique(), plt.get_cmap("tab10").colors))

fig, axis = plt.subplots(figsize=(7, 4.5), constrained_layout=True)
axis.axvspan(630.9, 2816.4, color="tab:green", alpha=0.1, label="Banda común")
for row in selected.itertuples():
    axis.scatter(
        row.elevation_m,
        row.beta,
        s=90,
        color=colors[row.zone],
        label=row.zone,
    )
    axis.annotate(
        row.station_name,
        (row.elevation_m, row.beta),
        xytext=(5, 6),
        textcoords="offset points",
        fontsize="small",
    )
axis.axvline(630.9, color="tab:green", linestyle="--", linewidth=1)
axis.axvline(2816.4, color="tab:green", linestyle="--", linewidth=1)
axis.axhline(0, color="0.55", linewidth=0.8)
axis.set_xlabel("Elevación (m)")
axis.set_ylabel(r"$\hat{\beta}_1$")
axis.legend(title="Zona", fontsize="small")
axis.grid(alpha=0.25)
output = ROOT / "images" / "o3" / "beta_elevation.png"
output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(output, dpi=200)
plt.close(fig)
