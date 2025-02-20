import netCDF4 as nc
from Get_Weather_Event import get_bus_removal_data
import numpy as np

def get_boxes(lats, lons):
    #for this, assume all points are perfectly spaced in a rectangular pattern
    #this assumption is valid for CMIP data (where they are squares)
    dx = lons[1] - lons[0]
    dy = lats[1] - lons[0]
    boxes = np.array([])
    for y in lats:
        for x in lons:
            start = np.array([x, y])
            boxes.append(np.vstack((start+[dx/2, dy/2], start+[-dx/2, dy/2],start-[dx/2, -dy/2], start+[-dx/2, -dy/2])))

    #The order of boxes in this array should be the same as they are presented in 
    return boxes



class wind_ice_events:
    def __init__(self, path, evtype, substations, tls):
        self.windspeeds = nc.Dataset(path + '/Stats.period_windspeed.nc')
        if evtype == 'ice':
            self.precipdata = nc.Dataset(path + '/Stats.period_precip.nc')
            self.snow_meltdata = nc.Dataset(path + '/Stats.period_snow_melt.nc')
            self.tempdata = nc.Dataset(path + '/Stats.period_Tair.nc')

            self.pricip = self.windspeeds.variables['precip'][:]
            self.pricip = self.pricip[0]
            self.snow_melt = self.windspeeds.variables['snow_melt'][:]
            self.snow_melt = self.snow_melt[0]
            self.temp = self.windspeeds.variables['Tair'][:]
            self.temp = self.temp[0]
        
        self.lats = self.windspeeds.variables['Lats'][:]
        self.lons = self.windspeeds.variables['Lons'][:]
        self.times = self.windspeeds.variables['Time'][:] #may not be needed
        self.wind = self.windspeeds.variables['windspeed'][:]
        self.wind = self.wind[0]
        #self.wind's dimensions are now time, lat, lon

        boxes = get_boxes(self.lats, self.lons)
        self.filledboxes = []
        for box in boxes:
            busesinbox, __ = get_bus_removal_data.getbusesinbox(substations, box)
            tlsinbox = get_bus_removal_data.gettlinbox(tls, box)
            self.filledboxes.append({'box' : box, 'buses' : busesinbox, 'loc': tlsinbox})

        #generate box with buses here

#NOTEE WITH MY METHODS, I WILL NEED TO CHECK FOR DUPLICATE LINES