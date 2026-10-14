from pathlib import Path
import json
import pandas as pd
import geopandas as gpd


ROOT = Path(__file__).resolve().parent.parent

config = json.loads((ROOT / "config/station_filter.json").read_text())
study_area = config["study_area"]
elev = config["elevation_m"]
keep_elements = config["keep_elements"]


# Keep stations within elevation range and study area.
stations_raw = pd.read_fwf(ROOT / "inventory/stations.txt", widths=[11, 9, 10, 7, 50], header=None)
stations_raw.columns = ["station_id", "latitude", "longitude", "elevation_m", "station_name"]
stations_raw = stations_raw[
    stations_raw["elevation_m"].between(elev["min"], elev["max"])
    & stations_raw["latitude"].between(study_area["latitude_min"], study_area["latitude_max"])
    & stations_raw["longitude"].between(study_area["longitude_min"], study_area["longitude_max"])
]


# Keep selected variables. 
inventory_raw = pd.read_csv(
    ROOT / "inventory/inventory.txt", sep=r"\s+", header=None,
    usecols=[0, 3 ,4 ,5], names=["station_id", "latitude", "longitude", "element", "start_year", "end_year"]
)
inventory_raw = inventory_raw[
    inventory_raw["element"].isin(keep_elements)
    & inventory_raw["station_id"].isin(stations_raw["station_id"])
    ]

inventory = inventory_raw.pivot(index="station_id", columns="element", values=["start_year", "end_year"])
elements = inventory_raw["element"].unique()
inventory = inventory[[(kind, el) for el in elements for kind in ("start_year", "end_year")]]
inventory.columns = [f"{element}_{kind}" for kind, element in inventory.columns]
inventory = inventory.reset_index()

stations = (stations_raw.merge(inventory, on="station_id", how="inner"))


# Classify stations by zone.
zones = gpd.read_file(ROOT / "data/geography/wbd_huc8_simplified.json")[["huc8", "name", "geometry"]]
zones = zones.rename(columns={"name": "zone_name"})

points = gpd.GeoDataFrame(
    stations,
    geometry=gpd.points_from_xy(stations["longitude"], stations["latitude"]),  # x = lon, y = lat
    crs="EPSG:4326",
)

stations = (
    gpd.sjoin(points, zones.to_crs(points.crs), how="inner", predicate="within")
    .sort_values("station_id")
    .reset_index(drop=True)
)


# Export.
out = ROOT / "data/01_stations.csv"
out.parent.mkdir(parents=True, exist_ok=True)
stations.drop(columns="geometry").to_csv(out, index=False)