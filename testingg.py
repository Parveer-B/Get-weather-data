import get_bus_removal_data
import netCDF4 as nc

event_generator = get_bus_removal_data.Buses_Removed()


event_generator.get_event_data()

