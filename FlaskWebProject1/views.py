"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from flask import session, request, abort, redirect, url_for
import random
import string
import os
from FlaskWebProject1 import app
from FlaskWebProject1 import login_manager, users, User
from FlaskWebProject1 import nntest
from FlaskWebProject1 import feed_db
from FlaskWebProject1 import feed_registration_info
import flask_login


user_feed_db = feed_registration_info.feed_registration_info();
user_feed_db.load_from_file("./user_feed_db.db");

lfeed_db = feed_db.feed_db(60*60); #expire once in an hour
lfeed_db.load_from_file("./feed_db.db");


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        application_name = "Mustafa",
        main_debug_text = "My main debug txt!",
    )

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return """
            <form action='login' method ='POST'>
            <input type='text' name='email' id='email' placeholder='email'></input>
            <input type='password' name='passwd' id='passwd' placeholder='password'></input>
            <input type='submit' name='submit' id='submit'></input>
            </form>
        """
    email = request.form['email'];
    if email in users and request.form['passwd'] == users[email]:
        user = User();
        user.id = email;
        flask_login.login_user(user);
        return redirect(url_for('home'));
    return "Bad login!";

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.',
        application_name = "Mustafa"
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.',
        application_name = "Mustafa",
    )

@app.route('/my_feeds')
@flask_login.login_required
def my_feeds():
    """ Renders personal feeds!"""
    global user_feed_db;
    global lfeed_db;
    m_username = flask_login.current_user.id;
    print("Username is:"+ m_username);
    mfeed_list = user_feed_db.get_feed_list(m_username);
    news_list = lfeed_db.get_feeds_for_urls(mfeed_list);
    print("Feed list:"+str(mfeed_list));
    return render_template(
        'my_feeds.html',
        title = 'my feeds',
        year = datetime.now().year,
        message = 'my Application my_feeds',
        application_name = "Mustafa",
        feed_list = news_list,
    )


my_local_var = 0;

import pprint

@app.route("/add_feed", methods=['POST'])
@flask_login.login_required
def add_feed_url():
    global user_feed_db;
    if request.method == "POST":
        pprint.pprint(request)
        for feed_url in request.form:
            user_feed_db.add_feed(flask_login.current_user, feed_url.strip);
    return "Added!";
    

@app.route("/run_jquery", methods=['POST'])
@flask_login.login_required
def run_network():
    global my_local_var;
    if request.method == "POST":
        my_local_var = my_local_var + 1;
        mynn = nntest.nntest();
        return "This is the result! " + str(my_local_var) + mynn.toString();
    return "Not found!";

@app.route("/save", methods = ['POST','GET'])
def save_everything():
    global user_feed_db;
    global lfeed_db;
    user_feed_db.save_to_file("./user_feed_db.db");
    lfeed_db.save_to_file("./feed_db.db");
    return redirect(url_for('my_feeds'))

@app.route("/decode_post")
def decode_post():
    global lfeed_db;
    return lfeed_db.get_news_string_for_post(request.args.get("post_url"));

@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user();
    return redirect(url_for('home'))

@app.route('/shut_down_server')
@flask_login.login_required
def shut_down_server():
    os._exit(0);    
    
@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("login"));