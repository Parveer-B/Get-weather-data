import netCDF4 as nc
import numpy as np
from random import randint
windspeeds = nc.Dataset('Get_Weather_Event/WeatherProjections/wp1/Extraction_windspeed.nc')
print(windspeeds.variables.keys())
print(('   '))
print(windspeeds.dimensions.keys())

c = windspeeds.variables['windspeed'][:]
#np.squeeze(c) #c has a projections index first, which is of length 1
a = c[0][211][59][208]
b = 6