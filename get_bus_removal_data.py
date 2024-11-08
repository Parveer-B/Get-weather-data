import readheatmapdata
import grabtornadoazlen
import gettlandsubcoords
import netCDF4 as nc
import numpy as np
import random
import math

def getbox(slon, slat, len, wid, az):
    start = np.array([slon, slat])
    forw = np.array([math.cos(az), math.sin(az)]) #forward unit vector
    side = np.random.randn(2)
    side -= side.dot(forw) * forw
    side /= np.linalg.norm(side) #perpindicular unit vector to forw
    dlonside = (wid*side[0])/(2*(111.32*np.cos(np.deg2rad(slat)))) #kilometres to delta degree longitude
    #divide the above by two since we want to go from the centre point to either side of our starting positions
    dlonfor = (len*forw[0])/(111.32*np.cos(np.deg2rad(slat)))

    dlatside = (wid*side[1])/(2*110.57)
    dlatfor =  (len*forw[1])/110.57

    dside = np.array([dlonside, dlatside])
    dfor = np.array([dlonfor, dlatfor])

    return np.vstack((start+dside, start-dside, start+dside+dfor, start-dside+dfor))


class Buses_Removed:
    def __init__(self):
        #studylocation = [-110, -79, 25, 47.6] #minx, maxx, miny, maxy, whole mainland
        studylocation = [-108, -93, 25, 37]
        self.tornadoposgen = readheatmapdata.location_generation(nc.Dataset('Heatmaps/sigtornEF2orhigher.nc'), studylocation, 'sigtorn')
        self.hailposgen = readheatmapdata.location_generation(nc.Dataset('Heatmaps/sighailover2inches.nc'), studylocation, 'sighail')
        self.windposgen = readheatmapdata.location_generation(nc.Dataset('Heatmaps/allsigwindover64knots.nc'), studylocation, 'allsigwind')
        #note, when filtering wind and hail data, make it consistent with the heatmaps

        self.tornadodatagen = grabtornadoazlen.get_tornado_data()
        #add these (with the same class for them) for hail and wind


        self.probwindhailtorn = [0, 0, 1] #MODIFY!!
        #you know what, calculate this in a function above (not in the class). Start at 1998

        self.eventtypes = {0 : 'wind', 1: 'hail', 2 : 'tornado'}

        self.substations = gettlandsubcoords.getsubcoords()

        self.transmissionlines = gettlandsubcoords.gettlcoords()

    def generate_tornado(self):
        slon, slat = self.tornadoposgen.get_touchdown_point()
        print(slon, slat)
        magnitude, length, width, azimuth = self.tornadodatagen.gettornadostats(slon, slat)
        #length and width are in kilometres, azimuth is in radians
        eventbox = getbox(slon, slat, length, width, azimuth)
        return 3, 7
    
    def generate_wind_hail(self, event):
        #this just returns the box
        return 5, 6


    def get_event_data(self):
        
        eventtype = self.eventtypes[np.searchsorted(np.cumsum(self.probwindhailtorn), random.random())]
        if eventtype == 'tornado':
            eventbox, severity = self.generate_tornado()
        else:
            eventbox, severity = self.generate_windhail(eventtype)
        print('nothing broke too badly ig')
    







