def has_repeats(lst):
    counter = 0
    size = len(lst)
    for i in range(size-1):
        element = lst[i]
        counter +=1
        for j in range(i+1, size):
            counter += 1
            if element == list[j]:
                print(counter)
                return True
    print(counter)
    return False
