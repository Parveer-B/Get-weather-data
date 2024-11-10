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

    return np.vstack((start+dside, start-dside,start-dside+dfor, start+dside+dfor))

def getbusesinbox(substations, box):
    #Box has corners ABCD in the order of the box array
    AD = box[3] - box[0]
    AB = box[1] - box[0]
    ADsq = np.dot(AD, AD)
    ABsq = np.dot(AB, AB)
    hitbuses = []
    for substation in substations:
        P = substation['loc'] #location of substation
        AP = P - box[0]
        val1 = np.dot(AP, AB)/ABsq
        val2 = np.dot(AP, AD)/ADsq

        if 0<=val1<=1 and 0<=val2<=1:
            hitbuses.extend(substation['buses'])
    return hitbuses

def gettlinbox(lines, box):
    AD = box[3] - box[0]
    AB = box[1] - box[0]
    ADsq = np.dot(AD, AD)
    ABsq = np.dot(AB, AB)
    boxlines = []
    for x in range(4):
        #In Ax+By+C form, put A,B,C in the array as indexes 0,1,2
        #The array has lines AB, BC, CD, DA
        A = box[(x+1)%4][1] - box[x][1]
        B = box[x][0] - box[(x+1)%4][0]
        C = A*box[x][0] + B*box[x][1]
        boxlines.append([A, B, C])
    linesinbox = []
    lenlinesinbox = []
    for tlinedict in lines:
        st = tlinedict['from']
        end = tlinedict['to']
        tline = [end[1] - st[1], st[0] - end[0], end[1]*st[0] - end[0]*st[1]]

        #now using https://math.stackexchange.com/questions/424723/determinant-in-line-line-intersection, with denominator being D
        connections = []
        for boxline, i in enumerate(boxlines):
            #tline is index 1 and boxline is index 2 in the post above
            D = tline[0]*boxline[1] -boxline[0]*tline[1]
            if D==0:
                pass
            x_int = (tline[2]*boxline[1] - boxline[2]*tline[1])/D
            if (box[i][0] < x_int < box[(i+1)%4][0]) or (box[i][0] > x_int > box[(i+1)%4][0]):
                y_int = (tline[2] - tline[0]*x_int)/tline[1]
                connections.append([x_int, y_int])
                if len(connections) == 2:
                    break #shouldn't need this, but might have a corner edgecase
        if len(connections) == 2:
            linesinbox.append(tlinedict)
            dlat = connections[1][1] - connections[0][1]
            dlon = connections[1][0] - connections[0][0]
            dy = dlat*110.57 #y change in km
            dx = dlon*111.32.np.cos(np.deg2rad(connections[0][1])) #just use the first connection y value as the latitude
            lenlinesinbox.append(math.sqrt(dy**2 + dx**2))
        elif len(connections) == 1:
            #one end of TL might be in the box while to other isn't
            AP = st - box[0]
            val1 = np.dot(AP, AB)/ABsq
            val2 = np.dot(AP, AD)/ADsq

            AP = end - box[0]
            val3 = np.dot(AP, AB)/ABsq
            val4 = np.dot(AP, AD)/ADsq

            if 0<=val1<=1 and 0<=val2<=1:
                linesinbox.append(tlinedict)
                dlat = st[1] - connections[0][1]
                dlon = st[0] - connections[0][0]
                dy = dlat*110.57 #y change in km
                dx = dlon*111.32.np.cos(np.deg2rad(connections[0][1]))
                lenlinesinbox.append(math.sqrt(dy**2 + dx**2))
            elif 0<=val3<=1 and 0<=val4<=1:
                linesinbox.append(tlinedict)
                dlat = end[1] - connections[0][1]
                dlon = end[0] - connections[0][0]
                dy = dlat*110.57 #y change in km
                dx = dlon*111.32.np.cos(np.deg2rad(connections[0][1]))
                lenlinesinbox.append(math.sqrt(dy**2 + dx**2))
        else: #len(connections) = 0, entire TL can be in the box
            AP = st - box[0]
            val1 = np.dot(AP, AB)/ABsq
            val2 = np.dot(AP, AD)/ADsq

            AP = end - box[0]
            val3 = np.dot(AP, AB)/ABsq
            val4 = np.dot(AP, AD)/ADsq
            if 0<=val1<=1 and 0<=val2<=1 and 0<=val3<=1 and 0<=val4<=1:
                #technically if this is true for one end of the TL it has to be true for the other but whatever
                linesinbox.append(tlinedict)
                dlat = st[1] - end[1]
                dlon = st[0] - end[1]
                dy = dlat*110.57 #y change in km
                dx = dlon*111.32.np.cos(np.deg2rad(st[1]))
                lenlinesinbox.append(math.sqrt(dy**2 + dx**2))


    return linesinbox, lenlinesinbox










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
        magnitude, length, width, azimuth = self.tornadodatagen.gettornadostats(slon, slat)
        #length and width are in kilometres, azimuth is in radians
        eventbox = getbox(slon, slat, length, width, azimuth)
        return eventbox, magnitude
    
    def generate_wind_hail(self, event):
        #this just returns the box
        return 5, 6


    def get_event_data(self):
        
        eventtype = self.eventtypes[np.searchsorted(np.cumsum(self.probwindhailtorn), random.random())]
        if eventtype == 'tornado':
            eventbox, severity = self.generate_tornado()
        else:
            eventbox, severity, __, __ = self.generate_windhail(eventtype)

        busesinbox = getbusesinbox(self.substations, eventbox)
        tlinbox, lentlinbox = gettlinbox(self.transmissionlines, eventbox)
        
        return busesinbox, tlinbox, lentlinbox, busesremoved, tlremoved, eventbox, weathertype, severity

        
    







