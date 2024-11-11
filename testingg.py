import get_bus_removal_data
import netCDF4 as nc
import math

from collections import Counter
event_generator = get_bus_removal_data.Buses_Removed()


num_buses_hit = []
for x in range(1):
    hitbuses = event_generator.get_event_data(['tornado', -103.548, 29.4217, 3, 20, 4, math.pi/8])
    #if event inputted it's
    #'tornado', slon, slat, magnitude, length, width, azimuth
    #azimuth in radians, length and width in km
    num_buses_hit.append(len(hitbuses[0]))
    if x%200 == 0:
        print(x)
print(Counter(num_buses_hit))


