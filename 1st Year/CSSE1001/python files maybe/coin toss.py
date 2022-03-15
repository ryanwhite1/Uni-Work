import random


def toss():
    """Return a head or tail (head = 1, tail = 0)."""
    return random.randint(0, 1)

def move(position, coin):
    """Return the new position of the pirate give current position & coin toss

    Parameters:
        position (int): Current position of the pirate on the plank.
        coin (int): Coin toss result (head = 1, tail = 0).

    Return:
        int: New position of pirate on plank.

    Preconditions:
        0 <= coin <= 1
        position >= 0
    """
    if coin == 1:
        position += 1
    elif position > 0:
        position -= 1
    else:
        position = 0

    return position
    
def game_loop(plank_length):
    """Return the nuber of coin tosses needed for pirate to walk off the plank.

    Parameters:
        plank_length (int): Positive Integer that is length of the plank.

    Return:
        int: Number of coin tosses until pirate walked off the plank.
    """
    num_tosses = 0
    position = 0
    while position < plank_length:
        position = move(position, toss())
        num_tosses += 1

    return num_tosses

def get_average(total_trials, plank_length):
    """Return the average number of coin tosses across several trials.

    Parameters:
        total_trials (int): Positive integer that is the total number of trials.
        plank_length (int): Positive integer that is the length of the plank.

    Return:
        int: Average number of coin tosses until pirate walked off of the plank.
    """
    num_trials = 0
    total_tosses = 0
    while num_trials < total_trials:
        num_trials += 1
        total_tosses += game_loop(plank_length)

    return total_tosses / num_trials
