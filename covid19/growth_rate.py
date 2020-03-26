import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .utils import find_newest_dataset, name_for
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


path, date = find_newest_dataset(download=True)
df = pd.read_excel(path)
df.rename(columns={'DateRep': 'Date'}, inplace=True)
df = df.sort_values('Date', ascending=True)
df.set_index('Date')

fig, ax = plt.subplots()

countries = ('CN', 'IT', 'ES', 'EC', 'BR', 'CL', 'EC', 'CO', 'US', 'MX')
countries = ('CN', 'IT', 'AR', 'EC', 'MX', 'BR', 'US')
max_days = 0
min_deaths = 5
max_deaths = 0
for geoid in countries:
    geo_df = df[df['GeoId'] == geoid].copy()

    geo_df['Cumulative'] = geo_df['Deaths'].cumsum()

    geo_df.drop(index=geo_df[geo_df['Cumulative'] < min_deaths].index,
                inplace=True)
    geo_df['Cumulative'] -= min_deaths

    geo_df['DaysSince'] = range(len(geo_df))

    ax.plot(geo_df['DaysSince'], geo_df['Cumulative'], label=name_for(geo_df))

    max_days = max(max_days, len(geo_df))
    max_deaths = max(max_deaths, geo_df['Cumulative'].iloc[-1])

indexes = (2, 3, 5, 10)
data = list()
for i in range(max_days):
    datum = [i] + list(map(lambda x: np.power(2, i / x), indexes))
    data.append(datum)

curves = pd.DataFrame(
            data=data,
            columns=['x'] + list(map(lambda x: f'd{x}', indexes))
        )
for d in indexes:
    ax.plot(curves['x'], curves[f'd{d}'], linestyle='--', label=f'doubles in {d} days')


ax.set_yscale('log')
plt.legend()
plt.ylim(top=max_deaths, bottom=1)
plt.ylabel('Deaths')
plt.xlabel(f'Days since first {min_deaths} deaths')
plt.title('Cumulative deaths')

plt.show()
