import cs304dbi as dbi

dsn = dbi.cache_cnf()
dbi.use('wmdb')
conn = dbi.connect()
curs = dbi.dict_cursor(conn)
curs.execute('''
select name,birthdate
from person
where nm in (123,147,155)''')
rows = curs.fetchall()
for row in rows:
    print('{} born on {}'.format(row['name'],row['birthdate']))

