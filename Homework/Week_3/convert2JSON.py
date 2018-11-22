#!/usr/bin/env python
# Name: Siger de Vries
# Student number: 10289321

import pandas as pd
from datetime import datetime

df = pd.read_csv('gemiddeldetemperatuur.csv')
df = df.drop([' STN'], axis=1)
#df['YYYYMMDD'] = pd.to_datetime(df['YYYYMMDD'].astype(str), format='%Y%m%d')
df.columns = ['datum','temperatuur']
if __name__ == "__main__":

    with open('output.json', 'w') as f:
        df.to_json(f, orient='values')
        print(df.temperatuur.min())
        print(df.temperatuur.max())
