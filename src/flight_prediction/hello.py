### Copyright notice goes here as a comment block.

import logging

"""hello - Function to say hello.

This is an example of how to put a module inside a package.
"""

def say_hello():
    """Say hello and print file location.

    Arguments:
        No arguments.

    Returns:
        None
    """

    print("Hello world!")

    # This is called a formatted string -- *f-string* for short.
    # Inside an f-string, text inside curly braces is replaced
    # with the value of whatever variable it names.  The variable
    # __file__ is defined inside all Python source files (but not
    # Jupyter notebooks) and contains the full path to the file
    # being executed.
    logging.debug(f"This file's location: {__file__}")