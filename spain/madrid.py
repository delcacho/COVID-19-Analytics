import tabula 
import urllib3
import requests
import pandas as pd
import datetime
import email.utils as eut
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import traceback
import numpy as np
from utils import plotSubchart
from utils import downloadSpainData
pd.set_option('display.max_columns', None)
urllib3.disable_warnings()

def genData(nreport,region):
   df, lastModified = downloadSpainData(nreport,region)
   hosp = df.loc[region,"Hospitalizados"] if "Hospitalizados" in df.columns else np.NaN

   return (df.loc[region,"Total casos"], df.loc[region,"Fallecidos"],\
           hosp, lastModified)

cases = []
dates = []
reports = []
fatalities = []
hospitalized = []
region = "Madrid"

for nreport in range(36,9999):
   try:
      case,fatality, hosp, date=genData(nreport,region)
      cases.append(case)
      fatalities.append(fatality)
      hospitalized.append(hosp)
      dates.append(date)
      reports.append(nreport)
   except FileNotFoundError:
      break
   except Exception as e:
      print(e)
      print(traceback.format_exc())
      pass
print("NREPORT FAIL",nreport)
df = pd.DataFrame(data={"Date":dates,"Cases":cases,"Fatalities": fatalities,
                  "Hospitalized": hospitalized, "Report":reports})

df["Date"] = [datetime.datetime(*eut.parsedate(x)[:6]) for x in df["Date"]]
print(df)
for col in ["Cases","Fatalities","Hospitalized"]:
   if col in df.columns:
      df[col] = df[col].astype(str)
      df[col] = [x.replace('.0','') if x.endswith('.0') else x for x in df[col]]
      df[col] = [x.replace('.','').replace(',','') for x in df[col]]
      df[col] = df[col].astype(float)

df["Newly confirmed cases"] = df["Cases"].diff()
df["Hospitalization ratio"] = 100 * df["Hospitalized"] / df["Cases"]
df["Deaths / Confirmed cases"] = 100 * df["Fatalities"] / df["Cases"]
print(df)
f, ax = plt.subplots(1, 1)
plotSubchart(df,ax,cols=["Newly confirmed cases"],title=region)
lockdown = datetime.datetime(2020, 3, 14)
ax.annotate('Lockdown announced', (mdates.date2num(lockdown)+0.2, 1100))
plt.axvline(lockdown, linestyle="dashed", color="gray")
plt.show()
