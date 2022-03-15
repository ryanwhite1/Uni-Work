def minimum(lst):
    n = len(lst)
    if lst == []:
        raise ValueError
    if len(lst) == 1:
        return lst[0]
    else:
        if lst[0] < lst[1]:
            return minimum([lst[0]] + lst[2:])
        else:
            return minimum(lst[1:])
            
        
