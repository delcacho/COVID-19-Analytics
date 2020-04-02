import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np
from collections import Counter
from utils import downloadCovidData
from utils import plotChart

target = "Italy"
confirmed, death, _ = downloadCovidData()
confirmed = confirmed[confirmed.Date >= '2020-03-01']
print(confirmed)
cols = [target]
for col in cols:
   confirmed[col] = confirmed[col].diff()

plotChart(confirmed,title="Newly confirmed cases",cols=[target])
