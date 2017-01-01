"""
The flask application package.
"""
import sys
from flask_login import login_manager
print(sys.version)
from flask import Flask
import flask_login
from FlaskWebProject1 import nntest
from FlaskWebProject1 import feed_db
from FlaskWebProject1 import feed_registration_info

app = Flask(__name__)
app.secret_key = u'P7AMgp0YOyzAR3JxsOQ2vEIoe7o5aPkG/swP+dUVYmBwJhh75zAd1S5kQt6XJRfsKLOWvDsTz6DGjbRldrGfoA==';

login_manager = flask_login.LoginManager();
login_manager.init_app(app);


users = {"mustafa":"pwd",'mahmut':'ppw'};
user_names = {"mustafa":"muser","mahmut":"usermahmut"};
class User(flask_login.UserMixin):
    def __init__(self):
        super(User,self).__init__();
        self.is_admin = False


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    
    user = User();
    user.id = email;
    user.is_admin = False;
    user.name = user_names[email];
    return user;

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email');
    if email not in users:
        return;
    user = User();
    user.id = email;
    user.is_authenticated = request.form['pw'] == users[email]
    user.is_admin = email == "mahmut";
    user.name = usernames[email];
    return user;
    
print("Initializing python: name=" + __name__)

import FlaskWebProject1.views
