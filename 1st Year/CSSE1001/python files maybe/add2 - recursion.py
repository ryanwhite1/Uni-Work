def add2(lst):
    if len(lst) == 1:
        return lst[0]
    else:
        mid = len(lst) // 2
        return add2(lst[:mid]) + add2(lst[mid:])
