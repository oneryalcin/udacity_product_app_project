import os
from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask_dance.contrib.google import make_google_blueprint, google as auth


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret' if not os.environ.get('FLASK_SECRET') else os.environ.get('FLASK_SECRET')

##############################
# Database Setup

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

###############################
# Setup OAuth

# Flask-Login provides the endpoint security
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    return User(userid)


# Very simple user model, We use Google Oauth and track user email
# for authentication in Flask-Login user id is user email
class User(UserMixin):
    def __init__(self, email):
        self.id = email

    def __repr__(self):
        return "User : {}".format(self.id)


# Need these lines for testing locally
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = '1'

# This Google Blueprint is used for Oauth via Flask Dance
blueprint = make_google_blueprint(
    client_id="363934459936-4rv2gcjfag21qror01a3cj0smsmtqokp.apps.googleusercontent.com",
    client_secret="vn31AYsiZxJmj5UuDCvtsvG6",
    offline=True,
    scope=["profile", 'email'],
    redirect_to='finish_login'
)

# Register Google oauth to app
app.register_blueprint(blueprint, url_prefix="/login")


# Google Oauth is pretty strict where login request can come,
# therefore all protected endpoints first redirected to 'login' and
# from here it is redirected to 'google.login'
@app.route('/login')
def login():
    return redirect(url_for('google.login'))


# Upon successful authentication with Google Oauth, login user locally
@app.route("/finish_login")
def finish_login():
    email = auth.get("/oauth2/v2/userinfo").json()['email']
    user = User(email)
    login_user(user)
    if request.args.get("next"):
        return redirect(request.args.get("next"))
    return redirect(url_for('core.index'))


# Logout user, you must be logged in to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))


################################
# # Other Blueprint registrations
# from catalog_app.core.views import core
# from catalog_app.category.views import categories
# from catalog_app.item.views import items
#
#
# app.register_blueprint(core)
# app.register_blueprint(categories)
# app.register_blueprint(items)

