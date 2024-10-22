#draw a random magnitude from our study area
#draw a random azimuth with that magnitude from our study area
#draw a random length (not from the same azimuth) with that magnitude from our study area

import pandas as pd
import random
import numpy as np
import math

df = pd.read_csv('all tornadoes/1950-2023_torn.csv')

#filter by my study region state
global df_tx
df_tx = df.loc[(df['st'] == 'TX') & (df['mag'] >= 2)]


def gettornadostats():
    


    #get a random magnitude and azimuth

    randrow = df_tx.sample(n=1)
    magnitude = randrow['mag'].item()
    df_tx_mag = df_tx.loc[(df_tx['mag'] == magnitude)]


    start_lon = randrow['slon'].item()
    start_lat = randrow['slat'].item()
    end_lon = randrow['elon'].item()
    end_lat = randrow['elat'].item()

    deltalon = end_lon - start_lon
    deltalat = end_lat - start_lat


    while deltalon == deltalat == 0:
        #if no azimuth just get another azimuth
        mag_randrow = df_tx_mag.sample(n=1)
        start_lon = mag_randrow['slon'].item()
        start_lat = mag_randrow['slat'].item()
        end_lon = mag_randrow['elon'].item()
        end_lat = mag_randrow['elat'].item()
        deltalon = end_lon - start_lon
        deltalat = end_lat - start_lat

    if deltalon != 0:
        azimuth = math.atan(deltalat/deltalon) #this is our azimuth
    else:
        azimuth = (math.pi)/2
    #May want to account for curvature of the earth, this is kinda sus

    if deltalon < 0: #above only gives angles from -pi/2 to pi/2
        azimuth += math.pi

    #grab rows of that specific magnitude to get length
    mag_randrow = df_tx_mag.sample(n=1)
    length = mag_randrow['len'].item() * 1.60934
    #get length in km (originally in miles)

    #width = weibullwidthget(magnitude)
    #return length, width, azimuth
    return magnitude, length

a = [0, 0, 0, 0, 0, 0]

for i in range(5000):
    mag, len = gettornadostats()
    print(len)
print(a)