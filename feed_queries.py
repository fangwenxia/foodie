import cs304dbi as dbi

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
    curs.execute('select username,entered,rating,comment,name,fid \
        from feedback inner join food using (fid) \
        order by entered DESC limit 10')
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
return a list of dictionary with the fid and username
used for checking duplicates when submitting a feedback form
@ param: fid, username
@ return: a list of dictionary pubulished by username on fid
'''
def feedback_duplicate(conn,fid,username):
    curs=dbi.dict_cursor(conn)
    curs.execute('''select username,fid from feedback\
        where username=%s and fid=%s''',[username,fid])
    return curs.fetchall()

'''
return all reviews published by this profile person 
@ param: username
@ return: a list of dictionary of reviews with username,entered time, 
        rating, comment, food name that this user has published 
'''
def user_reviews(conn,username):
    curs=dbi.dict_cursor(conn)
    curs.execute('select username,entered,rating,comment,name \
        from feedback inner join food using (fid) \
            where username=%s \
            order by entered DESC',[username])
    return curs.fetchall()