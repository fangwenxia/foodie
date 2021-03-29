import cs304dbi as dbi

# helper function to add new user into student and passwords database
def add_username(conn, name, username, passwd1, hashed): 
    curs = dbi.dict_cursor(conn)
    curs2 = dbi.dict_cursor(conn)
    curs.execute('INSERT INTO student(username, name, password, hashed) \
                VALUES (%s, %s, %s, %s);', [username, name, passwd1, hashed])
    conn.commit()

# helper function to check if username already exists in database
def username_exists(conn, username): 
    curs = dbi.dict_cursor(conn)
    curs.execute('select username from student where username = %s;', [username])
    if len(curs.fetchall()) == 0: 
        return False
    else: 
        return True

# helper function to access all users info from student table
def get_user_info(conn, username):
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute('''select student.name, username, classYear, diningHall.name as favoriteDH, favoriteFood
                    from student, diningHall
                    where student.favoriteDH = diningHall.did
                    and username = %s;''', [username])
    # print (curs.fetchone())
    return curs.fetchone()

# is supposed to allow user to change/update information
# doesn't crash but doesnt update ?!?!
def update_profile(conn, username, name, year, diningHall, food):
    curs = dbi.dict_cursor(conn)
    curs.execute('''UPDATE student 
                    SET name = %s, classYear = %s, favoriteDH = %s, favoriteFood  = %s
                    WHERE username = %s;''', 
                    [name, year, diningHall, food, username])
    conn.commit()
    return 

def DHName(conn, diningHall):
    curs = dbi.dict_cursor(conn)
    curs.execute('''select name
                from diningHall
                where did = %s''', [diningHall])
    return curs.fetchone()

    