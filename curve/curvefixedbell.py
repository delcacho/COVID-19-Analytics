import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np
import datetime
import math
from collections import Counter
from utils import downloadCovidData
from utils import plotChart
from model import forecastRegion

confirmed,death,_ = downloadCovidData()
col = "World w/o China"
confirmed[col] = np.log(1+confirmed.sum(axis=1))
confirmed["Hubei"] = confirmed["Hubei"].astype(float)
cols = ["Italy", "Spain","Hubei", "Germany", "France"]
for col in cols:
   confirmed[col] = np.log(1+confirmed[col])
death["World w/o China"] = death.sum(axis=1)
start = "2020-02-25"
daysforecast = 200
target = "Spain"
print(confirmed[target])
projections, model = forecastRegion(confirmed,target,start,daysforecast)
print(projections)
projections["Forecast"] = [math.exp(x) for x in projections["Forecast"]]
projections["Forecast"] = projections["Forecast"].diff()
i = 80
projections = projections.iloc[:i,:]
print(projections)
plotChart(projections,"Newly confirmed cases",cols=["Forecast"],legend=False,labels=["Spain"])
projections["Cumulative"] = projections["Forecast"]
projections["Forecast"] = projections["Cumulative"].diff()
print(projections[["Date","Cumulative","Forecast"]])
print("MAX: ",projections["Forecast"].max())
print(projections[projections["Forecast"] == projections["Forecast"].max()])
