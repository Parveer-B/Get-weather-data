import netCDF4 as nc
import numpy as np
from random import randint
from Get_Weather_Event import get_bus_removal_data

test = get_bus_removal_data.Buses_Removed('tornado')
lines = test.transmissionlines
stations = test.substations
box = [[-96.8974473203806, 32.5441868221133],
[-96.8975435156131, 32.5443363879726],
[-96.8945328659410, 32.5457310970455],
[-96.8944366707084, 32.5455815311862]]

b = get_bus_removal_data.getbusesinbox(stations, box, areaofbox = 0)
a = 6