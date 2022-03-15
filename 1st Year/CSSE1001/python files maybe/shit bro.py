grade = int(input("Result "))
while grade <0 or grade>100:
    grade=int(input("Result "))

if grade>=85:
    print("Well Done bitch")
    result = 7
elif grade>=75 and grade<85:
    print("no one cares if you only just missed out, shut up")
    result = 6
else:
    print("you dumb as shit")
    
print("i'm gonna rate you out of 10:",result)
