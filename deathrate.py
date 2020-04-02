import pandas as pd
import numpy as np
from utils import downloadCovidData
from utils import plotChart

confirmed, death, _ = downloadCovidData()
print(confirmed.columns)
death["Spain"] = 100 * death["Spain"] / confirmed["Spain"]
death["Germany"] = 100 * death["Germany"] / confirmed["Germany"]
death["Italy"] = 100 * death["Italy"] / confirmed["Italy"]
death["France"] = 100 * death["France"] / confirmed["France"]
death["Hubei"] = 100 * death["Hubei"] / confirmed["Hubei"]
plotChart(death,title="Deaths / Confirmed cases",
   cols=["Spain","Italy","France","Germany","Hubei"],
   percent=True)
