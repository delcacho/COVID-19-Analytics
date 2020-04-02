import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np
from utils import downloadCovidData
from utils import removeColumn

confirmed, death, latitude = removeColumn(downloadCovidData(),"Hubei")
bins = [np.floor(l/15) for l in latitude]
i = -180
result = {}
x = []
while i < 180:
  result[np.floor(float(i)/15)] = 0
  i+=12
  x.append("{}-{}".format(15*np.floor(float(i)/15),15*np.floor(float(i+12)/15)))
for i in range(0,len(confirmed.columns)):
  if not np.isnan(bins[i]):
     result[bins[i]] += confirmed.iloc[-1,i]

y = []
for key in sorted(result):
  y.append(result[key])

ax = sns.barplot(x=sorted(result), y=y)
x = []
for key in sorted(result):
  x.append("{} to {}".format(int(key*15),int((key+1)*15)))
ax.set_xticklabels(labels=x,rotation=90)
ax.set(xlabel='Latitude', ylabel='Confirmed cases')
plt.tight_layout()
plt.show()
