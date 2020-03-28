import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .utils import read_dataset, name_for
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


df = read_dataset()
fig, ax = plt.subplots()

countries = ('CN', 'IT', 'ES', 'EC', 'BR', 'CL', 'EC', 'CO', 'US', 'MX')
countries = ('CN', 'ES', 'IT', 'AR', 'EC', 'MX', 'BR', 'US')
max_days = 0
min_deaths = 5
max_deaths = 0
for geoid in countries:
    geo_df = df[df['geoId'] == geoid].copy()

    geo_df['cumulative'] = geo_df['deaths'].cumsum()

    geo_df.drop(index=geo_df[geo_df['cumulative'] < min_deaths].index,
                inplace=True)
    geo_df['cumulative'] -= min_deaths

    geo_df['daysSince'] = range(len(geo_df))

    ax.plot(geo_df['daysSince'], geo_df['cumulative'], label=name_for(geo_df))

    max_days = max(max_days, len(geo_df))
    max_deaths = max(max_deaths, geo_df['cumulative'].iloc[-1])

indexes = (2, 3, 5, 10)
data = list()
for i in range(max_days):
    datum = [i] + list(map(lambda x: np.power(2, i / x), indexes))
    data.append(datum)

curves = pd.DataFrame(
            data=data,
            columns=['x'] + list(map(lambda x: f'd{x}', indexes))
        )
print(curves.iloc[0:10])
print(curves.iloc[15:25])
for d in indexes:
    ax.plot(curves['x'], curves[f'd{d}'], linestyle='--', label=f'doubles every {d} days')


# ax.set_yscale('log')
plt.legend()
plt.ylim(top=max_deaths, bottom=1)
plt.ylabel('Deaths')
plt.xlabel(f'Days since first {min_deaths} deaths')
plt.title('Cumulative deaths')

plt.show()
