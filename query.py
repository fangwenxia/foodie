import cs304dbi as dbi

# helper function to add new user into student and passwords database
def add_username(conn, name, username, password, favoriteDH, classYear): 
    curs = dbi.dict_cursor(conn)
    curs2 = dbi.dict_cursor(conn)
    curs.execute('INSERT INTO student(username, name, favoriteDH, classYear, password) \
                VALUES (%s, %s, %s, %s, %s);', [username, name, favoriteDH, classYear, password])
    conn.commit()

# helper function to check if username already exists in database
def username_exists(conn, username): 
    curs = dbi.dict_cursor(conn)
    curs.execute('select username from student where username = %s;', [username])
    if len(curs.fetchall()) == 0: return False
    else: return True

# helper function to access all users info from student table
def get_user_info(conn, username):
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute('select name, username, classYear, favoriteDH, favoriteFood \
                    from student \
                    where username = %s;', [username])
    # print (curs.fetchone())
    return curs.fetchone()

# is supposed to allow user to change/update information
# doesn't crash but doesnt update ?!?!
def update_profile(conn, username, info):
    curs = dbi.dict_cursor(conn)
    curs2 = dbi.dict_cursor(conn)
    curs3 = dbi.dict_cursor(conn)
    # curs4 = dbi.dict_cursor(conn)
    
    curs.execute('''UPDATE student \
                    SET name = %s \
                    WHERE username = %s;''', 
                    [info['name'], username])
    curs2.execute('''UPDATE student \
                    SET classYear = %s \
                    WHERE username = %s;''', 
                    [info['classYear'], username])
    curs3.execute('''UPDATE student \
                    SET favoriteDH = %s \
                    WHERE username = %s;''', 
                    [info['favoriteDH'], username])
    # curs4.execute('''UPDATE student SET favoriteFood = %s
    #                 WHERE favoriteFood=%s;''', [favoriteFood])
    # what is favorite food options ?!?!
    conn.commit()
    return 


    