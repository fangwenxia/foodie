#module to update foodie database from the menu page

import cs304dbi as dbi

def avgRating(conn, fid):
    '''compute average rating for a given food item, return tuple containing average rating and number of ratings
    Implemented this using Python rather than MySQL because of an issue when joining the table 
    that contains the list of food items and the table that contains the ratings and reviews for 
    those items. Essentially, because not every food has a rating (ie does not exist in the 
    feedback table), by using MySQL, only food items that have been rated are returned. 
    Hence, the complex code that manually adds a rating value to the dictionary.'''
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
    curs.execute('''select fid, food.name, diningHall.name as dh from food inner join diningHall 
    using (did) where lastServed = %s;''', [now])
    # curs.execute("select food.fid, name, avg(rating) as rating from food inner join feedback using (fid) group by feedback.fid;")
    # ^^ The above code was removed because it then only displays menu items that have a rating
     # where lateServed= %s [now];
    menu = curs.fetchall()
    '''The following for loop is used to ensure that every value in the food table has a rating
    to display on the menu page, even if the food item does not yet exist in the feedback table.
    In this way, the default rating can be set to 0 rather than NULL as is done with an outer join in MySQL'''
    for item in menu:
        fid = item["fid"]
        item['rating'], item['sumRankings'] = avgRating(conn, fid)
    return sorted(menu, reverse = True, key = lambda i: i['rating'])

def filterMenuList(conn, dh, mealtype, label, now):
    '''
        return list of dictionaries of food name, dining hall, fid, ranking for food
    '''
    curs = dbi.dict_cursor(conn)
    preference = ["%" + label + "%"]
    if label: #case where a user filters by label and the value of label is not null
        #case where a user filters by label, dining hall, and meal type
        if dh and mealtype: 
            sql = '''select food.fid, name from food inner join labels using (fid)
             where did = %s and type = %s and preference like %s and lastServed = %s;'''
            values = [dh, mealtype, preference, now]
        #case where a user filters by label and dining hall
        elif dh: #if the value for mealtype is null
            sql = ("select food.fid, name from food inner join labels using (fid) where did = %s and preference like %s and lastServed = %s;")
            values = [dh, preference, now]
        #case where a user filters by label and meal type
        elif mealtype:
            sql = ("select food.fid, name from food inner join labels using (fid) where type = %s and preference like %s and lastServed = %s;")
            values = [mealtype, preference, now]
        #case where a user filters by label only
        else:
            sql = ("select food.fid, name from food inner join labels using (fid) where preference like %s and lastServed = %s;")
            values = [preference, now]
    #case where a user does not select a preference to filter by
    elif not label:
        #case where a user does not select a preference to filter by, but filters by dining hall and meal type
        if dh and mealtype: #if the values are both not null
            sql = ("select food.fid, name from food where did = %s and type = %s and lastServed = %s;")
            values = [dh, mealtype, now]
        #case where a user does not select a preference to filter by, but filters by dining hall
        elif dh:
            sql = ("select food.fid, name from food where did = %s and lastServed = %s;")
            values = [dh, now]
        #case where a user does not select a preference to filter by, but filters by meal type
        elif mealtype:
            sql = ("select food.fid, name from food where type = %s and lastServed = %s;")
            values = [mealtype, now]
    #case where the user clicks the filter button without selecting any filters
    else: 
        sql = ("select food.fid, name from food where lastServed = %s;")
        values = [now]
    curs.execute(sql, values) # where lateServed= %s [now];
    menu = curs.fetchall()
    '''The following for loop is used to ensure that every value in the food table has a rating
    to display on the menu page, even if the food item does not yet exist in the feedback table.
    In this way, the default rating can be set to 0 rather than NULL as is done with an outer join in MySQL'''
    for item in menu:
        fid = item["fid"]
        item['rating'], item['sumRankings'] = avgRating(conn, fid)
    return sorted(menu, reverse = True, key = lambda i: i['rating'])

def lookupFoodItem(conn, fid):
    '''
        return dictionary of a food's name, type, description, preference, label given an id
    '''
    curs = dbi.dict_cursor(conn)
    sql = '''select fid, food.name, ingredients, preference, allergen, 
    lastServed, type, diningHall.name as dh
     from food inner join labels using (fid)
     inner join diningHall using (did)
     where food.fid = %s'''
    #  the following code only renders results for food items in the feedback table
    #  '''select fid, food.name, ingredients, preference, allergen, 
    # lastServed, type, avg(rating) as avgRating, count(rating) as countRating, diningHall.name as dh
    #  from food inner join labels using (fid)
    #  inner join diningHall using (did)
    #  inner join feedback using (fid)
    #  where food.fid = %s
    #  group by (feedback.fid);'''
    curs.execute(sql, [fid])
    # curs.execute("select name, ingredients, preference, allergen, lastServed type from food inner join labels using (fid) where fid = %s;", [fid])
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
        return name of dining hall based of off did
    '''
    curs = dbi.cursor(conn)
    curs.execute("select name from diningHall where did = %s;", [did])
    return curs.fetchone()

def updateFoodItem(conn, fid, ingredients):
    '''
        edit food item and commit changes
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute("update labels set ingredients = %s where fid = %s;", [ingredients, fid])
    conn.commit()

def updateFoodItem(conn, fid, waittime):
    '''
        Update dining hall's wait time
    '''
    curs = dbi.cursor(conn)
    curs.execute("update diningHall set waitTime = %s where did = %s;", [waittime, fid])
    conn.commit()

def updateLastServed(conn, fid, now):
    '''
        Adding a food to today's menu by updating last served date
    '''
    curs = dbi.cursor(conn)
    curs.execute("update food set lastServed = %s where fid = %s;", [now, fid])
    conn.commit()

def searchMenu(conn, search):
    '''Returns the food items that match the query of all the entries in
the food table, as a list of dictionaries.
    '''
    curs = dbi.dict_cursor(conn)
    curs.execute("select fid, name from food inner join labels using (fid) where lower(name) like %s or lower(ingredients) like %s group by fid;", ['%' + search + '%', '%' + search + '%']) 
    menu = curs.fetchall()
    '''The following for loop is used to ensure that every value in the food table has a rating
    to display on the menu page, even if the food item does not yet exist in the feedback table.
    In this way, the default rating can be set to 0 rather than NULL as is done with an outer join in MySQL'''
    for item in menu:
        fid = item["fid"]
        item['rating'], item['sumRankings'] = avgRating(conn, fid)
    return menu

def getWaittime(conn, did):
    curs = dbi.cursor(conn)
    curs.execute("select waitTime from diningHall where did = %s", [did])
    return curs.fetchone()