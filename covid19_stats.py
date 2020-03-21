import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import requests
import sys
import re
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


date = datetime.today().strftime('%Y-%m-%d')
fname_prefix = 'COVID-19-geographic-disbtribution-worldwide'
fname = Path(f'{fname_prefix}-{date}.xlsx')

if not fname.exists():
    print(f'fetching {date} data')
    BASE_URL = 'https://www.ecdc.europa.eu/sites/default/files/documents/'
    res = requests.get(BASE_URL + str(fname))
    if res.status_code == 200:
        with open(fname, 'wb') as f:
            f.write(res.content)
    else:
        data_files = sorted(Path('.').glob(fname_prefix + '*'))
        if len(data_files) == 0:
            print('no data files')
            sys.exit(1)
        fname = data_files[-1]
        match = re.search(r'(\d{4}-\d{2}-\d{2})', str(fname))
        if match is None:
            print('couldn\'t extract date')
            sys.exit(1)
        date = match.group(1)
        print(f'using {fname}')

df = pd.read_excel(fname)
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
plt.ylabel('Casos')
plt.title(f'Casos sudamérica confirmados al {date}')

plt.show()
