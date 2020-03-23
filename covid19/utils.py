from pathlib import Path
from datetime import datetime
import requests
import sys
import re
from bs4 import BeautifulSoup
import json


def find_newest_dataset():
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
    return (fname, date)


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
