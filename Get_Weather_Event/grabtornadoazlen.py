#draw a random magnitude from our study area
#draw a random azimuth with that magnitude from our study area
#draw a random length (not from the same azimuth) with that magnitude from our study area

import pandas as pd
import random
import numpy as np
import math
from Get_Weather_Event import tornadowidthweibull

def get_distance(dblon, dblat, lon, lat):
    return math.sqrt((dblon-lon)**2 + (dblat-lat)**2)

class get_tornado_data:
    def __init__(self):
        df = pd.read_csv('Get_Weather_Event/all tornadoes/1950-2023_torn.csv')
        df_tx_with_dup = df.loc[(df['st'] == 'TX') & (df['mag'] >= 2)]
        self.df_tx = df_tx_with_dup.drop_duplicates(subset=['time', 'date'])
        df_mag_5_with_dup = df.loc[(df['st'].isin(['TX', 'LA', 'OK', 'AR', 'NM'])) & (df['mag'] == 5)]
        self.df_mag_5 = df_mag_5_with_dup.drop_duplicates(subset=['time', 'date'])
        self.widthgen = tornadowidthweibull.widthGenerator()



    def gettornadostats(self, slon, slat):
        #get a random magnitude and azimuth
        distances = self.df_tx.apply(lambda row: get_distance(row['slon'], row['slat'], slon, slat), axis=1)
        n = 50 #closest tornadoes to grab a magnitude from
        lowest_dis_rows = self.df_tx.loc[distances.nsmallest(n).index]
        row = (lowest_dis_rows.sample(n=1)).iloc[0]
        magnitude = row['mag']
        if magnitude !=5:
            df_tx_mag = self.df_tx.loc[(self.df_tx['mag'] == magnitude)]
        else:
            df_tx_mag = self.df_mag_5
            
        randrow = (df_tx_mag.sample(n=1)).iloc[0]

        while True:
            azimuth = tornadowidthweibull.get_azimuth(randrow)
            if azimuth != 'false':
                break
            randrow = (df_tx_mag.sample(n=1)).iloc[0]

        #grab row of that specific magnitude to get length
        mag_randrow = (df_tx_mag.sample(n=1)).iloc[0]
        length = mag_randrow['len'] * 1.60934
        while length == 0:
            mag_randrow = (df_tx_mag.sample(n=1)).iloc[0]
            length = mag_randrow['len'] * 1.60934
        #get length in km (originally in miles)

        width = self.widthgen.get_width(df_tx_mag, magnitude)
        #return length, width, azimuth
        return magnitude, length, width, azimuth

df = pd.read_csv('Get_Weather_Event/all tornadoes/1950-2023_torn.csv')
df_mag_5 = df.loc[(df['st'].isin(['TX', 'LA', 'OK', 'AR', 'NM'])) & (df['mag'] == 5)]
f = 6