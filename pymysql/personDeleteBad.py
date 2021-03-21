'''Deletes a person

Written Spring 2015
Re-written Spring 2018
Re-written Fall 2018 for C9
Re-written in Fall 2019 for pymysql, dbi, and python3
Re-written in Spring 2020 for new DBI module
Scott D. Anderson
'''

import sys
import cs304dbi as dbi

# ================================================================
# The functions that do most of the work.

def deleteByNM(conn, nm):
    '''Deletes the person with the given NM. 
    Returns number of affected rows.'''
    curs = dbi.cursor(conn)
    nr = curs.execute('''delete from person where nm = %s''' % (nm))
    conn.commit()
    return nr

# ================================================================
# This starts the ball rolling, *if* the script is run as a script,
# rather than just being imported.    

def usage():
    print('Usage: {script} NM\nDeletes the person with that NM'
            .format(script=sys.argv[0]), 
                    file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        conn = dbi.connect()    # connect to personal database
        n = deleteByNM(conn,sys.argv[1])
        print('Deleted {} rows'.format(n))
