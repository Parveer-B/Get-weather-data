import netCDF4 as nc
import numpy as np
from random import randint
from Get_Weather_Event import get_bus_removal_data

test = get_bus_removal_data.Buses_Removed('ice', 'Get_Weather_Event/WeatherProjections/wp1')
test.get_windorice("wind", 0)