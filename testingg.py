import get_bus_removal_data
import netCDF4 as nc

from collections import Counter
event_generator = get_bus_removal_data.Buses_Removed()


num_buses_hit = []
for x in range(6000):
    hitbuses = event_generator.get_event_data()
    num_buses_hit.append(len(hitbuses))
print(Counter(num_buses_hit))


