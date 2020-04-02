import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick
import numpy as np
import datetime
import math
from collections import Counter
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from utils import downloadCovidData
from utils import plotSubchart

confirmed, death, _ = downloadCovidData()
col = "World w/o China"
confirmed[col] = np.log(confirmed.drop("Hubei",axis=1).sum(axis=1))
confirmed["Hubei"] = confirmed["Hubei"].astype(float)
cols = ["Italy", "Spain","Hubei", "Germany", "France"]
for col in cols:
   confirmed[col] = np.log(confirmed[col])
death["World w/o China"] = death.sum(axis=1)
#death["World w/o China"] = death["World w/o China"] / confirmed["World w/o China"]
#print("Min: ",np.min(confirmed["World w/o China"]))
#print("Max: ",np.max(confirmed["World w/o China"]))
#print("Min date: ",np.min(confirmed["Date"]))
#print("Max date: ",np.max(confirmed["Date"]))
print(confirmed["Spain"])
start = "2020-02-25"
confirmed = confirmed[confirmed["Date"] >= start]
y = confirmed["Spain"]
polynomial_features= PolynomialFeatures(degree=2)
x_poly = polynomial_features.fit_transform(np.array(range(0,len(y))).reshape(-1, 1))
model = LinearRegression()
model.fit(x_poly, y)
y_poly_pred = model.predict(x_poly)
rmse = np.sqrt(mean_squared_error(y,y_poly_pred))
r2 = r2_score(y,y_poly_pred)
print(rmse)
print(r2)
x_poly = polynomial_features.fit_transform(np.array(range(0,200)).reshape(-1, 1))
y_poly_pred = model.predict(x_poly)
print(y_poly_pred)
numdays = 200
base = datetime.datetime.strptime(start, '%Y-%m-%d')
date_list = [base + datetime.timedelta(days=x) for x in range(numdays)]
projections = pd.DataFrame({"Date":date_list,"Forecast":y_poly_pred})
print(projections)
for i,row in projections.iterrows():
   if i > 0:
      if projections.iloc[i,1] < projections.iloc[i-1,1]:
          break
projections = projections.iloc[:i,:]
print(projections)
print(math.exp(projections["Forecast"][i-1]))
#projections["Forecast"] = [math.exp(x) for x in projections["Forecast"]]
#projections["Forecast"] = projections["Forecast"].diff()
f, ax = plt.subplots(1, 1)
plotSubchart(confirmed,ax,title="log(Confirmed cases)",cols=["Italy","Spain","World w/o China","Hubei"])
plotSubchart(projections.iloc[:60,:],ax,title="log(Confirmed cases)",cols=["Forecast"],legend=False,useLabels=False)
plt.show()
projections["Forecast"] = [math.exp(x) for x in projections["Forecast"]]
projections["Forecast"] = projections["Forecast"].diff()
print("MAX: ",projections["Forecast"].max())
print(projections[projections["Forecast"] == projections["Forecast"].max()])
