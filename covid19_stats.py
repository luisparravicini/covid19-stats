import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

path = 'COVID-19-geographic-disbtribution-worldwide-2020-03-20.xlsx'
df = pd.read_excel(path)
df.rename(columns={'DateRep': 'Date'}, inplace=True)
df = df.sort_values('Date', ascending=True)
df.set_index('Date')

for geoid in ('AR', 'BR', 'CL', 'BO', 'PE', 'UY', 'PY', 'EC', 'CO', 'VE'):
    geo_df = df[df['GeoId'] == geoid]
    geo_df['Cumulative'] = geo_df['Cases'].cumsum().replace(0, np.nan)
    name = geo_df['Countries and territories'].iloc[0]
    plt.plot(geo_df['Date'], geo_df['Cumulative'], label=name)

plt.legend()
plt.xlabel('Fecha')
plt.ylabel('Casos')

plt.show()
