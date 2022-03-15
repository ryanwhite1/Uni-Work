"""Example of handling and raising exceptions."""

__author__ = "Richard Thomas"
__email__ = "richard.thomas@uq.edu.au"
__copyright__ = "Copyright 2018, University of Queensland"



def input_int(prompt) :
    """Guarantee that an integer is input.

    Parameters:
        prompt (str): Message to prompt for use input.

    Return:
        int: Entered integer value.
    """
    valid_number = False
    while not valid_number :
        entered_number = input(prompt)
        try :
            return int(entered_number)
        except ValueError :
            print("You have entered a non-integer value, please try again.")



def divide(dividend, divisor) :
    """Divide dividend by divisor.

    Parameters:
        dividend (float): Number to be divided.
        divisor (float): Number used to divide 'dividend'.

    Return:
        float: Result of dividend divided by divisor.

    Raise:
        ValueError: If attempt is made to divide by 0.
    """
    if divisor == 0:
        raise ValueError("Divisor cannot be '0'.")
    return dividend / divisor



def intermediate(dividend, divisor) :
    """Simple example of exceptions passing through intermediate function calls.

    Return:
        float: Result of dividend divided by divisor.

    Raise:
        ValueError: If attempt is made to divide by 0.
    """
    # Do something with dividend, divisor and quotient.
    return divide(dividend, divisor)



def main() :
    quotient = None
    dividend = input_int("Please enter dividend for calculation: ")
    while quotient is None :
        divisor = input_int("Please enter divisor for calculation: ")
        try:
            quotient = intermediate(dividend, divisor)
            print("{0} divided by {1} equals {2}"
                  .format(dividend, divisor, quotient))
        except ValueError as e:
            # Normally do some error handling that is more sophisticated 
            # than just printing the exception's error message.
            print(str(e))



if __name__ == "__main__" :
    main()
