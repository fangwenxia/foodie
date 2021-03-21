#!/bin/env python3

import sys

if __name__ == '__main__':
    def usage():
        print('''Usage: {script} nm name [birthdate]
                Inserts that person; birthdate is optional'''
              .format(script=sys.argv[0]), file=sys.stderr)

    if len(sys.argv) < 3:
        usage()
    else:
        print('argc: ',len(sys.argv))
        print('0 script',sys.argv[0])
        print('1 nm: ',sys.argv[1])
        print('2 name: ',sys.argv[2])
        if len(sys.argv) < 4:
            print('omitting birthdate info')
        else:
            print('3 birthdate',sys.argv[3])
