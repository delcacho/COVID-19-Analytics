import pandas as pd
import tabula
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from io import StringIO
import requests

pd.set_option('display.max_rows', 500)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

def processJohnsHopkinsDF(df,withHubei=True):
   df = df.transpose()
   hubei = [x == 'Hubei' for x in df.iloc[0,:].values.tolist()]
   for i,v in enumerate(hubei):
     if v == True:
        break
   df.iloc[0,hubei] = np.NaN
   df.iloc[1,hubei] = "Hubei"
   df['Date'] = df.index
   df.loc['Province/State','Date'] = np.NaN
   df.loc['Lat','Date'] = np.NaN
   df.loc['Country/Region','Date'] = 'Date'
   latitude = df.iloc[2,:].values
   colna = df.loc["Province/State"].isna()
   latitude = latitude[colna]
   df = df[df.columns[colna]]
   headers = df.iloc[1,:].values
   df = df.iloc[4:]
   df.columns = headers
   df['Date'] =  pd.to_datetime(df['Date'], format='%m/%d/%y', errors='ignore')
   df.index = df['Date']
   cols = df.columns.values.tolist()
   for col in cols:
      if col != "China" and col != "Date":
         df[col] = df[col].astype(float)
   return(df,latitude)
  
def downloadCovidData():

   confirmed = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
   death = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
   confirmed, latitude = processJohnsHopkinsDF(confirmed)
   death,_ = processJohnsHopkinsDF(death)
   return (confirmed,death,latitude)

def downloadUsaCovidData():

   url = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv"
   resp = requests.get(url, verify=False)
   try:
      lastModified = resp.headers["Last-modified"]
   except:
      lastModified = None
   print("LAST MODIFIED: {}".format(lastModified))
   confirmed = pd.read_csv(StringIO(resp.content.decode("UTF-8")))
   confirmed = confirmed.drop("countyFIPS",axis=1).drop("stateFIPS",axis=1)
   #confirmed = confirmed.groupby("State").sum().iloc[:,:-1].transpose()
   confirmed = confirmed.groupby("State").sum().transpose()
   confirmed['Date'] = confirmed.index
   try:
      confirmed['Date'] = pd.to_datetime(confirmed['Date'], format='%m/%d/%Y')
   except:
      confirmed['Date'] = pd.to_datetime(confirmed['Date'], format='%m/%d/%y')
   return(confirmed)

def downloadSpainData(nreport,region):
   urls = []
   urls.append("https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/documentos/Actualizacion_{}_COVID-19.pdf".format(nreport))
   urls.append("https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/documentos/Actualizacion_{}_COVID_1200.pdf".format(nreport))
   urls.append("https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/documentos/Actualizacion_{}_COVID.pdf".format(nreport))
   ok = False
   for url in urls:
      resp = requests.get(url, verify=False)
      if resp.status_code == 200:
         ok = True
         break
      resp = requests.get(url, verify=False)
   if not ok:
      raise FileNotFoundError

   try:
      lastModified = resp.headers["Last-modified"]
   except:
      lastModified = None
   print("LASTMODIFIED: ",lastModified)
   open('report.pdf', 'wb').write(resp.content)


   npage=1
   # Columns iterpreted as str
   tables = tabula.read_pdf("report.pdf",multiple_tables=True,pages='all',encoding='utf-8',
              pandas_options={'dtype':str})
   for table in tables:
      if region in table.values:
         df = table
         break

   if not 'CCAA' in df.columns:
      for i,row in df.iterrows():
         if 'CCAA' in row.values:
            break
      df = df.iloc[i:,:]
      for col in df.columns.tolist():
         if df[col].isnull().all():
            df = df.drop(columns=[col])
      df = df.reset_index()
      df.columns = df.iloc[0]
      df = df.iloc[1:,:]
      for i,col in enumerate(df.columns.tolist()):
         if col == 'CCAA':
            break
      df = df.iloc[:,i:]
   df["CCAA"] = df["CCAA"].replace("Castilla La Mancha", "Castilla-La Mancha")
   df["CCAA"] = df["CCAA"].replace("C. Valenciana", "C Valenciana")
   if pd.isnull(df["CCAA"].values[0]):
     df = df.iloc[1:,:]
   df.index = df.iloc[:,0]
   df = df.fillna(0)

   cols = df.columns.tolist()
   cols = [str(x) if not "IA" in str(x) else "IA (14 d.)" for x in cols]
   df.columns = cols

   if "IA (14 d.)" in df.columns:
     cols[cols.index("IA (14 d.)")-1] = "Total casos"
   df.columns = cols
      
   for i,col in enumerate(df.columns.tolist()):
      values = df.iloc[:,i].values.tolist()
      for val in values:
         if "ospitali" in str(val):
           cols[i] = "Hospitalizados"
         if "UCI" in str(val):
           cols[i] = "Ingreso en UCI"
         if "total" in str(val).lower() and ("caso" in str(val).lower() or "conf" in str(val).lower()):
           cols[i] = "Total casos"

   df.columns = cols

   if df.iloc[0,0] == 0:
      df = df.iloc[1:,:]
   df = df.head(19)
   print(df)
   for col in ["Total casos","Hospitalizados", "UCI", "Fallecidos", "Ingreso en UCI"]:
      if col in df.columns:
         df[col] = df[col].astype(str)
         df[col] = [x.replace('.0','') if x.endswith('.0') else x for x in df[col]]
         df[col] = [x.replace('.','').replace(',','') for x in df[col]]
         df[col] = df[col].str.extract('(\d+)', expand=False)
         df[col] = df[col].astype(float)
   return (df, lastModified)



def removeColumn(datatuple,col):
   confirmed, death, latitude = datatuple
   notcol = [x != col for x in confirmed.columns]
   confirmed = confirmed[confirmed.columns[notcol]]
   death = death[death.columns[notcol]]
   latitude = latitude[notcol]
   return (confirmed,death,latitude)

def plotChart(df,title=None,cols=None, percent=False, legend=True, labels=None, useLabels=True):
   f, ax = plt.subplots(1, 1)
   plotSubchart(df,ax,title,cols,percent,legend,labels,useLabels=True)
   plt.tight_layout()
   plt.show()

def plotSubchart(df,ax,title=None,cols=None, percent=False, legend=True, labels=None, useLabels=True):
   for col in cols:
      sns.lineplot(x="Date", y=col, ax=ax, data=df)
   ax.set(xlabel='Date', ylabel=title)
   if useLabels == False:
      ax.set(xlabel=None)
   if labels is None:
      labels = cols
   if legend:
      ax.legend(labels=labels)
   if percent:
      ax.yaxis.set_major_formatter(mtick.PercentFormatter())
   plt.tight_layout()

