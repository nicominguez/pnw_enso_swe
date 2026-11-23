from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import skew


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "data" / "ds2.csv"

df = pd.read_csv(DATA)
print("Box-Cox lambda used by log1p: 0")
print(f"SWE skewness before: {skew(df['SWE'], nan_policy='omit', bias=False):.4f}")
print(
    f"SWE skewness after log1p: "
    f"{skew(np.log1p(df['SWE']), nan_policy='omit', bias=False):.4f}"
)
print(f"ENSO skewness: {skew(df['enso'], nan_policy='omit', bias=False):.4f}")
