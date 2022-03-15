i = 1
while i <= 12:
    if 3 <= i <= 4:
        print(i, " o'clock")
    elif 7 <= i <= 8:
        print(i, " o'clock")
    elif 11 <= i <= 12:
        print(i, " o'clock")
    else:
        print(i)
    if i%4 == 0:
        print("rock")
    i = i + 1
print("We're gonna rock around the clock tonight")
