import pandas as pd
import math
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

def get_azimuth(row):
    start_lon = row['slon']
    start_lat = row['slat']
    end_lon = row['elon']
    end_lat = row['elat']

    deltalon = end_lon - start_lon
    deltalat = end_lat - start_lat

    if deltalon == deltalat == 0:
        return 'false' #string to not conflate with 0 which is legit

    if deltalon != 0:
        azimuth = math.atan(deltalat/deltalon) #this is our azimuth
    else:
        if deltalat>0:
            azimuth = (math.pi)/2
        else:
            azimuth = 3*(math.pi)/2
    #May want to account for curvature of the earth, but should be ok

    if deltalon < 0: #above only gives angles from -pi/2 to pi/2
        azimuth += math.pi
    return azimuth

class widthGenerator:
    def __init__(self):
        self.distribution_params = {} #dictionary stored as c, loc, scale in a list
    
    def get_weibull_fit(self, data, magnitude):
        widths = data['wid'].to_list()
        c, loc, scale = stats.weibull_min.fit(widths)
        self.distribution_params[magnitude] = [c, loc, scale]


    def get_width(self, sld_df, magnitude, num = 1, genwidths = []):
        if magnitude not in self.distribution_params.keys():
            self.get_weibull_fit(sld_df, magnitude)
        parameters = self.distribution_params[magnitude]
        width_imperial = stats.weibull_min.rvs(parameters[0], loc=parameters[1], scale=parameters[2])
        #me just testing stuff is below, page 17 of october notes
        if num%100 == 0:
            stats.probplot(genwidths, dist='weibull_min', sparams=(parameters[0], parameters[1], parameters[2]), fit=True, rvalue=True, plot=plt)
            plt.title('Magnitude '+ str(5) +  ' data Weibull q-q plot with generated data')
            plt.show()
        return width_imperial/1094 #convert to normal people units


def data_testing(variable, limdata, largerdata):
    if variable == 'azimuth':
        kappalar, loclar, scalelar = stats.vonmises.fit(largerdata, fscale = 1)
        kappalim, loclim, scalelim = stats.vonmises.fit(limdata, fscale = 1)
        x = np.linspace(0, 2*math.pi, 1000)
        limpdf = stats.vonmises.pdf(x, kappalar, loclar, scalelar)
        larpdf = stats.vonmises.pdf(x, kappalim, loclim, scalelim)
        plt.subplot(projection='polar')

    else:
        shapelar, loclar, scalelar = stats.weibull_min.fit(largerdata)
        shapelim, loclim, scalelim = stats.weibull_min.fit(limdata)
        maxx = max(largerdata)      
        x = np.linspace(0.1, maxx, 1000)
        limpdf = stats.weibull_min.pdf(x, shapelim, loclim, scalelim)
        larpdf = stats.weibull_min.pdf(x, shapelar, loclar, scalelar)

        
    plt.title('Magnitude 4 ' + variable +  ' data fitted to a Weibull')
    
    plt.plot(x, limpdf, label = 'just texas')
    plt.plot(x, larpdf, label = 'texas and surrounding')
    plt.legend()
    plt.xlabel(variable + ' value')
    plt.ylabel('pdf value')
    plt.show()

    


def test_weibull(mag, widths):
    c, loc, scale = stats.weibull_min.fit(widths) #for some reason this requires a shape
    fig = plt.figure()
    ax = fig.add_subplot(111)
    stats.probplot(widths, dist='weibull_min', sparams=(c, loc, scale), plot=ax)
    ax.axline((0, 0), slope=1)
    plt.title('Magnitude '+ str(mag) +  ' data Weibull q-q plot')
    plt.show()
    


    
df = pd.read_csv('all tornadoes/1950-2023_torn.csv') #needed for testing below
df = df.drop_duplicates(subset=['time', 'date'])

#below is just testing get_width, page 17 of october notes
""" generated = []
for i in range(1000):
    generated.append(get_width(df.loc[(df['st'].isin(['TX', 'LA', 'OK', 'AR', 'NM'])) & (df['mag'] == 5)], i, generated)) """



#below is plots for in and out of state variables, page 11-13 of october notes
""" 

justtx = df.loc[(df['st'] == 'TX') & (df['mag'] == 4)]
inc_other_states = df.loc[(df['st'].isin(['TX', 'LA', 'OK', 'AR', 'NM'])) & (df['mag'] == 4)]


txlens = justtx['len'].to_list()
inc_lens = inc_other_states['len'].to_list()

txwid = justtx['wid'].to_list()
inc_wid = inc_other_states['wid'].to_list()

tx_az = []
inc_az = []
for index, row in justtx.iterrows():
    az = get_azimuth(row)
    if az != 'false':
        tx_az.append(az)

for index, row in inc_other_states.iterrows():
    az = get_azimuth(row)
    if az != 'false':
        inc_az.append(az)

data_testing('width', txwid, inc_wid) """


#Weibull testing is below, page 14-16 of october notes
for magnitude in range(2, 6):

    if magnitude == 5:
        sampleset = df.loc[(df['st'].isin(['TX', 'LA', 'OK', 'AR', 'NM'])) & (df['mag'] == 5)]
    else:
        sampleset = df.loc[(df['st'] == 'TX') & (df['mag'] == magnitude)]

    widths = sampleset['wid'].to_list()
    test_weibull(magnitude, widths)