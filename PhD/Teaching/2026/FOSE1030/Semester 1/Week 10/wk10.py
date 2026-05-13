import numpy as np
import matplotlib.pyplot as plt

# ### --- Activity 1 --- ###
# house_x = np.array([0, 10, 10, 11, 5, -1, 0, 0, np.nan, 4.3, 4.3, 5.7, 5.7, np.nan, 1.5, 3.5, 3.5, 1.5, 1.5, np.nan, 6.5, 8.5, 8.5, 6.5, 6.5])
# house_y = np.array([0, 0, 10, 10, 15, 10, 10, 0, np.nan, 0, 4, 4, 0, np.nan, 5.5, 5.5, 7.5, 7.5, 5.5, np.nan, 5.5, 5.5, 7.5, 7.5, 5.5])

# fig, ax = plt.subplots()
# ax.plot(house_x, house_y)

# ax.set(aspect='equal')

# plt.show()


# ### --- Activity 2 --- ###
# g = 9.8

# def trajectory(x, v0, theta):
#     y_vals = x * np.tan(theta) - (0.5 / (v0**2)) * g*x**2 / (np.cos(theta)**2)
#     return y_vals

# theta_1 = np.deg2rad(45)
# vels = [10, 20, 30]
# linestyles = ['-', '--', '-.']
# colours = ['tab:red', 'tab:green', 'tab:blue']

# fig, ax = plt.subplots(figsize=(12, 6))

# for i in range(3):
#     xvals = np.linspace(0, vels[i]**2 * np.sin(2 * theta_1) / g, 100)
#     yvals = trajectory(xvals, vels[i], theta_1)
#     ax.plot(xvals, yvals, ls=linestyles[i], c=colours[i], label=f'Init. vel = {vels[i]} m/s')

# ax.set(xlabel='Horizontal Distance (metres)', ylabel='Vertical height (m)', title='Javelin Trajectory for Varying Initial Velocities, theta = 45 degrees',
#        xlim=(0, 100), ylim=(0, 40))
# ax.legend()

# plt.show()


# v0 = 30
# thetas = np.deg2rad(np.array([30, 45, 60]))

# fig, ax = plt.subplots(figsize=(12, 6))

# for i in range(3):
#     xvals = np.linspace(0, v0**2 * np.sin(2 * thetas[i]) / g, 100)
#     yvals = trajectory(xvals, v0, thetas[i])
#     ax.plot(xvals, yvals, ls=linestyles[i], c=colours[i], label=f'theta = {round(np.rad2deg(thetas[i]))} degrees')

# ax.set(xlabel='Horizontal Distance (metres)', ylabel='Vertical height (m)', title='Javelin Trajectory for Varying Launch Angles, Vnought= 30 m/s',
#        xlim=(0, 100), ylim=(0, 40))
# ax.legend()

# plt.show()


# ### --- Activity 3 --- ###
# arr = np.load('California_House_Price_Info.npy')

# long = arr[:, 0]
# lat = arr[:, 1]
# population = arr[:, 2]
# price = arr[:, 3]

# fig, ax = plt.subplots(figsize=(10, 10))

# plot = ax.scatter(long, lat, c=price, s=0.03 * population, alpha=0.3, cmap='plasma')
# ax.set(xlabel='Longitude (deg)', ylabel='Latitude (deg)', aspect='equal')

# fig.colorbar(plot, label='Median House Price (USD)')

# plt.show()



### --- Activity 4 --- ###
arr = np.load("Penguin_Info.npy")

fig, axes = plt.subplots(figsize=(12, 12), nrows=2, ncols=2)

fig2, ax2 = plt.subplots(figsize=(8, 8))

colours = ['tab:purple', 'tab:green', 'tab:blue']
labels = ['Adelie', 'Chinstrap', 'Gentoo']


for i in range(3):
    species_mask = arr[:, 0] == i
    axes[0][0].hist(arr[species_mask][:, 1], alpha=0.3, color=colours[i], label=labels[i])
    axes[0][1].hist(arr[species_mask][:, 2], alpha=0.3, color=colours[i], label=labels[i])
    axes[1][0].hist(arr[species_mask][:, 3], alpha=0.3, color=colours[i], label=labels[i])
    axes[1][1].hist(arr[species_mask][:, 4], alpha=0.3, color=colours[i], label=labels[i])

    ax2.scatter(arr[species_mask][:, 1], arr[species_mask][:, 2], color=colours[i], label=labels[i])

axes[0][0].set(xlabel='Beak Length (mm)')
axes[0][1].set(xlabel='Beak Depth (mm)')
axes[1][0].set(xlabel='Flipper Length (mm)')
axes[1][1].set(xlabel='Mass (g)')

axes[0][1].legend()

ax2.set(xlabel='Beak Length (mm)', ylabel='Beak Depth (mm)')
ax2.legend()

plt.show()