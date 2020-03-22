from pathlib import Path
from datetime import datetime
import requests
import sys
import re


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
