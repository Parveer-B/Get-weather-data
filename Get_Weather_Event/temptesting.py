import netCDF4 as nc

windspeeds = nc.Dataset('Get_Weather_Event/WeatherProjections/wp1/Stats.period_windspeed.nc')
print(windspeeds.variables.keys())
print(('   '))
print(windspeeds.dimensions.keys())
a = 6