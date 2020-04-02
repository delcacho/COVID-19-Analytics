# COVID-19-Analytics
KPI Tracking of Coronavirus spread over time along with some forecasting models.

## Data Sources
Currently downloading country level data from Johns Jopkins CSSE, regional data for the
US from  USAFacts.org, and regional level data for Spain straight from the PDFs the
Health Ministry publishes daily and parsing it with tabula.

In file utils/utils.py there are several functions to process these data sources and convert
them to Pandas data frames. The function downloadSpainData might be particularly useful if
you are interested in analyzing Spanish data because I don't know any source like USAFacts
for Spain. Sometimes the ministry switches formats and breaks things, but hopefully the code
is already quite resistant to those mischiefs.

## Forecasting model

After plotting several log charts over time I noticed that the curve's arch could be approximated with a
second degree polynomial quite well. The code to perform the polynomial regression is in file (model/model.py).
There is a further refinement afterwards, that forces the forecast to be normally distributed. This is accomplished
through symmetry of the left hand side of the Bell curve with some fancy mathematics. Notice that it is not
guaranteed that a country's newly confirmed cases curve should be normally distributed, but it is a good approximation
nonetheless.

A better way to forecast a country would be to fit individual regional models and add them up.
Central Limit Theorem should make sure the addition of all estimates is normally distributed itself, but typically 
there aren't that many regions for the approximation to apply, and more importantly, they are not identically distributed.
So the shape depends on the different time intervals of the spread of the disease along with other factors such
as population density.

## Dependencies


- pandas
- urllib3
- request
- seaborn
- tabula_py
- matplotlib
- numpy
- scikit_learn
- scipy
- tabula

## How to get this running

Python 3 is a hard requirement. If you are not using it, you should.

There is a requirements.txt file that allows installing needed libraries:

```
pip install -r requirements.txt
```

After this step, make sure that the current directory appears in the PYTHONPATH environment variable.

Individual files are expected to be executed from the root folder, like so:
```
python3 spain/madrid.py
```

## Currently tracked KPIs
- Case fatality rate over time (file deathrate.py)
- Confirmed cases over time in logarithmic representation (file logchart.py)
- Several ratios for hospitalization data for Spain (file spain/icu.py) including:
  - Case fatality rate per region
  - Share of total fatalities for a given region for all fatalities in Spain
  - ICU fill rate (with number of beds prior to the Covid-19 crisis, which is a surrogate for available ventilators)
  - ICU patients to confirmed cases ratio (as an indicator of severity)
  - Hospitalized patients to confirmed cases ratio (resolved cases still count as hospitalized if hospitalized once)
  - Confirmed cases per 1M population (Incidence) 
  - Confirmed cases per 1M population adjusted for hospitalization rates (Higher hospitalization rates, suggest higher actual cases) 
  - Adjusted incidence to ICU beds ratio (as per the adjusment in the previous line)
  - Suspected actual total cases (Adjustment for hospitalization rate under the idea that only 20% of patients warrant hospitalization)
- Newly confirmed cases over time for Madrid (file spain/madrid.py). This file can be used to chart any of the regional metrics for Spain outlined above.
- Some metrics for Italy:
  - Newly confirmed cases over time for Italy (file italy/italy.py)
  - Lombardy under lockdown newly confirmed cases (file italy/lombardy.py), from static data downloaded from here (http://lispa.maps.arcgis.com/apps/opsdashboard/index.html#/637ec3dc28ec4ea591cc5c724f127701)
  - Lombardy under lockdown growth rate (file italy/lombardy2.py)
- Analysis of confirmed cases by latitude:
  - Bar chart of confirmed cases (file latitude/latitude.py)  
  - Confirmed cases over time in logarithmic representation (file latitude/latitude2.py)  
  - Northern hemisphere vs Southern hemisphere confirmed cases over time in lograithmic representation (file latitude/hemisphere.py)  
- Forecasts with a polynomial model to try to fit a Bell curve for newly confirmed cases:
  - Forecasts for several countries (Spain, Italy, UK) along with expected crossing points (file curve/cross.py)
  - Simple polynomial model without correcting the right hand side of the Bell curve (file curve/curve.py).
  - Polynomial model with Bell curve reflection after finding maximum with Newton-Raphson method  (file curve/curvefixed.py).
  - Newly confirmed cases for polynomial model with Bell curve reflection (file curve/curvefixedbell.py).
- Analysis for newly confirmed cases vs newly confirmed deaths for Hubei (file china/hubei.py). This data seems to be manually altered to hide the severity of the epidemic.
- Some attempts to fit polynomial models to several states in the US can be found in (file usa/curveusa.py)
