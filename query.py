import cs304dbi as dbi

# helper function to add new user into student
def add_username(conn, username, passwd1, hashed_str): 
    curs = dbi.dict_cursor(conn)
    curs.execute('''INSERT INTO student(username, password, hashed)
                VALUES (%s, %s, %s);''', [username, passwd1, hashed_str])
    conn.commit()


# helper function to check if username already exists in database
def username_exists(conn, username): 
    curs = dbi.dict_cursor(conn)
    curs.execute('''select username from student where username = %s;''', [username])
    return len(curs.fetchall()) != 0

def is_admin(conn, username):
    curs = dbi.dict_cursor(conn)
    curs.execute('''select * from admin where adminname = %s;''', [username])
    print('is_admin result',len(curs.fetchall()) != 0)
    return len(curs.fetchall()) != 0
        

# helper function to access all users info from student table
def get_user_info(conn, username):
    curs = dbi.dict_cursor(conn)
    curs.execute('''select student.name, username, classYear, favoriteDH, favoriteFood, allergies, preferences
                    from student
                    where username = %s;''', [username])
    return curs.fetchone()

# helper function to get diningHall name
def DH_name(conn, id):
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


    