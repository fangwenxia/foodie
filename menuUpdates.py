#module to update foodie database from the menu page

import cs304dbi as dbi

def lookupMenuList(now):
    '''
        return list of dictionaries of food name, dining hall, fid, ranking for all food matching 
    '''
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute("select fid, name, rating from food inner join feedback using (fid) order by rating DESC;") # where lateServed= %s [now];
    #---------------------------UPDATE to include DH info AND current date --------------------------
    return curs.fetchall()

def filterMenuList(dh, mealtype, label):
    '''
        return list of dictionaries of food name, dining hall, fid, ranking for food
    '''
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    if dh and mealtype: #if the values are both not null
        sql = ("select fid, name, rating from food inner join feedback using (fid) where did = %s and type = %s" + 
        "order by rating DESC;")
        values = [dh, mealtype]
    elif dh: #if the value for mealtype is null
        sql = ("select fid, name, rating from food inner join feedback using (fid) where did = %s" + 
        "order by rating DESC;")
        values = [dh]
    elif mealtype: #if the value for mealtype is null
        sql = ("select fid, name, rating from food inner join feedback using (fid) where type = %s" + 
        "order by rating DESC;")
        values = [mealtype]
    else: #if the value for mealtype and dh is null
        sql = ("select fid, name, rating from food inner join feedback using (fid) order by rating DESC;")
    curs.execute(sql, values) # where lateServed= %s [now];
    #---------------------------UPDATE to include DH info AND current date --------------------------
    return curs.fetchall()

def lookupFoodItem(fid):
    '''
        return dictionary of a food's name, type, rating, description, preference, label given an id
    '''
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute("select name, rating, ingredients, preference, allergen, comment, type from food,feedback,labels where food.fid = %s;", [fid])
    #---------------------------UPDATE to include DH info AND current date --------------------------
    return curs.fetchone()
def updateFoodItem(fid, ingredients):
    '''
        edit food item and commit changes
    '''
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute("update labels set ingredients = %s where fid = %s;", [ingredients, fid])
    conn.commit()  

    #---------------------------UPDATE to include DH info AND current date --------------------------