import cs304dbi as dbi

# ==========================================================
# The functions that do most of the work.

def peopleBornInMonth(conn,month):
    '''Returns the name and birthdate of people born in given month,
    as a list of dictionaries
    '''
    curs = dbi.dict_cursor(conn)
    # this uses a prepared query, since the 'month' comes
    # from an untrustworthy source
    curs.execute('''
        select name,birthdate from person 
        where month(birthdate) = %s''',
                 [month])
    return curs.fetchall()

# ==========================================================
# This starts the ball rolling, *if* the file is run as a
# script, rather than just being imported.    

def usage():
    print('''Usage: {script} month
    Prints actors born in given month, a number from 1-12'''
            .format(script=sys.argv[0]), file=sys.stderr)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        usage()
    elif not( sys.argv[1].isdigit() and
              1 <= int(sys.argv[1]) <= 12):
        usage()
    else:
        dbi.cache_cnf()   # defaults to ~/.my.cnf
        dbi.use('wmdb')
        conn = dbi.connect()
        people = peopleBornInMonth(conn,int(sys.argv[1]))
        for person in people:
            print(('{} born on {}'
                  .format(person['name'], person['birthdate'])))
