import pandas as pd
import numpy as np
from .utils import read_dataset, name_for
from datetime import datetime
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


df = read_dataset()

print('Doubles\tDeaths\tLocation')
today = datetime.today()
countries = df['geoId'].dropna().unique()
for geoid in countries:
    geo_df = df[df['geoId'] == geoid]
    name = name_for(geo_df)

    geo_df['cumulative'] = geo_df['deaths'].cumsum()
    max_deaths = geo_df['cumulative'].iloc[-1]
    half_current_max = max_deaths / 2

    if half_current_max <= 0:
        continue

    row = geo_df[geo_df['cumulative'] >= half_current_max].iloc[0]

    doubles_in = round((today - row['date']).total_seconds() / (24 * 3600))
    print("\t".join(map(str, (doubles_in, max_deaths, name))))
