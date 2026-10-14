from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent

FIRST_WINTER, LAST_WINTER = 1981, 2025
START_MONTH, WEEKS = 11, 21 # Nov-Mar
MAX_MISSING = 0.5 # A week is usable if x days have data
MIN_WEEKS = 17
MIN_WINTERS = 20

df = pd.read_csv(ROOT / "data/02_land_daily.csv", parse_dates=["date"])


# Fill in missing days with multiday totals.
df["SNOW"] = df["SNOW"].fillna(df["MDSF"])
df["PRCP"] = df["PRCP"].fillna(df["MDPR"])


# Define winter, week, and drop anything outside of selected timeframe.
df["winter"] = df["date"].dt.year - (df["date"].dt.month < START_MONTH)
df["week"] = (df["date"] - pd.to_datetime(df["winter"].astype(str) + f"-{START_MONTH:02d}-01")).dt.days // 7
df = df[df["winter"].between(FIRST_WINTER, LAST_WINTER) & (df["week"] < WEEKS)]


# Aggregate data to winter x week x station, with the fraction of missing days per variable.
g = df.groupby(["winter", "week", "station_id"])
weekly = pd.concat([
    g[["SNOW", "PRCP", "WESF"]].sum(min_count=1),
    g[["TMAX", "TMIN", "TAVG"]].mean(),
    g[["SNWD", "WESD"]].last(),
    (1 - g[["SNOW", "PRCP", "SNWD", "WESD"]].count() / 7).add_suffix("_missing"),
], axis = 1).reset_index()


# Keep usable weeks -> winters -> stations.
weekly["usable"] = weekly[["SNOW_missing", "PRCP_missing", "SNWD_missing", "WESD_missing"]].min(axis=1) <= MAX_MISSING
usable_weeks = weekly.groupby(["station_id", "winter"])["usable"].sum()
kept = usable_weeks[usable_weeks >= MIN_WEEKS].reset_index()
kept = kept[kept.groupby("station_id")["winter"].transform("size") >= MIN_WINTERS]
weekly = weekly.merge(kept[["station_id", "winter"]]).drop(columns="usable")


# Add zone and elevation. Reorden columns: winter, week, station, ...
stations = pd.read_csv(
    ROOT / "data/01_stations.csv",
    usecols=["station_id", "huc8", "zone_name", "elevation_m"], dtype={"huc8":str}
)
weekly = weekly.merge(stations, on="station_id", how="left")
first = ["winter", "week", "station_id", "huc8", "zone_name", "elevation_m"]
weekly = weekly[first + [c for c in weekly.columns if c not in first]].sort_values(first[:3]) # TODO: Optionally order by weeks <-> stations

print(f"{weekly['winter'].nunique()} winters, {weekly['station_id'].nunique()} stations, {len(weekly):,} rows")


# Export.
weekly.round(2).to_csv(ROOT / "data/03_land_weekly.csv", index=False)