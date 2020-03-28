import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .utils import find_newest_dataset, countries_population, name_for
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


populations = countries_population()
path, date = find_newest_dataset(download=True)
df = pd.read_excel(path)
df.rename(columns={'dateRep': 'date'}, inplace=True)
df = df.sort_values('date', ascending=True)
df.set_index('date')

fig, ax = plt.subplots()
#countries = df['GeoId'].dropna().unique()
countries = ('AR', 'BR', 'CL', 'BO', 'PE', 'UY', 'PY', 'EC', 'CO', 'VE')
for geoid in countries:
    geo_df = df[df['geoId'] == geoid]
    name = name_for(geo_df)
    inhabitants = populations[name] / 1000000
    geo_df['cumulative'] = (geo_df['cases'].cumsum() / inhabitants).replace(0, np.nan)
    # geo_df['CumulativeDeaths'] = (geo_df['Deaths'].cumsum() / inhabitants).replace(0, np.nan)

    ax.plot(geo_df['date'], geo_df['cumulative'], label=name)
    # ax[1].plot(geo_df['Date'], geo_df['CumulativeDeaths'], label=name)
    # ax[1].set_title('Muertes')

fig.autofmt_xdate()
plt.legend()
plt.title('Confirmed cases (per millon inhabitants)')

plt.show()
