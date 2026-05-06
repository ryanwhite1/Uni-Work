### --- Activity 5 --- ###
# def is_even(n):
#     if n%2 == 0:
#         return True
#     else:
#         return False
    
# integer = 4
# print(is_even(integer))


### --- Activity 6 --- ###
# def higher(a, b):
#     if a > b:
#         return a
#     else:
#         return b
    
# num1 = 3
# num2 = 10
# print(higher(num1, num2))


### --- Activity 7 --- ###
# def highest(a, b, c):
#     if a >= b and a >= c:
#         return a
#     if b >= c:
#         return b
#     return c
    
# print(highest(30, 40, 40))


### --- Activity 8 --- ###
# def average(my_list):
#     if len(my_list) == 0:
#         return None
#     total = 0
#     for item in my_list:
#         total += item
#     result = total / len(my_list)
#     return result

# my_list = []

# print(average(my_list))


### --- Activity 9 --- ###
# - Part 1 - #
# def smaller(a, b):
#     if a < b:
#         return a 
#     return b

# print(smaller(3, 3))

# - Part 2 - #
# def one_even_only(a, b, c):
    # even_counter = 0
    # for num in [a, b, c]:
    #     if num % 2 == 0:
    #         even_counter += 1
    # if even_counter == 1:
    #     return True 
    # return False
#     if (a%2 + b%2 + c%2) == 2:
#         return True 
#     return False

# print(one_even_only(1, 1, 2))

# - Part 3 - #
def key_counter(items, key):
    key_count = 0
    for number in items:
        if number == key:
            key_count += 1
    return key_count

items = [1, 1, 2, 3, 4, 5]
key = 10

print(key_counter(items, key))