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

confirmed, death, _ = downloadCovidData()
col = "World w/o China"
confirmed[col] = np.log(confirmed.drop("Hubei",axis=1).sum(axis=1))
cols = ["Italy", "Spain","Hubei", "Germany", "France", "United Kingdom"]
for col in cols:
   confirmed[col] = np.log(confirmed[col])
death["World w/o China"] = death.sum(axis=1)
print(confirmed["Spain"])
startDate = "2020-02-25"
confirmed = confirmed[confirmed["Date"] >= startDate]

daysforecast = 100
projectionsSpain, model = forecastRegion(confirmed,"Spain",startDate,daysforecast)
projectionsItaly, model = forecastRegion(confirmed,"Italy",startDate,daysforecast)
projectionsUK, model = forecastRegion(confirmed,"United Kingdom",startDate,daysforecast)

for i,row in projectionsSpain.iterrows():
   if i > 0:
      if projectionsSpain.iloc[i,1] > projectionsItaly.iloc[i-1,1]:
          break

print("Cross at ",projectionsSpain["Date"][i])
projections = pd.DataFrame({
   "Date":projectionsSpain["Date"],
   "ForecastSpain":projectionsSpain["Forecast"],
   "ForecastItaly":projectionsItaly["Forecast"],
   "ForecastUK":projectionsUK["Forecast"]
})
f, ax = plt.subplots(1, 1)
plotSubchart(confirmed,ax,title="log(Confirmed cases)",
   cols=["Italy","Spain","World w/o China","Hubei","United Kingdom"])
plotSubchart(projections,ax,title="log(Confirmed cases)",
   cols=["ForecastSpain", "ForecastItaly","ForecastUK"],legend=False,useLabels=False)
plt.show()
projections["ForecastSpain"] = [math.exp(x) for x in projections["ForecastSpain"]]
projections["ForecastItaly"] = [math.exp(x) for x in projections["ForecastItaly"]]
projections["ForecastUK"] = [math.exp(x) for x in projections["ForecastUK"]]
print(projections[projections["ForecastSpain"] > projections["ForecastItaly"]].head(1))
print("MAX SPAIN: ",projections["ForecastSpain"].max())
print("MAX ITALY: ",projections["ForecastItaly"].max())
projections["ForecastSpain"] = projections["ForecastSpain"].diff()
projections["ForecastItaly"] = projections["ForecastItaly"].diff()
print("MAXDIFF SPAIN: ",projections["ForecastSpain"].max())
print("MAXDIFF ITALY: ",projections["ForecastItaly"].max())
print("PEAK SPAIN: ",projections[projections["ForecastSpain"] == projections["ForecastSpain"].max()])
print("PEAK ITALY: ",projections[projections["ForecastItaly"] == projections["ForecastItaly"].max()])
