# El Niño and Pacific Northwest Snowfall

Builds a weekly winter dataset (Nov–Mar, 1981 onward) of snow and weather by station, with the Niño 3.4 index, to study El Niño's effect on snowfall.

## Pipeline

Blue = sources, orange = scripts, green = CSVs (rows × columns, approximate).

```mermaid
flowchart TB
    I1[GHCN-D inventory<br>+ WBD HUC-8 zones] --> P1[01_candidate_stations.py]
    P1 --> D1[(01_candidate_stations.csv<br>~1.4k × 31)]
    D1 --> P2[02_land_daily.py]
    I2[GHCN-D daily<br>station data] --> P2
    P2 --> D2[(02_land_daily.csv<br>~4M × 14)]
    D2 --> P3[03_land_weekly.py]
    D1 --> P3
    P3 --> D3[(03_land_weekly.csv<br>~210k × 18)]
    D3 --> P4[04_land_enso_weekly.py]
    I4[Niño 3.4 index] --> P4
    P4 --> D4[(04_land_enso_weekly.csv<br>~210k × 19)]

    classDef source fill:#dbeafe,stroke:#2563eb,color:#111
    classDef script fill:#fef3c7,stroke:#d97706,color:#111
    classDef data fill:#dcfce7,stroke:#16a34a,color:#111
    class I1,I2,I4 source
    class P1,P2,P3,P4 script
    class D1,D2,D3,D4 data
```

Run the scripts in order from `src/`. Filters are set in `config/station_filter.json`.

## Sources

1. **Zones:** USGS Watershed Boundary Dataset (HUC-8). https://prd-tnm.s3.amazonaws.com/index.html?prefix=StagedProducts/Hydrography/WBD/National/
2. **Land data:** NOAA NCEI GHCN-Daily. https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily
3. **Ocean data:** NOAA PSL monthly Niño 3.4 index (ERSST v5). https://psl.noaa.gov/data/timeseries/month/Nino34_CPC/

##

![Study area and Niño 3.4 box](inventory/images/selected_zones_nino34.png)