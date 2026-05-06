### --- Activity 4 --- ###
# def highest(list):
#     if len(list) == 0:
#         return None
#     temp_highest = list[0]
#     for number in list:
#         if number > temp_highest:
#             temp_highest = number
#     return temp_highest

# my_list = [70, 5, 101, 50000000]

# print(highest(my_list))


### --- Activity 5 --- ###
# def is_even(n):
#     if n%2 == 0:
#         return True
#     return False

# print(is_even(4))


### --- Activity 6 --- ###
# def higher(a, b):
#     if a > b:
#         return a
#     else:
#         return b
    
# print(higher(4, 10))

### --- Activity 7 --- ###
# def highest(a, b, c):
#     if a >= b and a >= c:
#         return a
#     if b >= c:
#         return b
#     return c
    
# print(highest(5, 7, 7))


### --- Activity 8 --- ###
# def average(my_list):
#     if len(my_list) == 0:
#         return 0
#     total = 0
#     for item in my_list:
#         total += item
#     result = total / len(my_list)
#     return result

# num_list = [4, 6, 6]
# print(average(num_list))




### --- Activity 9 --- ###
# Part 1:
# def smaller(a, b):
#     if a < b:
#         return a 
#     return b 

# print(smaller(1, 2))

# Part 2:
# def one_even(a, b, c):
#     even_counter = 0
#     for num in [a, b, c]:
#         if num%2 == 0:
#             even_counter += 1
#     if even_counter == 1:
#         return True
#     return False

# print(one_even(2, 2, 2))

# Part 3:
def key_count(items, key):
    key_counter = 0
    for num in items:
        if num == key:
            key_counter += 1
    return key_counter

items = [1, 2, 3, 4, 5, 6, 7, 2, 2, 2, 2]
key = 10

print(key_count(items, key))