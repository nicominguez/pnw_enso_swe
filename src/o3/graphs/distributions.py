from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde


ROOT = Path(__file__).resolve().parents[3]
df = pd.read_csv(ROOT / "data" / "ds2.csv")
enso_z = (df["enso"] - df["enso"].mean()) / df["enso"].std()

transformed_swe = np.log1p(df["SWE"])


def density(axis, values, color, label):
    values = np.asarray(values.dropna(), dtype=float)
    x = np.linspace(values.min(), values.max(), 300)
    y = gaussian_kde(values)(x)
    axis.plot(x, y, color=color, linewidth=2, label=label)
    axis.fill_between(x, y, color=color, alpha=0.16)


fig, axes = plt.subplots(1, 2, figsize=(9, 3.8), constrained_layout=True)
for axis, original, transformed, original_label, transformed_label in [
    (
        axes[0],
        df["SWE"],
        transformed_swe,
        "SWE original (mm)",
        r"$\log(1+\mathrm{SWE})$",
    ),
    (
        axes[1],
        df["enso"],
        enso_z,
        "ENSO original (°C)",
        "ENSO estandarizado (z; solo escala)",
    ),
]:
    transformed_axis = axis.inset_axes([0, 0, 1, 1], zorder=2)
    transformed_axis.patch.set_alpha(0)
    density(axis, original, "tab:red", "Original")
    density(transformed_axis, transformed, "tab:green", "Transformado")
    axis.set_xlabel(original_label, color="tab:red")
    transformed_axis.set_xlabel(transformed_label, color="tab:green")
    axis.set_ylabel("Densidad original", color="tab:red")
    transformed_axis.set_ylabel("Densidad transformada", color="tab:green")
    axis.tick_params(axis="x", colors="tab:red")
    axis.tick_params(axis="y", colors="tab:red")
    transformed_axis.xaxis.tick_top()
    transformed_axis.xaxis.set_label_position("top")
    transformed_axis.yaxis.tick_right()
    transformed_axis.yaxis.set_label_position("right")
    transformed_axis.tick_params(axis="x", colors="tab:green")
    transformed_axis.tick_params(axis="y", colors="tab:green")
    axis.spines["bottom"].set_color("tab:red")
    transformed_axis.spines["top"].set_color("tab:green")
    transformed_axis.spines["right"].set_color("tab:green")
    transformed_axis.spines["left"].set_visible(False)
    transformed_axis.spines["bottom"].set_visible(False)
    handles, labels = axis.get_legend_handles_labels()
    handles_new, labels_new = transformed_axis.get_legend_handles_labels()
    axis.legend(handles + handles_new, labels + labels_new, loc="upper right")

output = ROOT / "images" / "o3" / "distributions.png"
output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(output, dpi=200)
plt.close(fig)
