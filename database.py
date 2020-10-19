from flask_sqlalchemy import SQLAlchemy
from app import app

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

    @classmethod
    def get_user(self,username):
        return UserModel.query.filter_by(username=username).first()