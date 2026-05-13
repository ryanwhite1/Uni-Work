### --- Activity 1 --- ###
# import os
# # Part 1
# print(os.sep)
# # Part 2
# print(os.getcwd())
# # Part 3
# print(os.listdir())

### --- Activity 2 --- ###
# import glob
# python_files = glob.glob("*.py")
# print(python_files)


### --- Activity 4 --- ###
# import numpy as np
# # Part 1
# arr1 = np.arange(1, 11)
# # or:
# list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# arr1 = np.array(list1)
# print(arr1)

# # Part 2 
# arr2 = np.arange(1, 10.5, 0.5)
# # or:
# step = 0.5
# arr2 = np.arange(1, 10 + step, step) 
# print(arr2)

# # Part 3
# arr3 = np.zeros((3, 5))
# print(arr3)

# # Part 4
# arr4 = np.ones(np.shape(arr2)) * np.pi
# # or:
# arr4 = np.zeros(arr2.shape) + np.pi
# print(arr4)

# # Part 5
# arr5 = np.arange(1, 13)
# arr5 = np.reshape(arr5, (4, 3))
# # or:
# arr5 = np.arange(1, 13).reshape((4, 3))
# print(arr5)


### --- Activity 5
import numpy as np
arr = np.arange(1, 16).reshape((3, 5)).T
print(arr)

# Part 1
arr1 = arr[[1, 3]]
# print(arr1)

# Part 2
arr2 = arr > 3
# print(arr2)

# Part 4
# arr4 = (arr > 3) & (arr < 7)
# print(arr4)

# Part 5
for number in [2, 9, 10]:
    print(np.argwhere(arr == number))

# ### --- Activity 7 --- ###
# import numpy as np
# g = 9.8
# def heights(v0):
#     times = np.linspace(0, 2 * v0 / g, 1000)
#     height_vals = v0 * times - 0.5 * g * times**2
#     return height_vals

# def analytic_max(v0):
#     return v0**2 / (2 * g)

# for init_velocity in [10, 15, 20]:
#     trajectory = heights(init_velocity)
#     print("The estimated max height for initial velocity of", init_velocity, "m/s, is", np.max(trajectory), "m")
#     print("This is compared to the maximum analytic height of", analytic_max(init_velocity), "m")