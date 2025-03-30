import matplotlib.pyplot as plt
from Get_Weather_Event import readheatmapdata
import netCDF4 as nc

studylocation = [-110, -79, 25, 47.6]

# Create a mosaic where each plot is two entries wide.  Dots represent spaces.
tornadoposgen = readheatmapdata.location_generation(nc.Dataset('Get_Weather_Event/Heatmaps/sigtornEF2orhigher.nc'), studylocation, 'sigtorn')

lon = []
lat = []
for x in range(100000):
    if x%50 == 0:
        print(x)
    slon, slat = tornadoposgen.get_touchdown_point()
    lon.append(slon)
    lat.append(slat)

tornadoposgen.get_heatmap_visualizations(lon, lat)
