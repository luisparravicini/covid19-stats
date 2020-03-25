import pandas as pd
import numpy as np
from .utils import find_newest_dataset, name_for
from datetime import datetime
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


path, date = find_newest_dataset(download=True)
df = pd.read_excel(path)
df.rename(columns={'DateRep': 'Date'}, inplace=True)
df = df.sort_values('Date', ascending=True)
df.set_index('Date')

print('Doubles\tDeaths\tLocation')
today = datetime.today()
countries = df['GeoId'].dropna().unique()
for geoid in countries:
    geo_df = df[df['GeoId'] == geoid]
    name = name_for(geo_df)

    geo_df['Cumulative'] = geo_df['Deaths'].cumsum()
    max_deaths = geo_df['Cumulative'].iloc[-1]
    half_current_max = max_deaths / 2

    if half_current_max <= 0:
        continue

    row = geo_df[geo_df['Cumulative'] >= half_current_max].iloc[0]

    doubles_in = (today - row['Date']).days
    print("\t".join(map(str, (doubles_in, max_deaths, name))))
