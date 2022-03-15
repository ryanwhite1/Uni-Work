

def is_palindrome(word):
    """Determine if 'word' is a palindrome.

    Parameters:
        word (str): Non-empty string containing a word to test.

    Return:
        (bool): True if 'word' is a palindrome. False otherwise.
    """
    if len(word) <=1:
        return True
##    if word[0] == word[-1] and is_palindrome(word[1:-1]):
##       return True
##    else:
##        return False
    return word[0] == word[-1] and is_palindrome(word[1:-1])

def test_palindrome(word):
    """Determine if 'word' is a palindrome.

    Parameters:
        word (str): Non-empty string containing a word to test.

    Return:
        (bool): True if 'word' is a palindrome. False otherwise.
    """
    if len(word) == 0:
        return False
    if not word.isalpha():
        return False
    word = word.upper()
    return is_palindrome(word)
