import netCDF4 as nc
from Get_Weather_Event import get_bus_removal_data
import numpy as np
import matplotlib.pyplot as plt

def get_boxes(lats, lons):
    #for this, assume all points are perfectly spaced in a rectangular pattern
    #this assumption is valid for CMIP data (where they are squares)
    dx = lons[1] - lons[0]
    dy = lats[1] - lats[0]
    lon_grid, lat_grid = np.meshgrid(lons, lats, indexing="xy")

    corners = np.array([
        [-dx/2, -dy/2],
        [dx/2, -dy/2],
        [dx/2, dy/2],
        [-dx/2, dy/2]
    ])
    boxes = np.stack((lon_grid[..., None], lat_grid[..., None]), axis=-1) + corners

    return boxes



class wind_ice_events:
    def __init__(self, path, evtype, substations, tls):
        self.windspeeds = nc.Dataset(path + '/Extraction_windspeed.nc')

        self.precipdata = nc.Dataset(path + '/Extraction_precip.nc')
        self.snow_meltdata = nc.Dataset(path + '/Extraction_snow_melt.nc')
        self.tempdata = nc.Dataset(path + '/Extraction_Tair.nc')

        self.pricip = self.precipdata.variables['precip'][:]
        self.pricip = self.pricip[0]
        self.snow_melt = self.snow_meltdata.variables['snow_melt'][:]
        self.snow_melt = self.snow_melt[0]
        self.temp = self.tempdata.variables['Tair'][:]
        self.temp = self.temp[0]
        
        self.lats = self.windspeeds.variables['Lat'][:]
        self.lons = self.windspeeds.variables['Lon'][:]
        self.times = self.windspeeds.variables['Time'][:] #may not be needed
        self.wind = self.windspeeds.variables['windspeed'][:]
        self.wind = self.wind[0]
        #self.wind's dimensions are now time, lat, lon
        #for wp1, we have 174 lats and 214 lons
        """
        boxes = get_boxes(self.lats, self.lons)
        self.filledboxes = np.array(
            [[{'box': box, 'buses': [], 'tls': []} for box in latline] for latline in boxes], 
            dtype=object
        )

        for substation in substations:
            P = substation['loc'] #location of substation
            lonidx = np.argmin(np.abs(self.lons - P[0])) #get closest lon and lat
            latidx = np.argmin(np.abs(self.lats - P[1]))
            self.filledboxes[latidx, lonidx]['buses'].extend(substation['buses'])
        for tl in tls:
            st = tl['from']
            end = tl['to']
            lonidxst = np.argmin(np.abs(self.lons - st[0]))
            latidxst = np.argmin(np.abs(self.lats - st[1]))
            lonidxend = np.argmin(np.abs(self.lons - end[0]))
            latidxend = np.argmin(np.abs(self.lats - end[1]))


            lonidxa, lonidxb = sorted([lonidxst, lonidxend])
            latidxa, latidxb = sorted([latidxst, latidxend])
            for i in range(latidxa, latidxb + 1):
                for j in range(lonidxa, lonidxb + 1):
                    line = get_bus_removal_data.gettlinbox([tl], boxes[i, j], (self.lons[1] - self.lons[0])*(self.lats[1] - self.lats[0]))
                    if line != []:
                        self.filledboxes[i, j]['tls'].append(line[0])
        """
    def run_through_events(self, evtype, index):
        #for now just run an event if the wind somewhere is above 55 m/s
        if evtype == "wind":
            for time in range(index, 500):
                curwinds = self.wind[time]
            maxwinds = np.amax(self.wind, axis = 0)
            plt.imshow(maxwinds, cmap = "bwr", origin = "lower")
            plt.colorbar(location = "bottom")
            plt.title("Max wind speed (m/s) via access 1-0 climate model using LOCA downscaling from 2025-2041")
            plt.show()
        inonelocation = self.wind[:, 140, 50]
        plt.plot(inonelocation)
        plt.show()
        return 1, 2



#NOTEE WITH MY METHODS, I WILL NEED TO CHECK FOR DUPLICATE LINES