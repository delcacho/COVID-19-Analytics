import math
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import datetime
import pandas as pd

def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]
    return helper

def newtonRaphson(model,xi):
   tol = 999
   while tol > 0.00001:
      xi = xi - derivative(model,xi)/secondDerivative(model,xi)
      tol = derivative(model,xi)
   return(xi)

def findMaximum(model):
   maxdiff = -999999
   xmax = 0
   for xi in range(0,200,1):
      xr = newtonRaphson(model,xi)
      diff = evaluateDiff(model,xr)
      if diff > maxdiff:
         xmax = xr
         maxdiff = diff
   return(xmax)
findMaximum = memoize(findMaximum)

def evaluateDiff(model,x,step=1):
   return (np.exp(evaluateModel(model,x)) - np.exp(evaluateModel(model,x-step)))

def derivative(model,x):
   h = 0.0001
   return (evaluateDiff(model,x+h) - evaluateDiff(model,x))/h

def secondDerivative(model,x):
   h = 0.0001
   val = (derivative(model,x+h) - derivative(model,x))/h
   return(val)

def evaluateModel(model,x):
   return(np.sum(model.coef_ * [1,x,math.pow(x,2)]) + model.intercept_)

def polyCalc(model,x):
   tng = findMaximum(model)
   mx = evaluateModel(model,tng)
   if x <= tng:
      y = evaluateModel(model,x)
   else:
      y = math.log(2 * math.exp(evaluateModel(model,tng)) -
                       math.exp(evaluateModel(model,tng - (x-tng))))
   return(y)

def forecastRegion(confirmed,target,startDate,daysforecast=200):

   base = datetime.datetime.strptime(startDate, '%Y-%m-%d')
   confirmed = confirmed[confirmed["Date"] >= base]
   lenini = confirmed.shape[0]
   confirmed = confirmed[confirmed[target] >= 1.1]
   lenend = confirmed.shape[0]
   y = confirmed[target]
   start = lenini-lenend
   polynomial_features= PolynomialFeatures(degree=2)
   x_poly = polynomial_features.fit_transform(np.array(range(start,start+len(y))).reshape(-1, 1))
   model = LinearRegression()
   model.fit(x_poly, y)
   y_poly_pred = model.predict(x_poly)
   rmse = np.sqrt(mean_squared_error(y,y_poly_pred))
   r2 = r2_score(y,y_poly_pred)
   print(rmse)
   print(r2)
   x_poly = polynomial_features.fit_transform(np.array(range(0,daysforecast)).reshape(-1, 1))
   y_poly_pred = model.predict(x_poly)

   date_list = [base + datetime.timedelta(days=x) for x in range(daysforecast)]
   projections = pd.DataFrame({"Date":date_list,"Forecast":y_poly_pred})
   projections["Forecast"] = [polyCalc(model,x) for x in range(daysforecast)]
   return(projections, model)
