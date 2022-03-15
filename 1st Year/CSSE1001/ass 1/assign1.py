"""
Implement your solution to assignment 1 in this file.
Write an informative header comment for this file.
"""

__author__ = Ryan White, 44990392"Your Name and Student Number"


from assign1_utilities import get_column, replace_column, truncate_string



def remove_athlete_id(row) :
    pass    # Replace this line with your implementation



def main() :
    """Main functionality of program."""
    with open("athlete_data.csv", "r") as raw_data_file, \
         open("athlete_data_clean.csv", "w") as clean_data_file :
        for row in raw_data_file :
            corrupt = False
            row = remove_athlete_id(row)
            row_to_process = row    # Saves row in original state, minus athlete id.

            # You need to implement the functionality of your program
            # inside of this loop. The variable 'row' is a string containing
            # a single row of data from the raw data file.
            # It is advisable to implement the functionality in a number of
            # functions and call those functions from inside this loop.
            # Continue your processing logic here.

            # Save the row data to the cleaned data file.
            if not corrupt :
                clean_data_file.write(row_to_process)
            else :
                clean_data_file.write(row + ",CORRUPT")    



# Call the main() function if this module is executed
if __name__ == "__main__" :
    main()
