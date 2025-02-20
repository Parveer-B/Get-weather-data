import netCDF4 as nc


class location_generation:
    def __init__(self, path, evtype):
        self.windspeeds = nc.Dataset(path + '/Stats.period_windspeed.nc')
        if evtype == 'ice':
            self.precipitation = nc.Dataset(path + '/Stats.period_precip.nc')
            self.snow_melt = nc.Dataset(path + '/Stats.period_snow_melt.nc')
            self.temp = nc.Dataset(path + '/Stats.period_Tair.nc')
            
