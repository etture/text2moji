import os

import pandas as pd

if not os.path.exists('Data'):
    os.makedirs('Data')

if not os.path.exists('Logs'):
    os.makedirs('Logs')

emoji_codes = pd.read_csv('../emoji_unicode.csv', header=None, names =['code', 'zipped'])
for z in emoji_codes.zipped:
    if not os.path.exists('Data/{}'.format(z)):
        os.makedirs('Data/{}'.format(z))
    if not os.path.exists('Logs/{}'.format(z)):
        os.makedirs('Logs/{}'.format(z))