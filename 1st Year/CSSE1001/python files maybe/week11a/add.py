def add(numbers) :
    """Add up a list of numbers.
    
    Parameters:
        numbers (list<float>): List of numbers to be summed.

    Return:
        float: Sum of all the values in 'numbers'.
    """
    if not numbers :
        return 0
    else :
        return numbers[0] + add(numbers[1:])


# Example use

print(add([3, 8, 5]))
