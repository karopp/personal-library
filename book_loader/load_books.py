#!/usr/bin/env python3

import getopt
import os
import sys
import json


file_path = os.path.realpath(__file__)
script_path = os.path.dirname(file_path)

# Make library available in path
#library_paths = [
#    os.path.join(script_path, "lib")
#]

#for p in library_paths:
#    if not (p in sys.path):
#        sys.path.insert(0, p)

#
# Main
#

def main():
    # Set default values
    print("Hello World")

if __name__ == "__main__":
    main()
