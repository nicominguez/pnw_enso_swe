from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import requests


ROOT = Path(__file__).resolve().parents[3]
LAND_URL = "https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1"
OCEAN_URL = "https://psl.noaa.gov/data/timeseries/month/data/nino34.long.anom.csv"
STATION = "788:WA:SNTL"
START, END = "2023-11-01", "2026-04-01"
SEASON_MONTHS = [12, 1, 2, 3, 4]

with requests.Session() as session:
    data_response = session.get(
        f"{LAND_URL}/data",
        params={
            "stationTriplets": STATION,
            "elements": "WTEQ",
            "duration": "MONTHLY",
            "beginDate": START,
            "endDate": END,
            "periodRef": "START",
        },
        timeout=120,
    )
    data_response.raise_for_status()

swe = pd.Series(
    {
        pd.Timestamp(int(value["year"]), int(value["month"]), 1): value.get("value")
        for value in data_response.json()[0]["data"][0]["values"]
    },
    dtype=float,
) * 25.4
enso = pd.read_csv(
    OCEAN_URL,
    skiprows=1,
    names=["date", "enso"],
    parse_dates=["date"],
    skipinitialspace=True,
)
enso = enso[enso["enso"] > -99].set_index("date")["enso"]

dates = pd.date_range(START, END, freq="MS")
df = pd.DataFrame({"SWE": swe, "ENSO": enso}).reindex(dates)
df["season"] = df.index.year + (df.index.month >= 12)
df["x"] = range(len(df))
seasonal = df[df.index.month.isin(SEASON_MONTHS)]

fig, axes = plt.subplots(2, 1, sharex=True, figsize=(12, 6), constrained_layout=True)
for axis, column in zip(axes, ["SWE", "ENSO"]):
    axis.plot(df["x"], df[column], ":o", color="0.65", markersize=3)
    axis.set_ylabel(column)
    axis.grid(axis="y", alpha=0.3)
axes[1].axhline(0, color="black", linewidth=0.6)

for color, (season, group) in zip(
    ["tab:blue", "tab:orange", "tab:green"], seasonal.groupby("season")
):
    left, right = group["x"].min() - 0.5, group["x"].max() + 0.5
    for axis, column in zip(axes, ["SWE", "ENSO"]):
        axis.axvspan(left, right, color=color, alpha=0.12)
        axis.plot(group["x"], group[column], "-o", color=color, linewidth=2, markersize=4)
    axes[0].text(
        (left + right) / 2,
        0.96,
        f"Temporada {season}",
        color=color,
        ha="center",
        va="top",
        fontweight="bold",
        fontsize=12,
        transform=axes[0].get_xaxis_transform(),
    )
    peak = group["SWE"].idxmax()
    axes[0].plot(
        group.loc[peak, "x"],
        group.loc[peak, "SWE"],
        "*",
        color="crimson",
        markersize=15,
        zorder=4,
    )
    axes[0].annotate(
        f"pico {group.loc[peak, 'SWE']:.0f}",
        (group.loc[peak, "x"], group.loc[peak, "SWE"]),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        color="crimson",
        fontweight="bold",
        bbox={"boxstyle": "round", "facecolor": "white", "edgecolor": "crimson"},
    )
    mean = group["ENSO"].mean()
    axes[1].hlines(mean, left, right, colors="crimson", linestyles="--", linewidth=1.5)
    axes[1].text(
        (left + right) / 2,
        mean,
        f"media {mean:.2f}",
        color="crimson",
        fontweight="bold",
        ha="center",
        va="bottom",
        bbox={"boxstyle": "round", "facecolor": "white", "edgecolor": "crimson"},
    )

axes[-1].set_xticks(df["x"], df.index.strftime("%b\n%y"))
axes[0].set_ylim(0, df["SWE"].max() * 1.3)
output = ROOT / "images" / "o1" / "swe_enso_station.png"
output.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(output, dpi=200)
plt.close(fig)
