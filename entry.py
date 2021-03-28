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
def insert_label(conn,allergens,preferences,ingredients,id): 
    curs2 = dbi.cursor(conn)
    sql2 = '''insert into labels(allergen,preference,ingredients,fid) values (%s,%s,%s,%s);'''
    labelvals = [allergens,preferences,ingredients,id]
    print(labelvals)
    curs2.execute(sql2,labelvals)
    conn.commit()