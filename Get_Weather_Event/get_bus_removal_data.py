from Get_Weather_Event import readheatmapdata
from Get_Weather_Event import grabtornadoazlen
from Get_Weather_Event import gettlandsubcoords
from Get_Weather_Event import genwindhail
import netCDF4 as nc
import numpy as np
from shapely.geometry import Polygon
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

def pointinquadral(point, box):
    areaofbox = 0
    for x in range(len(box)):
        areaofbox+=box[x][1]*(box[(x-1)%len(box)][0]-box[(x+1)%len(box)][0])
    areaofbox = abs(areaofbox)/2

    areatriangles = 0
    for x in range(len(box)):
        A = box[x]
        B = box[(x+1)%len(box)]
        areatriangles += Polygon(np.vstack((A, B, point))).area
    if abs(areatriangles - areaofbox) <= 1e-5:
        return True
    else:
        return False


def getbusesinbox(substations, box):
    #Box has corners ABCD in the order of the box array
    hitbuses = []
    hitsubstations = []
    for substation in substations:
        P = substation['loc'] #location of substation
        if pointinquadral(P, box):
            hitbuses.extend(substation['buses'])
            hitsubstations.append(substation['subid'])
    return hitbuses, hitsubstations

def gettlinbox(lines, box):
    boxlines = []
    for x in range(4):
        #In Ax+By=C form, put A,B,C in the array as indexes 0,1,2
        #The array has lines AB, BC, CD, DA
        A = box[(x+1)%4][1] - box[x][1]
        B = box[x][0] - box[(x+1)%4][0]
        C = A*box[x][0] + B*box[x][1]
        boxlines.append([A, B, C])
    linesinbox = []
    for tlinedict in lines:
        st = tlinedict['from']
        end = tlinedict['to']
        tline = [end[1] - st[1], st[0] - end[0], end[1]*st[0] - end[0]*st[1]] #equation for a line in [A,B,C] array

        #now using https://math.stackexchange.com/questions/424723/determinant-in-line-line-intersection, with denominator being D
        connections = []
        for i, boxline in enumerate(boxlines):
            #tline is index 1 and boxline is index 2 in the post above
            D = tline[0]*boxline[1] -boxline[0]*tline[1]
            if D==0:
                pass
            x_int = (tline[2]*boxline[1] - boxline[2]*tline[1])/D
            if (box[i][0] < x_int < box[(i+1)%4][0]) or (box[i][0] > x_int > box[(i+1)%4][0]):
                if (st[0] < x_int < end[0]) or (st[0] > x_int > end[0]):
                    y_int = (tline[2] - tline[0]*x_int)/tline[1]
                    connections.append([x_int, y_int])
                    if len(connections) == 2:
                        break #shouldn't need this, but might have a corner edgecase
        if len(connections) == 2:
            linesinbox.append(tlinedict)
            dlat = connections[1][1] - connections[0][1]
            dlon = connections[1][0] - connections[0][0]
            dy = dlat*110.57 #y change in km
            dx = dlon*111.32*np.cos(np.deg2rad(connections[0][1])) #just use the first connection y value as the latitude
            linesinbox[-1]['leninbox'] = math.sqrt(dy**2 + dx**2)
            #not append? just add to a dictionary?
        elif len(connections) == 1:
            #one end of TL might be in the box while to other isn't

            if pointinquadral(st, box): #one end in box
                linesinbox.append(tlinedict)
                dlat = st[1] - connections[0][1]
                dlon = st[0] - connections[0][0]
                dy = dlat*110.57 #y change in km
                dx = dlon*111.32*np.cos(np.deg2rad(connections[0][1]))
                linesinbox[-1]['leninbox'] = math.sqrt(dy**2 + dx**2)
            elif pointinquadral(end, box): #other end in box
                linesinbox.append(tlinedict)
                dlat = end[1] - connections[0][1]
                dlon = end[0] - connections[0][0]
                dy = dlat*110.57 #y change in km
                dx = dlon*111.32*np.cos(np.deg2rad(connections[0][1]))
                linesinbox[-1]['leninbox'] = math.sqrt(dy**2 + dx**2)
        else: #len(connections) = 0, entire TL can be in the box
            if pointinquadral(st, box) and pointinquadral(end, box):
                #technically if this is true for one end of the TL it has to be true for the other but whatever
                linesinbox.append(tlinedict)
                dlat = st[1] - end[1]
                dlon = st[0] - end[0]
                dy = dlat*110.57 #y change in km
                dx = dlon*111.32*np.cos(np.deg2rad(st[1]))
                linesinbox[-1]['leninbox'] = math.sqrt(dy**2 + dx**2)


    return linesinbox



class Buses_Removed:
    def __init__(self, eventtype, path = None):
        self.substations = gettlandsubcoords.getsubcoords()
        self.transmissionlines = gettlandsubcoords.gettlcoords()
        #studylocation = [-110, -79, 25, 47.6] #minx, maxx, miny, maxy, whole mainland
        if eventtype == 'tornado':
            studylocation = [-108, -93, 25, 37]
            self.tornadoposgen = readheatmapdata.location_generation(nc.Dataset('Get_Weather_Event/Heatmaps/sigtornEF2orhigher.nc'), studylocation, 'sigtorn')
            self.tornadodatagen = grabtornadoazlen.get_tornado_data()
        #self.hailposgen = readheatmapdata.location_generation(nc.Dataset('Get_Weather_Event/Heatmaps/sighailover2inches.nc'), studylocation, 'sighail')
        #self.windposgen = readheatmapdata.location_generation(nc.Dataset('Get_Weather_Event/Heatmaps/allsigwindover64knots.nc'), studylocation, 'allsigwind')
        #note, when filtering wind and hail data, make it consistent with the heatmaps
        #self.probwindhailtorn = [0, 0, 1] #MODIFY!!
        #self.eventtypes = {0 : 'wind', 1: 'hail', 2 : 'tornado'}

        if eventtype == 'wind' or eventtype == 'ice':
            self.stormboxes = genwindhail(path, eventtype)
        


    def generate_tornado(self, givenevent):
        if givenevent:
            slon, slat, magnitude, length, width, azimuth = givenevent[1:]
        else:
            slon, slat = self.tornadoposgen.get_touchdown_point()
            magnitude, length, width, azimuth = self.tornadodatagen.gettornadostats(slon, slat)
        #length and width are in kilometres, azimuth is in radians
        eventbox = getbox(slon, slat, length, width, azimuth)
        return eventbox, magnitude
    


    def get_event_data(self, givenevent = False):
        #I can also add an event here if I want to test MATLAB
        givenevent = ['tornado', -103.548, 29.4217, 3, 20, 4, math.pi/8]
        if givenevent:
            eventtype = givenevent[0]
        else:
            eventtype = self.eventtypes[np.searchsorted(np.cumsum(self.probwindhailtorn), random.random())]
        if eventtype == 'tornado':
            eventbox, severity = self.generate_tornado(givenevent)
        else:
            eventbox, severity, __, __ = self.generate_wind_hail(eventtype, givenevent)

        busesinbox, substationsinbox = getbusesinbox(self.substations, eventbox)
        tlinbox = gettlinbox(self.transmissionlines, eventbox)

        #just put these in for now, will modify when civ model added
        busesremoved = busesinbox
        tlremoved = tlinbox

        
        return busesinbox, tlinbox, busesremoved, tlremoved, eventbox, eventtype, severity, substationsinbox

        
    







