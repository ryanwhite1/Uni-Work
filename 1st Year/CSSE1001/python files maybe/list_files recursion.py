import os
directory = os.getcwd()

def list_files(directory):
    lst = []
    direc_list = os.listdir(directory)
    for file in direc_list:
        direc_file = os.path.join(directory, file)
        if os.path.isdir(direc_file):
            lst.extend(list_files(direc_file))
        else:
            lst.append(direc_file)
    return lst
            
            
    
