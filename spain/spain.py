import urllib3
import requests
import pandas as pd
import traceback
import numpy as np
import datetime
import email.utils as eut
from utils import plotChart
from utils import downloadSpainData

pd.set_option('display.max_columns', None)
urllib3.disable_warnings()

region = "Madrid"
finalDf = None
for nreport in range(32,999):
   try:
      df,lastModified=downloadSpainData(nreport,region)
      print(df)
      #df["HospitalizationRate"] = 100 * df["Hospitalizados"] / df["Total casos"]
      df = df.loc[:,["Total casos"]].transpose()
      df["Date"] = [datetime.datetime(*eut.parsedate(lastModified)[:6])]
      #df = df.drop("CCAA",axis=1)
      df.index = df["Date"]
      if finalDf is None:
         finalDf = df
      else:
         finalDf = pd.concat([finalDf,df],axis=0)

   except FileNotFoundError:
      break
   except Exception as e:
      pass

cols = finalDf.columns.tolist()
cols.remove("Date")

for col in cols:
  finalDf[col] = np.log(finalDf[col])

last_row = finalDf.ix[finalDf.last_valid_index()].drop("Date")
#cols = finalDf.columns[last_row.argsort()].tolist()[-5:]
plotChart(finalDf,title="Log(Confirmed cases)", cols=cols, percent=False)
