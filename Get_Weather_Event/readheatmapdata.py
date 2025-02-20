import netCDF4 as nc
import numpy as np
from scipy.interpolate import griddata
from scipy.stats import gaussian_kde
from scipy.ndimage import zoom
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity
import random
import seaborn as sns
from matplotlib.collections import LineCollection
import matplotlib.colors as colors
print(' ')
# Open the NetCDF file

def averagee(arr):
    newarr = []
    for x in range(len(arr) - 1):
        newarr.append((arr[x] + arr[x+1])/2)
    return newarr

#create a class for this, initializing 3 times in the "parent" file for tornaodoes, wind and hail

# List variables and dimensions
#print(dataset.variables.keys())   # Variables in the file
#these are sigtorn, lon and lat
#these store the actual data, each variable is associated with one or more dimensions

#print(dataset.dimensions.keys())  # Dimensions in the file
#these are lons, lats, x and y
#Dimensions are the shape of the data and are the axes along which data is organized

# Access a variable (e.g., temperature)
class location_generation:
    def __init__(self, dataset, studylocation, evtype):
        lons = dataset.variables['lon'][:]
        lats = dataset.variables['lat'][:]

        frequency = dataset.variables[evtype][:]

        dataset.close()
        points = np.column_stack((lons.ravel(), lats.ravel())) #unravels the grids and converts them to a set of points
        values = frequency.ravel()
        #get a grid of locations to interpolate to
        grid_x, grid_y = np.mgrid[np.min(lons):np.max(lons):4000j, np.min(lats):np.max(lats):4000j]
        #get a grid of the tornado probabilities wrt grid x and y (4000x4000)
        grid_z = griddata(points, values, (grid_x, grid_y), method='cubic')

        minlonidx = np.abs(grid_x[:, 0] - studylocation[0]).argmin()
        maxlonidx = np.abs(grid_x[:, 0] - studylocation[1]).argmin()
        minlatidx = np.abs(grid_y[0, :] - studylocation[2]).argmin()
        maxlatidx = np.abs(grid_y[0, :] - studylocation[3]).argmin()



        #slice arrays, I slice them afterwards cause the initial set is a little wonky in shape
        self.sl_grid_x = grid_x[minlonidx:maxlonidx, minlatidx:maxlatidx]
        self.sl_grid_y = grid_y[minlonidx:maxlonidx, minlatidx:maxlatidx]
        self.sl_grid_z = grid_z[minlonidx:maxlonidx, minlatidx:maxlatidx]


        alllatitudes = self.sl_grid_y[0] #get all lat values
        normalizer = alllatitudes * np.cos(np.radians(alllatitudes))
        #WHY am I multiplying by alllatitudes here?? Doesn't seem like I should be :0
        self.norm_grid_z = self.sl_grid_z*normalizer #normalized grid to make it even along the sphere

        #get p(x) discrete probability "distribution" (not normalized yet)
        probx = np.sum(self.norm_grid_z, axis = 1) #sum all rows together
        self.cdfx = np.cumsum(probx/sum(probx)) #get discrete cdf of longitudes

    




    def get_touchdown_point(self):
        randx = random.random() #generate our x value
        closestx = np.abs(self.cdfx - randx).argmin() #find what x value it's closest to
        if randx>self.cdfx[closestx]: #overshoot
            percentageover = (randx-self.cdfx[closestx])/(self.cdfx[closestx+1] - self.cdfx[closestx])
            longitude = self.sl_grid_x[closestx, 0] + percentageover*(self.sl_grid_x[closestx+1, 0] - self.sl_grid_x[closestx, 0])
            #interpolate to get longitude
        else:
            if closestx == 0: #cdf means we have some probability below the min longitude
                percentageunder = (self.cdfx[closestx] - randx)/(self.cdfx[closestx] - 0)
                longitude = self.sl_grid_x[closestx, 0] - percentageunder*(self.sl_grid_x[closestx+1, 0] - self.sl_grid_x[closestx, 0])
                #equal grid spacing means this is equivalent anyways
            else:
                percentageunder = (randx - self.cdfx[closestx])/(self.cdfx[closestx] - self.cdfx[closestx-1])
                longitude = self.sl_grid_x[closestx, 0] - percentageunder*(self.sl_grid_x[closestx, 0] - self.sl_grid_x[closestx-1, 0])

        pygivenx = self.norm_grid_z[closestx, :]
        cdfy = np.cumsum(pygivenx/sum(pygivenx)) #might be able to just get this beforehand

        randy = random.random()
        closesty = np.abs(cdfy - randy).argmin() #find what x value it's closest to

        if randy>cdfy[closesty]: #overshoot
            percentageover = (randy-cdfy[closesty])/(cdfy[closesty+1] - cdfy[closesty])
            latitude = self.sl_grid_y[0, closesty] + percentageover*(self.sl_grid_y[0, closesty+1] - self.sl_grid_y[0, closesty])
            #interpolate to get latitude
        else:
            if closesty == 0: #cdf means we have some probability below the min latitude
                percentageunder = (cdfy[closesty] - randy)/(cdfy[closesty] - 0)
                latitude = self.sl_grid_y[0, closesty] - percentageunder*(self.sl_grid_y[0, closesty+1] - self.sl_grid_y[0, closesty])
                #equal grid spacing means this is equivalent anyways
            else:
                percentageunder = (randy - cdfy[closesty])/(cdfy[closesty] - cdfy[closesty-1])
                latitude = self.sl_grid_y[0, closesty] - percentageunder*(self.sl_grid_y[0, closesty] - self.sl_grid_y[0, closesty-1])
        return longitude, latitude

    def get_heatmap_visualizations(self, longitudes, latitudes):
        new_norm_grid_z =  self.norm_grid_z/np.max(self.norm_grid_z) #normalize for heatmaps
        allpoints = np.vstack([longitudes, latitudes])
        kernel = gaussian_kde(allpoints)
        numpoints = 200j
        mchmgrid_x, mchmgrid_y = np.mgrid[self.sl_grid_x[0, 0]:self.sl_grid_x[-1, 0]: numpoints, self.sl_grid_y[0, 0]:self.sl_grid_y[0, -1]:numpoints]

        positions = np.vstack([mchmgrid_x.ravel(), mchmgrid_y.ravel()])
        montecarloheatmap = np.reshape(kernel(positions).T, mchmgrid_x.shape)

        rescaled_montecarloheatmap = zoom(montecarloheatmap, (self.sl_grid_x.shape[0]/mchmgrid_x.shape[0], self.sl_grid_x.shape[1]/mchmgrid_x.shape[1]), order=1)
        rescaled_montecarloheatmap = rescaled_montecarloheatmap/np.max(rescaled_montecarloheatmap)



        # Plot the result
        plt.subplot(2, 2, 1)
        plt.imshow(new_norm_grid_z.T, extent=(self.sl_grid_x[0, 0], self.sl_grid_x[-1, 0], self.sl_grid_y[0, 0], self.sl_grid_y[0, -1]), origin='lower', cmap="inferno")
        #plt.plot(longitudes, latitudes, 'ro', markersize = 0.5, alpha = 0.15)  # mark the data points
        plt.colorbar()
        plt.title('Linear Interpolation using griddata')


        plt.subplot(2, 2, 2)
        plt.imshow(rescaled_montecarloheatmap.T, extent=(self.sl_grid_x[0, 0], self.sl_grid_x[-1, 0], self.sl_grid_y[0, 0], self.sl_grid_y[0, -1]), origin='lower', cmap="inferno")
        #plt.plot(longitudes, latitudes, 'ro', markersize = 0.5, alpha = 0.15)  # mark the data points
        plt.colorbar()

        plt.subplot(2, 2, 3)
        difference = new_norm_grid_z/rescaled_montecarloheatmap
        plt.imshow(difference.T, extent=(self.sl_grid_x[0, 0], self.sl_grid_x[-1, 0], self.sl_grid_y[0, 0], self.sl_grid_y[0, -1]), origin='lower', cmap="coolwarm", norm = colors.LogNorm(vmin = 10e-2, vmax = 10, clip = True))
        #plt.plot(longitudes, latitudes, 'ro', markersize = 0.5, alpha = 0.15)  # mark the data points
        plt.colorbar()
        plt.show()

"""
heatmap_res = 75
xedges_hist = np.linspace(sl_grid_x[0, 0], sl_grid_x[-1, 0], heatmap_res)
yedges_hist = np.linspace(sl_grid_y[0, 0], sl_grid_y[0, -1], heatmap_res)
montecarlohist, _ , _  = np.histogram2d(longitudes, latitudes, bins=[xedges_hist, yedges_hist])
histpoints = [[x0, y0] for x0 in averagee(xedges_hist) for y0 in averagee(yedges_hist)]
montecarloheatmap = griddata(histpoints, montecarlohist.ravel(), (sl_grid_x, sl_grid_y), method='linear')
# very ugly and granular 
"""