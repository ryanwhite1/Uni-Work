def divide(dividend, divisor):
    """Divide divedened by divisor

    Parameters:
        divedend (float): Number to be divided
        divisor (float): Number to divide by.

    Return:
        float: Result of division.

    Raise:
        ValueError: If attempt is made to divide by 0.
    """
    if divisor == 0:
        raise TypeError("Divisor cannot be '0'.")
    return dividend / divisor

def intermediate(dividend, divisor):
    return divide (dividend, divisor)

def main():
    quotient = None
    dividend = input("Please enter a dividend for the calculation: ")
    while quotient is None:
        divisor = float(input("Please enter the divisor: "))
        try:
            quotient = intermediate(dividend, divisor)
            print("{0} divided by {1} equals {2}"
                  .format(dividend, divisor, quotient))
        except ValueError as e:
            print(str(e))

if __name__ == "__main__":
    main()
