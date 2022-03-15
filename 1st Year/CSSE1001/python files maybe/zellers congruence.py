#Define Variables
day_m = int(input('Please enter the day of the month: '))
month = int(input('Please enter the month of the year: '))
year = int(input('Please enter the last 2 digits of the year: '))
year_c = int(input('Please enter the first 2 digits of the year: '))

h = (day_m + (13*(month + 1))//5 + year + year//4 + year_c//4 - 2*year_c)%7

if h==0:
    print("Saturday")
elif h==1:
    print("Sunday")
elif h==2:
    print("Monday")
elif h==3:
    print("Tuesday")
elif h==4:
    print("Wednesday")
elif h==5:
    print("Thursday")
else:
    print("Friday")
