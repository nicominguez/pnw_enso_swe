from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
df = pd.read_csv(ROOT / "data" / "ds2.csv")
df = df[df["station_name"] == "Stampede Pass"].copy()

colors = df["enso"].map(
    lambda value: "tab:red" if value >= 1 else "tab:blue" if value <= -1 else "0.55"
)
fig, axis = plt.subplots(figsize=(7, 4.5), constrained_layout=True)
axis.scatter(df["season"], df["SWE"], s=25, c=colors, alpha=0.6)
axis.set_xlabel("Temporada")
axis.set_ylabel("SWE (mm)")
axis.grid(alpha=0.25)
axis.legend(
    handles=[
        axis.scatter([], [], color="tab:red", label="El Niño"),
        axis.scatter([], [], color="tab:blue", label="La Niña"),
        axis.scatter([], [], color="0.55", label="Neutral"),
    ]
)
output = ROOT / "images" / "o2" / "year_enso_vs_swe.png"
output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(output, dpi=200)
plt.close(fig)
