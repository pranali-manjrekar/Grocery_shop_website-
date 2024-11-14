from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from rope.base.oi.type_hinting.evaluate import method
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from functools import wraps
from werkzeug.datastructures import  FileStorage

import urllib
#from pyfcm import FCMNotification
#============Apriory========================
import numpy as np
from flask_uploads import UploadSet, configure_uploads, IMAGES

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

import timeit
import datetime
from flask_mail import Mail, Message
import os
from wtforms.fields import EmailField
import csv
import TimePrediction
#from TimePrediction import timePredict

import pandas as pd
from apyori import apriori

store_data=pd.read_csv('groceries1.csv',header=None)
store_data.shape
store_data=store_data.fillna(0)#from werkzeug.utils import secure_filename


# records=[]
# for i in range(0,9836):
    # records.append([str(store_data.values[i,j]) for j in range(0,32)])

# association_rules=apriori(records,min_support=0.0053,min_confidence=0.22,min_lift=0.01,min_length=2)
# association_rules=list(association_rules)
# print(len(association_rules))
#
# cur.execute("TRUNCATE TABLE apriori_model")
#
# for i in range(1,len-1):
#     #print()
#     x = association_rules[i].items
#     #print(x)
#     x = list(x)
#
#
#     listToStr = ','.join([str(elem) for elem in x])
#     print(listToStr)
#
#
#     sql = "INSERT INTO apriori_model (productname) VALUES (%s)"
#     val = (listToStr)
#     cur.execute(sql, val)
#     mysql.connection.commit()
#     #con.commit()
#
#


#====================================


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/groceryimages'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Config MySQL
mysql = MySQL()
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = '35farmerconsumerblockchain'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize the app for use with this MySQL class
mysql.init_app(app)


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('login'))

    return wrap


def not_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return redirect(url_for('index'))
        else:
            return f(*args, *kwargs)

    return wrap


def is_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return f(*args, *kwargs)
        else:
            return redirect(url_for('admin_login'))
    return wrap


def not_admin_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'admin_logged_in' in session:
            return redirect(url_for('admin'))
        else:
            return f(*args, *kwargs)

    return wrap


def wrappers(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)

    return wrapped


def content_based_filtering(product_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id=%s", (product_id,))  # getting id row
    data = cur.fetchone()  # get row info
    data_cat = data['category']  # get id category ex shirt
    print('Showing result for Product Id: ' + product_id)
    category_matched = cur.execute("SELECT * FROM products WHERE category=%s", (data_cat,))  # get all shirt category
    print('Total product matched: ' + str(category_matched))
    cat_product = cur.fetchall()  # get all row
    cur.execute("SELECT * FROM product_level WHERE product_id=%s", (product_id,))  # id level info
    id_level = cur.fetchone()
    recommend_id = []
    cate_level = ['v_shape', 'polo', 'clean_text', 'design', 'leather', 'color', 'formal', 'converse', 'loafer', 'hook',
                  'chain']
    for product_f in cat_product:
        cur.execute("SELECT * FROM product_level WHERE product_id=%s", (product_f['id'],))
        f_level = cur.fetchone()
        match_score = 0
        if f_level['product_id'] != int(product_id):
            for cat_level in cate_level:
                if f_level[cat_level] == id_level[cat_level]:
                    match_score += 1
            if match_score == 11:
                recommend_id.append(f_level['product_id'])
    print('Total recommendation found: ' + str(recommend_id))
    if recommend_id:
        cur = mysql.connection.cursor()
        placeholders = ','.join((str(n) for n in recommend_id))
        query = 'SELECT * FROM products WHERE id IN (%s)' % placeholders
        cur.execute(query)
        recommend_list = cur.fetchall()
        return recommend_list, recommend_id, category_matched, product_id
    else:
        return ''


#@app.route('/')
@app.route('/index')
def index():
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    values = 'fruit'
    cur.execute("SELECT * FROM groceryname WHERE category=%s and imagename != ''", (values,))
    fruit = cur.fetchall()
    values = 'bakery'
    cur.execute("SELECT * FROM groceryname WHERE category=%s and imagename != ''", (values,))
    bakery = cur.fetchall()
    values = 'Vegetables'
    cur.execute("SELECT * FROM groceryname WHERE category=%s and imagename != ''", (values,))
    Vegetables = cur.fetchall()
    values = 'Cereals'
    cur.execute("SELECT * FROM groceryname WHERE category=%s and imagename != ''", (values,))
    Cereals = cur.fetchall()

    cur.close()
    return render_template('home.html', fruit=fruit, bakery=bakery, Vegetables=Vegetables, Cereals=Cereals, form=form)


class LoginForm(Form):  # Create Login Form
    username = StringField('', [validators.length(min=1)],
                           render_kw={'autofocus': True, 'placeholder': 'Username'})
    password = PasswordField('', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})


# User Login
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
@not_logged_in
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        # GEt user form
        username = form.username.data
        # password_candidate = request.form['password']
        password_candidate = form.password.data
        # Create cursor
        cur = mysql.connection.cursor()
        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username=%s", [username])
        if result > 0:
            # Get stored value
            data = cur.fetchone()
            print(data)
            password = data['password']
            uid = data['id']
            name = data['name']
            noofpeople = data['noofpeople']
            print(noofpeople)

            children = data['children']
            print(children)
            # Compare password
            if sha256_crypt.verify(password_candidate, password):
                # passed
                session['logged_in'] = True
                session['uid'] = uid
                session['s_name'] = name
                session['noofpeople'] = noofpeople
                session['children'] = children
                x = '1'
                cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
                return redirect(url_for('index'))
            else:
                flash('Incorrect password', 'danger')
                return render_template('login.html', form=form)

        else:
            flash('Username not found', 'danger')
            # Close connection
            cur.close()
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/out')
def logout():
    if 'uid' in session:
        # Create cursor
        cur = mysql.connection.cursor()
        uid = session['uid']
        x = '0'
        cur.execute("UPDATE users SET online=%s WHERE id=%s", (x, uid))
        session.clear()
        flash('You are logged out', 'success')
        return redirect(url_for('login'))
    return redirect(url_for('login'))


class RegisterForm(Form):
    name = StringField('', [validators.length(min=3, max=50)], render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    username = StringField('', [validators.length(min=3, max=25)], render_kw={'placeholder': 'Username'})
    email = EmailField('', [validators.DataRequired() ], render_kw={'placeholder': 'Email'})
    password = PasswordField('', [validators.length(min=3)], render_kw={'placeholder': 'Password'})
    mobile = StringField('', [validators.length(min=10, max=10)], render_kw={'placeholder': 'Mobile'})


@app.route('/register', methods=['GET', 'POST'])
@not_logged_in
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
    #     name = form.name.data
    #     email = form.email.data
    #     username = form.username.data
    #     password = sha256_crypt.encrypt(str(form.password.data))
    #     mobile = form.mobile.data
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = sha256_crypt.encrypt(str(request.form.get('password')))
        mobile = request.form.get('mobile')
        people = request.form.get('people')
        children = request.form.get('children')
        age = request.form.get('age')
        pincode = request.form.get('pincode')

        # Create Cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password, mobile, noofpeople, children, age, pincode) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (name, email, username, password, mobile,people,children, age, pincode))

        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()
        flash('You are now registered and can login', 'success')
        return redirect(url_for('index'))
    return render_template('register.html',form=form)


class MessageForm(Form):  # Create Message Form
    body = StringField('', [validators.length(min=1)], render_kw={'autofocus': True})


@app.route('/chatting/<string:id>', methods=['GET', 'POST'])
def chatting(id):
    if 'uid' in session:
        form = MessageForm(request.form)
        # Create cursor
        cur = mysql.connection.cursor()

        # lid name
        get_result = cur.execute("SELECT * FROM users WHERE id=%s", [id])
        l_data = cur.fetchone()
        if get_result > 0:
            session['name'] = l_data['name']
            uid = session['uid']
            session['lid'] = id

            if request.method == 'POST' and form.validate():
                txt_body = form.body.data
                # Create cursor
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO messages(body, msg_by, msg_to) VALUES(%s, %s, %s)",
                            (txt_body, id, uid))
                # Commit cursor
                mysql.connection.commit()

            # Get users
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()

            # Close Connection
            cur.close()
            return render_template('chat_room.html', users=users, form=form)
        else:
            flash('No permission!', 'danger')
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/chats', methods=['GET', 'POST'])
def chats():
    if 'lid' in session:
        id = session['lid']
        uid = session['uid']
        # Create cursor
        cur = mysql.connection.cursor()
        # Get message
        cur.execute("SELECT * FROM messages WHERE (msg_by=%s AND msg_to=%s) OR (msg_by=%s AND msg_to=%s) "
                    "ORDER BY id ASC", (id, uid, uid, id))
        chats = cur.fetchall()
        # Close Connection
        cur.close()
        return render_template('chats.html', chats=chats, )
    return redirect(url_for('login'))


class OrderForm(Form):  # Create Order Form
    name = StringField('', [validators.length(min=1), validators.DataRequired()],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    mobile_num = StringField('', [validators.length(min=1), validators.DataRequired()],
                             render_kw={'autofocus': True, 'placeholder': 'Mobile'})
    quantity = SelectField('', [validators.DataRequired()],
                           choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')])
    order_place = StringField('', [validators.length(min=1), validators.DataRequired()],
                              render_kw={'placeholder': 'Order Place'})


@app.route('/fruit', methods=['GET', 'POST'])
def fruit():
    #print("fruittttttttttt")
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'fruit'
    cur.execute("SELECT * FROM groceryname WHERE category=%s", (values,))

    products = cur.fetchall()
    # Close Connection
    cur.close()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data

        now = datetime.datetime.now()

        pid = request.args['order']
        people = request.form.get('noofpeople')
        children = request.form.get('children')

        predres = predicttime(pid, quantity, people, children)
        #print(predres)
        nextdate = datetime.timedelta(days=predres)
        remind_date1 = now + nextdate
        remind_date = remind_date1.strftime("%Y-%m-%d")

        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")

        # Create Cursor
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))

            curs.execute("INSERT INTO datepredict(productid, uid, predictdate, mobile) "
                         "VALUES(%s, %s, %s, %s)",
                         (pid, uid, remind_date, mobile))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))
        # Commit cursor
        mysql.connection.commit()
        cur.close()

        flash('Order successful', 'success')
        flash('Item Finish within '+str(predres)+' days', 'success')
        return render_template('fruit.html', products=products, form=form)
    if 'view' in request.args:
        #print()
        product_id = request.args['view']
        pid = product_id;
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM groceryname WHERE id=%s", (product_id,))
        product = curso.fetchall()
        return render_template('view_product.html', products=product)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM groceryname WHERE id=%s", (product_id,))
        product = curso.fetchall()
        #x = content_based_filtering(product_id)
        # ====================Recommendation=================
        cur1 = mysql.connection.cursor()
        q = "select * from groceryname where id= " + product_id
        print(q)
        cur1.execute(q)
        prod = cur1.fetchone()
        cur2 = mysql.connection.cursor()
        print("select length(productname) as lenofproduct, productname from apriori_model where productname like '%" +
              prod['name'] + "%' order by lenofproduct")
        rowcount = cur2.execute(
            "select length(productname) as lenofproduct, productname from apriori_model where productname like '%" +
            prod['name'] + "%' order by lenofproduct ")

        if rowcount > 0:
            x = cur2.fetchall()
            print(x)

            x2 = []
            for a in x:
                x1 = a['productname']
                x2.extend(list(x1.split(',')))

            # x3 = tuple(x2)
            x3 = tuple(set(x2))
            print(x3)
            cur3 = mysql.connection.cursor()
            q1 = "select * from groceryname where  name in {}".format(x3) + " and imagename !=''"
            print(q1)
            cur3.execute(q1)
            rec_products = cur3.fetchall()
        else:
            rec_products = {}
        # ====================Recommendation=================
        people = ''
        children = ''
        #if 'logged_in' in session:
        if 'uid' in session:
            people = session['noofpeople']
            children = session['children']

        return render_template('order_product.html', products=product, form=form, x= rec_products,people=people,children=children )
    return render_template('fruit.html', products=products, form=form)


@app.route('/bakery', methods=['GET', 'POST'])
def bakery():
    print("bakery")
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'bakery'
    cur.execute("SELECT * FROM groceryname WHERE category=%s", (values,))

    products = cur.fetchall()
    # Close Connection
    cur.close()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        now = datetime.datetime.now()
        pid = request.args['order']
        people = request.form.get('noofpeople')
        children = request.form.get('children')
        predres = predicttime(pid, quantity, people, children)
        # print(predres)
        nextdate = datetime.timedelta(days=predres)
        remind_date1 = now + nextdate
        remind_date = remind_date1.strftime("%Y-%m-%d")
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # Create Cursor
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))

            curs.execute("INSERT INTO datepredict(productid, uid, predictdate, mobile) "
                         "VALUES(%s, %s, %s, %s)",
                         (pid, uid, remind_date, mobile))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))
        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('Order successful', 'success')
        flash('Item Finish within ' + str(predres) + ' days', 'success')
        return render_template('bakery.html', products=products, form=form)
    if 'view' in request.args:
        print()
        product_id = request.args['view']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM groceryname WHERE id=%s", (product_id,))
        product = curso.fetchall()

        return render_template('view_product.html', products=product)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM groceryname WHERE id=%s", (product_id,))
        product = curso.fetchall()
        # x = content_based_filtering(product_id)

        # ====================Recommendation=================
        cur1 = mysql.connection.cursor()
        q = "select * from groceryname where id= " + product_id
        print(q)
        cur1.execute(q)
        prod = cur1.fetchone()
        cur2 = mysql.connection.cursor()
        print("select length(productname) as lenofproduct, productname from apriori_model where productname like '%" +
              prod['name'] + "%' order by lenofproduct")
        rowcount = cur2.execute(
            "select length(productname) as lenofproduct, productname from apriori_model where productname like '%" +
            prod['name'] + "%' order by lenofproduct ")

        if rowcount > 0:
            x = cur2.fetchall()
            print(x)

            x2 = []
            for a in x:
                x1 = a['productname']
                x2.extend(list(x1.split(',')))

            # x3 = tuple(x2)
            x3 = tuple(set(x2))
            print(x3)
            cur3 = mysql.connection.cursor()
            q1 = "select * from groceryname where  name in {}".format(x3) + " and imagename !=''"
            print(q1)
            cur3.execute(q1)
            rec_products = cur3.fetchall()
        else:
            rec_products = {}
        # ====================Recommendation=================
        people = ''
        children = ''
        # if 'logged_in' in session:
        if 'uid' in session:
            people = session['noofpeople']
            children = session['children']

        return render_template('order_product.html', products=product, form=form, x=rec_products, people=people, children=children)
        #return render_template('order_product.html', products=product, form=form, x= rec_products, people=session['noofpeople'],children=session['children'] )
    return render_template('bakery.html', products=products, form=form)


@app.route('/Cereals', methods=['GET', 'POST'])
def drink():
    print("Cereals")
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'Cereals'
    cur.execute("SELECT * FROM groceryname WHERE category=%s", (values,))

    products = cur.fetchall()
    # Close Connection
    cur.close()
    if request.method == 'POST' and form.validate():
        # name = form.name.data
        # mobile = form.mobile_num.data
        # order_place = form.order_place.data
        # quantity = form.quantity.data
        # pid = request.args['order']
        # now = datetime.datetime.now()
        # week = datetime.timedelta(days=7)
        # delivery_date = now + week
        # now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # # Create Cursor
        # curs = mysql.connection.cursor()
        # if 'uid' in session:
        #     uid = session['uid']
        #     curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
        #                  "VALUES(%s, %s, %s, %s, %s, %s, %s)",
        #                  (uid, pid, name, mobile, order_place, quantity, now_time))
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        now = datetime.datetime.now()
        pid = request.args['order']
        people = request.form.get('noofpeople')
        children = request.form.get('children')
        predres = predicttime(pid, quantity, people, children)
        # print(predres)
        nextdate = datetime.timedelta(days=predres)
        remind_date1 = now + nextdate
        remind_date = remind_date1.strftime("%Y-%m-%d")
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # Create Cursor
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))

            curs.execute("INSERT INTO datepredict(productid, uid, predictdate, mobile) "
                         "VALUES(%s, %s, %s, %s)",
                         (pid, uid, remind_date, mobile))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))
        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('Order successful', 'success')
        flash('Item Finish within ' + str(predres) + ' days', 'success')
        return render_template('Cereals.html', products=products, form=form)
    if 'view' in request.args:
        print()
        product_id = request.args['view']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM groceryname WHERE id=%s", (product_id,))
        product = curso.fetchall()

        return render_template('view_product.html', products=product)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM groceryname WHERE id=%s", (product_id,))
        product = curso.fetchall()
        # x = content_based_filtering(product_id)

        # ====================Recommendation=================
        cur1 = mysql.connection.cursor()
        q = "select * from groceryname where id= " + product_id
        print(q)
        cur1.execute(q)
        prod = cur1.fetchone()
        cur2 = mysql.connection.cursor()
        print("select length(productname) as lenofproduct, productname from apriori_model where productname like '%" +
              prod['name'] + "%' order by lenofproduct")
        rowcount = cur2.execute(
            "select length(productname) as lenofproduct, productname from apriori_model where productname like '%" +
            prod['name'] + "%' order by lenofproduct ")

        if rowcount > 0:
            x = cur2.fetchall()
            print(x)

            x2 = []
            for a in x:
                x1 = a['productname']
                x2.extend(list(x1.split(',')))

            # x3 = tuple(x2)
            x3 = tuple(set(x2))
            print(x3)
            cur3 = mysql.connection.cursor()
            q1 = "select * from groceryname where  name in {}".format(x3) + " and imagename !=''"
            print(q1)
            cur3.execute(q1)
            rec_products = cur3.fetchall()
        else:
            rec_products = {}
        # ====================Recommendation=================
        people = ''
        children = ''
        # if 'logged_in' in session:
        if 'uid' in session:
            people = session['noofpeople']
            children = session['children']

        return render_template('order_product.html', products=product, form=form, x=rec_products, people=people,children=children)
        #return render_template('order_product.html', products=product, form=form,  x= rec_products, people=session['noofpeople'],children=session['children'] )
    return render_template('Cereals.html', products=products, form=form)


@app.route('/Vegetables', methods=['GET', 'POST'])
def homeproduct():
    print("Vegetables")
    form = OrderForm(request.form)
    # Create cursor
    cur = mysql.connection.cursor()
    # Get message
    values = 'Vegetables'
    cur.execute("SELECT * FROM groceryname WHERE category=%s", (values,))
    products = cur.fetchall()
    # Close Connection
    cur.close()
    if request.method == 'POST' and form.validate():
        # name = form.name.data
        # mobile = form.mobile_num.data
        # order_place = form.order_place.data
        # quantity = form.quantity.data
        # pid = request.args['order']
        # now = datetime.datetime.now()
        # week = datetime.timedelta(days=7)
        # delivery_date = now + week
        # now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # # Create Cursor
        # curs = mysql.connection.cursor()
        # if 'uid' in session:
        #     uid = session['uid']
        #     curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
        #                  "VALUES(%s, %s, %s, %s, %s, %s, %s)",
        #                  (uid, pid, name, mobile, order_place, quantity, now_time))
        name = form.name.data
        mobile = form.mobile_num.data
        order_place = form.order_place.data
        quantity = form.quantity.data
        now = datetime.datetime.now()
        pid = request.args['order']
        people = request.form.get('noofpeople')
        children = request.form.get('children')
        predres = predicttime(pid, quantity, people, children)
        # print(predres)
        nextdate = datetime.timedelta(days=predres)
        remind_date1 = now + nextdate
        remind_date = remind_date1.strftime("%Y-%m-%d")
        week = datetime.timedelta(days=7)
        delivery_date = now + week
        now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
        # Create Cursor
        curs = mysql.connection.cursor()
        if 'uid' in session:
            uid = session['uid']
            curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                         (uid, pid, name, mobile, order_place, quantity, now_time))

            curs.execute("INSERT INTO datepredict(productid, uid, predictdate, mobile) "
                         "VALUES(%s, %s, %s, %s)",
                         (pid, uid, remind_date, mobile))
        else:
            curs.execute("INSERT INTO orders(pid, ofname, mobile, oplace, quantity, ddate) "
                         "VALUES(%s, %s, %s, %s, %s, %s)",
                         (pid, name, mobile, order_place, quantity, now_time))
        # Commit cursor
        mysql.connection.commit()

        # Close Connection
        cur.close()

        flash('Order successful', 'success')
        flash('Item Finish within ' + str(predres) + ' days', 'success')
        return render_template('Vegetables.html', products=products, form=form)
    if 'view' in request.args:
        print()
        product_id = request.args['view']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM groceryname WHERE id=%s", (product_id,))
        product = curso.fetchall()

        return render_template('view_product.html', products=product)
    elif 'order' in request.args:
        product_id = request.args['order']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM groceryname WHERE id=%s", (product_id,))
        product = curso.fetchall()
        #x = content_based_filtering(product_id)

        # ====================Recommendation=================
        cur1 = mysql.connection.cursor()
        q = "select * from groceryname where id= " + product_id
        print(q)
        cur1.execute(q)
        prod = cur1.fetchone()
        cur2 = mysql.connection.cursor()
        print("select length(productname) as lenofproduct, productname from apriori_model where productname like '%" +
              prod['name'] + "%' order by lenofproduct")
        rowcount = cur2.execute(
            "select length(productname) as lenofproduct, productname from apriori_model where productname like '%" +
            prod['name'] + "%' order by lenofproduct ")


        if rowcount  > 0:
            x = cur2.fetchall()
            print(x)

            x2 = []
            for a in x:
                x1 = a['productname']
                x2.extend(list(x1.split(',')))

            # x3 = tuple(x2)
            x3 = tuple(set(x2))
            print(x3)
            cur3 = mysql.connection.cursor()
            q1 = "select * from groceryname where  name in {}".format(x3) + " and imagename !=''"
            print(q1)
            cur3.execute(q1)
            rec_products = cur3.fetchall()
        else:
            rec_products = {}
        # ====================Recommendation=================
        people = ''
        children = ''
        # if 'logged_in' in session:
        if 'uid' in session:
            people = session['noofpeople']
            children = session['children']

        return render_template('order_product.html', products=product, form=form, x=rec_products, people=people,children=children)
        #return render_template('order_product.html', products=product, form=form,  x= rec_products, people=session['noofpeople'],children=session['children'] )
    return render_template('Vegetables.html', products=products, form=form)


@app.route('/admin_login', methods=['GET', 'POST'])
@not_admin_logged_in
def admin_login():
    if request.method == 'POST':
        # GEt user form
        username = request.form['email']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM admin WHERE email=%s", [username])

        if result > 0:
            # Get stored value
            data = cur.fetchone()
            password = data['password']
            uid = data['id']
            name = data['firstName']

            # Compare password
            if sha256_crypt.verify(password_candidate, password):
                # passed
                session['admin_logged_in'] = True
                session['admin_uid'] = uid
                session['admin_name'] = name

                return redirect(url_for('admin'))

            else:
                flash('Incorrect password', 'danger')
                return render_template('pages/login.html')

        else:
            flash('Username not found', 'danger')
            # Close connection
            cur.close()
            return render_template('pages/login.html')
    return render_template('pages/login.html')


@app.route('/admin_out')
def admin_logout():
    if 'admin_logged_in' in session:
        session.clear()
        return redirect(url_for('admin_login'))
    return redirect(url_for('admin'))


@app.route('/admin')
@is_admin_logged_in
def admin():
    curso = mysql.connection.cursor()
    #num_rows = curso.execute("SELECT * FROM products")
    num_rows = curso.execute("SELECT * FROM groceryname")
    result = curso.fetchall()
    order_rows = curso.execute("SELECT * FROM orders")
    users_rows = curso.execute("SELECT * FROM users")
    return render_template('pages/index.html', result=result, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)


@app.route('/orders')
@is_admin_logged_in
def orders():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM products")
    order_rows = curso.execute("SELECT * FROM orders")
    result = curso.fetchall()
    users_rows = curso.execute("SELECT * FROM users")
    return render_template('pages/all_orders.html', result=result, row=num_rows, order_rows=order_rows,
                           users_rows=users_rows)


@app.route('/users')
@is_admin_logged_in
def users():
    curso = mysql.connection.cursor()
    num_rows = curso.execute("SELECT * FROM groceryname")
    order_rows = curso.execute("SELECT * FROM orders")
    users_rows = curso.execute("SELECT * FROM users")
    result = curso.fetchall()
    return render_template('pages/all_users.html', result=result, row=num_rows, order_rows=order_rows,users_rows=users_rows)


@app.route('/admin_add_product', methods=['POST', 'GET'])
@is_admin_logged_in
def admin_add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form['price']
        category = request.form['category']
        file = request.files['picture']
        if name and price and category and file:
            pic = file.filename
            photo = pic.replace("'", "")
            picture = photo.replace(" ", "_")
            if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                save_photo = photos.save(file)
                if save_photo:
                    # Create Cursor
                    curs = mysql.connection.cursor()
                    curs.execute("INSERT INTO groceryname(name,imagename,price,category)"
                                 "VALUES(%s, %s, %s, %s)",
                                 (name, picture, price, category))
                    mysql.connection.commit()
                    curs.close()
                    flash('Product added successful', 'success')
                    return redirect(url_for('admin_add_product'))
                else:
                    flash('Picture not save', 'danger')
                    return redirect(url_for('admin_add_product'))
            else:
                flash('File not supported', 'danger')
                return redirect(url_for('admin_add_product'))
        else:
            flash('Please fill up all form', 'danger')
            return redirect(url_for('admin_add_product'))
    else:
        return render_template('pages/add_product.html')


@app.route('/edit_product', methods=['POST', 'GET'])
@is_admin_logged_in
def edit_product():
    if 'id' in request.args:
        product_id = request.args['id']
        curso = mysql.connection.cursor()
        res = curso.execute("SELECT * FROM groceryname WHERE id=%s", (product_id,))
        product = curso.fetchall()
        if res:
            if request.method == 'POST':
                name = request.form.get('name')
                price = request.form['price']
                category = request.form['category']
                file = request.files['picture']
                # Create Cursor
                if name and price and category and file:
                    pic = file.filename
                    photo = pic.replace("'", "")
                    picture = photo.replace(" ", "")
                    if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
                        file.filename = picture
                        save_photo = photos.save(file)
                        if save_photo:
                            # Create Cursor
                            cur = mysql.connection.cursor()
                            exe = curso.execute("UPDATE groceryname SET name=%s, price=%s, category=%s, imagename=%s WHERE id=%s",(name, price, category, picture, product_id))
                            mysql.connection.commit()
                            flash('Product updated successful', 'success')
                            return redirect(url_for('admin_add_product'))
                        else:
                            flash('Pic not upload', 'danger')
                            return render_template('pages/edit_product.html', product=product)
                    else:
                        flash('File not support', 'danger')
                        return render_template('pages/edit_product.html', product=product)
                else:
                    flash('Fill all field', 'danger')
                    return render_template('pages/edit_product.html', product=product)
            else:
                return render_template('pages/edit_product.html', product=product)
        else:
            return redirect(url_for('admin_login'))
    else:
        return redirect(url_for('admin_login'))


@app.route('/reminder', methods=['POST', 'GET'])
@is_admin_logged_in
def reminder():
    now = datetime.datetime.now()
    remind_date = now.strftime("%Y-%m-%d")

    nextdate1 = datetime.timedelta(days=1)
    remind_date_daybefore = now + nextdate1
    remind_date_daybefore1 = remind_date_daybefore.strftime("%Y-%m-%d")

    nextdate2 = datetime.timedelta(days=2)
    remind_date_twodaybefore = now + nextdate2
    remind_date_twodaybefore1 = remind_date_twodaybefore.strftime("%Y-%m-%d")

    #product_id = request.args['id']
    curso = mysql.connection.cursor()
    res = curso.execute("SELECT * FROM datepredict WHERE predictdate=%s", (remind_date,))
    products = curso.fetchall()
    products1 = products
    if request.method == 'POST':
        for a in products1:
            prodid = a['productid']
            mobileno = a['mobile']
            curso.execute("SELECT * FROM groceryname WHERE id=%s", (prodid,))
            productname = curso.fetchone()
            pname = productname['name']
            msg = "Your product " + pname + " is finish today"
            smsfunction(mobileno,prodid,msg)


        curso.execute("SELECT * FROM datepredict WHERE predictdate=%s", (remind_date_daybefore1,))
        products2 = curso.fetchall()
        for a in products2:
            prodid = a['productid']
            mobileno = a['mobile']
            curso.execute("SELECT * FROM groceryname WHERE id=%s", (prodid,))
            productname = curso.fetchone()
            pname = productname['name']
            msg = "Your product "+pname+" is finish tomorrow"
            smsfunction(mobileno, prodid, msg)

        curso.execute("SELECT * FROM datepredict WHERE predictdate=%s", (remind_date_twodaybefore1,))
        products3 = curso.fetchall()
        for a in products3:
            prodid = a['productid']
            mobileno = a['mobile']
            curso.execute("SELECT * FROM groceryname WHERE id=%s", (prodid,))
            productname = curso.fetchone()
            pname = productname['name']
            msg = "Your product " + pname + " is finish after 2 days"
            smsfunction(mobileno, prodid, msg)

        flash('Remind successful', 'success')
    return render_template('pages/reminder.html', products=products)


@app.route('/search', methods=['POST', 'GET'])
def search():
    form = OrderForm(request.form)
    if 'q' in request.args:
        q = request.args['q']
        # Create cursor
        cur = mysql.connection.cursor()
        # Get message
        query_string = "SELECT * FROM groceryname WHERE name LIKE %s and imagename != '' ORDER BY id ASC"
        cur.execute(query_string, ('%' + q + '%',))
        products = cur.fetchall()
        # Close Connection
        cur.close()
        flash('Showing result for: ' + q, 'success')
        return render_template('search.html', products=products, form=form)
    else:
        flash('Search again', 'danger')
        return render_template('search.html')

#-----------
def predicttime(item,iteminkg,people,children):
    pred = TimePrediction.timePredict(item, iteminkg, people, children)
    #print(pred)
    pred1 = int(pred)
    return pred1
#-----------




@app.route('/profile')
@is_logged_in
def profile():
    if 'user' in request.args:
        q = request.args['user']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM users WHERE id=%s", (q,))
        result = curso.fetchone()
        if result:
            if result['id'] == session['uid']:
                #curso.execute("SELECT * FROM orders WHERE uid=%s ORDER BY id ASC", (session['uid'],))
                curso.execute("select 	o.*, g.name from orders o, groceryname g where o.pid=g.id and uid=%s ORDER BY id ASC", (session['uid'],))
                res = curso.fetchall()
                return render_template('profile.html', result=res)
            else:
                flash('Unauthorised', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


@app.route('/mycart')
@is_logged_in
def mycart():
    if 'user' in request.args:
        q = request.args['user']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM users WHERE id=%s", (q,))
        result = curso.fetchone()
        if result:
            if result['id'] == session['uid']:
                #curso.execute("SELECT * FROM orders WHERE uid=%s ORDER BY id ASC", (session['uid'],))
                curso.execute("select * from cart where uid=%s ORDER BY id ASC", (session['uid'],))
                res = curso.fetchall()
                return render_template('cart.html', result=res)
            else:
                flash('Unauthorised', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


@app.route('/cart')
@is_logged_in
def cart():
    if 'user' in request.args:
        q = request.args['user']
        pid = request.args['pid']
        pname = request.args['pname']
        price = request.args['price']
        cat = request.args['cat']

        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM users WHERE id=%s", (q,))
        result = curso.fetchone()
        if result:
            if result['id'] == session['uid']:
                #curso.execute("select * from cart where uid=%s ORDER BY id ASC", (session['uid'],))
                curso.execute("INSERT INTO cart(uid, pid, pname, price, category) "
                             "VALUES(%s, %s, %s, %s, %s)",
                             (str(session['uid']), str(pid), pname, price, cat))
                # Commit cursor
                mysql.connection.commit()
                curso.execute("select * from cart where uid=%s ORDER BY id ASC", (session['uid'],))
                res = curso.fetchall()
                return render_template('cart.html', result=res)
            else:
                flash('Unauthorised', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


@app.route('/removefromcart')
@is_logged_in
def removefromcart():
    if 'id' in request.args:
        q = request.args['id']

        curso = mysql.connection.cursor()
        curso.execute("delete FROM cart WHERE id=%s", (q))
        mysql.connection.commit()

        curso.execute("select * from cart where uid=%s ORDER BY id ASC", (session['uid'],))
        res = curso.fetchall()
        return render_template('cart.html', result=res)

    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


@app.route('/cancelorder')
@is_logged_in
def cancelorder():
    if 'uid' in session:
        uid = session['uid']
        q = request.args['id']

        curso = mysql.connection.cursor()
        curso.execute("delete FROM orders WHERE id="+str(q))
        mysql.connection.commit()

        #curso.execute("select * from cart where uid=%s ORDER BY id ASC", (session['uid'],))
        #res = curso.fetchall()
        return redirect(url_for('index'))

    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


@app.route('/orderfromcart', methods=['GET', 'POST'])
@is_logged_in
def orderfromcart():
    if 'uid' in session:
        form = OrderForm(request.form)
        if request.method == 'POST':
            name = form.name.data
            mobile = form.mobile_num.data
            order_place = form.order_place.data
            quantity = 1
            now = datetime.datetime.now()
            #pid = request.args['order']
            people = request.form.get('noofpeople')
            children = request.form.get('children')

            userid = session['uid']
            curso = mysql.connection.cursor()
            curso.execute("select * from cart WHERE uid=%s", (userid,))
            # mysql.connection.commit()
            # curso.execute("select * from cart where uid=%s ORDER BY id ASC", (session['uid'],))
            res = curso.fetchall()
            for p in res:
                print(p)
                predres = predicttime(p["pid"], quantity, people, children)
                # print(predres)
                nextdate = datetime.timedelta(days=predres)
                remind_date1 = now + nextdate
                remind_date = remind_date1.strftime("%Y-%m-%d")
                week = datetime.timedelta(days=7)
                delivery_date = now + week
                now_time = delivery_date.strftime("%y-%m-%d %H:%M:%S")
                # Create Cursor
                curs = mysql.connection.cursor()
                if 'uid' in session:
                    uid = session['uid']
                    curs.execute("INSERT INTO orders(uid, pid, ofname, mobile, oplace, quantity, ddate) "
                                 "VALUES(%s, %s, %s, %s, %s, %s, %s)",
                                 (uid, p["pid"], name, mobile, order_place, quantity, now_time))

                    curs.execute("INSERT INTO datepredict(productid, uid, predictdate, mobile) "
                                 "VALUES(%s, %s, %s, %s)",
                                 (p["pid"], uid, remind_date, mobile))
                    mysql.connection.commit()
                else:
                    return redirect(url_for('login'))
            curs.execute("delete from cart where uid = '"+str(uid)+"'")
            mysql.connection.commit()
            return redirect(url_for("cart"))
        people = session['noofpeople']
        children = session['children']
        return render_template('orderfromcart.html', form=form, people=people, children=children)
        #return render_template('orderfromcart.html', result=res)
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


class UpdateRegisterForm(Form):
    name = StringField('Full Name', [validators.length(min=3, max=50)],
                       render_kw={'autofocus': True, 'placeholder': 'Full Name'})
    email = EmailField('Email', [validators.DataRequired()],
                       render_kw={'placeholder': 'Email'})
    password = PasswordField('Password', [validators.length(min=3)],
                             render_kw={'placeholder': 'Password'})
    mobile = StringField('Mobile', [validators.length(min=10, max=11)], render_kw={'placeholder': 'Mobile'})


@app.route('/settings', methods=['POST', 'GET'])
@is_logged_in
def settings():
    form = UpdateRegisterForm(request.form)
    if 'user' in request.args:
        q = request.args['user']
        curso = mysql.connection.cursor()
        curso.execute("SELECT * FROM users WHERE id=%s", (q,))
        result = curso.fetchone()
        if result:
            if result['id'] == session['uid']:
                if request.method == 'POST' and form.validate():
                    name = form.name.data
                    email = form.email.data
                    password = sha256_crypt.encrypt(str(form.password.data))
                    mobile = form.mobile.data

                    # Create Cursor
                    cur = mysql.connection.cursor()
                    exe = cur.execute("UPDATE users SET name=%s, email=%s, password=%s, mobile=%s WHERE id=%s",
                                      (name, email, password, mobile, q))
                    if exe:
                        flash('Profile updated', 'success')
                        return render_template('user_settings.html', result=result, form=form)
                    else:
                        flash('Profile not updated', 'danger')
                return render_template('user_settings.html', result=result, form=form)
            else:
                flash('Unauthorised', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Unauthorised! Please login', 'danger')
            return redirect(url_for('login'))
    else:
        flash('Unauthorised', 'danger')
        return redirect(url_for('login'))


class DeveloperForm(Form):  #
    id = StringField('', [validators.length(min=1)],
                     render_kw={'placeholder': 'Input a product id...'})


@app.route('/developer', methods=['POST', 'GET'])
def developer():
    form = DeveloperForm(request.form)
    if request.method == 'POST' and form.validate():
        q = form.id.data
        curso = mysql.connection.cursor()
        result = curso.execute("SELECT * FROM products WHERE id=%s", (q,))
        if result > 0:
            x = content_based_filtering(q)
            wrappered = wrappers(content_based_filtering, q)
            execution_time = timeit.timeit(wrappered, number=0)
            seconds = ((execution_time / 1000) % 60)
            return render_template('developer.html', form=form, x=x, execution_time=seconds)
        else:
            nothing = 'Nothing found'
            return render_template('developer.html', form=form, nothing=nothing)
    else:
        return render_template('developer.html', form=form)



def a():
    DataCaptured = csv.reader('groceries.csv', delimiter=',')
    product = []
    cur = mysql.connection.cursor()


    for a in DataCaptured:
        if a not in product:
            product.append(a)

            sql = "INSERT INTO groceryname (name) VALUES (%s)"
            val = (a)
            cur.execute(sql, val)
            mysql.connection.commit()

    # if row[1] not in Category:
    #     Category.append(row[1])


def smsfunction(mobile,  pid, msg):
    authkey = "175606AVhvZO37X59c2613b"  # Your authentication key.
    mobiles = mobile  # Multiple mobiles numbers separated by comma.
    message = msg
    #message = "Your product id"+pid+" is finished today"  # Your message to send.
    sender = "GROCER"  # Sender ID,While using route4 sender id should be 6 characters long.
    route = "route4"  # Define route
    # Prepare you post parameters
    values = {
        'authkey': authkey,
        'mobiles': mobiles,
        'message': message,
        'sender': sender,
        'route': route
    }
    url = "http://api.msg91.com/api/sendhttp.php"  # API URL
    postdata = urllib.parse.urlencode(values).encode("utf-8")  # URL encoding the data here.
    req = urllib.request.Request(url, postdata)
    response = urllib.request.urlopen(req)
    output = response.read()  # Get Response
    print(output)


if __name__ == '__main__':
    #app.run('0.0.0.0')
    app.run(debug=True)
