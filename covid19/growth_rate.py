import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .utils import find_newest_dataset, countries_population
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


populations = countries_population()
path, date = find_newest_dataset(download=True)
df = pd.read_excel(path)
df.rename(columns={'DateRep': 'Date'}, inplace=True)
df = df.sort_values('Date', ascending=True)
df.set_index('Date')

fig, ax = plt.subplots()
#countries = ('BE', 'NL', 'DE', 'ES', 'IT')
countries = ('AR', 'BR', 'CL', 'BO', 'PE', 'PY', 'EC', 'CO', 'VE')
for geoid in countries:
    geo_df = df[df['GeoId'] == geoid]
    name = geo_df['Countries and territories'].iloc[0].replace('_', ' ')
    inhabitants = populations[name] / 1000000

    geo_df['Cumulative'] = (geo_df['Deaths'] / inhabitants).cumsum()
    # geo_df['GrowthRate'] = geo_df['Cumulative'].pct_change()
    geo_df['GrowthRate'] = geo_df['Cumulative'].replace(0, np.nan)

    ax.plot(geo_df['Date'], geo_df['GrowthRate'], label=name)

# ax.axhline(y=1, linestyle='--')

fig.autofmt_xdate()
plt.legend()
plt.ylabel('Rate')
plt.title('Cumulative deaths per million inhabitantes')

plt.show()
