from __future__ import print_function
import sys

def eprint(*args, **kwargs):
    """
    print function which prints to stderr
    """
    print(*args, file=sys.stderr, **kwargs)
