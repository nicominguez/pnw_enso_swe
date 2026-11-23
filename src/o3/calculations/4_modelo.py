from pathlib import Path

import numpy as np
import pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.sandwich_covariance import cov_cluster
from scipy.stats import shapiro
from scipy.stats import chi2


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "ds3.csv"

df = pd.read_csv(DATA)

model = ols(
    "SWE_log1p ~ season + C(zone) + elevation_within_zone + ENSO "
    "+ ENSO:C(zone) + ENSO:elevation_within_zone",
    data=df,
).fit()
anova = anova_lm(model, typ=2)
shapiro_p = shapiro(model.resid).pvalue
bp_p = het_breuschpagan(model.resid, model.model.exog)[3]
station_groups = pd.factorize(df["station_name"])[0]
cluster_cov = cov_cluster(model, station_groups, use_correction=True)


def robust_wald(term):
    names = model.params.index.to_list()
    indices = [
        i for i, name in enumerate(names)
        if name == term or name.startswith(term + "[")
    ]
    estimate = model.params.to_numpy()[indices]
    covariance = cluster_cov[np.ix_(indices, indices)]
    statistic = float(estimate @ np.linalg.pinv(covariance) @ estimate)
    return statistic, len(indices), chi2.sf(statistic, len(indices))

print(f"observations: {len(df)}")
print(f"stations: {df[['station_name', 'zone']].drop_duplicates().shape[0]}")
print(f"residual Shapiro-Wilk p-value: {shapiro_p:.4g}")
print(f"residual Breusch-Pagan p-value: {bp_p:.4g}")
for term in ("ENSO:C(zone)", "ENSO:elevation_within_zone"):
    print(
        f"{term} classical type-II decomposition (descriptive only): "
        f"F={anova.loc[term, 'F']:.4f}, "
        f"p={anova.loc[term, 'PR(>F)']:.4g}"
    )
    statistic, df_term, p_value = robust_wald(term)
    print(
        f"{term} station-clustered Wald: chi2={statistic:.4f}, "
        f"df={df_term}, p={p_value:.4g}"
    )
