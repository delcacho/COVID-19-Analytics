import tabula
import urllib3
import requests
import pandas as pd
import traceback
import numpy as np
from utils import downloadSpainData

pd.set_option('display.max_columns', None)
urllib3.disable_warnings()

region = "Madrid"
for nreport in range(51,999):
   try:
      df, lastModified = downloadSpainData(nreport,region)
   except FileNotFoundError:
      break
   except Exception as e:
      print(traceback.format_exc())
      pass

print("LAST REPORT",nreport)
beds = pd.read_csv("data/beds.csv")
df = df.set_index('CCAA').join(beds.set_index('CCAA'),lsuffix='_left', rsuffix='_right')
df["CasesToBedsRatio"] = df["Total casos"] / df["Camas"]
df["CaseFatalityRate"] = df["Fallecidos"] / df["Total casos"]
df["ShareFatality"] = df["Fallecidos"] / sum(df["Fallecidos"])
df["ICUFillRatio"] = df["Ingreso en UCI"] / df["Camas"]
df["ICUToCasesRatio"] = df["Ingreso en UCI"] / df["Total casos"]
df["CasesToPopRatio"] = 1000000 * df["Total casos"] / df["Poblacion"]
df["HospRatio"] = df["Hospitalizados"] / df["Total casos"]
df["AdjustedIncidence"] = (df["HospRatio"] /0.2)* df["CasesToPopRatio"] 
df["TotalCases"] = (df["AdjustedIncidence"] * df["Poblacion"] / 1000000.0)
df["AdjustedIncidenceToBeds"] = df["AdjustedIncidence"] / (df["Camas"]*1000/df["Poblacion"])
print(df)
print("Cases Spain {}".format(df["TotalCases"].sum()))
