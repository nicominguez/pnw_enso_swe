from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent

START_MONTH = 11  # must match 03_prepare_land.py
ENSO_URL = "https://psl.noaa.gov/data/correlation/nina34.anom.data"

weekly = pd.read_csv(ROOT / "data/03_land_weekly.csv", dtype={"huc8": str})

# Organize ENSO by months.
enso = pd.read_csv(ENSO_URL, sep=r"\s+", skiprows=1, header=None, index_col=0, na_values=[-99.99], on_bad_lines="skip", engine="python")
enso = enso[enso.index.astype(str).str.isdigit()].astype(float).stack()
enso.index = pd.PeriodIndex([f"{y}-{m}" for y, m in enso.index], freq="M", name="month")
enso = enso.rename("nino34").reset_index()

# Match each week to the month of its middle day.
middle = pd.to_datetime(weekly["winter"].astype(str) + f"-{START_MONTH:02d}-01") + pd.to_timedelta(weekly["week"] * 7 + 3, unit="D")
weekly["month"] = middle.dt.to_period("M")
land_ocean = weekly.merge(enso, on="month", how="left").drop(columns="month")

print(f"{len(land_ocean):,} rows, {land_ocean['nino34'].isna().sum()} without a Nino 3.4 value")


# Export.
land_ocean.to_csv(ROOT / "data/04_land_and_ocean_weekly.csv", index=False)