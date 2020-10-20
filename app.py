from flask import Flask,render_template,redirect,url_for,get_flashed_messages,flash
import flask
from flask_wtf import FlaskForm
import os
from user import User
from flask_socketio import SocketIO,join_room
from wtforms import (
    StringField,
    PasswordField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    EqualTo
)
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    current_user,
    logout_user
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "alsdkjflkqjletkjalsdf"
basedir = os.path.abspath(os.path.dirname(__file__))
databasePath = "sqlite:///"+os.path.join(basedir,"db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = databasePath
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app)


@login_manager.user_loader
def load_user(username):
    db_result = UserModel.get_user(username)
    if db_result:
        return User(db_result.username,db_result.password)
    return None

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Log in")

class RegisterForm(FlaskForm):
    username = StringField("Username",[DataRequired()])
    password = PasswordField("Password",[DataRequired()])
    confirm = PasswordField("Repeat Password",[DataRequired()])
    submit = SubmitField("Register")


@app.route("/chat",methods=["GET","POST"])
@login_required
def chat():
    return render_template("chat.html")

@app.route("/logout")
@login_required
def log_out():
    logout_user()
    return redirect(url_for("index"))

@app.route("/",methods = ["GET","POST"])
def index():

    if current_user.is_authenticated:
        return redirect(url_for("chat"))

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = load_user(username)
        if user:
            if user.check_password(password):
                login_user(user)
                return redirect(url_for("chat"))
            else:
                flash("Wrong Password","wrong-pass")
        else:
            flash("Wrong Username","wrong-user")        

    return render_template("index.html",form=form)

@app.route("/register",methods=["GET","POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm = form.confirm.data
        if(UserModel.get_user(username) == None):
            if(password == confirm):
                newUser = UserModel(username,password)
                db.session.add(newUser)
                db.session.commit()
                return redirect(url_for("index"))
            else:
                flash("Passwords must match","error")
        else:
            flash("Username already used","error")
        
    return render_template("register.html",form=form)

@socketio.on("message")
def message(message):
    print(f"Received message: {message}")

@socketio.on("join")
def join(roomNumber):
    join_room(roomNumber)

if __name__ == "__main__":
    from database import UserModel,db
    db.init_app(app)
    socketio.run(app,debug=True,port=80)