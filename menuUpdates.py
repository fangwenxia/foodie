#module to update foodie database from the menu page

import cs304dbi as dbi

def avgRating(fid):
    '''compute average rating for a given food item, return tuple containing average rating and number of ratings'''
    conn = dbi.connect()
    curs = dbi.cursor(conn)
    curs.execute("select rating from feedback where fid = %s;", [fid])
    ratingsList = curs.fetchall()
    if ratingsList:
        ratingSum, numRatings = 0, 0
        for rating in ratingsList:
            ratingSum += int(rating[0])
            numRatings += 1
        avg = ratingSum/numRatings
        return avg, numRatings
    else:
        return 0,0

def lookupMenuList(now):
    '''
        return list of dictionaries of food name, dining hall, fid, ranking for all food matching 
    '''
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute("select food.fid, name from food;") # where lateServed= %s [now];
    #---------------------------UPDATE to include DH info AND current date --------------------------
    
    menu = curs.fetchall()
    for item in menu:
        fid = item["fid"]
        item['rating'], item['sumRankings'] = avgRating(fid)
    return menu

def filterMenuList(dh, mealtype, label):
    '''
        return list of dictionaries of food name, dining hall, fid, ranking for food
    '''
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    if dh and mealtype: #if the values are both not null
        sql = ("select food.fid, name from food where did = %s and type = %s;")
        values = [dh, mealtype]
    elif dh: #if the value for mealtype is null
        sql = ("select food.fid, name from food where did = %s;")
        values = [dh]
    elif mealtype: #if the value for mealtype is null
        sql = ("select food.fid, name from food where type = %s;")
        values = [mealtype]
    else: #if the value for mealtype and dh is null
        sql = ("select food.fid, name from food;")
    curs.execute(sql, values) # where lateServed= %s [now];
    menu = curs.fetchall()
    for item in menu:
        fid = item["fid"]
        item['rating'], item['sumRankings'] = avgRating(fid)
    return menu

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

def searchMenu(search):
    '''Returns the food items that match the query of all the entries in
the food table, as a list of dictionaries.
    '''
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute("select fid, name from food inner join labels using (fid) where (lower(name) like %s) or (lower(ingredients) like %s);", ['%' + search + '%', '%' + search + '%']) 
    # curs.execute("select fid, name from food inner join labels using (fid) where name like %s or ingredients like %s;", [('%' + search + '%'),('%' + search + '%')]) 
    menu = curs.fetchall()
    for item in menu:
        fid = item["fid"]
        item['rating'], item['sumRankings'] = avgRating(fid)
    return menu