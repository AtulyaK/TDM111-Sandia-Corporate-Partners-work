### UNRELEASED SOURCE CODE - DO NOT DISTRIBUTE

"""Example: Print command-line arguments.

This script is a minimal example of how to access command-line arguments
from within Python.

Command line arguments are stored in the array ``sys.argv``.  The first
element (sys.argv[0]) is the name of the script.  The first command-line
argument is in sys.argv[1].  The second argument is in sys.argv[2].

When counting arguments using len(sys.argv), remember that the actual
number of arguments is one less than the length of the list because the
first element is the name of the script.
"""

# You'll need sys in order to access sys.argv
import sys


def print_arguments(args):
    """Print command-line arguments along with their indices.

    This function demonstrates that you can pass arguments around
    like any other variable.

    Arguments:
        args {list of str}: Command-line arguments

    Returns:
        None
    """

    if len(args) == 0:
        print("No command-line arguments were supplied.")
    for (i, argument) in enumerate(args):
        print("Argument {}: {}".format(i, argument))


def main():
    script_name = sys.argv[0]
    print("This script was invoked using the name {}".format(script_name))

    # The syntax my_list[1:] means "all elements of my_list starting with
    # the one at index 1".
    print_arguments(sys.argv[1:])

    # Always return a value from main().  It should be 0 if everything went
    # according to plan and some positive number if it didn't.
    return 0

if __name__ == '__main__':
    sys.exit(main())
