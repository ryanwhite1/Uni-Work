power = input('Enter the power: ')
power = float(power)
pow = 0
count = 0
while pow <= power:
    print(pow,2**pow)
    pow = pow + 1
    count = count + 1
    if count > power:
        break
     
