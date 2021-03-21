import cs304dbi as dbi

# ==========================================================
# The functions that do most of the work.

def getPeople(conn):
    '''Returns the name and birthdate of all the entries in
the person table, as a list of dictionaries.
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute('select name,birthdate from person')
    return curs.fetchall()

# ==========================================================
# This starts the ball rolling, *if* the file is run as a
# script, rather than just being imported.    

if __name__ == '__main__':
    dbi.cache_cnf()   # defaults to ~/.my.cnf
    dbi.use('wmdb')
    conn = dbi.connect()
    pl = getPeople(conn)
    for person in pl:
        print('{name} born on {date}'
              .format(name=person['name'],
                      date=person['birthdate']))
        
