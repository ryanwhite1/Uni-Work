n = 5

# for i in range(n):
#     spaces = n - i
#     for j in range(spaces):
#         print(" ", end='')
#     for j in range(i*2 + 1):
#         print("*", end='')
#     print()
# for i in range(n - 2, -1, -1):
#     spaces = n - i 
#     for j in range(spaces):
#         print(" ", end='')
#     for j in range(i*2 + 1):
#         print("*", end='')
#     print()

for i in range(n):
    spaces = n - i
    print(" " * spaces, end='')
    print("*" * (i * 2 + 1), end='')
    print()
for i in range(n-2, -1, -1):
    spaces = n - i 
    for j in range(spaces):
        print(" ", end='')
    for j in range(i*2 + 1):
        print("*", end='')
    print()