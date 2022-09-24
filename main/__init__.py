from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import sqlite3
from sqlalchemy.ext.automap import automap_base
# from flask_jsglue import JSGlue
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///FashionDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# engine = create_engine("sqlite:///C:/Users/gokul/OneDrive/Desktop/Projects/Fasion Recommender/CODE-master/main/FashionDB.db")
Base = automap_base()
Base.prepare(db.engine , reflect = True)
Products = Base.classes.file123
# print(Products)
# pro = db.session.query(Products).paginate(page = 1)
# for c in pro.items:
#     print(c.articleType)

connection1 = sqlite3.connect('FashionDB.db',check_same_thread=False)



from main import routes