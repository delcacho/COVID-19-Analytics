import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np
import datetime
import math
import traceback
from collections import Counter
from utils import downloadUsaCovidData
from utils import plotSubchart
from utils import plotChart
from model import forecastRegion

target = "NY"
confirmed= downloadUsaCovidData()
last_row = confirmed.loc[confirmed.last_valid_index(),:].drop("Date")
print(confirmed.columns[last_row.argsort()])
cols = ["NY"]
#cols = confirmed.columns[last_row.argsort()].tolist()[-5:]
print(last_row[cols])
if "Date" in cols:
   cols.remove("Date")
for col in cols:
   confirmed[col] = np.log(1+confirmed[col])
plotChart(confirmed,title="log(Confirmed cases)",cols=cols,useLabels=True)

def processState(confirmed,target):
   try:
      print("Forecasting... {}".format(target))
      startDate = "2020-03-01"
      confirmed = confirmed[confirmed["Date"] >= startDate]
      #confirmed = confirmed[confirmed[target] >= np.log(1.1)]
      base = confirmed["Date"][0].strftime("%Y-%m-%d")
      if confirmed[target].max() < np.log(1000):
          print("TARGET: {} MAX: {}".format(target,confirmed[target].max()))
          raise Exception("spam","eggs")
      projections, model = forecastRegion(confirmed,target,base)
      f, ax = plt.subplots(1, 1)
      plotSubchart(confirmed,ax,"log(Confirmed cases)",cols=cols,useLabels=True)
      plotSubchart(projections.iloc[:60,:],ax,title="log(Confirmed cases)",cols=["Forecast"],legend=False,useLabels=False)
      plt.show()
      for i,row in projections.iterrows():
         if i > 0:
            if projections.iloc[i,1] < projections.iloc[i-1,1]:
                break
      i = min(80,i)
      projections = projections.iloc[:i,:]
      print(math.exp(projections["Forecast"][i-1]))
      projections["Cumulative"] = [math.exp(x) for x in projections["Forecast"]]
      projections["New Cases"] = projections["Cumulative"].diff()
      print(projections[["Date","Cumulative","New Cases"]])
      return(projections["Cumulative"].max())
   except Exception as e:
      print(traceback.format_exc())
      return(0)

result = {}
for target in cols:
   result[target] = processState(confirmed,target)
print(result)
print(last_row)
print("TOTAL: ",np.sum(list(result.values())))
