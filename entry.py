import cs304dbi as dbi
from flask import (flash, render_template,url_for)

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
    prefs = ','.join(preferences)
    allgns = ','.join(allergens)
    labelvals = [allgns,prefs,ingredients,id]
    curs2.execute(sql2,labelvals)
    conn.commit()
# checks to see if the name of the food already exists in the database

def exists(conn,name):
    curs = dbi.cursor(conn)
    sql = '''select * from food where name=%s'''
    curs.execute(sql,name)
    food_name=curs.fetchone()
    print(food_name)
    if food_name is not None: 
        return True
    else: 
        return False 
def get_all_food(conn):
    sql = '''select fid,food.name from food'''
    curs = dbi.dict_cursor(conn)
    curs.execute(sql)
    return curs.fetchall() 
def get_all_students(conn):
    sql = '''select username,student.name from student'''
    curs = dbi.dict_cursor(conn)
    curs.execute(sql)
    return curs.fetchall()
def delete_labels(conn,fid):
    sql = '''delete from labels where fid = %s'''
    curs = dbi.dict_cursor(conn)
    curs.execute(sql,fid)
    conn.commit()
def delete_food(conn,fid):
    sql = '''delete from food where fid = %s'''
    curs = dbi.dict_cursor(conn)
    curs.execute(sql,fid)
    conn.commit()
    

    # this function should handle all the empty values
# def handle_empty_values(name,category,dhall,preferences,allergens,ingredients): 
    # if len(name)==0: 
    #     flash("Please enter in the name of the food.")
    #     return render_template('dataentry.html', action=url_for('addfood'))
    # if len(category)==0: 
    #     flash("Please select in the category of the food (breakfast,lunch,dinner or all-day).")
    #     return render_template('dataentry.html', action=url_for('addfood'))
    # if len(dhall)==0: 
    #     flash("Please enter in the dining hall the meal was consumed in.")
    #     return render_template('dataentry.html', action=url_for('addfood'))
    # if len(preferences)==0: 
    #     flash("Please select in the food's associated preferences (i.e. vegan)")
    #     return render_template('dataentry.html', action=url_for('addfood'))
    # if len(allergens)==0: 
    #     flash("Please select in the food's associated allergies (i.e. peanuts)")
    #     return render_template('dataentry.html', action=url_for('addfood'))
    # if ingredients == '': 
    #     flash("Please enter in the food's ingredients.")
    #     return render_template('dataentry.html', action=url_for('addfood'))
    