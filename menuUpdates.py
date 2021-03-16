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
        return list of dictionaries of food name, dining hall, fid, ranking for all food matching 
    '''
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    curs.execute("select fid, name, rating from food inner join feedback using (fid) where did = %s and type = %s" + 
    "order by rating DESC;", [dh, mealtype]) # where lateServed= %s [now];
    #---------------------------UPDATE to include DH info AND current date --------------------------
    return curs.fetchall()