### Copyright notice goes here as a comment block.

import logging

"""
    This file demostrates a docString and function definition
"""

def test():
    """Print 'Hello world!'
    
    Students:
        Bryce Castle

    Arguments:
        No arguments.

    Returns:
        None
    """

    print("Hello world!")
    logging.debug(f"This file's location: {__file__}")