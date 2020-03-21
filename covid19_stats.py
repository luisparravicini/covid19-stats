import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()

date = '2020-03-20'
path = f'COVID-19-geographic-disbtribution-worldwide-{date}.xlsx'
df = pd.read_excel(path)
df.rename(columns={'DateRep': 'Date'}, inplace=True)
df = df.sort_values('Date', ascending=True)
df.set_index('Date')

fig, ax = plt.subplots()
countries = ('AR', 'BR', 'CL', 'BO', 'PE', 'UY', 'PY', 'EC', 'CO', 'VE')
for geoid in countries:
    geo_df = df[df['GeoId'] == geoid]
    geo_df['Cumulative'] = geo_df['Cases'].cumsum().replace(0, np.nan)
    # geo_df['CumulativeDeaths'] = geo_df['Deaths'].cumsum().replace(0, np.nan)
    name = geo_df['Countries and territories'].iloc[0]

    ax.plot(geo_df['Date'], geo_df['Cumulative'], label=name)
    # ax[1].plot(geo_df['Date'], geo_df['CumulativeDeaths'], label=name)
    # ax[1].set_title('Muertes')

fig.autofmt_xdate()
plt.legend()
plt.xlabel('Fecha')
plt.ylabel('Casos confirmados')
plt.title(f'Casos confirmados al {date}')

plt.show()
