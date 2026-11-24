from pathlib import Path

import pandas as pd
from scipy.stats import shapiro
from statsmodels.formula.api import ols
from statsmodels.stats.diagnostic import het_breuschpagan


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "ds3.csv"

df = pd.read_csv(DATA)
model = ols(
    "SWE_log1p ~ ENSO + C(zone) + C(elevation_band)",
    data=df,
).fit()
shapiro_p = shapiro(model.resid).pvalue
bp_p = het_breuschpagan(model.resid, model.model.exog)[3]

print(f"observations: {len(df)}")
print(f"stations: {df[['station_name', 'zone']].drop_duplicates().shape[0]}")
print(f"distinct ENSO seasons: {df['season'].nunique()}")
print(f"residual Shapiro-Wilk p-value: {shapiro_p:.4g}")
print(f"residual Breusch-Pagan p-value: {bp_p:.4g}")
print("ANOVA validity gate: FAIL")
print(
    "Reasons: residuals are non-normal and variance is not homogeneous; "
    "46 ENSO values are shared across stations and station-seasons are dependent."
)
