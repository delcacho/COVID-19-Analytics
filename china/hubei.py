import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
import matplotlib.ticker as mtick
import numpy as np
from collections import Counter
from utils import downloadCovidData
from utils import plotSubchart

confirmed, death, _ =  downloadCovidData()
cols = ["Italy", "Spain","Hubei", "Germany", "France"]
country = "Hubei"
cols = [country]
for col in cols:
   confirmed[col] = confirmed[col].diff()
   death[col] = death[col].diff()

confirmed = confirmed[confirmed.Date > '2020-01-24']
death = death[death.Date > '2020-01-24']
sns.set(rc={'figure.figsize':(16,4)})
f, ax = plt.subplots(1, 2)
f.tight_layout()
plotSubchart(confirmed,ax[0],title="Newly confirmed cases",cols=[country])
plotSubchart(death,ax[1],"Newly confirmed deaths",cols=[country])
f.tight_layout()
f.savefig("output.png")
plt.show()
