import numpy as np
import matplotlib.pyplot as plt

### --- Activity 3 --- ###
arr = np.load('California_House_Price_Info.npy')

long = arr[:, 0]
lat = arr[:, 1]
population = arr[:, 2]
price = arr[:, 3]


plt.scatter(long, lat, c=price, s=0.01 * population, 
            cmap='prism', label='Population',
            alpha=0.4)

plt.axis('equal')
plt.xlabel("Longitude (deg)")
plt.ylabel("Latitude (deg)")
plt.legend()
plt.colorbar(label='Median House Price (USD)')

plt.show()