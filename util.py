#!/usr/bin/env python

from __future__ import print_function

import sys

def eprint(*args, **kwargs):
    """
    print function which prints to stderr
    """
    print(*args, file=sys.stderr, **kwargs)

if __name__ == "__main__":
    print("Hello World")
    eprint("Error Workd...")
