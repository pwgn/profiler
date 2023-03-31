import sys
import getopt
import os
import pandas as p
from profiler import profile

def main(argv):
    inputfile = ''
    opts, args = getopt.getopt(argv, 'i:')
    for opt, arg in opts:
        if opt == '-i':
            print(f'inputfile:{arg}')
            inputfile = os.path.abspath(arg)
        else:
            print('cli.py -i <inputfile>')
            sys.exit()

    profile(inputfile)

if __name__ == "__main__":
    main(sys.argv[1:])