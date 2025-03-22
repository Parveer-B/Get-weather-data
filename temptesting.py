import netCDF4 as nc
import numpy as np
from random import randint
from Get_Weather_Event import get_bus_removal_data

test = get_bus_removal_data.Buses_Removed('tornado')
lines = test.transmissionlines
stations = test.substations
box = [[-96.4442687455020, 30.0381457302045],
[-96.4450537371116, 30.0356470679912],
[-95.0550470570980, 29.7039174738072],
[-95.0542620654884, 29.7064161360206]]

b = get_bus_removal_data.gettlinbox(lines, box, areaofbox = 0)
a = 6