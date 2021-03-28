import pymysql

conn = pymysql.connect(host='localhost',
                       user='cs304guest',
                       password='secret')
conn.select_db('wmdb')
curs = conn.cursor(pymysql.cursors.DictCursor)
curs.execute('''
    select nm,name,birthdate
    from person
    where nm = 123''')
row = curs.fetchone()
print(row)
