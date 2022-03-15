def sum_list(values):
    result = 0                  # 1 step
    for value in values:        # len(values)   
        result += value         # len(values)
    return result               # 1 step


                                # Complexity: 2 + 2*len(values)
                                # O(n)

def double_sum_list(values):
    result = 0                  # 1 step
    for value in values:        # len(values)   
        result += value         # len(values)
    for value in values:        # len(values)   
        result += value         # len(values)
    return result               # 1 step
                                # O(n)


def exponentiation(value, exponent):
    result = 1
    while exponent > 0:
        exponent -= 1
        result *= value
    return result
