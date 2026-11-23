from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[2]
URL_LAND = "https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1"
URL_OCEAN = "https://psl.noaa.gov/data/timeseries/month/data/nino34.long.anom.csv"
OUT_PATH = ROOT / "data" / "ds1.csv"
CONFIG_PATH = ROOT / "config" / "station-year_filter.json"
STATIONS_PER_REQUEST = 25
MAX_WORKERS = 4

config = json.loads(CONFIG_PATH.read_text())
ms, me = int(config["month_range"]["start"]), int(config["month_range"]["end"])
months = [(m - 1) % 12 + 1 for m in range(ms, ms + (me - ms) % 12 + 1)]


def seasonal(df):
    df = df[df["date"].dt.month.isin(months)]
    return df.assign(season=df["date"].dt.year + (df["date"].dt.month >= ms))


def get_json(session, url, **kwargs):
    response = session.get(url, timeout=120, **kwargs)
    response.raise_for_status()
    return response.json()


def get_station_data(station_ids):
    with requests.Session() as session:
        return get_json(
            session,
            f"{URL_LAND}/data",
            params={
                "stationTriplets": ",".join(station_ids),
                "elements": ",".join(config["keep_elements"]),
                "duration": "MONTHLY",
                "beginDate": config["date_range"]["start"],
                "endDate": config["date_range"]["end"],
                "periodRef": "START",
            },
        )


with requests.Session() as session:
    # Obtain SNOTEL stations within HUC2 17 and the configured elevation range.
    stations = pd.DataFrame(
        get_json(
            session,
            f"{URL_LAND}/stations",
            params={
                "stationTriplets": "*:*:SNTL",
                "hucs": "17*",
                "activeOnly": "false",
            },
        )
    )
    stations = stations.rename(
        columns={
            "stationTriplet": "station_id",
            "name": "station_name",
            "elevation": "elevation_m",
        }
    )
    stations["huc6"] = stations["huc"].str[:6]
    stations["elevation_m"] *= 0.3048
    stations = stations[
        stations["elevation_m"].between(
            config["elevation_m"]["min"], config["elevation_m"]["max"]
        )
    ]

ids = stations["station_id"].tolist()
batches = [
    ids[start : start + STATIONS_PER_REQUEST]
    for start in range(0, len(ids), STATIONS_PER_REQUEST)
]
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    response = [
        station
        for batch in executor.map(get_station_data, batches)
        for station in batch
    ]

enso = pd.read_csv(
    URL_OCEAN,
    skiprows=1,
    names=["date", "nino34"],
    parse_dates=["date"],
    skipinitialspace=True,
)
enso = (
    seasonal(enso[enso["nino34"] > -99])
    .groupby("season")["nino34"]
    .agg(enso="mean", n_enso="count")
    .reset_index()
)

rows = [
    {
        "station_id": station["stationTriplet"],
        "element": element["stationElement"]["elementCode"],
        "date": f'{value["year"]}-{int(value["month"]):02d}-01',
        "value": value.get("value"),
    }
    for station in response
    for element in station.get("data", [])
    for value in element.get("values", [])
]
raw = pd.DataFrame(rows)
raw["date"] = pd.to_datetime(raw["date"])
raw["value"] = pd.to_numeric(raw["value"], errors="coerce")
# AWDB's stored units are English: inches for PRCP/WTEQ and Fahrenheit for TAVG.
raw.loc[raw["element"].isin(["PRCP", "WTEQ"]), "value"] *= 25.4
raw.loc[raw["element"] == "TAVG", "value"] = (
    raw.loc[raw["element"] == "TAVG", "value"] - 32
) * 5 / 9
raw = seasonal(raw)

# Aggregate station data to seasons.
seasons = (
    raw.pivot(index=["station_id", "season", "date"], columns="element", values="value")
    .groupby(["station_id", "season"])
    .agg(
        TAVG=("TAVG", "mean"),
        n_TAVG=("TAVG", "count"),
        PRCP=("PRCP", lambda s: s.sum(min_count=1)),
        n_PRCP=("PRCP", "count"),
        SWE=("WTEQ", "max"),
        n_SWE=("WTEQ", "count"),
    )
    .reset_index()
)

# The station endpoint supplies the metadata, so no third source is needed.
out = seasons.merge(
    stations[
        [
            "station_id",
            "station_name",
            "latitude",
            "longitude",
            "elevation_m",
            "huc6",
        ]
    ],
    on="station_id",
)
out = out.merge(enso, on="season", how="left").sort_values(
    ["station_id", "season"]
)

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
out.to_csv(OUT_PATH, index=False)
