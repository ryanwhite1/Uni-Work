class Question(object):
    """A multiple choice question with answer options."""

    def __init__(self, question):
        """
        Parameters:
            question (str): Question to be asked.
        """
        self._question = question
        self._answer_options = []
        self._user_answer = None
        self._correct_answer = None

    def add_answer(self, answer):
        """Ass a single answer to the question.

        Parameters:
            answer (str): Answer to be added as the next option.
        """
        self._answer_options.append(answer)

    def set_correct_answer(self, correct_answer):
        """Sets the number of the correct answer.

        Parameters:
            correct_answer (int): Number of the correct answer.

        """
        self._correct_answer = correct_answer

    def ask_question(self):
        """Display the question and answer options and store user's answer."""
        print(self._question)
        for i, option in enumerate(self._answer_options):
            print(" ", i+1, ") ", option, sep='')
        self._user_answer = input("Please enter your choice: ")

    def is_answer_correct(self):
        """(bool) Returns if the suer's answer is correct or not."""
        return int(self._user_answer) == self._correct_answer


class Exam(object):
    """An exam made up of several multiple choice questions."""

    def __init__(self):
        """Create an exam with no questions initially."""
        self._questions = []
        self._mark = None   #mark user achieved on this exam.

    def add_question(self, question):
        """Add a question to the exam.

        Parameters:
            question (Question): Question to be added to the exam.
        """
        self._questions.append(question)

    def give_exam(self):
        """Ask a user to answer the questions in this exam."""
        for question in self._questions:
            question.ask_question()

    def mark(self):
        """(int) Returns the user's mark for the exam."""
        self._mark_exam()
        return self._mark

    def percent(self):
        self._mark_exam()
        return self._mark / len(self._questions)

    def _mark_exam(self):
        """Calculates the user's result for the exam."""
        self._mark = 0
        for result in self._questions:
            if result.is_answer_correct():
                self._mark += 1


q1 = Question("What does the expression (6.0 + 11) / 2 evaluate to?")
q1.add_answer("8")
q1.add_answer("8.0")
q1.add_answer("8.5")
q1.add_answer("Error")
q1.set_correct_answer(3)

q2 = Question("What does the expression 4+3 %2 evaluate to?")
q2.add_answer("1")
q2.add_answer("4")
q2.add_answer("4.5")
q2.add_answer("5")
q2.set_correct_answer(4)


e = Exam()
e.add_question(q1)
e.add_question(q2)
e.give_exam()
print("The exam result was:", e.mark())

##questions = [q1, q2]
##for question in questions:
##    question.ask_question()
##
##mark = 0
##for q_num, result in enumerate(questions):
##    print("\nAnswer to question", q_num+1, "was:")
##    if result.is_answer_correct():
##        mark += 1
##        print("\tCorrect")
##    else:
##        print("\tIncorrect")
##
##result = mark / len(questions)
##print("\nFinal result was {0:.0%}".format(result))
