#module to update foodie database from the menu page

import cs304dbi as dbi

def lookupMenuList(now):
    '''
        return list of dictionaries of food name, dining hall, fid, ranking for all food matching 
    '''
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute("select food.fid, name, avg(rating) from food inner join feedback using (fid) group by feedback.fid order by avg(rating) DESC;") # where lateServed= %s [now];
    #---------------------------UPDATE to include DH info AND current date --------------------------
    return curs.fetchall()

def filterMenuList(dh, mealtype, label):
    '''
        return list of dictionaries of food name, dining hall, fid, ranking for food
    '''
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    if dh and mealtype: #if the values are both not null
        sql = ("select food.fid, name, avg(rating) from food inner join feedback using (fid) where did = %s and type = %s" + 
        "group by feedback.fid order by avg(rating) DESC;")
        values = [dh, mealtype]
    elif dh: #if the value for mealtype is null
        sql = ("select food.fid, name, avg(rating) from food inner join feedback using (fid) where did = %s" + 
        "group by feedback.fid order by avg(rating) DESC;")
        values = [dh]
    elif mealtype: #if the value for mealtype is null
        sql = ("select food.fid, name, avg(rating) from food inner join feedback using (fid) where type = %s" + 
        "group by feedback.fid order by avg(rating) DESC;")
        values = [mealtype]
    else: #if the value for mealtype and dh is null
        sql = ("select food.fid, name, avg(rating) from food inner join feedback using (fid) group by feedback.fid order by avg(rating) DESC;")
    curs.execute(sql, values) # where lateServed= %s [now];
    return curs.fetchall()

def lookupFoodItem(fid):
    '''
        return dictionary of a food's name, type, description, preference, label given an id
    '''
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute("select name, ingredients, preference, allergen, type from food inner join labels using (fid) where fid = %s;", [fid])
    return curs.fetchone()

def lookupLastServed(fid):
    '''
        return tuple of a food's last served location, date last served
    '''
    conn = dbi.connect()
    curs = dbi.cursor(conn)
    curs.execute("select diningHall.name, lastServed from food inner join diningHall using (did) where fid = %s;", [fid])
    return curs.fetchone()

def avgRating(fid):
    '''compute average rating for a given food item, return tuple containing average rating and number of ratings'''
    conn = dbi.connect()
    curs = dbi.cursor(conn)
    curs.execute("select rating from feedback where fid = %s;", [fid])
    ratingsList = curs.fetchall()
    ratingSum, numRatings = 0, 0
    for rating in ratingsList:
        ratingSum += rating
        numRatings += 1
    avg = ratingSum/numRatings
    return avg, numRatings


def lookupComments(fid):
    '''
        return a list of dictionaries for each comment for a given food item and with the comment's rating and user
    '''
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute("select username, rating, comment from feedback where fid = %s;", [fid])
    return curs.fetchall()

def updateFoodItem(fid, ingredients):
    '''
        edit food item and commit changes
    '''
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute("update labels set ingredients = %s where fid = %s;", [ingredients, fid])
    conn.commit()