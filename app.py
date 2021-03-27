from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

import cs304dbi as dbi
import menuUpdates as menuUp #module to update foodie database from the menu page
import random
import sys
import pymysql
import feed_queries
import query

from datetime import date,datetime

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
# file upload content 
app.config['UPLOADS'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1*1024*1024 # 1 MB

def today():
    """Returns a tuple with the string for the current day and time (SQL format)
    and a string for the day/time for display purposes. This is used to primarily to query the database according
    to the lastServed date for a given food item.
    """
    now = date.today()
    return now.strftime("%Y-%m-%d"), now.strftime("%A, %B %d")

@app.route('/pic/<int:fid>') 
#route to image for food photos, can later be generalized and applied to other photos too
def pic(fid):
    conn = dbi.connect()
    curs = dbi.cursor(conn)
    sql = '''select filename from foodPics where fid = %s'''
    curs.execute(sql, [fid])
    try:
        filename = curs.fetchone()[0]
        return send_from_directory(app.config['UPLOADS'],filename)
    except Exception as err: #in the case when there is not yet a photo uploaded
        return None

@app.route('/')
def home():
    # the base template needs only one filler
    return render_template('home.html',title='foodie.')

@app.route('/form/')
def form():
    return render_template('form.html')
@app.route('/mainmenu/')
def mainmenu():
    '''Page with menu and form without any filters'''
    conn = dbi.connect()
    menu = menuUp.lookupMenuList(conn, today()[0])
    return render_template('menu.html',date=today()[1], menu = menu, title ="Menu")

@app.route('/menu/', methods=["GET", "POST"])
def menu():
    conn = dbi.connect()
    if request.method == 'GET':
        # mealtype = ""
        dh = request.args.get('dh-filter', "")
        mealtype = request.args.get("type-filter", "")
        preference = request.args.getlist("preference")
        now = today()[0]
            
        if preference:
            preference = ",".join(preference)
        else:
            preference = ""
        if dh:
            dhName = menuUp.lookupDH(conn, dh)[0]
            waitTime = menuUp.getWaittime(conn, int(dh))[0]
        else:
            dhName = ""
            waitTime = ""
        # IMPLEMENT SEARCH BY LABEL label = ""
        search = request.args["query"]
        # the variable date = today()[] generates the current date to display on the menu page
        if dh == '3' or dh == '4':
            flash("So sorry to be the bearer of bad news, but {} is closed today.".format(dhName))
        if dh or mealtype or preference: #if given a dining hall request and mealtype
            menu = menuUp.filterMenuList(conn, dh, mealtype,preference,now)
        elif search:
            menu = menuUp.searchMenu(conn, search)
            print(menu)
            if len(menu)==1:
                # if there's only one matching result, redirect directly to the food page 
                fid=menu[0]['fid']
                return redirect(url_for('food',fid=int(fid)))
            elif len(menu)==0:
                flash("The name you entered does not match any dish in the databse. \
                    Wold you like to add a new food entry? ")
                return redirect(url_for('addfood'))
            else: 
                flash("Your entry matched multiple entries. Pick from one of the below. ")
        else: #if not given a dining hall request or a mealtype request
            menu = menuUp.lookupMenuList(conn, today()[0])
        return render_template('menu.html',date=today()[1], location = dhName, type = mealtype, menu = menu, title ="Menu", waitTime = waitTime)
    # else: if we decide to add a post method to our menu

#for beta: how do I pass in the fid for processing too? 
@app.route('/autocomplete',methods=['GET'])
def autocomplete():
    conn = dbi.connect()
    # keyword to search: q is from jQuery, looking for 'q'
    search=request.args.get('q')
    # returns a list of dictionary of fid and food name
    dishes=menuUp.searchMenu(conn,search)
    #gets only the food name list 
    results=[entry["name"] for entry in dishes]
    # jsonify makes the list of food names in a JavaScript format
    return jsonify(matching_results=results)

@app.route('/food/<int:fid>', methods=["GET", "POST"])
def food(fid):
    conn = dbi.connect()
    if request.method == 'GET':
        # dictionary containing a food's name, ingredients, preference, allergen, type
        item = menuUp.lookupFoodItem(conn, fid)
        #average rating and number of ratings given to a food item
        avgRating, totalRatings = menuUp.avgRating(conn, fid) 
        # list of dictionaries for each comment for a given food item and with the comment's rating and user
        comments = menuUp.lookupComments(conn, fid)
        filename = pic(fid)
        return render_template('food.html', food = item, comments = comments, fid = fid, rating = avgRating, title = item["name"], filename = filename)

@app.route('/updateFood/<int:fid>', methods=["GET","POST"])
# name, type, rating, description, preference, label
def updateFood(fid):
    conn = dbi.connect()
    if request.method == "GET":
        item = menuUp.lookupFoodItem(conn, fid)
        return render_template('foodUpdate.html', food = item, title = ("Update " + item["name"]))
    elif request.form["submit"] == "update":
        try:
            ingredients = request.form["ingredients"]
            menuUp.updateFoodItem(conn, fid, ingredients)
            item = menuUp.lookupFoodItem(conn, fid)
            flash("Thank you for updating {}, we really appreciate it!".format(item['name']))
            avgRating, totalRatings = menuUp.avgRating(conn, fid)
            comments = menuUp.lookupComments(conn,fid)
            return render_template('food.html', food = item, comments = comments, fid = fid, rating = avgRating)
        except Exception as err:
            flash('Update failed {why}'.format(why=err))
            return render_template('foodUpdate.html', food = item, title = ("Update " + item["name"]))
    else:
        try:
            item = menuUp.lookupFoodItem(conn, fid)
            flash("Thank you for updating {}, we really appreciate it!".format(item['name']))
            avgRating, totalRatings = menuUp.avgRating(conn, fid)
            comments = menuUp.lookupComments(conn,fid)
            f = request.files['pic']
            user_filename = f.filename
            ext = user_filename.split('.')[-1]
            filename = secure_filename('{}.{}'.format(fid,ext))
            pathname = os.path.join(app.config['UPLOADS'],filename)
            f.save(pathname)
            curs = dbi.dict_cursor(conn)
            curs.execute(
                '''insert into foodPics(fid,filename) values (%s,%s)
                   on duplicate key update filename = %s''',
                [fid, filename, filename])
            conn.commit()
            flash('Upload successful.')
            return render_template('food.html', food = item, comments = comments, fid = fid, rating = avgRating)
        except Exception as err:
            flash('Update failed {why}'.format(why=err))
            item = menuUp.lookupFoodItem(conn, fid)
            return render_template('foodUpdate.html', food = item, title = ("Update " + item["name"]))


# Gigi's Stuff!!
@app.route('/create/', methods=["GET", "POST"]) 
def create():   
    if request.method == 'GET':
        return render_template(
            'create.html', 
            )
    else:
        # next three lines takes user input from form and stores in variables
        name = request.form['name'] 
        username = request.form['username'] 
        password = request.form['password'] 
        favoriteDH = request.form['diningHall'] 
        classYear = request.form['year'] 

        conn = dbi.connect()

        # next helper function checks to see if username is already in database and prompts user to log in instead 
        if query.username_exists(conn, username): 
            flash('This username already exists. If this is you, please log in. \
                If not, please enter your Wellesley email username.')
            return redirect(url_for('login')) 
        
        # if username doesn't exist, user is added to database and can now log in
        else: 
            query.add_username(conn, name, username, password, favoriteDH, classYear) # used to be add_username, tt, title,  release
            flash('Profile was created successfully! You can now log in')
            return redirect(url_for('login')) 

# allows user to log in
@app.route('/login/', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template(
            'create.html'
            )
    # form gets user inputs and stores into variables
    else:
        username = request.form['username'] 
        password = request.form['password'] 
        conn = dbi.connect()
        # helper function checks to make sure username exists in database
        if query.username_exists(conn, username): 
            curs = dbi.dict_cursor(conn)

            # query finds password saved in database to compare with user input
            curs.execute ('''select username, password 
                            from student
                            where username = %s''', [username])
            user = curs.fetchone()
            
            # checks if user input matches password on file
            check_pass = user['password']
            if check_pass  == password:
                flash('Successfully logged in.')
                # print(check_pass, password)
                return redirect(url_for('profile', username=username))
            else:
                flash('Incorrect login. Please try again.')
                return redirect(url_for('login'))

        # if username doesn't exist in database, user is let known
        else: 
            flash('This username does not exist. Please create an account.')
            return redirect(url_for('create')) 

# allows user to see their profile
# how to get actual text instead of values for DH and Classyear 
@app.route('/profile/<username>', methods=['GET','POST'])
def profile(username):
    if request.method == 'GET':
        conn = dbi.connect()
        info = query.get_user_info(conn,username)
        return render_template('profile.html',  
                                info=info,
                                username=username)
    else:
        return render_template('home.html')
        
# should allow user to update profile information. doesn't work yet. ?!?!
@app.route('/update/<username>', methods = ["GET", "POST"])
def update(username):
    conn = dbi.connect()
    info = query.get_user_info(conn, username)
    if request.method == "GET":
        # flash('Profile was updated successfully!')
        return render_template('update.html', 
                                username=username, 
                                info=info)
    else:
        query.update_profile(conn, username, info)
        flash("Successfully updated your profile!")
        return render_template('update.html', 
                                conn=conn,
                                username=username, 
                                info=info)

# temporary solution for catching broken link error
# better way of doing this ?!?!
@app.route('/profile/', methods = ["GET", "POST"])
def profile_error():
    flash("Please log in to see your profile.")
    return render_template('create.html')

# temporary solution for catching broken link error
# better way of doing this ?!?!
@app.route('/update/', methods = ["GET", "POST"])
def username_error():
    flash("Please log in to update your profile.")
    return render_template('create.html')

## Here's the route to entering a feedback form
@app.route('/reviews/<int:fid>',methods=['POST','GET'])
def reviews(fid):
    conn=dbi.connect()
    if request.method=='GET':
        # get the form to display 
        name=feed_queries.search_fid(conn,fid)['name']
        return render_template('feed.html',name=name, fid = fid)
    else:
        # get the input form values from the submitted form
        username=request.form['user']
        #to gigi: how do I link the user here? 
        if len(feed_queries.search_user(conn,username))==0:
            # Because the username is not complete, temp is used for flashing tempoararily 
            # to show available usernames you can possibly input
            temp=[person["username"] for person in feed_queries.temp_user(conn)]
            flash('Username Under Construction:only enter below for usernames:' )
            flash(temp)
            return render_template('feed.html')
        rating=request.form['rating']
        comment=request.form['comment']
        time=datetime.now()
        # stored form info into the database here
        feed_queries.feedback(conn,username,fid,rating,comment,time)
        return redirect(url_for('feed'))

@app.route('/feed/')     
def feed(): #rename review() to feed
    conn=dbi.connect()
    feedbacks= feed_queries.recent_feedback(conn)
    top_rated=feed_queries.food_rating(conn)
    for item in top_rated:
        item['avg']=str(item['avg'])
    return render_template('reviews.html',feedbacks=feedbacks,ranking=top_rated)

    # LEAH's STUFF
'''
def handleErrors(name,category,hall,preferences,allergens,ingredients): 
    message="hello"
    return message
'''
@app.route('/addfood/', methods=["GET", "POST"])
def addfood():
    if request.method == 'GET':
        return render_template('dataentry.html', action=url_for('addfood'))
    elif request.method == 'POST':
        food_name = request.form.get('food-name') 
        food_category = request.form.get('food-type')
        food_dhall = request.form.get('food-hall')
        food_preferences = request.form.get('food-preferences')
        food_allergens = request.form.get('food-allergens')
        food_ingredients = request.form.get('food-ingredients')
        print([food_name,food_category,food_dhall,food_preferences,food_allergens,food_ingredients])
        error_messages = []
        #message = handleErrors(food_name,food_category,food_dhall,food_preferences,food_allergens,food_ingredients)
        # message = ""
        # if food_name is None: 
        #     message = "missing input: Food name is missing."
        # elif food_category is None: 
        #     message = "missing input: Food category is missing."
        # elif food_dhall is None:
        #     message = "missing input: Food dining hall is missing."
        # elif food_preferences is None:
        #     message = "missing input: Food preferences is missing."
        # elif food_allergens is None: 
        #     message = "missing input: Food allergens is missing."
        # elif food_ingredients is None: 
        #     message = "missing ingredients: Food ingredients are missing."
        # error_messages.append(message)
        # if len(error_messages) > 0:
        #     return render_template('dataentry.html', action=url_for('addfood'), messages=error_messages)
        # print("form submission successful.")

        #insert stuff into database
        connect = dbi.connect()
        print("connected!")
        curs = dbi.cursor(connect)
        sql = '''insert into food(name,lastServed,type,did) 
                  values (%s,%s,%s,%s);'''
        food_date = today()[0]
        vals = [food_name,food_date,food_category,food_dhall]
        curs.execute(sql,vals)
        connect.commit()
        print("success!")
        success_message = "Food {fname} inserted".format(fname=food_name)
        print(success_message)

        curs1 = dbi.cursor(connect)
        sql = '''select fid from food where name=%s'''
        curs1.execute(sql,food_name)
        food_id = curs1.fetchone()[0]
        print(food_id)

        curs2 = dbi.cursor(connect)
        sql2 = '''insert into labels(allergen,preference,ingredients,fid) 
                  values (%s,%s,%s,%s);'''
        labelvals = [food_allergens,food_preferences,food_ingredients,food_id]
        print(labelvals)
        curs2.execute(sql2,labelvals)
        connect.commit()

        print("label inserted")
        
        # added successful flashing functionality from most recent version of app.py
        flash(success_message)

        return redirect(url_for('addfood',msg=success_message,action='addfood'))
        
    
@app.before_first_request
def init_db():
    dbi.cache_cnf()
    dbi.use('foodie_db')  

if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
        # port = 7739
    app.debug = True
    app.run('0.0.0.0',port)
