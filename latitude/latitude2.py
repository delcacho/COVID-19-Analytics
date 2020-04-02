import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np
from utils import downloadCovidData
from utils import removeColumn
from utils import plotChart
   
confirmed, death, latitude = removeColumn(downloadCovidData(),"Hubei")
bins = [np.floor(l/15) for l in latitude]
i = -180
result = {}
x = []
while i < 180:
  result[np.floor(float(i)/15)] = np.zeros(confirmed.shape[0])
  i+=12
  x.append("{}-{}".format(15*np.floor(float(i)/15),15*np.floor(float(i+12)/15)))

for i in range(0,len(confirmed.columns)):
  if not np.isnan(bins[i]):
    result[bins[i]] += confirmed.iloc[:,i]
finalDf = pd.DataFrame(data=pd.to_datetime(confirmed.index,format='%m/%d/%y'),columns=["Date"])
cols = []
for i in result.keys():
   if np.sum(result[i]) > 0:
      label = "{}-{}".format(15*i,15*(i+1))
      cols.append(label)
      finalDf.loc[:, label] = result[i].values

for col in cols:
  finalDf[col] = np.log(1+finalDf[col])
print(finalDf)
plotChart(finalDf,title="log(Confirmed cases)",cols=cols)
