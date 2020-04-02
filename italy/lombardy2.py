import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import matplotlib.ticker as mtick
import numpy as np
from collections import Counter
from utils import plotChart

confirmed = pd.read_csv("data/lombardy.csv").iloc[17:,]
print(confirmed)
confirmed["Lombardy"] = confirmed["Cases"].diff()
confirmed["LogGrowth"] = np.log(confirmed["Cases"])
confirmed["LogGrowth"] = 100*confirmed["Cases"].pct_change(periods=1)
confirmed['Date'] =  pd.to_datetime(confirmed['Date'], format='%d-%m-%Y')
confirmed.index = confirmed['Date']

def exponential(x, a, k, b):
    return a*np.exp(x*k) + b

confirmed = confirmed.iloc[1:,]
country = "LogGrowth"
print(confirmed[country])
plotChart(confirmed,title="Newly confirmed cases", cols=[country], percent=True)
