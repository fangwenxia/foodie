import cs304dbi as dbi

# given a connection and the properties of a meal, inserts the food into the food table. 
def insert_food(conn,name,date,category,dhall): 
    curs = dbi.cursor(conn)
    sql = '''insert into food(name,lastServed,type,did) 
                  values (%s,%s,%s,%s);'''
    vals = [name,date,category,dhall]
    curs.execute(sql,vals)
    conn.commit()

# given a connection and name, returns the given food's fid
def get_food_id(conn,name): 
    curs1 = dbi.cursor(conn)
    sql = '''select fid from food where name=%s'''
    curs1.execute(sql,name)
    food_id = curs1.fetchone()[0]
    return food_id
    
# given food information, inserts a label into the labels table
def insert_label(conn,allergens,preferences,ingredients,id): 
    curs2 = dbi.cursor(conn)
    sql2 = '''insert into labels(allergen,preference,ingredients,fid) values (%s,%s,%s,%s);'''
    preferences = ['gluten sensitive' if i=='gluten-sensitive' else i for i in preferences]
    allergens = ['tree nut' if i=='tree-nut' else i for i in allergens]
    prefs = ','.join(preferences)
    allgns = ','.join(allergens)
    labelvals = [allgns,prefs,ingredients,id]
    curs2.execute(sql2,labelvals)
    conn.commit()

# checks to see if the name of the food already exists in the database
# test w/ Chicken Tikka Masala, Tower
def exists(conn,name,did):
    curs = dbi.cursor(conn)
    sql = '''select * from food where name=%s and did=%s'''
    vals = [name,did]
    curs.execute(sql,name)
    food_name=curs.fetchone()
    print(food_name)
    if food_name is not None: 
        return True
    else: 
        return False 
        
# gets all the food in the database
def get_all_food(conn):
    sql = '''select fid,food.name from food'''
    curs = dbi.dict_cursor(conn)
    curs.execute(sql)
    return curs.fetchall() 

# # get all the username and full name for students from the database
# def get_all_students(conn):
#     sql = '''select username,student.name from student'''
#     curs = dbi.dict_cursor(conn)
#     curs.execute(sql)
#     return curs.fetchall()

#get a student's comments from the database, given a specific username
def get_all_comments(conn,student):
    sql = '''select comment,entered,fid from feedback where username = %s'''
    curs = dbi.dict_cursor(conn)
    curs.execute(sql,student)
    return curs.fetchall()

#deletes a label for the associated food item
def delete_labels(conn,fid):
    sql = '''delete from labels where fid = %s'''
    curs = dbi.dict_cursor(conn)
    curs.execute(sql,fid)
    conn.commit()
    
#deletes a food item from the food table, given the food id
def delete_food(conn,fid):
    sql = '''delete from food where fid = %s'''
    curs = dbi.dict_cursor(conn)
    curs.execute(sql,fid)
    conn.commit()

#deletes a comment given the username and the time the comment was entered
def delete_comment(conn,username,entered): 
    sql = '''delete from feedback where username = %s and entered = %s'''
    curs = dbi.dict_cursor(conn)
    vals = [username,entered]
    curs.execute(sql,vals)
    conn.commit()

#returns the name of a food given the food id
def get_food(conn,fid): 
    sql = '''select food.name from food where fid=%s'''
    curs = dbi.dict_cursor(conn)
    curs.execute(sql,fid)
    food_name = curs.fetchone()
    food_name = food_name.get('name')
    return food_name

#deletes comments associated with a specific food item
def delete_comments(conn,fid): 
    sql = '''select * from feedback where fid = %s'''
    curs = dbi.dict_cursor(conn)
    curs.execute(sql,fid)
    comments = curs.fetchall()
    if comments is not None: 
        sql = '''delete from feedback where fid = %s'''
        curs = dbi.dict_cursor(conn)
        curs.execute(sql,fid)
        conn.commit()
    


    

    