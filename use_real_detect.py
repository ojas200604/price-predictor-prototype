# Update existing training code to use the new real CSV (if present)
# This wrapper will modify train.py if it exists to prefer data/real CSV.

import os
from pathlib import Path

REAL_FILES = list(Path('data').glob('*Marketwise_Wholesale_Arrivals_Monthly_Analysis*(All_Districts)*.csv'))
if REAL_FILES:
    print('Real CSV found:', REAL_FILES[0])
else:
    print('No real CSV with expected pattern found in data/')
