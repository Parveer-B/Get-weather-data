#draw a random magnitude from our study area
#draw a random azimuth with that magnitude from our study area
#draw a random length (not from the same azimuth) with that magnitude from our study area

import pandas as pd
import random
import numpy as np
import math
import tornadowidthweibull

class get_tornado_data:
    def __init__(self):
        df = pd.read_csv('all tornadoes/1950-2023_torn.csv')
        df_tx_with_dup = df.loc[(df['st'] == 'TX') & (df['mag'] >= 2)]
        self.df_tx = df_tx_with_dup.drop_duplicates(subset=['time'])
        df_mag_5_with_dup = df.loc[(df['st'].isin(['TX', 'LA', 'OK', 'AR', 'NM'])) & (df['mag'] == 5)]
        self.df_mag_5 = df_mag_5_with_dup.drop_duplicates(subset=['time'])
        self.widthgen = tornadowidthweibull.widthGenerator()



    def gettornadostats(self):
        #get a random magnitude and azimuth

        randrow = (self.df_tx.sample(n=1)).iloc[0]
        magnitude = randrow['mag']
        if magnitude !=5:
            df_tx_mag = self.df_tx.loc[(self.df_tx['mag'] == magnitude)]
        else:
            df_tx_mag = self.df_mag_5
            randrow = df_tx_mag.sample(n=1)

        while True:
            azimuth = tornadowidthweibull.get_azimuth(randrow)
            if azimuth != 'false':
                break

        #grab rows of that specific magnitude to get length
        mag_randrow = (df_tx_mag.sample(n=1)).iloc[0]
        length = mag_randrow['len'] * 1.60934
        #get length in km (originally in miles)

        width = self.widthgen.get_width(df_tx_mag)
        #return length, width, azimuth
        return magnitude, length, width

df = pd.read_csv('all tornadoes/1950-2023_torn.csv')
df_mag_5 = df.loc[(df['st'].isin(['TX', 'LA', 'OK', 'AR', 'NM'])) & (df['mag'] == 5)]
f = 6