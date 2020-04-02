import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np
import datetime
import math
from collections import Counter
from utils import downloadCovidData
from utils import plotSubchart
from model import forecastRegion

target = 'Spain'
confirmed, death, _ = downloadCovidData()
col = "World w/o China"
confirmed[col] = np.log(confirmed.drop("Hubei",axis=1).sum(axis=1))
confirmed["Hubei"] = confirmed["Hubei"].astype(float)
cols = ["Italy", "Spain","Hubei", "Germany", "France", "United Kingdom"]
#print(confirmed[target])
for col in cols:
   confirmed[col] = np.log(confirmed[col])
death["World w/o China"] = death.sum(axis=1)
#death["World w/o China"] = death["World w/o China"] / confirmed["World w/o China"]
#print("Min: ",np.min(confirmed["World w/o China"]))
#print("Max: ",np.max(confirmed["World w/o China"]))
#print("Min date: ",np.min(confirmed["Date"]))
#print("Max date: ",np.max(confirmed["Date"]))

startDate = "2020-03-01"
confirmed = confirmed[confirmed["Date"] >= startDate]
daysforecast = 200
projections, model = forecastRegion(confirmed,target,startDate,daysforecast)

for i,row in projections.iterrows():
   if i > 0:
      if projections.iloc[i,1] < projections.iloc[i-1,1]:
          break
i = min(120,i)
projections = projections.iloc[:i,:]
#print(math.exp(projections["Forecast"][i-1]))
f, ax = plt.subplots(1, 1)
plotSubchart(confirmed,ax,"log(Confirmed cases)",cols=["Italy","Spain","Germany","France", "United Kingdom"],useLabels=True)
plotSubchart(projections.iloc[:60,:],ax,title="log(Confirmed cases)",cols=["Forecast"],legend=False,useLabels=False)
plt.show()
projections["Cumulative"] = [math.exp(x) for x in projections["Forecast"]]
projections["New Cases"] = projections["Cumulative"].diff()
print(projections[["Date","Cumulative","New Cases"]])
print("MAX: ",projections["Forecast"].max())
print(projections[projections["Forecast"] == projections["Forecast"].max()])
