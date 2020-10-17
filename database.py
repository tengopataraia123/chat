import os
from flask_sqlalchemy import SQLAlchemy
from app import app

basedir = os.path.abspath(os.path.dirname(__file__))
databasePath = "sqlite:///"+os.path.join(basedir,"db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = databasePath

db = SQLAlchemy(app)

class UserModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,unique=True)
    password = db.Column(db.String)

    def __init__(self,username,password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f"( {self.username}, {self.password} )"