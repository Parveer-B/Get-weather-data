import readheatmapdata
import grabtornadoazlen
import netCDF4 as nc


class Buses_Removed:
    def __init__(self):
        #studylocation = [-110, -79, 25, 47.6] #minx, maxx, miny, maxy, whole mainland
        studylocation = [-108, -93, 25, 37]
        self.tornadoposgen = readheatmapdata.location_generation(nc.Dataset('Heatmaps/sigtornEF2orhigher.nc'), studylocation)
        self.hailposgen = readheatmapdata.location_generation(nc.Dataset('Heatmaps/sighailover2inches.nc'), studylocation)
        self.windposgen = readheatmapdata.location_generation(nc.Dataset('Heatmaps/allsigwindover64knots.nc'), studylocation)
        #note, when filtering wind and hail data, make it consistent with the heatmaps

        self.tornadodatagen = grabtornadoazlen.get_tornado_data()
        