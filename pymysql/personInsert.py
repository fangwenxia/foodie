'''Inserts a person

Written Spring 2015
Re-written Spring 2018
Re-written Fall 2018 for C9
Re-written in Fall 2019 for pymysql, dbi, and python3
Re-written in Spring 2020 for updated dbi module
Scott D. Anderson
'''

import sys
import cs304dbi as dbi

STAFFID = 1  # my id is 1. Yours is different. See assignment 1

# ================================================================
# The functions that do most of the work.

def personInsert(conn, nm, name, birthdate=None):
    '''Inserts the given person'''
    curs = dbi.cursor(conn)
    # nr is number of rows affected. Should be 1
    nr = curs.execute('''
        insert into person(nm,name,birthdate,addedby) 
        values (%s,%s,%s,%s)''',
                      [nm,name,birthdate,STAFFID])
    conn.commit()
    return nr                   
    
# ================================================================

def usage():
    print('''Usage: {script} nm name [birthdate]
    Inserts that person; birthdate is optional'''
            .format(script=sys.argv[0]), 
                    file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage()
    elif not sys.argv[1].isdigit():
        usage()
    else:
        conn = dbi.connect()
        if len(sys.argv) < 4:
            print('omitting birthdate info')
            nr = personInsert(conn,sys.argv[1],sys.argv[2],None)
        else:
            nr = personInsert(conn,sys.argv[1],sys.argv[2],sys.argv[3])
        print('{} inserted'.format(nr))
