import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .utils import read_dataset, name_for
from datetime import timedelta
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


def find_doubles(df, cumName, dataName):
    df[cumName] = df[dataName].cumsum()
    max_value = df[cumName].iloc[-1]
    half_current_max = int(max_value / 2)

    if half_current_max <= 0:
        return None

    row = df[df[cumName] >= half_current_max].iloc[0]
    doubles_in = (date - row['date']).total_seconds() / (24 * 3600)

    return doubles_in


df = read_dataset()
fig, ax = plt.subplots(4, 3, sharex=True)

last_date = df['date'].max()
start_date = last_date - timedelta(days=30)

countries = ('NL', 'CN', 'AR', 'IT', 'ES', 'EC', 'BR', 'CL', 'UY', 'CO', 'US', 'MX')

for geoid, ax in zip(countries, ax.flat):
    country_df = df[df['geoId'] == geoid]
    data = [[], [], []]
    for date in pd.date_range(start_date, last_date):
        geo_df = country_df[country_df['date'] <= date]

        if len(geo_df) == 0:
            continue

        doubles_deaths_in = find_doubles(geo_df,
                                         'cumulativeDeaths',
                                         'deaths')

        doubles_cases_in = find_doubles(geo_df,
                                        'cumulativeCases',
                                        'cases')

        data[0].append(date)
        data[1].append(doubles_deaths_in)
        data[2].append(doubles_cases_in)

    ax.set_title(name_for(geo_df), fontsize=10)

    min_y = 10
    if max([x for x in data[1] + data[2] if x is not None]) < min_y:
        ax.set_ylim(top=min_y)

    ax.invert_yaxis()
    ax.plot(data[0], data[1], label='deaths', color='red')
    ax.plot(data[0], data[2], label='cases', color='blue')


handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right')

fig.text(0.5, 0.05, 'Weeks', ha='center')
fig.text(0.05, 0.5, 'Days to double', va='center', rotation='vertical')

fig.autofmt_xdate()

start_date = start_date.date()
last_date = last_date.date()
fig.text(0.5, 0.92, f'({start_date} to {last_date})',
         fontsize=10, horizontalalignment='center')
fig.suptitle(f'Trends', fontsize=12)

plt.xticks(ticks=pd.date_range(start_date, last_date, freq='1w'), labels=[])
plt.tight_layout(rect=[0.05, 0.075, 1, 0.9])

plt.show()
