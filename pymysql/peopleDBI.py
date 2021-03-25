'''Lists the first few names in the person table'''

import cs304dbi as dbi

dsn = dbi.read_cnf()
conn = dbi.connect(dsn)
conn.select_db('wmdb')
curs = dbi.dict_cursor(conn)
curs.execute('''
    select nm,name,birthdate
    from person
    where nm < 10''')
for row in curs.fetchall():
    print('{} born on {}'.format(row['name'],row['birthdate']))
