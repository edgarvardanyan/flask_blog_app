# main init file
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'somesecretkey'

# setting up the database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

# setting up login configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

# importing and registering the blueprints
from blog.core.views import core
from blog.error_pages.handlers import error_pages
from blog.users.views import users
from blog.blog_posts.views import blog_posts 

app.register_blueprint(error_pages)
app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(blog_posts)

