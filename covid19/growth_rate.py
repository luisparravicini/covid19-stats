import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .utils import find_newest_dataset
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


path, date = find_newest_dataset()
df = pd.read_excel(path)
df.rename(columns={'DateRep': 'Date'}, inplace=True)
df = df.sort_values('Date', ascending=True)
df.set_index('Date')

fig, ax = plt.subplots()
countries = ('AR', 'BR', 'CL', 'BO', 'PE', 'UY', 'PY', 'EC', 'CO', 'VE')
for geoid in countries:
    geo_df = df[df['GeoId'] == geoid]
    geo_df['Cumulative'] = geo_df['Deaths'].cumsum()
    geo_df['GrowthRate'] = geo_df['Cumulative'].pct_change()
    name = geo_df['Countries and territories'].iloc[0]

    ax.plot(geo_df['Date'], geo_df['GrowthRate'], label=name)

ax.axhline(y=1, linestyle='--')

fig.autofmt_xdate()
plt.legend()
plt.ylabel('Rate')
plt.title('Confirmed cases growth rate')

plt.show()
