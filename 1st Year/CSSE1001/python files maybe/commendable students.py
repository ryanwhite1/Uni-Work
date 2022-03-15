students = {'s1111111': ("Mary Smith", 6.5),
            's2222222': ("John Lee", 6.6),
            's3333333': ("Amy Quentin", 7)}

COMMENDATION_LEVEL = 6.6
GPA_INDEX = -1

def deans_commendation(students):
    """Find all students who have GPAs of COMMENDATION_LEVEL or higher.

    Parameters:
        students (dict{str, (name, GPA)}): Students in the Faculty.

    Return:
        dict{str, (name, GPA)}: All students with GPA >= COMMENDATION_LEVEL
    """
    commendable_students = {}
    for student in students:
        if students[student][GPA_INDEX] >= COMMENDATION_LEVEL:
            commendable_students[student] = students[student]
    return commendable_students

def main():
    commendable_students = deans_commendation(students)

    print("All students who have achieved a Dean's Commendation award:")
    for student in commendable_students:
        print('\t', student)

if __name__ == "__main__":
    main()
