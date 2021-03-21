import cs304dbi as dbi

# ==========================================================
# The functions that do most of the work.

def personLookup(conn,nm):
    '''Returns the name and birthdate of person with given NM,
    as a dictionary. Returns None if person is not in database.
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select name,birthdate from person 
        where nm = %s''',
                 [nm])
    return curs.fetchone()

# ==========================================================
# This starts the ball rolling, *if* the file is run as a
# script, rather than just being imported.    

def usage():
    print(('''Usage: {script} nm
    Prints actor with that nm'''
           .format(script=sys.argv[0], file=sys.stderr)))

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        usage()
    elif not( sys.argv[1].isdigit()):
        usage()
    else:
        dbi.cache_cnf()
        dbi.use('wmdb')
        conn = dbi.connect()
        person = personLookup(conn,int(sys.argv[1]))
        if person is not None:
            print(('{} born on {}'
                   .format(person['name'], person['birthdate'])))
        else:
            print('no person with that NM is in WMDB')
            
