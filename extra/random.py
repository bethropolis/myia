import random
import string


def random_string(string_length=4):
    """
    Generate a random string of fixed length 
    
    args:
        string_length (int): The length of the random string.
    returns:
        string: The random string.
    """
    
    
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))
