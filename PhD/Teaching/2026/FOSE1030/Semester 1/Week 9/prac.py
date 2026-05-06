### --- Activity 1 --- ###
# # 1
# import os
# print(os.sep)
# # 2
# print(os.getcwd())
# # 3
# print(os.listdir())


# ### --- Activity 2 --- ###
# import glob
# print(glob.glob("*.py"))


### --- Activity 3 --- ###
# import sys, math
# operator, value = sys.argv[1], float(sys.argv[2])
# if operator == "sin":
#     print(math.sin(value))
# elif operator == "cos":
#     print(math.cos(value))
# elif operator == "tan":
#     print(math.tan(value))
# else:
#     print("Please input a valid trigonometric operator.")


### --- Activity 4 --- ###
# import numpy as np
# # 1
# arr1 = np.arange(1, 11)
# # 2 
# delta = 0.5
# arr2 = np.arange(1, 10 + delta, delta)
# # 3 
# arr3 = np.zeros((3, 5))
# # 4
# arr4 = np.ones(np.shape(arr2)) * np.pi
# # 5
# arr5 = np.ones(12).reshape((4, 3))


### --- Activity 5 --- ###
# import numpy as np
# arr = np.arange(1, 16).reshape(3, 5).T
# # 1
# arr1 = arr[[1, 3]]
# # 2
# arr2 = arr > 3
# # 3
# arr3 = arr < 7
# # 4
# arr4 = (arr > 3) & (arr < 7)
# # 5
# for i in [2, 9, 10]:
#     print(np.argwhere(arr == i))


### --- Activity 6 --- ###
# import math
# import numpy as np
# def exp_range(x, a, b):
#     '''return exp(x) if a<= x <=b, else return 0'''
#     mask = (x >= a) & (x <= b)
#     return np.exp(x) * mask

# x = np.linspace(0, 8, 10)
# print(exp_range(x, 2, 5))


### --- Activity 7 --- ###
# import numpy as np
# g = 9.8
# def height(v0, n_t=10):
#     times = np.linspace(0, 2 * v0 / g, n_t)
#     return v0 * times - 0.5 * g * times**2
# def max_height(v0):
#     return v0**2 / (2 * g)

# for v0 in [10, 15, 20]:
#     heights = height(v0, n_t=50)
#     print("Estimated max height is", np.max(heights), "versus analytic max of", max_height(v0))


### --- Activity 8 --- ###
# import numpy as np
# arr1 = np.arange(12).reshape(4, 3)
# arr2 = np.array([1, 3, 6, 9])
# print(arr1 / arr2[:,np.newaxis])


### --- Activity 9 --- ###
import numpy as np

arr = np.random.uniform(0, 1, (10, 3))
print(arr)
print(np.sum(arr, axis=0), np.sum(arr, axis=1))
print(np.min(arr), np.argmin(arr), np.argmin(arr, axis=0), np.argmin(arr, axis=1), np.unravel_index(np.argmin(arr), np.shape(arr)))