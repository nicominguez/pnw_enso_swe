from pathlib import Path
import json

import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
DS1 = ROOT / "data" / "ds1.csv"
DS2 = ROOT / "data" / "ds2.csv"
CONFIG = ROOT / "config" / "station-year_filter.json"

ds1 = pd.read_csv(DS1)
ds2 = pd.read_csv(DS2)
config = json.loads(CONFIG.read_text())
ms, me = int(config["month_range"]["start"]), int(config["month_range"]["end"])
required_months = (me - ms) % 12 + 1

complete = ds1[(ds1["n_SWE"] == required_months) & ds1["SWE"].notna()]
print(f"X station-seasons after SWE completeness: {len(complete)}")
print(f"X stations: {complete['station_id'].nunique()}")
print(f"Y station-seasons after station filter: {len(ds2)}")
print(f"Y stations: {ds2['station_name'].nunique()}")
