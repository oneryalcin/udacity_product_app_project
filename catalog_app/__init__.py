import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_dance.contrib.google import make_google_blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret' if not os.environ.get('FLASK_SECRET')\
    else os.environ.get('FLASK_SECRET')

##############################
# Database Setup

basedir = os.path.abspath(os.path.dirname(__file__))
dbdir = 'sqlite:///' + os.path.join(basedir, 'database.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

###############################
# Setup Login

# Flask-Login provides the endpoint security
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'core.login'


# Need these lines for testing locally
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = '1'

# This Google Blueprint is used for Oauth via Flask Dance
blueprint = make_google_blueprint(
    client_id="363934459936-4rv2gcjfag21qror01a3cj0smsmtqokp.apps.googleusercontent.com",   # noqa
    client_secret="vn31AYsiZxJmj5UuDCvtsvG6",
    offline=True,
    scope=["profile", 'email'],
    redirect_to='core.finish_login'
)

# Register Google oauth to app
app.register_blueprint(blueprint, url_prefix="/login")


################################
# Other Blueprint registrations
from catalog_app.core.views import core     # noqa
from catalog_app.category.views import categories   # noqa
from catalog_app.item.views import items    # noqa


app.register_blueprint(core)
app.register_blueprint(categories)
app.register_blueprint(items)
