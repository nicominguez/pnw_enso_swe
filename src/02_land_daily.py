from pathlib import Path
import json
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
URL = "https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/{}.csv"

elements = json.loads((ROOT / "config/station_filter.json").read_text())["keep_elements"]
station_ids = pd.read_csv(ROOT / "data/01_stations.csv", usecols=["station_id"])["station_id"]


def load(sid):
    df = pd.read_csv(
        URL.format(sid), parse_dates=["DATE"], low_memory=False,
        usecols=lambda c: c == "DATE" or c.removesuffix("_ATTRIBUTES") in elements
    )
    for el in elements:
        if el in df:  # attributes = "measurement,quality,source,time"; blank quality = passed QC
            df.loc[df[f"{el}_ATTRIBUTES"].astype("string").str.split(",").str[1].fillna("") != "", el] = float("nan")
    df = df.drop(columns=df.filter(like="_ATTRIBUTES").columns)
    df = df[(df["DATE"].dt.year >= 1981) & df["DATE"].dt.month.isin([10, 11, 12, 1, 2, 3, 4])]
    df = df.set_index("DATE").dropna(how="all").rename_axis("date").reset_index()
    df.insert(0, "station_id", sid)
    return df


frames = []
for sid in station_ids:
    try:
        frames.append(load(sid))
    except Exception as e:
        print(f"skipped {sid}: {e}")

out = ROOT / "data/02_land_daily.csv"
pd.concat(frames, ignore_index=True).to_csv(out, index=False)