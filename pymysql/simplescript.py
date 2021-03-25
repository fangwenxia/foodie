import cs304dbi as dbi

dsn = dbi.cache_cnf()
dbi.use('wmdb')
conn = dbi.connect()
curs = dbi.cursor(conn)
curs.execute('''
    select name,birthdate
    from person
    where nm=123''')
row = curs.fetchone()
print('{} born on {}'.format(row[0],row[1]))
