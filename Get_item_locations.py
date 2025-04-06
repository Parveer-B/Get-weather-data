import netCDF4 as nc
import numpy as np
from Get_Weather_Event import get_bus_removal_data

impbuses = np.array([130104, 210145, 210146, 111078, 110404])
test = get_bus_removal_data.Buses_Removed('tornado')
lines = test.transmissionlines
stations = test.substations
b = 6
for station in stations:
    intersect = np.intersect1d(impbuses, station["buses"])
    for i in intersect:
        print(i, round(station["loc"][0], 2), round(station["loc"][1], 2))




