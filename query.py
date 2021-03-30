import cs304dbi as dbi

# old helper function to add new user into student and passwords database without CAS
# def add_username(conn, name, username, passwd1, hashed): 
#     curs = dbi.dict_cursor(conn)
#     curs.execute('''INSERT INTO student(username, name, password, hashed)
#                 VALUES (%s, %s, %s, %s);''', [username, name, passwd1, hashed])
#     conn.commit()

# new  helper function to add new user into student
def add_username(conn, username): 
    curs = dbi.dict_cursor(conn)
    curs.execute('''INSERT INTO student(username)
                VALUES (%s);''', [username])
    conn.commit()


# helper function to check if username already exists in database
def username_exists(conn, username): 
    curs = dbi.dict_cursor(conn)
    curs.execute('''select username from student where username = %s;''', [username])
    if len(curs.fetchall()) == 0: 
        return False
    else: 
        return True

# helper function to access all users info from student table
def get_user_info(conn, username):
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute('''select student.name, username, classYear, favoriteDH, favoriteFood, allergies, preferences
                    from student
                    where username = %s;''', [username])
    return curs.fetchone()

# helper function to get diningHall name
def DH_name(conn, id):
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute('''select name
                    from diningHall
                    where did = %s;''', [id])
    return curs.fetchone()

# is supposed to allow user to change/update information
# doesn't crash but doesnt update ?!?!
def update_profile(conn, username, name, year, diningHall, food, allergies, preferences):
    curs = dbi.dict_cursor(conn)
    curs.execute('''UPDATE student 
                    SET name = %s, classYear = %s, favoriteDH = %s, favoriteFood  = %s, allergies = %s,
                    preferences  = %s
                    WHERE username = %s;''', 
                    [name, year, diningHall, food, allergies, preferences, username])
    conn.commit()
    return 


    