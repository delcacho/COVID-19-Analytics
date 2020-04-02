import pandas as pd
import numpy as np

imperial = pd.read_csv("data/imperial.csv")
agedist = pd.read_csv("data/spaindist.csv")
df = imperial.set_index('AgeGroup').join(agedist.set_index('AgeGroup'),lsuffix='_left', rsuffix='_right')

target = 12
df["Proportion"] = df["Proportion"] * df["HospRatio"]
df["Proportion"] /= df["Proportion"].sum()
df["ICURatio"] = 1
print(df)

def computeMortality(df):
   inicu = np.sum(df["Proportion"] * df["FatalityRate"] * df["ICURatio"])
   outicu = np.sum(df["Proportion"] * df["FatalityRate"] * 2 * (1 - df["ICURatio"]))
   return inicu + outicu

def findICUPolicy(df,target):
   n = df.shape[0]
   policy = [1] * n
   while n > 0:
      n = n-1
      while policy[n] >= 0:
         df["ICURatio"] = policy
         if computeMortality(df) >= target:
            return(df)
         policy[n] -= 0.01
      # restore at minimum
      policy[n] = 0
   return(df)

print("Expected Fatality with no Triage: ",computeMortality(df))
print("ICU Policy for {} fatality rate: ".format(target))
print(findICUPolicy(df,target))
