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
import bcrypt
from flask_cas import CAS
from datetime import date,datetime

CAS(app)

app.config['CAS_SERVER'] = 'https://login.wellesley.edu:443'
app.config['CAS_LOGIN_ROUTE'] = '/module.php/casserver/cas.php/login'
app.config['CAS_LOGOUT_ROUTE'] = '/module.php/casserver/cas.php/logout'
app.config['CAS_VALIDATE_ROUTE'] = '/module.php/casserver/serviceValidate.php'
app.config['CAS_AFTER_LOGIN'] = 'profile_error' # use regular username or cas_username also how to do that?
# the following doesn't work :-(
app.config['CAS_AFTER_LOGOUT'] = 'http://cs.wellesley.edu:1945/'

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

def today():
    """Returns a tuple with the string for the current day and time (SQL format)
    and a string for the day/time for display purposes

    The output is in something close to Internet format. It's not really
    Internet format because it neither converts to UTC nor
    appends the time zone.  However, it will work nicely for MySQL.
    """
    now = date.today()
    return now.strftime("%Y-%m-%d"), now.strftime("%A, %B %d")

@app.route('/')
def home():
    # the base template needs only one filler
    return render_template('home.html',title='foodie.')

@app.route('/form/')
def form():
    return render_template('form.html')

@app.route('/menu/', methods=["GET", "POST"])
def menu():
    if request.method == 'GET':
        menu = menuUp.lookupMenuList(today()[0])
        return render_template('menu.html',date=today()[1], menu = menu, title ="Menu")
    else:
        dh = request.form["dh-filter"]
        mealtype = request.form["type-filter"]
        label = ""
        search = request.form["query"]
        if dh and mealtype: #if given a dining hall request and mealtype
            if int(dh) == 3 or int(dh) == 4: #message for Pom and Stone-D, which are closed
                flash("We're sorry. Pom and Stone-D are closed this year. Why don't you try another dining hall?")
                menu = menuUp.filterMenuList(None, mealtype,None)
            else:
                menu = menuUp.filterMenuList(dh, mealtype,None)
        elif dh: #if given dining hall but not meal type
            if int(dh) == 3 or int(dh) == 4: #message for Pom and Stone-D, which are closed
                flash("We're sorry. Pom and Stone-D are closed this year. Why don't you try another dining hall?")
                menu = menuUp.lookupMenuList(today()[0])
                # menu = menuUp.filterMenuList(None, None ,None)
            else:
                menu = menuUp.filterMenuList(dh, None,None)
        elif mealtype: #if given meal type but not dining hall
            menu = menuUp.filterMenuList(None, mealtype,None)
        elif search:
            menu = menuUp.searchMenu(search)
        else:#if not given a dining hall request or a mealtype request
            menu = menuUp.lookupMenuList(today()[0])
        return render_template('menu.html',date=today()[1], type=mealtype, menu = menu, title ="Menu")

@app.route('/food/<int:fid>', methods=["GET", "POST"])
def food(fid):
    if request.method == 'GET':
        item = menuUp.lookupFoodItem(fid) # dictionary containing a food's name, ingredients, preference, allergen, type
        avgRating, totalRatings = menuUp.avgRating(fid) #average rating and number of ratings given to a food item
        dh, lastServedDate = menuUp.lookupLastServed(fid) #the date the food item was most recently served and the dining hall it was served at
        comments = menuUp.lookupComments(fid) # list of dictionaries for each comment for a given food item and with the comment's rating and user
        return render_template('food.html', name = item["name"], type = item["type"], 
        rating = avgRating, comments = comments, description = item["ingredients"], 
        preference = item["preference"], labels = (item["allergen"]).split(","), 
        title = item["name"], fid = fid, dh = dh)
    else:
        item = menuUp.lookupFoodItem(fid) # dictionary containing a food's name, ingredients, preference, allergen, type
        avgRating, totalRatings = menuUp.avgRating(fid) #average rating and number of ratings given to a food item
        dh, lastServedDate = menuUp.lookupLastServed(fid) #the date the food item was most recently served and the dining hall it was served at
        comments = menuUp.lookupComments(fid) # list of dictionaries for each comment for a given food item and with the comment's rating and user
        return render_template('food.html', name = item["name"], type = item["type"], 
        rating = avgRating, comments = comments, description = item["ingredients"], 
        preference = item["preference"], labels = (item["allergen"]).split(","), 
        title = item["name"], fid = fid, dh = dh)

@app.route('/updateFood/<int:fid>', methods=["GET","POST"])
# name, type, rating, description, preference, label
def updateFood(fid):
    if request.method == "GET":
        item = menuUp.lookupFoodItem(fid)
        dh, lastServedDate = menuUp.lookupLastServed(fid)
        return render_template('foodUpdate.html', name = item["name"], dh = dh, lastServed = lastServedDate, description = item["ingredients"], title = item["name"], fid = fid)
    else:
        ingredients = request.form["ingredients"]
        menuUp.updateFoodItem(fid, ingredients)
        item = menuUp.lookupFoodItem(fid) # dictionary containing a food's name, ingredients, preference, allergen, type
        flash("Thank you for updating {}, we really appeciate it!".format(item['name']))
        avgRating, totalRatings = menuUp.avgRating(fid) #average rating and number of ratings given to a food item
        dh, lastServedDate = menuUp.lookupLastServed(fid) #the date the food item was most recently served and the dining hall it was served at
        comments = menuUp.lookupComments(fid) # list of dictionaries for each comment for a given food item and with the comment's rating and user
        return render_template('food.html', name = item["name"], type = item["type"], 
        rating = avgRating, comments = comments, description = item["ingredients"], 
        preference = item["preference"], labels = (item["allergen"]).split(","), 
        title = item["name"], fid = fid, dh = dh)







################################################################################################
################################################################################################
################################################################################################

# Gigi's Stuff!!
@app.route('/create/', methods=["GET", "POST"]) 
def create():
    if request.method ==  "GET":
        return render_template('create.html')
    else:
        name = request.form['name']
        username = request.form['username']
        passwd1 = request.form['password1']
        passwd2 = request.form['password2']
        if passwd1 != passwd2:
            flash('passwords do not match. please try again.')
            return render_template('create.html')
        hashed = bcrypt.hashpw(passwd1.encode('utf-8'),
                               bcrypt.gensalt())
        hashed_str = hashed.decode('utf-8')
        conn = dbi.connect()
        curs = dbi.cursor(conn)
        # next helper function checks to see if username is already in database and prompts user to log in instead 
        if query.username_exists(conn, username): 
            flash('This username already exists. If this is you, please log in. \
                If not, please enter your Wellesley email username.')
            return render_template('create.html')
        
        # if username doesn't exist, user is added to database and can now log in
        else: 
            query.add_username(conn, name, username, passwd1, hashed_str) # used to be add_username, tt, title,  release
            flash('Profile was created successfully! You can post, review and more!')
            return redirect(url_for('menu')) 
        curs.execute('select last_insert_id()') # whats this ?!?!
        row = curs.fetchone()
        session['username'] = username
        session['logged_in'] = True        
        return redirect( url_for('menu') )

    # except Exception as err:
    #     flash('form submission error 1 '+str(err))
    #     return render_template('create.html')

def create_CAS():
    flash('Profile was created successfully! You can post, review and more!')
    return redirect( url_for('home') )



# allows user to log in
@app.route('/user_login/', methods=["GET", "POST"])
def user_login():
    if request.method ==  "GET":
        return render_template('create.html')
    else:
        username = request.form['username'] 
        passwd = request.form['password'] 
        conn = dbi.connect()
        curs = dbi.dict_cursor(conn)
        # helper function checks to make sure username exists in database
        if query.username_exists(conn, username): 
            # query finds password saved in database to compare with user input
            curs.execute('select username, hashed \
                        from student \
                        where username = %s;', [username])
            user = curs.fetchone()
            # checks if user input matches password on file
            hashed = user['hashed']
            hashed2 = bcrypt.hashpw(passwd.encode('utf-8'),
                                    hashed.encode('utf-8'))
            hashed2_str = hashed2.decode('utf-8')
            if hashed2_str  == hashed:
                flash('Successfully logged in.')
                
                if '_CAS_TOKEN' in session:
                    token = session['_CAS_TOKEN']
                if 'CAS_ATTRIBUTES' in session:
                    attribs = session['CAS_ATTRIBUTES']
                if 'CAS_USERNAME' in session:
                    is_logged_in = True
                    username = session['CAS_USERNAME']
                else:
                    if username is None:
                        redirect(url_for('profile'))
                    else:
                        is_logged_in = True
                        session['username'] = username
                    # username = None
                session['username'] = username
                session['logged_in'] = True              
                return redirect(url_for('profile', username=username))
            else:
                flash('Incorrect login. Please try again.')
                return redirect(url_for('user_login'))
        else:
            flash("This username doesn't exist. Please try again.")
            return render_template('create.html')

def login_CAS():
    flash('successfully logged in!')
    return redirect( url_for('home') )

    # except Exception as err:
    #     flash('This username does not exist. Please create an account.')
    #     return redirect('create')

# temporary solution for catching broken link error
# better way of doing this ?!?!
@app.route('/profile/', methods = ["GET", "POST"])
def profile_error():
    sessvalue = request.cookies.get('session')
    if sessvalue is None:
        print("SHOULD GO TO LOGIN HERE")
        return redirect(url_for('cas.login'))
    else:
        if 'CAS_USERNAME' in session:            
            #check to see if 'CAS_USERNAME' in data base
            #if in database:
            username = session['CAS_USERNAME']
            conn = dbi.connect()
            curs = dbi.cursor(conn)
            if query.username_exists(conn, username):
                print("HEHEHEHE USERNAME", username)
                return redirect(url_for('profile', username=username))
            else:
                flash("Looks like  you don't have an account yet, let's make one first.")
                return redirect(url_for('create'))
        else: 
                #need to create account
            if request.method == 'GET':
                if 'username' in session:
                    username = session['username']
                    print("ONCE AGAINNNN",username)
                    print("AND AGAINNNN SESSION:",session)
                    return redirect(url_for('profile', username=username))
                print('GETTTT')
            elif request.method == 'POST':
                print('POSTTTTT')
            else:
                print('WHATS GOING ONNNN')
            print("THIS IS WHERE YOU NEED TO CREATE", sessvalue)
            return redirect(url_for('create'))


# allows user to see their profile
# how to get actual text instead of values for DH and Classyear 
@app.route('/profile/<username>', methods=['GET','POST'])
def profile(username):
    sessvalue = request.cookies.get('session')
    print('WHAT ARE THESE SESSIONS', session)
    print('Session keys1: ',list(session.keys()))
    user = session.get('user', {'name': "None", 'year': "None", 'diningHall': None, 'favoriteFood': None})

    conn = dbi.connect()
    info =  query.get_user_info(conn, username)
    for k in list(session.keys()):
        print(k,' => ',session[k])
    if 'CAS_USERNAME' in session:
        is_logged_in = True
        username = session['CAS_USERNAME']
        print(('CAS_USERNAME is: ',username))
    elif 'username' in session:
        is_logged_in = True
        username = session['username']
        print("THREEEEEE",username, "WOOHOO SESSION", session, type(session), "WOOHOO USER",  user, type(user))
        # name = user['name']
        session['user'] = user
    else:
        is_logged_in = False
        username = None
        print('CAS_USERNAME is STILL not in the session')
        session['user'] = user
    return render_template('profile.html',
                           username=username,
                           is_logged_in=is_logged_in,
                           cas_attributes = session.get('CAS_ATTRIBUTES'),
                        #    name=name,
                        #    year=year,
                        #    diningHall=diningHall,
                        #    favoriteFood=favoriteFood,
                           session=session,
                        #    name=session['name'],
                           sessvalue=sessvalue,
                           user=user,
                           info=info)
# @app.route('/logout', methods = ["GET", "POST"])
# def logout():
#     logout_user = session.get('logout',)
#     is_logged_in = False
#     print("LOGOUT SESSION", session)
#     return redirect(url_for('home.html'))
        
# should allow user to update profile information. doesn't work yet. ?!?!
@app.route('/update/<username>', methods = ["GET", "POST"])
def update(username):
    conn = dbi.connect()
    info = query.get_user_info(conn, username)
    if request.method == "POST":
        # flash('Profile was updated successfully!')
        name2 = request.form['name']
        year2 = request.form['year']
        diningHall2 = request.form['diningHall']
        favoriteFood2 = request.form['favoriteFood']
        query.update_profile(conn, username, name2, year2, diningHall2, favoriteFood2)
        info = query.get_user_info(conn, username)
        flash("Successfully updated your profile!")
        return redirect(url_for('profile', 
                                username=username, 
                                info=info,
                                cas_attributes = session.get('CAS_ATTRIBUTES')))
    else:
        sessvalue = request.cookies.get('session')
        user = session.get('user', {'name': None, 'year': None, 'diningHall': None, 'favoriteFood': None})
        info = query.get_user_info(conn, username)
        name = info['name']
        year = info['classYear']        
        diningHall = info['favoriteDH']
        favoriteFood = info['favoriteFood']
        session['user'] =  user
        return render_template('update.html', username=username, info=info)
def upload(username):
    # profile picture upload
    # f = request.files['propic']
    # user_filename = f.filename
    # ext = user_filename.split('.')[-1]
    # filename = secure_filename('{}.{}'.format(fid,ext))
    # pathname = os.path.join(app.config['UPLOADS'],filename)
    # f.save(pathname)
    # curs = dbi.dict_cursor(conn)
    # curs.execute(
    #         '''insert into proPics(username,filename) values (%s,%s)
    #            on duplicate key update filename = %s''',
    #         [username, filename, filename])
    # conn.commit()
    # filename = propic(username)
    return 


@app.route('/propic/<username>') 
#route to image for food photos, can later be generalized and applied to other photos too
def propic(username):
    # conn = dbi.connect()
    # curs = dbi.cursor(conn)
    # curs.execute('''select filename from foodPics where username = %s''', [username])
    # try:
    #     filename = curs.fetchone()[0]
    #     return send_from_directory(app.config['UPLOADS'],filename)
    # except Exception as err: #in the case when there is not yet a photo uploaded
    #     return None

    # print("SESSION AGAIN",session)
    # username = session['CAS_ USERNAME']
    # flash('Successfully logged in.')
    return redirect(url_for('profile', username=username))

# temporary solution for catching broken link error
# better way of doing this ?!?!
@app.route('/update/', methods = ["GET", "POST"])
def username_error():
    flash("Please log in to update your profile.")
    return render_template('create.html')



################################################################################################
################################################################################################
################################################################################################








#FANGWEN's STUFF
@app.route('/addreview/',methods=['POST','GET'])
def feed(): #rename feed() to add review
    conn=dbi.connect()
    if request.method=='GET':
        #feedbacks=feed_queries.recent_feedback(conn)
        #dishes=feed_queries.top_rated(conn)
        return render_template('feed.html')
    else:
        # get the input form values from the submitted form
        username=request.form['user']
        if len(feed_queries.search_user(conn,username))==0:
            temp=[]
            for item in feed_queries.temp_user(conn):
                temp.append(item['name'])
            flash('Username Under Construction:only enter below for usernames:' )
            flash(temp)
            return render_template('feed.html')
        name=request.form['food']
        if len(feed_queries.search_food(conn,name))==0:
            temp=[]
            for item in feed_queries.temp_food(conn):
                temp.append(item['name'])
            flash('Food Item Under Constuction: only enter below for food item:')
            flash(temp)
            return render_template('feed.html')
        else: 
            fid=feed_queries.search_food(conn,name)[0]['fid']
        rating=request.form['rating']
        comment=request.form['comment']
        time=datetime.now()
        # stored form info into the database here
        feed_queries.feedback(conn,username,fid,rating,comment,time)
        return redirect(url_for('review'))

@app.route('/feed/')     
def review(): #rename review() to feed
    conn=dbi.connect()
    feedbacks= feed_queries.recent_feedback(conn)
    top_rated=feed_queries.food_rating(conn)
    for item in top_rated:
        item['avg']=str(item['avg'])
    return render_template('reviews.html',feedbacks=feedbacks,ranking=top_rated)

    # LEAH's STUFF

def handleErrors(name,category,hall,preferences,allergens,ingredients): 
    message="hello"
    return message

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
        food_date = "2021-03-19"
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

        return redirect(url_for('addfood',messages=success_message,action='addfood'))
    
@app.before_first_request
def init_db():
    dbi.cache_cnf()
    dbi.use('foodie_db') # or whatever db

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
