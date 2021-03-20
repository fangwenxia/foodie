from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

# one or the other of these. Defaults to MySQL (PyMySQL)
# change comment characters to switch to SQLite

import cs304dbi as dbi
# import cs304dbi_sqlite3 as dbi

import random

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

# might need to change this. Basically, the user should be redirected to entry.html.
# but I think they started there?  
# app.route('/')
# def home():
#     # the base template needs only one filler
#     return render_template('dataentry.html',action=url_for('entry'))

# based on insert CRUD code. 
@app.route('/', methods=["GET", "POST"])
def insert():
    if request.method == 'GET':
        return render_template('dataentry1.html', action=url_for('insert'))
    elif request.method == 'POST':
        food_name = request.form.get('food-name') 
        food_date = request.form.get('food-date')
        food_category = request.form.get('food-type')
        food_dhall = request.form.get('food-hall')
        food_id = request.form.get('food-id')
        print(food_id)
        error_messages=[]
        if food_name is None: 
            message = "missing input: Food name is missing."
            error_messages.append(message)
        if food_date is None: 
            message = "missing input: Food date is missing."
            error_messages.append(message)
        if food_category is None: 
            message = "missing input: Food category is missing."
            error_messages.append(message)
        if food_dhall is None:
            message = "missing input: Food dining hall is missing."
        if food_id is None:
            message = "missing input: Food ID is missing."
        if len(error_messages) > 0: 
            render_template('insert.html',messages=error_messages,  title='Add Food!')
        flash('form submission successful')
        #insert stuff into database
        connect = dbi.connect()
        curs = dbi.cursor(connect)
        sql = '''insert food(fid,name,lastServed,type,did) 
                  values (%s,%s,%s,%s,%s);'''
        vals = [food_id,food_name,food_date,food_category]
        #determining dhall: 
        fid=None
        # if food_dhall == "Bates": 
        #     fid = 1
        # elif food_dhall == "Lulu":
        #     fid = 2
        # elif food_dhall == "Pom":
        #     fid = 3
        # elif food_dhall == "Stone-D":
        #     fid = 4
        # elif food_dhall == "Tower":
        #     fid = 5
        # implement else case. 
        
        vals.append(food_dhall)
        curs.execute(sql,vals)
        connect.commit()
        success_message = "Food {fname} inserted".format(fname=food_name)
        print(success_message)
        return redirect(url_for('insert',messages=success_message))
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