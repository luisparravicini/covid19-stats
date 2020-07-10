from pathlib import Path
import pandas as pd
from datetime import datetime
import requests
import sys
import re
import json


def read_dataset():
    path = find_newest_dataset(download=True)
    df = pd.read_csv(path, parse_dates=['dateRep'], dayfirst=True)
    df.rename(columns={'dateRep': 'date'}, inplace=True)
    df = df.sort_values('date', ascending=True)
    df.set_index('date')
    print(df)
    return df


def name_for(df):
    return df['countriesAndTerritories'].iloc[0].replace('_', ' ')


def find_newest_dataset(download=True):
    date = datetime.today().strftime('%Y-%m-%d')
    fname_prefix = 'covid19-data-'
    fname = Path(f'{fname_prefix}{date}.csv')

    if not fname.exists():
        if download:
            print(f'fetching data file')
            url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'
            res = requests.get(url)
            if res.status_code == 200:
                with open(fname, 'wb') as f:
                    f.write(res.content)

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

    return fname


def countries_population():
    path = Path('population.json')
    if path.exists():
        with open(path) as file:
            return json.load(file)

    print('fetching countries populations')
    res = requests.get('https://www.worldometers.info/world-population/population-by-country/')
    res.raise_for_status()

    population = dict()

    soup = BeautifulSoup(res.content, 'html.parser')
    for row in soup.table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) > 0:
            name = cols[1].text
            n = int(cols[2].text.replace(',', ''))
            population[name] = n

    with open(path, 'w') as file:
        json.dump(population, file)

    return population
