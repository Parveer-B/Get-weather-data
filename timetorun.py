import matplotlib.pyplot as plt
import numpy as np
ns = np.arange(1, 61, 1)
xs = ns*0 + 1
xs[12: 15] = np.floor(ns[12:15]/4) # 13 to 15 is n/4
xs[8: 12] = np.floor(ns[8:12]/2) # 13 to 15 is n/4
xs[0: 8] = ns[0:8] # 13 to 15 is n/4

sims = []
for j in range(60):
	sum = ns[j]
	for i in range(2, int(ns[j]+1)):
		sum+= xs[j]*(ns[j] - i + 1)
	sims.append(sum)

sims = np.array(sims)
minutes = sims/15
hours = minutes/60 #hours to run keepx for each n value given the x values above

times = [hours[0]]
for i in range(1, len(ns)):
	times.append(hours[i] + (i+1)*hours[i-1])

times = np.array(times)

plt.plot(ns, times/24)
plt.xlabel('n')
plt.ylabel('days to complete')
plt.axhline(y=1, color = 'r')
plt.axhline(y=0.25, color = 'g')
plt.yscale('log')
plt.show()