import cs304dbi as dbi
def search_food(conn,food):
    curs= dbi.dict_cursor(conn)
    food="%"+food+"%"
    curs.execute('select fid from food where name like %s',[food])
    return curs.fetchall()

def feedback(conn,username,fid,rating,comment,time):
    curs = dbi.cursor(conn)
    curs.execute('''insert into feedback(username,fid,rating,comment,entered)
    values(%s,%s,%s,%s,%s)''',[username,fid,rating,comment,time])
    conn.commit()

def recent_feedback(conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('select username,entered,rating,comment from feedback order by entered limit 10')
    return curs.fetchall()

def top_rated(conn):
    curs=dbi.dict_cursor(conn)
    # how can I order by week in the time column?
    curs.execute('select name,avg(rating) from feedback inner join food using fid group by fid order by time DESC, rating limit 5')
    # sort by month and select by month
    return curs.fetchall()

def food_rating(conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('select name,avg(rating) from food inner join (feedback) using (fid) group by fid order by rating DESC')
    return curs.fetchall()

'''
Meeting 3.18.2021:
Things to talk about: 

Scott: 
git- connecting to the remote repository, branch and stuff

Sara: 
1. What should I do with searching the food? What exactly should it look like?
2. Username issue- sessions? 
3. Am I on the right repository? 

Updates made: 
1. DDL changed; new column added: time in feedback
2. dining hall served put on hold in feedback menu 
2. Currently: need to load DDL every time to try to insert fx1 3(Beef Stroganoff)
'''
