from Get_Weather_Event.get_bus_removal_data import Buses_Removed
from scipy.io import savemat
import sys
import time

numcases = sys.argv[1]
setnum = sys.argv[2]
buses_removed = Buses_Removed(eventtype='tornado')
alltornadoes = []
start = time.time()
print('startingg')
for x in range(int(numcases)):
    dictt = {}
    busesinbox, tlinbox, busesremoved, tlremoved, eventbox, eventtype, magnitude, substationsinbox = buses_removed.generate_tornado()
    dictt['busesinbox'] =  busesinbox
    dictt['tlremoved'] =  tlremoved
    dictt['magnitude'] =  magnitude
    dictt['busesremoved'] =  busesremoved
    dictt['eventbox'] =  eventbox
    dictt['substationsinbox'] =  substationsinbox
    alltornadoes.append(dictt)

mat_data = {"data": [dict(item) for item in alltornadoes]}
a = 54
savemat("gentornadoes/tornadoes_set" + str(setnum) + ".mat", mat_data)
