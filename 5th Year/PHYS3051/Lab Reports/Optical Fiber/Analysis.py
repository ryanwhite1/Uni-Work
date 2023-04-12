# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 15:40:34 2023

@author: ryanw
"""

import numpy as np
import matplotlib.pyplot as plt

# read in the image
image = plt.imread('single16.5.jpg') # the read image is a numpy ndarray with dimensions (vertical, horizontal, RGB)

# # find the row with the brightest red pixel
# row = np.unravel_index(np.argmax(image[:, :, 0]), image[:, :, 0].shape)[1]

# find the row with the largest sum of the red pixel values
row = image[:, :, 0].sum(axis=1).argmax()

# create x data point for each column (pixel)
x = np.arange(0, image.shape[1], 1)

# show the red pixel values across the chosen row
fig, ax = plt.subplots()
ax.plot(x, image[row, :, 0])
ax.set_ylabel("Red Pixel Value")
ax.set_xlabel("Horizontal Pixel")

# now show the image along with the chosen row
fig, ax = plt.subplots()
ax.imshow(image)
ax.axhline(row)
ax.set_xlabel("Horizontal Pixel")
ax.set_ylabel("Vertical Pixel")
