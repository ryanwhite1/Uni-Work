def find_functions(filename):

    with open(filename, 'r') as file_in, \
         open('functions.txt', 'w') as file_out:
        for line in file_in:
            if line[:4] == 'def ':
                funk = line
                file_out.write(funk)

def name_functions(filename):
    i = 1
    with open(filename, 'r') as file_in:
        for line in file_in:
            if line[:4] == 'def ':
                _,_,end = line.partition(' ')
                name,_,args = end.partition('(')
                print(i, name, args)
            i += 1
            

#find_functions('week05_functions.py')
name_functions('week05_functions.py')
