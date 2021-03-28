import pymysql

conn = pymysql.connect(read_default_file='/home/cs304/.my.cnf')
conn.select_db('wmdb')
curs = conn.cursor(pymysql.cursors.DictCursor)
curs.execute('''
select nm,name,birthdate
from person
where nm = 123''')
row = curs.fetchone()
print(row)
