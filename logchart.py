import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np
from collections import Counter
from utils import downloadCovidData
from utils import plotChart

confirmed, death, _ = downloadCovidData()
confirmed["World w/o China"] = np.log(confirmed.drop(["Hubei"], axis=1).sum(axis=1))
confirmed["Hubei"] = confirmed["Hubei"].astype(float)
cols = ["Italy", "Spain","Hubei", "Germany", "France", "United Kingdom"]
for col in cols:
   confirmed[col] = np.log(confirmed[col])
death["World w/o China"] = death.sum(axis=1)
plotChart(confirmed,title="log(Confirmed cases)",cols=["Italy","Spain","World w/o China","Hubei","France","United Kingdom"])
