import cs304dbi as dbi

''' 
temporary function for flashing: 
show availble usernames you can input
@ return: a list of dictionary of student usernames
'''
def temp_user(conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('select username from student')
    return curs.fetchall()

'''
search food name by fid
@ param: food id 
@ return: dictionary of food name
'''
def search_fid(conn,fid):
    curs=dbi.dict_cursor(conn)
    curs.execute('select name from food where fid = %s',[fid])
    return curs.fetchone()

'''
temporary function: search if the username exists 
delete later when Gigi's stuff is linked 
'''
def search_user(conn,username):
    curs= dbi.dict_cursor(conn)
    curs.execute('select username \
        from student where username = %s',[username])
    return curs.fetchall()

'''
insert into the feedback table
@ param: username, fid, rating, comment, time
'''
def feedback(conn,username,fid,rating,comment,time):
    curs = dbi.cursor(conn)
    curs.execute('''insert into feedback\
        (username,fid,rating,comment,entered)\
        values(%s,%s,%s,%s,%s)''',[username,fid,rating,comment,time])
    conn.commit()

'''
displaying the most recent 10 comments 
@ return: a list of dictionary of the most recent 10 comments 
'''
def recent_feedback(conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('select username,entered,rating,comment,name \
        from feedback inner join food using (fid) \
        order by entered limit 10')
    return curs.fetchall()

# don't use this yet- not fully planned out 
def top_rated(conn):
    curs=dbi.dict_cursor(conn)
    # how can I order by week in the time column?
    curs.execute('select name,(avg(rating))as avg from feedback inner join food using fid group by fid order by time DESC, rating limit 5')
    # sort by month and select by month
    return curs.fetchall()

'''
displaying the top 10 rated food
@ return: a list of dictionary that includes food name and avg rating of top 10 food entries 
'''
def food_rating(conn):
    curs=dbi.dict_cursor(conn)
    curs.execute('select name,round(avg(rating),2) as avg \
        from food inner join (feedback) using (fid) \
            group by fid \
                order by rating DESC\
                    limit 10')
    return curs.fetchall()

'''
Some Questions for Scott: 
1. Can I order by week/month of the weekly food item? 
2. Can I get some more explaination of Ajax, flask stuff? 
'''