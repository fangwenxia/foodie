'''Lists pet addresses given a (partial) name

Written Spring 2015
Re-written Spring 2018
Re-written Fall 2018 for C9
Re-written for Fall 2019 for pymysql/dbi and python 3
Re-written for Spring 2020 for updated dbi
Scott D. Anderson
'''

import sys
import cs304dbi as dbi

# ================================================================
# The functions that do most of the work.

def getInfoGivenPartialName(conn, partialName):
    '''Returns a list of pets with that partial name'''
    curs = dbi.dict_cursor(conn)
    curs.execute('''select pet9.name,address 
                    from owner9 inner join pet9 using(oid)
                    where pet9.name like %s''', 
                ['%' + partialName + '%'])
    return curs.fetchall()

# ================================================================
# This starts the ball rolling, *if* the script is run as a script,
# rather than just being imported.    

def usage():
    print('''Usage: {script} partialName
      Prints pet's name and address'''
            .format(script=sys.argv[0],
                    file=sys.stderr))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        conn = dbi.connect()
        for pet in getInfoGivenPartialName(conn, sys.argv[1]):
            print('{} who lives at {}'
                  .format(pet['name'], pet['address']))
