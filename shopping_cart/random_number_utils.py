import random
import string

class RandomNumberUtils:
    """
    Utility class for generating random numbers as strings.
    """

    @staticmethod
    def generate_random_id() -> str:
        """
        Generate a random ID string of length 6.
        """
        return ''.join(random.choices(string.ascii_uppercase, k=6));
