from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)


import cs304dbi as dbi
import menuUpdates as menuUp #module to update foodie database from the menu page
import random
import sys

from datetime import date

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
    return render_template('base.html',title='foodie.')

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
        else:#if not given a dining hall request or a mealtype request
            menu = menuUp.lookupMenuList(today()[0])
        return render_template('menu.html',date=today()[1], type=mealtype, menu = menu, title ="Menu")

@app.route('/food/<int:fid>', methods=["GET", "POST"])
def food(fid):
    if request.method == 'GET':
        item = menuUp.lookupFoodItem(fid) # dictionary containing a food's name, ingredients, preference, allergen, type
        avgRating, totalRatings = 3, 5#menuUp.avgRating(fid) #average rating and number of ratings given to a food item
        dh, lastServedDate = menuUp.lookupLastServed(fid) #the date the food item was most recently served and the dining hall it was served at
        comments = menuUp.lookupComments(fid) # list of dictionaries for each comment for a given food item and with the comment's rating and user
        return render_template('food.html', name = item["name"], type = item["type"], 
        rating = avgRating, comments = comments, description = item["ingredients"], 
        preference = item["preference"], labels = (item["allergen"]).split(","), 
        title = item["name"], fid = fid, dh = dh)
    else:
        item = menuUp.lookupFoodItem(fid) # dictionary containing a food's name, ingredients, preference, allergen, type
        avgRating, totalRatings = 3, 5#menuUp.avgRating(fid) #average rating and number of ratings given to a food item
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
        avgRating, totalRatings = 3, 5 #menuUp.avgRating(fid) #average rating and number of ratings given to a food item
        dh, lastServedDate = menuUp.lookupLastServed(fid) #the date the food item was most recently served and the dining hall it was served at
        comments = menuUp.lookupComments(fid) # list of dictionaries for each comment for a given food item and with the comment's rating and user
        return render_template('food.html', name = item["name"], type = item["type"], 
        rating = avgRating, comments = comments, description = item["ingredients"], 
        preference = item["preference"], labels = (item["allergen"]).split(","), 
        title = item["name"], fid = fid, dh = dh)


@app.route('/feed/')
def feed():
    return render_template('feed.html')

@app.route('/profile/')
def profile():
    return render_template('profile.html')



# @app.route('/')
# def index():
#     return render_template('main.html',title='Hello')

# @app.route('/greet/', methods=["GET", "POST"])
# def greet():
#     if request.method == 'GET':
#         return render_template('greet.html', title='Customized Greeting')
#     else:
#         try:
#             username = request.form['username'] # throws error if there's trouble
#             flash('form submission successful')
#             return render_template('greet.html',
#                                    title='Welcome '+username,
#                                    name=username)

#         except Exception as err:
#             flash('form submission error'+str(err))
#             return redirect( url_for('index') )

# @app.route('/formecho/', methods=['GET','POST'])
# def formecho():
#     if request.method == 'GET':
#         return render_template('form_data.html',
#                                method=request.method,
#                                form_data=request.args)
#     elif request.method == 'POST':
#         return render_template('form_data.html',
#                                method=request.method,
#                                form_data=request.form)
#     else:
#         # maybe PUT?
#         return render_template('form_data.html',
#                                method=request.method,
#                                form_data={})

# @app.route('/testform/')
# def testform():
#     # these forms go to the formecho route
#     return render_template('testform.html')
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
    app.debug = True
    app.run('0.0.0.0',port)
