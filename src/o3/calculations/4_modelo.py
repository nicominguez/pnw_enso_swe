from pathlib import Path

import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.diagnostic import het_breuschpagan
from scipy.stats import shapiro


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "ds3.csv"

df = pd.read_csv(DATA)
cells = pd.crosstab(df["zone"], df["elevation_tercile"])
empty_cells = int((cells == 0).sum().sum())

model = ols(
    "SWE_log1p ~ season + C(zone) + C(elevation_tercile) + ENSO "
    "+ ENSO:C(zone) + ENSO:C(elevation_tercile)",
    data=df,
).fit()
anova = anova_lm(model, typ=2)
shapiro_p = shapiro(model.resid).pvalue
bp_p = het_breuschpagan(model.resid, model.model.exog)[3]

print(f"empty zone/elevation cells: {empty_cells}")
print(f"residual Shapiro-Wilk p-value: {shapiro_p:.4g}")
print(f"residual Breusch-Pagan p-value: {bp_p:.4g}")
for term in ("ENSO:C(zone)", "ENSO:C(elevation_tercile)"):
    print(f"{term}: F={anova.loc[term, 'F']:.4f}, p={anova.loc[term, 'PR(>F)']:.4g}")
