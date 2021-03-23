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

def lookupMenuList(conn, now):
    '''
        return list of dictionaries of food name, dining hall, fid, ranking for all food matching 
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute("select fid, food.name, diningHall.name as dh from food inner join diningHall using (did);")
    # curs.execute("select food.fid, name, avg(rating) as rating from food inner join feedback using (fid) group by feedback.fid;")
    # ^^ The above code was removed because it then only displays menu items that have a rating
     # where lateServed= %s [now];
    #---------------------------UPDATE to include DH info AND current date --------------------------
    
    menu = curs.fetchall()
    for item in menu:
        fid = item["fid"]
        item['rating'], item['sumRankings'] = avgRating(fid)
    return menu

def filterMenuList(conn, dh, mealtype, label):
    '''
        return list of dictionaries of food name, dining hall, fid, ranking for food
    '''
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

def lookupFoodItem(conn, fid):
    '''
        return dictionary of a food's name, type, description, preference, label given an id
    '''
    curs = dbi.dict_cursor(conn)
    sql = '''select fid, food.name, ingredients, preference, allergen, 
    lastServed, type, avg(rating) as avgRating, count(rating) as countRating, diningHall.name as dh
     from food inner join labels using (fid)
     inner join diningHall using (did)
     inner join feedback using (fid)
     where food.fid = %s
     group by (feedback.fid);'''
    curs.execute(sql, [fid])
    # curs.execute("select name, ingredients, preference, allergen, lastServed type from food inner join labels using (fid) where fid = %s;", [fid])
    return curs.fetchone()

def lookupLastServed(fid):
    '''
        return tuple of a food's last served location, date last served
    '''
    conn = dbi.connect()
    curs = dbi.cursor(conn)
    curs.execute("select diningHall.name, lastServed from food inner join diningHall using (did) where fid = %s;", [fid])
    return curs.fetchone()

def lookupComments(conn, fid):
    '''
        return a list of dictionaries for each comment for a given food item and with the comment's rating and user
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute("select username, rating, comment from feedback where fid = %s;", [fid])
    return curs.fetchall()

def lookupDH(conn, did):
    '''
        return a list of dictionaries for each comment for a given food item and with the comment's rating and user
    '''
    curs = dbi.cursor(conn)
    curs.execute("select name from diningHall where did = %s;", [did])
    return curs.fetchone()

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
