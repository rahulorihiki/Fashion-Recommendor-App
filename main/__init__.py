from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import sqlite3
from sqlalchemy.ext.automap import automap_base
# from flask_jsglue import JSGlue
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///FashionDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# engine = create_engine("sqlite:///C:/Users/gokul/OneDrive/Desktop/Projects/Fasion Recommender/CODE-master/main/FashionDB.db")
Base = automap_base()
Base.prepare(db.engine , reflect = True)
Products = Base.classes.file123
User = Base.classes.Users
Admin = Base.classes.Admin
class User123( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
# print(Products)
# pro = db.session.query(Products).paginate(page = 1)
# for c in pro.items:
#     print(c.articleType)

connection1 = sqlite3.connect('FashionDB.db',check_same_thread=False)



from main import routes