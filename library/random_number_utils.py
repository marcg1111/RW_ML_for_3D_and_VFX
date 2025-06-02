import random
import string

class RandomNumberUtils:
    """
    Utility class for generating random numbers as string
    """

    """___The @staticmethod decorator in Python is used to define a method inside a class that does not need access to the instance (self) or class (cls).___"""
    @staticmethod
    def generate_random_id() -> str:
        """
        Generate a random ID as string of length 6
        """

        """____'' is the seperator used by the join-function__"""
        return ''.join(random.choices(string.ascii_uppercase, k=6))