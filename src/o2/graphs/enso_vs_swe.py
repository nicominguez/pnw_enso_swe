from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
df = pd.read_csv(ROOT / "data" / "ds2.csv")
df = df[df["station_name"] == "Stampede Pass"].dropna(subset=["enso", "SWE"])

slope, intercept = np.polyfit(df["enso"], df["SWE"], 1)
correlation = df["enso"].corr(df["SWE"])
x = np.linspace(df["enso"].min(), df["enso"].max(), 100)

fig, axis = plt.subplots(figsize=(7, 4.5), constrained_layout=True)
axis.scatter(df["enso"], df["SWE"], s=25, color="0.45", alpha=0.6)
axis.plot(x, slope * x + intercept, color="tab:red")
axis.axvline(0, color="0.55", linestyle="--", linewidth=0.8)
axis.set_xlabel("ENSO (°C)")
axis.set_ylabel("SWE (mm)")
axis.text(
    0.04,
    0.95,
    f"Pearson r = {correlation:.2f}",
    transform=axis.transAxes,
    va="top",
)
axis.grid(alpha=0.25)
output = ROOT / "images" / "o2" / "enso_vs_swe.png"
output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(output, dpi=200)
plt.close(fig)
